"""
doc_builder.py: Academic Lab Report Document Builder for WAF Lab.
Produces high-quality, professional, beautifully paginated, and editable Microsoft Word (.docx)
documents adhering strictly to academic standards and Anthropic DOCX skill formatting guidelines.

Key Layout Systems:
- Strict A4 portrait geometry (210mm x 297mm) with uniform 0.75" margins.
- Built-in Word heading hierarchy with keep_with_next rules to prevent orphaned elements.
- Clean academic cover page with institutional hierarchy and compact student details.
- Clean first-page header/footer suppression with dynamic "Page X of Y" on content pages.
- Dynamic image aspect-ratio bounding box (max 6.0" wide, max 4.2" high) preventing multi-page overflow.
- Grouped demonstration outputs (heading + status pill + image + caption + technical explanation).
- Complete source code appendix with monospace styling, line numbering, and natural pagination.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import re

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from PIL import Image

from config import AssignmentConfig, SourceFileSpec


# Document Theme Palette (Academic Navy)
COLOR_PRIMARY_HEX = "1B365D"       # Deep Academic Navy
COLOR_SECONDARY_HEX = "2E75B6"     # Slate Blue
COLOR_ACCENT_HEX = "4B6B94"        # Muted Blue
COLOR_DARK_TEXT_HEX = "24292E"     # Charcoal body text
COLOR_LIGHT_BG_HEX = "F6F8FA"      # Subtle card fill
COLOR_CODE_BG_HEX = "F8F9FA"       # Code block background
COLOR_BORDER_HEX = "D0D7DE"        # Neutral border
COLOR_BORDER_MUTED = "E1E4E8"      # Light border
COLOR_PASS_HEX = "28A745"          # Green
COLOR_FAIL_HEX = "DC3545"          # Red

RGB_PRIMARY = RGBColor(0x1B, 0x36, 0x5D)
RGB_SECONDARY = RGBColor(0x2E, 0x75, 0xB6)
RGB_DARK_TEXT = RGBColor(0x24, 0x29, 0x2E)
RGB_MUTED = RGBColor(0x57, 0x60, 0x6A)
RGB_BORDER = RGBColor(0xD0, 0xD7, 0xDE)


# ==================== OPENXML TABLE & CELL HELPERS ====================

def set_cell_shading(cell, hex_color: str):
    """Set the background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    for s in tc_pr.findall(qn("w:shd")):
        tc_pr.remove(s)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def set_cell_margins(cell, top: int = 100, bottom: int = 100, left: int = 140, right: int = 140):
    """Set cell internal padding in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    for m in tc_pr.findall(qn("w:tcMar")):
        tc_pr.remove(m)
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def set_cell_width(cell, width_dxa: int):
    """Set explicit cell width in dxa."""
    tc_pr = cell._tc.get_or_add_tcPr()
    for w in tc_pr.findall(qn("w:tcW")):
        tc_pr.remove(w)
    tc_w = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{width_dxa}" w:type="dxa"/>')
    tc_pr.append(tc_w)


def set_table_borders(table, color: str = COLOR_BORDER_HEX, sz: str = "4", val: str = "single"):
    """Apply consistent subtle borders to a table."""
    tbl_pr = table._tbl.tblPr
    for b in tbl_pr.findall(qn("w:tblBorders")):
        tbl_pr.remove(b)
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)


def make_row_header(row):
    """Mark table row as header row that repeats automatically across page breaks."""
    tr_pr = row._tr.get_or_add_trPr()
    for h in tr_pr.findall(qn("w:tblHeader")):
        tr_pr.remove(h)
    tr_pr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))


def prevent_row_split(row):
    """Prevent table row from splitting mid-text across page breaks."""
    tr_pr = row._tr.get_or_add_trPr()
    for c in tr_pr.findall(qn("w:cantSplit")):
        tr_pr.remove(c)
    tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))


# ==================== MAIN DOCUMENT BUILDER ====================

class LabReportDocBuilder:
    """
    Constructs an academic lab record Word document from assignment configuration
    and captured browser evidence.
    """

    def __init__(
        self,
        config: AssignmentConfig,
        workspace_root: Path,
        student_name: Optional[str] = None,
        roll_no: Optional[str] = None
    ):
        self.config = config
        self.workspace_root = workspace_root
        self.assignment_dir = workspace_root / config.folder_name
        self.student_name = student_name or config.default_student_name
        self.roll_no = roll_no or config.default_roll_no
        self.doc = Document()
        self._setup_page_properties()

    def _setup_page_properties(self):
        """Configure page geometry, built-in styles, headers, and footers."""
        section = self.doc.sections[0]

        # 1. Page Geometry: A4 (8.27" x 11.69" / 210mm x 297mm) with uniform 0.75" margins
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        # 2. Built-in Word Styles Hierarchy
        styles = self.doc.styles

        # Normal (Body) Style
        normal_style = styles["Normal"]
        normal_font = normal_style.font
        normal_font.name = "Calibri"
        normal_font.size = Pt(10)
        normal_font.color.rgb = RGB_DARK_TEXT
        normal_style.paragraph_format.line_spacing = 1.15
        normal_style.paragraph_format.space_after = Pt(4)
        normal_style.paragraph_format.space_before = Pt(0)

        # Heading 1 Style
        h1_style = styles["Heading 1"]
        h1_font = h1_style.font
        h1_font.name = "Georgia"
        h1_font.size = Pt(14)
        h1_font.bold = True
        h1_font.color.rgb = RGB_PRIMARY
        h1_style.paragraph_format.space_before = Pt(14)
        h1_style.paragraph_format.space_after = Pt(4)
        h1_style.paragraph_format.keep_with_next = True

        # Heading 2 Style
        h2_style = styles["Heading 2"]
        h2_font = h2_style.font
        h2_font.name = "Calibri"
        h2_font.size = Pt(11.5)
        h2_font.bold = True
        h2_font.color.rgb = RGB_SECONDARY
        h2_style.paragraph_format.space_before = Pt(10)
        h2_style.paragraph_format.space_after = Pt(3)
        h2_style.paragraph_format.keep_with_next = True

        # 3. Clean First Page Header / Footer Suppression
        section.different_first_page_header_footer = True

        # First Page Header & Footer must be completely empty
        first_hdr = section.first_page_header
        first_hdr.is_linked_to_previous = False
        first_hdr.paragraphs[0].text = ""

        first_ftr = section.first_page_footer
        first_ftr.is_linked_to_previous = False
        first_ftr.paragraphs[0].text = ""

        # Normal Running Header (Page 2+)
        header = section.header
        header.is_linked_to_previous = False
        header_p = header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        header_p.paragraph_format.space_after = Pt(4)
        hrun = header_p.add_run(f"WAF Lab Record — Assignment {self.config.assignment_id}: {self.config.subtitle}")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGB_MUTED

        # Bottom subtle border on header paragraph
        pPr = header_p._p.get_or_add_pPr()
        for b in pPr.findall(qn("w:pBdr")):
            pPr.remove(b)
        pbdr = parse_xml(
            f'<w:pBdr {nsdecls("w")}>'
            f'<w:bottom w:val="single" w:sz="4" w:space="2" w:color="{COLOR_BORDER_HEX}"/>'
            f'</w:pBdr>'
        )
        pPr.append(pbdr)

        # Normal Running Footer (Page 2+) with dynamic "Page X of Y"
        footer = section.footer
        footer.is_linked_to_previous = False
        footer_p = footer.paragraphs[0]
        footer_p.text = ""  # Clear default paragraph
        footer_p.paragraph_format.space_before = Pt(0)
        footer_p.paragraph_format.space_after = Pt(0)

        # Build clean 2-column footer table across printable width (6.77" = 9749 dxa)
        ftr_tbl = footer.add_table(rows=1, cols=2, width=Inches(6.77))
        ftr_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        ftr_tbl.autofit = False

        c_left, c_right = ftr_tbl.rows[0].cells
        c_left.width = Inches(5.0)
        c_right.width = Inches(1.77)
        set_cell_width(c_left, 7200)
        set_cell_width(c_right, 2549)
        set_cell_margins(c_left, top=60, bottom=40, left=0, right=0)
        set_cell_margins(c_right, top=60, bottom=40, left=0, right=0)

        # Left: Institutional and student metadata
        p_fl = c_left.paragraphs[0]
        p_fl.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_fl = p_fl.add_run(f"{self.config.institution} · CSE · Student: {self.student_name} ({self.roll_no})")
        r_fl.font.name = "Calibri"
        r_fl.font.size = Pt(8.5)
        r_fl.font.color.rgb = RGB_MUTED

        # Right: Dynamic Page X of Y
        p_fr = c_right.paragraphs[0]
        p_fr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_p1 = p_fr.add_run("Page ")
        r_p1.font.name = "Calibri"
        r_p1.font.size = Pt(8.5)
        r_p1.font.color.rgb = RGB_MUTED

        fld_page = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls("w"))
        p_fr._p.append(fld_page)

        r_p2 = p_fr.add_run(" of ")
        r_p2.font.name = "Calibri"
        r_p2.font.size = Pt(8.5)
        r_p2.font.color.rgb = RGB_MUTED

        fld_numpages = parse_xml(r'<w:fldSimple %s w:instr="NUMPAGES"/>' % nsdecls("w"))
        p_fr._p.append(fld_numpages)

        # Top border line on footer table
        tbl_pr = ftr_tbl._tbl.tblPr
        tbl_borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{COLOR_BORDER_HEX}"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="none"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tbl_pr.append(tbl_borders)

    def build_report(self, evidence_list: List[Dict[str, Any]], output_path: Path):
        """Generate the complete, polished Word document."""
        print(f"[*] Building Word document for Assignment {self.config.assignment_id}...")

        # 1. Clean Academic Cover Page
        self._add_cover_page()

        # 2. Aim & Objectives (Beginning of main body)
        self._add_section_header("1. AIM & OBJECTIVES", level=1)
        self._add_aim_section()

        # 3. Software & System Requirements
        self._add_section_header("2. SOFTWARE & HARDWARE REQUIREMENTS", level=1)
        self._add_requirements_section()

        # 4. Faculty Requirements Mapping Table
        if self.config.faculty_requirements:
            self._add_section_header("3. FACULTY REQUIREMENTS COMPLIANCE MAPPING", level=1)
            self._add_compliance_table()

        # 5. Procedure / Implementation Steps
        self._add_section_header("4. ARCHITECTURAL PROCEDURE & IMPLEMENTATION STEPS", level=1)
        self._add_procedure_section()

        # 6. Experimental Verification & Output Screenshots
        self._add_section_header("5. EXPERIMENTAL VERIFICATION & DEMONSTRATION OUTPUTS", level=1)
        self._add_evidence_section(evidence_list)

        # 7. Result & Conclusion
        self._add_section_header("6. RESULT & CONCLUSION", level=1)
        self._add_conclusion_section()

        # 8. Viva-Voce Study Guide
        if self.config.viva_questions:
            self._add_section_header("7. LAB VIVA-VOCE STUDY GUIDE & TECHNICAL CONCEPTS", level=1)
            self._add_viva_section()

        # 9. Complete Source Code Appendix (Begins cleanly on a fresh page)
        self._add_section_header("8. APPENDIX: COMPLETE APPLICATION SOURCE CODE", level=1, page_break_before=True)
        self._add_source_code_appendix()

        # Save document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(output_path))
        print(f"[+] Document successfully generated and saved to: {output_path}")

    # ==================== SECTIONS BUILDERS ====================

    def _add_cover_page(self):
        """
        Build a clean, uncluttered academic cover page.
        Contains only:
        - GITAM Deemed to be University
        - Department of Computer Science & Engineering
        - Web Application Frameworks Lab
        - Assignment number & title
        - Compact student details table
        Generous whitespace, restrained accents, no headers/footers.
        """
        # Top margin spacer
        p_top = self.doc.add_paragraph()
        p_top.paragraph_format.space_before = Pt(28)
        p_top.paragraph_format.space_after = Pt(0)

        # Institution
        p_inst = self.doc.add_paragraph()
        p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_inst.paragraph_format.space_after = Pt(4)
        r_inst = p_inst.add_run(self.config.institution.upper())
        r_inst.font.name = "Georgia"
        r_inst.font.size = Pt(17)
        r_inst.font.bold = True
        r_inst.font.color.rgb = RGB_PRIMARY

        # Department
        p_dept = self.doc.add_paragraph()
        p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_dept.paragraph_format.space_after = Pt(4)
        r_dept = p_dept.add_run(self.config.department.upper())
        r_dept.font.name = "Calibri"
        r_dept.font.size = Pt(11)
        r_dept.font.bold = True
        r_dept.font.color.rgb = RGB_SECONDARY

        # Subject Title
        p_sub = self.doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.space_after = Pt(36)
        r_sub = p_sub.add_run(self.config.subject.upper())
        r_sub.font.name = "Calibri"
        r_sub.font.size = Pt(13)
        r_sub.font.bold = True
        r_sub.font.color.rgb = RGB_PRIMARY

        # Assignment Box Table (Width: 6.5 inches = 9360 dxa)
        box_table = self.doc.add_table(rows=1, cols=1)
        box_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        box_table.autofit = False

        box_cell = box_table.cell(0, 0)
        box_cell.width = Inches(6.5)
        set_cell_width(box_cell, 9360)
        set_cell_shading(box_cell, COLOR_LIGHT_BG_HEX)
        set_cell_margins(box_cell, top=180, bottom=180, left=240, right=240)

        p_box_num = box_cell.paragraphs[0]
        p_box_num.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_box_num.paragraph_format.space_after = Pt(3)
        r_box_num = p_box_num.add_run(f"ASSIGNMENT {self.config.assignment_id}")
        r_box_num.font.name = "Calibri"
        r_box_num.font.size = Pt(12)
        r_box_num.font.bold = True
        r_box_num.font.color.rgb = RGB_SECONDARY

        # Clean title: strip redundant "Lab Assignment X:" or "Assignment X:" prefix if present
        clean_title = re.sub(r'^(Lab\s+)?Assignment\s+\d+:\s*', '', self.config.title, flags=re.IGNORECASE).strip()
        p_box_title = box_cell.add_paragraph()
        p_box_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_box_title.paragraph_format.space_after = Pt(3)
        r_box_title = p_box_title.add_run(clean_title)
        r_box_title.font.name = "Georgia"
        r_box_title.font.size = Pt(13.5)
        r_box_title.font.bold = True
        r_box_title.font.color.rgb = RGB_PRIMARY

        if self.config.subtitle:
            p_box_sub = box_cell.add_paragraph()
            p_box_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_box_sub.paragraph_format.space_after = Pt(0)
            r_box_sub = p_box_sub.add_run(self.config.subtitle)
            r_box_sub.font.name = "Calibri"
            r_box_sub.font.size = Pt(10)
            r_box_sub.font.italic = True
            r_box_sub.font.color.rgb = RGB_MUTED

        set_table_borders(box_table, color=COLOR_PRIMARY_HEX, sz="6")

        # Whitespace before student table
        p_sp = self.doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(36)

        # Compact Student Details Table (Matching 6.5" width: 2.3" + 4.2" = 9360 dxa)
        student_fields = [
            ("Student Name", self.student_name),
            ("Roll Number / Reg. No.", self.roll_no),
            ("Course & Degree", "B.Tech — Computer Science & Engineering (CSE)"),
            ("Academic Year / Term", self.config.academic_year),
            ("Date of Submission", datetime.now().strftime("%d-%B-%Y"))
        ]

        tbl_student = self.doc.add_table(rows=len(student_fields), cols=2)
        tbl_student.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_student.autofit = False

        w_col1 = 3312  # 2.3 inches in dxa
        w_col2 = 6048  # 4.2 inches in dxa

        for i, (label, val) in enumerate(student_fields):
            row = tbl_student.rows[i]
            prevent_row_split(row)

            c_label = row.cells[0]
            c_val = row.cells[1]

            c_label.width = Inches(2.3)
            c_val.width = Inches(4.2)
            set_cell_width(c_label, w_col1)
            set_cell_width(c_val, w_col2)

            set_cell_shading(c_label, COLOR_LIGHT_BG_HEX)
            set_cell_shading(c_val, "FFFFFF")
            set_cell_margins(c_label, top=80, bottom=80, left=140, right=140)
            set_cell_margins(c_val, top=80, bottom=80, left=140, right=140)

            p_l = c_label.paragraphs[0]
            p_l.paragraph_format.space_after = Pt(0)
            p_l.paragraph_format.space_before = Pt(0)
            r_l = p_l.add_run(label)
            r_l.font.name = "Calibri"
            r_l.font.size = Pt(9.5)
            r_l.font.bold = True
            r_l.font.color.rgb = RGB_PRIMARY

            p_v = c_val.paragraphs[0]
            p_v.paragraph_format.space_after = Pt(0)
            p_v.paragraph_format.space_before = Pt(0)
            r_v = p_v.add_run(val)
            r_v.font.name = "Calibri"
            r_v.font.size = Pt(9.5)
            r_v.font.color.rgb = RGB_DARK_TEXT

        set_table_borders(tbl_student, color=COLOR_BORDER_HEX, sz="4")

        # Bottom Academic Hallmark Anchor
        p_anchor = self.doc.add_paragraph()
        p_anchor.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_anchor.paragraph_format.space_before = Pt(48)
        p_anchor.paragraph_format.space_after = Pt(0)
        r_anchor = p_anchor.add_run("ACADEMIC LAB RECORD · DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING")
        r_anchor.font.name = "Calibri"
        r_anchor.font.size = Pt(8.5)
        r_anchor.font.bold = True
        r_anchor.font.color.rgb = RGB_MUTED

        # Intentional Page Break after cover page
        self.doc.add_page_break()

    def _add_section_header(self, title: str, level: int = 1, page_break_before: bool = False):
        """Add styled section header with real Word heading style and decorative bottom rule for H1."""
        style_name = "Heading 1" if level == 1 else "Heading 2"
        p = self.doc.add_paragraph(style=style_name)
        p.paragraph_format.keep_with_next = True
        if page_break_before:
            p.paragraph_format.page_break_before = True

        run = p.add_run(title)
        run.font.bold = True

        if level == 1:
            run.font.name = "Georgia"
            run.font.size = Pt(13)
            run.font.color.rgb = RGB_PRIMARY
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(5)

            # Horizontal decorative rule under H1 headers
            pPr = p._p.get_or_add_pPr()
            pbdr = parse_xml(
                f'<w:pBdr {nsdecls("w")}>'
                f'<w:bottom w:val="single" w:sz="6" w:space="3" w:color="{COLOR_SECONDARY_HEX}"/>'
                f'</w:pBdr>'
            )
            pPr.append(pbdr)
        else:
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.color.rgb = RGB_SECONDARY
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)

    def _add_aim_section(self):
        """Add aim and objectives."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.15

        r_label = p.add_run("Aim: ")
        r_label.font.name = "Calibri"
        r_label.font.size = Pt(10)
        r_label.font.bold = True
        r_label.font.color.rgb = RGB_PRIMARY

        r_text = p.add_run(self.config.aim)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = RGB_DARK_TEXT

    def _add_requirements_section(self):
        """Add software and hardware requirements."""
        for req in self.config.software_requirements:
            p = self.doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2.5)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.line_spacing = 1.15

            parts = req.split(":", 1)
            if len(parts) == 2:
                r1 = p.add_run(parts[0] + ": ")
                r1.font.name = "Calibri"
                r1.font.size = Pt(9.5)
                r1.font.bold = True
                r1.font.color.rgb = RGB_PRIMARY

                r2 = p.add_run(parts[1].strip())
                r2.font.name = "Calibri"
                r2.font.size = Pt(9.5)
                r2.font.color.rgb = RGB_DARK_TEXT
            else:
                r = p.add_run(req)
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGB_DARK_TEXT

    def _add_compliance_table(self):
        """Add structured table mapping faculty syllabus requirements to implementation."""
        if not self.config.faculty_requirements:
            return

        table = self.doc.add_table(rows=len(self.config.faculty_requirements) + 1, cols=3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        headers = ["Faculty Syllabus Requirement", "Implementation File", "Code Evidence & Technical Verification"]
        # Total width = 1.8" + 1.5" + 3.4" = 6.7" (9648 dxa)
        widths_dxa = [2592, 2160, 4896]
        widths_in = [Inches(1.8), Inches(1.5), Inches(3.4)]

        # Header Row
        hdr_row = table.rows[0]
        make_row_header(hdr_row)
        prevent_row_split(hdr_row)

        for idx, (cell, title, w_in, w_dxa) in enumerate(zip(hdr_row.cells, headers, widths_in, widths_dxa)):
            cell.width = w_in
            set_cell_width(cell, w_dxa)
            set_cell_shading(cell, COLOR_PRIMARY_HEX)
            set_cell_margins(cell, top=100, bottom=100, left=130, right=130)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(title)
            run.font.name = "Calibri"
            run.font.size = Pt(9)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Content Rows
        for r_idx, item in enumerate(self.config.faculty_requirements, start=1):
            row = table.rows[r_idx]
            prevent_row_split(row)
            bg_color = COLOR_LIGHT_BG_HEX if r_idx % 2 == 1 else "FFFFFF"

            vals = [item["requirement"], item["implementation"], item["evidence"]]
            for cell, text, w_in, w_dxa in zip(row.cells, vals, widths_in, widths_dxa):
                cell.width = w_in
                set_cell_width(cell, w_dxa)
                set_cell_shading(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=130, right=130)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                run = p.add_run(text)
                run.font.name = "Calibri"
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGB_DARK_TEXT

        set_table_borders(table, color=COLOR_BORDER_HEX, sz="4")

        # Spacing after table
        p_sp = self.doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(6)

    def _add_procedure_section(self):
        """Add step-by-step procedural steps."""
        for step in self.config.procedure_steps:
            p = self.doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(3.5)
            p.paragraph_format.line_spacing = 1.15

            parts = step.split(":", 1)
            if len(parts) == 2:
                r1 = p.add_run(parts[0] + ": ")
                r1.font.name = "Calibri"
                r1.font.size = Pt(9.5)
                r1.font.bold = True
                r1.font.color.rgb = RGB_SECONDARY

                r2 = p.add_run(parts[1].strip())
                r2.font.name = "Calibri"
                r2.font.size = Pt(9.5)
                r2.font.color.rgb = RGB_DARK_TEXT
            else:
                r = p.add_run(step)
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGB_DARK_TEXT

    def _add_evidence_section(self, evidence_list: List[Dict[str, Any]]):
        """
        Add output screenshots, requirement status, captions, and deep technical explanations.
        Ensures strict aspect ratio bounding boxes and keep_with_next groupings to eliminate
        orphaned headings and accidental blank pages.
        """
        for i, ev in enumerate(evidence_list, 1):
            title = ev.get("title") or ev["name"].replace("_", " ").title()

            # 1. Demonstration Subsection Heading
            p_head = self.doc.add_paragraph(style="Heading 2")
            p_head.paragraph_format.space_before = Pt(10)
            p_head.paragraph_format.space_after = Pt(2)
            p_head.paragraph_format.keep_with_next = True

            r_h = p_head.add_run(f"Demonstration 5.{i}: {title}")
            r_h.font.name = "Calibri"
            r_h.font.size = Pt(11)
            r_h.font.bold = True
            r_h.font.color.rgb = RGB_SECONDARY

            # 2. Metadata Pill Table (Width: 6.5 inches = 9360 dxa)
            meta_tbl = self.doc.add_table(rows=1, cols=2)
            meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            meta_tbl.autofit = False
            prevent_row_split(meta_tbl.rows[0])

            c1, c2 = meta_tbl.rows[0].cells
            c1.width = Inches(4.7)
            c2.width = Inches(1.8)
            set_cell_width(c1, 6768)
            set_cell_width(c2, 2592)
            set_cell_shading(c1, COLOR_LIGHT_BG_HEX)
            set_cell_shading(c2, COLOR_LIGHT_BG_HEX)
            set_cell_margins(c1, top=40, bottom=40, left=120, right=120)
            set_cell_margins(c2, top=40, bottom=40, left=120, right=120)

            p1 = c1.paragraphs[0]
            p1.paragraph_format.space_before = Pt(0)
            p1.paragraph_format.space_after = Pt(0)
            p1.paragraph_format.keep_with_next = True
            r1 = p1.add_run(f"Requirement Tag: {ev.get('requirement_tag', 'Faculty Requirement')}")
            r1.font.name = "Calibri"
            r1.font.size = Pt(8.5)
            r1.font.bold = True
            r1.font.color.rgb = RGB_PRIMARY

            p2 = c2.paragraphs[0]
            p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(0)
            p2.paragraph_format.keep_with_next = True
            status = ev.get("status", "PASSED")
            r2 = p2.add_run(f"Status: {status}")
            r2.font.name = "Calibri"
            r2.font.size = Pt(8.5)
            r2.font.bold = True
            r2.font.color.rgb = RGBColor(0x28, 0xA7, 0x45) if "PASS" in status else RGBColor(0xDC, 0x35, 0x45)

            set_table_borders(meta_tbl, color=COLOR_BORDER_HEX, sz="4")

            # 3. Screenshot insertion with dynamic aspect-ratio bounding box
            image_path = ev.get("image_path")
            if image_path and Path(image_path).exists():
                p_img = self.doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(4)
                p_img.paragraph_format.space_after = Pt(2)
                p_img.paragraph_format.keep_with_next = True

                try:
                    with Image.open(image_path) as img:
                        w_px, h_px = img.size
                        aspect = w_px / h_px

                    # Calculate target dimensions:
                    # Landscape desktop: max width 5.9", max height 3.35"
                    # Portrait mobile: max width 3.2", max height 4.2"
                    if aspect >= 1.0:
                        max_w = 5.9
                        max_h = 3.35
                        if max_w / aspect <= max_h:
                            target_w = Inches(max_w)
                            target_h = Inches(max_w / aspect)
                        else:
                            target_h = Inches(max_h)
                            target_w = Inches(max_h * aspect)
                    else:
                        max_h = 4.2
                        max_w = 3.2
                        if max_h * aspect <= max_w:
                            target_h = Inches(max_h)
                            target_w = Inches(max_h * aspect)
                        else:
                            target_w = Inches(max_w)
                            target_h = Inches(max_w / aspect)

                    run_pic = p_img.add_run()
                    run_pic.add_picture(str(image_path), width=target_w, height=target_h)
                except Exception as img_err:
                    print(f"[!] Warning: Image bounding box calculation fallback for {image_path}: {img_err}")
                    run_pic = p_img.add_run()
                    run_pic.add_picture(str(image_path), width=Inches(5.6))

                # 4. Caption
                p_cap = self.doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_before = Pt(2)
                p_cap.paragraph_format.space_after = Pt(4)
                p_cap.paragraph_format.keep_with_next = True

                r_cap_num = p_cap.add_run(f"Figure 5.{i}: ")
                r_cap_num.font.name = "Calibri"
                r_cap_num.font.size = Pt(8.5)
                r_cap_num.font.bold = True
                r_cap_num.font.color.rgb = RGB_PRIMARY

                r_cap_txt = p_cap.add_run(ev.get("caption", "Output Screenshot"))
                r_cap_txt.font.name = "Calibri"
                r_cap_txt.font.size = Pt(8.5)
                r_cap_txt.font.italic = True
                r_cap_txt.font.color.rgb = RGB_DARK_TEXT
            else:
                p_err = self.doc.add_paragraph()
                p_err.paragraph_format.space_before = Pt(4)
                p_err.paragraph_format.space_after = Pt(4)
                p_err.paragraph_format.keep_with_next = True
                r_err = p_err.add_run(f"[!] Screenshot evidence unavailable: {ev.get('status', 'Failed to capture')}")
                r_err.font.name = "Calibri"
                r_err.font.size = Pt(9)
                r_err.font.color.rgb = RGBColor(0xDC, 0x35, 0x45)

            # 5. Technical Explanation
            p_desc = self.doc.add_paragraph()
            p_desc.paragraph_format.space_before = Pt(2)
            p_desc.paragraph_format.space_after = Pt(10)
            p_desc.paragraph_format.line_spacing = 1.15
            p_desc.paragraph_format.keep_with_next = False

            r_desc_label = p_desc.add_run("Technical Explanation & Demonstrated Behavior: ")
            r_desc_label.font.name = "Calibri"
            r_desc_label.font.size = Pt(9)
            r_desc_label.font.bold = True
            r_desc_label.font.color.rgb = RGB_SECONDARY

            r_desc = p_desc.add_run(ev.get("description", ""))
            r_desc.font.name = "Calibri"
            r_desc.font.size = Pt(9)
            r_desc.font.color.rgb = RGB_DARK_TEXT

    def _add_conclusion_section(self):
        """Add academic conclusion."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15

        r_text = p.add_run(self.config.conclusion)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = RGB_DARK_TEXT

    def _add_viva_section(self):
        """Add viva voce Q&A study guide."""
        for qa in self.config.viva_questions:
            p_q = self.doc.add_paragraph()
            p_q.paragraph_format.space_before = Pt(6)
            p_q.paragraph_format.space_after = Pt(2)
            p_q.paragraph_format.keep_with_next = True

            rq = p_q.add_run(qa["question"])
            rq.font.name = "Calibri"
            rq.font.size = Pt(9.5)
            rq.font.bold = True
            rq.font.color.rgb = RGB_PRIMARY

            p_a = self.doc.add_paragraph()
            p_a.paragraph_format.space_before = Pt(0)
            p_a.paragraph_format.space_after = Pt(5)
            p_a.paragraph_format.line_spacing = 1.15

            ra_label = p_a.add_run("Answer: ")
            ra_label.font.name = "Calibri"
            ra_label.font.size = Pt(9)
            ra_label.font.bold = True
            ra_label.font.color.rgb = RGB_SECONDARY

            ra = p_a.add_run(qa["answer"])
            ra.font.name = "Calibri"
            ra.font.size = Pt(9)
            ra.font.color.rgb = RGB_DARK_TEXT

    def _add_source_code_appendix(self):
        """
        Include complete, unabridged source code for all project files in the appendix.
        Formats each file with a prominent header banner, file purpose, line numbers,
        and natural pagination across page boundaries without massive empty voids.
        """
        p_intro = self.doc.add_paragraph()
        p_intro.paragraph_format.space_before = Pt(2)
        p_intro.paragraph_format.space_after = Pt(10)
        p_intro.paragraph_format.line_spacing = 1.15
        r_intro = p_intro.add_run(
            "This appendix contains the complete, unabridged source code for all implementation files "
            "comprising this assignment. Every HTML document, stylesheet, and JavaScript interaction "
            "module is documented below with its relative path, functional responsibility, and line numbers."
        )
        r_intro.font.name = "Calibri"
        r_intro.font.size = Pt(9)
        r_intro.font.color.rgb = RGB_MUTED

        for idx, src_spec in enumerate(self.config.source_files, 1):
            file_path = self.assignment_dir / src_spec.relative_path
            if not file_path.exists():
                print(f"[!] Warning: Source file not found: {file_path}")
                continue

            try:
                code_content = file_path.read_text(encoding="utf-8")
            except Exception as e:
                code_content = f"// Error reading file {src_spec.relative_path}: {e}"

            code_lines = code_content.splitlines()
            line_count = len(code_lines)

            # 1. File Header Banner Table (Width: 6.7 inches = 9648 dxa)
            tbl_hdr = self.doc.add_table(rows=1, cols=2)
            tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
            tbl_hdr.autofit = False
            prevent_row_split(tbl_hdr.rows[0])

            c_left, c_right = tbl_hdr.rows[0].cells
            c_left.width = Inches(4.9)
            c_right.width = Inches(1.8)
            set_cell_width(c_left, 7056)
            set_cell_width(c_right, 2592)

            set_cell_shading(c_left, COLOR_PRIMARY_HEX)
            set_cell_shading(c_right, COLOR_PRIMARY_HEX)
            set_cell_margins(c_left, top=70, bottom=70, left=130, right=130)
            set_cell_margins(c_right, top=70, bottom=70, left=130, right=130)

            p_l = c_left.paragraphs[0]
            p_l.paragraph_format.space_before = Pt(0)
            p_l.paragraph_format.space_after = Pt(0)
            p_l.paragraph_format.keep_with_next = True
            r_fn = p_l.add_run(f"File 8.{idx}: {src_spec.relative_path}")
            r_fn.font.name = "Consolas"
            r_fn.font.size = Pt(9)
            r_fn.font.bold = True
            r_fn.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

            r_role = p_l.add_run(f"  ({src_spec.role})")
            r_role.font.name = "Calibri"
            r_role.font.size = Pt(8)
            r_role.font.italic = True
            r_role.font.color.rgb = RGBColor(0xD0, 0xE0, 0xF0)

            p_r = c_right.paragraphs[0]
            p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p_r.paragraph_format.space_before = Pt(0)
            p_r.paragraph_format.space_after = Pt(0)
            p_r.paragraph_format.keep_with_next = True
            r_meta = p_r.add_run(f"{line_count} lines · {src_spec.language.upper()}")
            r_meta.font.name = "Consolas"
            r_meta.font.size = Pt(8)
            r_meta.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

            set_table_borders(tbl_hdr, color=COLOR_PRIMARY_HEX, sz="4")

            # 2. Description Paragraph
            p_desc = self.doc.add_paragraph()
            p_desc.paragraph_format.space_before = Pt(3)
            p_desc.paragraph_format.space_after = Pt(4)
            p_desc.paragraph_format.keep_with_next = True
            r_desc = p_desc.add_run(f"Purpose: {src_spec.description}")
            r_desc.font.name = "Calibri"
            r_desc.font.size = Pt(8.5)
            r_desc.font.italic = True
            r_desc.font.color.rgb = RGB_MUTED

            # 3. Monospace Code Box Table (Splits smoothly across pages)
            tbl_code = self.doc.add_table(rows=1, cols=1)
            tbl_code.alignment = WD_TABLE_ALIGNMENT.CENTER
            tbl_code.autofit = False
            # Crucial: DO NOT call prevent_row_split here, so Word splits code lines naturally across pages!

            code_cell = tbl_code.rows[0].cells[0]
            code_cell.width = Inches(6.7)
            set_cell_width(code_cell, 9648)
            set_cell_shading(code_cell, COLOR_CODE_BG_HEX)
            set_cell_margins(code_cell, top=70, bottom=70, left=80, right=80)

            # Hanging indent configuration: 0.40 inches (576 dxa)
            # Line number occupies 0 to 0.40", wrapped code lines indent cleanly to 0.40"
            INDENT_INCHES = 0.40
            INDENT_DXA = 576

            # Insert code lines with line numbers as individual paragraphs
            p_first = code_cell.paragraphs[0]
            for line_no, raw_line in enumerate(code_lines, 1):
                p_line = p_first if line_no == 1 else code_cell.add_paragraph()
                p_line.paragraph_format.space_before = Pt(0)
                p_line.paragraph_format.space_after = Pt(0)
                p_line.paragraph_format.line_spacing = 1.0
                p_line.paragraph_format.widow_control = False

                # Apply hanging indent and tab stop so wrapped code doesn't pollute line number column
                p_line.paragraph_format.left_indent = Inches(INDENT_INCHES)
                p_line.paragraph_format.first_line_indent = Inches(-INDENT_INCHES)
                pPr = p_line._p.get_or_add_pPr()
                for t in pPr.findall(qn("w:tabs")):
                    pPr.remove(t)
                tabs = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="left" w:pos="{INDENT_DXA}"/></w:tabs>')
                pPr.append(tabs)

                if line_no == 1:
                    # Keep first line with banner table to avoid orphaned header banner
                    p_line.paragraph_format.keep_with_next = True

                # Line number in muted gray with tab character
                r_num = p_line.add_run(f"{line_no:4d}\t")
                r_num.font.name = "Consolas"
                r_num.font.size = Pt(7.5)
                r_num.font.color.rgb = RGBColor(0x8C, 0x95, 0x9F)

                # Code content with tab expansion
                clean_text = raw_line.replace("\t", "    ")
                r_txt = p_line.add_run(clean_text)
                r_txt.font.name = "Consolas"
                r_txt.font.size = Pt(7.5)
                r_txt.font.color.rgb = RGB_DARK_TEXT

            set_table_borders(tbl_code, color=COLOR_BORDER_HEX, sz="4")


