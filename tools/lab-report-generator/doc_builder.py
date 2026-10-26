"""
Academic Lab Report (.docx) Document Builder for WAF Lab.
Produces high-quality, professional, editable Microsoft Word documents adhering to
academic standards: Cover page, Aim, Requirements, Procedure, Output Screenshots,
Technical Explanations, Complete Source Code Appendix, Result, and Viva Q&A.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from config import AssignmentConfig, SourceFileSpec


# Document Theme Palette (Academic Navy)
COLOR_PRIMARY_HEX = "1B365D"      # Deep Navy
COLOR_SECONDARY_HEX = "2E75B6"    # Slate Blue
COLOR_ACCENT_HEX = "4B6B94"       # Muted Blue
COLOR_DARK_TEXT_HEX = "262626"    # Charcoal text
COLOR_LIGHT_BG_HEX = "F2F4F8"     # Light Table / Card Fill
COLOR_CODE_BG_HEX = "F8F9FA"      # Code Block Fill
COLOR_BORDER_HEX = "D0D7DE"       # Subtle border

RGB_PRIMARY = RGBColor(0x1B, 0x36, 0x5D)
RGB_SECONDARY = RGBColor(0x2E, 0x75, 0xB6)
RGB_DARK_TEXT = RGBColor(0x26, 0x26, 0x26)
RGB_MUTED = RGBColor(0x60, 0x67, 0x70)


def set_cell_shading(cell, hex_color: str):
    """Set the background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    # Remove existing shading if any
    existing_shd = tc_pr.findall(qn("w:shd"))
    for s in existing_shd:
        tc_pr.remove(s)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def set_cell_margins(cell, top: int = 120, bottom: int = 120, left: int = 160, right: int = 160):
    """Set cell internal padding in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def set_table_borders(table, color: str = COLOR_BORDER_HEX, sz: str = "4", val: str = "single"):
    """Apply consistent subtle borders to a table."""
    tbl_pr = table._tbl.tblPr
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


class LabReportDocBuilder:
    """Constructs an academic lab record Word document from assignment configuration and captured evidence."""

    def __init__(self, config: AssignmentConfig, workspace_root: Path, student_name: Optional[str] = None, roll_no: Optional[str] = None):
        self.config = config
        self.workspace_root = workspace_root
        self.assignment_dir = workspace_root / config.folder_name
        self.student_name = student_name or config.default_student_name
        self.roll_no = roll_no or config.default_roll_no
        self.doc = Document()
        self._setup_page_properties()

    def _setup_page_properties(self):
        """Configure page margins, headers, and footers."""
        for section in self.doc.sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(0.8)
            section.right_margin = Inches(0.8)
            section.different_first_page_header_footer = True

            # Header on subsequent pages
            header = section.header
            header_p = header.paragraphs[0]
            header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            hrun = header_p.add_run(f"WAF Lab Record — Assignment {self.config.assignment_id}: {self.config.subtitle}")
            hrun.font.name = "Calibri"
            hrun.font.size = Pt(8.5)
            hrun.font.color.rgb = RGB_MUTED

            # Footer on subsequent pages
            footer = section.footer
            footer_p = footer.paragraphs[0]
            footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            frun = footer_p.add_run(f"{self.config.institution} · {self.config.department} · Student: {self.student_name} ({self.roll_no})")
            frun.font.name = "Calibri"
            frun.font.size = Pt(8.5)
            frun.font.color.rgb = RGB_MUTED

    def build_report(self, evidence_list: List[Dict[str, Any]], output_path: Path):
        """Generate the full Word document."""
        print(f"[*] Building Word document for Assignment {self.config.assignment_id}...")

        # 1. Cover Page
        self._add_cover_page()

        # 2. Assignment Metadata Header
        self._add_section_header("1. AIM & OBJECTIVES", level=1)
        self._add_aim_section()

        # 3. Software & System Requirements
        self._add_section_header("2. SOFTWARE & HARDWARE REQUIREMENTS", level=1)
        self._add_requirements_section()

        # 4. Faculty Requirements Mapping Table
        self._add_section_header("3. FACULTY REQUIREMENTS COMPLIANCE MAPPING", level=1)
        self._add_compliance_table()

        # 5. Procedure / Algorithm
        self._add_section_header("4. ARCHITECTURAL PROCEDURE & IMPLEMENTATION STEPS", level=1)
        self._add_procedure_section()

        # 6. Experimental Verification & Output Screenshots
        self._add_section_header("5. EXPERIMENTAL VERIFICATION & DEMONSTRATION OUTPUTS", level=1)
        self._add_evidence_section(evidence_list)

        # 7. Result & Conclusion
        self._add_section_header("6. RESULT & CONCLUSION", level=1)
        self._add_conclusion_section()

        # 8. Viva-Voce Cheat Sheet
        if self.config.viva_questions:
            self._add_section_header("7. LAB VIVA-VOCE STUDY GUIDE & TECHNICAL CONCEPTS", level=1)
            self._add_viva_section()

        # 9. Source Code Appendix
        self._add_section_header("8. APPENDIX: COMPLETE APPLICATION SOURCE CODE", level=1)
        self._add_source_code_appendix()

        # Save document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(output_path))
        print(f"[+] Document successfully generated and saved to: {output_path}")

    # ==================== SECTIONS BUILDERS ====================

    def _add_cover_page(self):
        """Build professional academic cover page."""
        # Institution
        p_inst = self.doc.add_paragraph()
        p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_inst = p_inst.add_run(self.config.institution.upper())
        r_inst.font.name = "Georgia"
        r_inst.font.size = Pt(17)
        r_inst.font.bold = True
        r_inst.font.color.rgb = RGB_PRIMARY

        # Department
        p_dept = self.doc.add_paragraph()
        p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_dept.paragraph_format.space_after = Pt(24)
        r_dept = p_dept.add_run(self.config.department.upper())
        r_dept.font.name = "Calibri"
        r_dept.font.size = Pt(11)
        r_dept.font.bold = True
        r_dept.font.color.rgb = RGB_SECONDARY

        # Subject Banner
        p_sub = self.doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_sub = p_sub.add_run(self.config.subject.upper())
        r_sub.font.name = "Calibri"
        r_sub.font.size = Pt(15)
        r_sub.font.bold = True
        r_sub.font.color.rgb = RGB_PRIMARY

        p_rec = self.doc.add_paragraph()
        p_rec.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_rec.paragraph_format.space_after = Pt(36)
        r_rec = p_rec.add_run("LABORATORY PRACTICAL RECORD & EVALUATION REPORT")
        r_rec.font.name = "Calibri"
        r_rec.font.size = Pt(11)
        r_rec.font.bold = True
        r_rec.font.color.rgb = RGB_MUTED

        # Assignment Box Table
        box_table = self.doc.add_table(rows=1, cols=1)
        box_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        box_cell = box_table.cell(0, 0)
        set_cell_shading(box_cell, COLOR_LIGHT_BG_HEX)
        set_cell_margins(box_cell, top=200, bottom=200, left=250, right=250)

        p_box_num = box_cell.paragraphs[0]
        p_box_num.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_box_num = p_box_num.add_run(f"ASSIGNMENT {self.config.assignment_id}")
        r_box_num.font.name = "Calibri"
        r_box_num.font.size = Pt(12)
        r_box_num.font.bold = True
        r_box_num.font.color.rgb = RGB_SECONDARY

        p_box_title = box_cell.add_paragraph()
        p_box_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_box_title = p_box_title.add_run(self.config.title.upper())
        r_box_title.font.name = "Georgia"
        r_box_title.font.size = Pt(13)
        r_box_title.font.bold = True
        r_box_title.font.color.rgb = RGB_PRIMARY

        p_box_sub = box_cell.add_paragraph()
        p_box_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_box_sub = p_box_sub.add_run(self.config.subtitle)
        r_box_sub.font.name = "Calibri"
        r_box_sub.font.size = Pt(10.5)
        r_box_sub.font.italic = True
        r_box_sub.font.color.rgb = RGB_DARK_TEXT

        set_table_borders(box_table, color=COLOR_SECONDARY_HEX, sz="12")

        # Spacing
        p_sp = self.doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(36)

        # Student Details Table
        tbl_student = self.doc.add_table(rows=6, cols=2)
        tbl_student.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_student.autofit = False

        student_fields = [
            ("Student Name", self.student_name),
            ("Roll Number / Reg. No.", self.roll_no),
            ("Course & Degree", "B.Tech — Computer Science & Engineering (CSE)"),
            ("Academic Year / Term", self.config.academic_year),
            ("Date of Conduction / Submission", datetime.now().strftime("%d-%B-%Y")),
            ("Evaluation & Signature", "Marks: [        / 10 ]      Faculty Sign: ________________")
        ]

        for i, (label, val) in enumerate(student_fields):
            c_label = tbl_student.cell(i, 0)
            c_val = tbl_student.cell(i, 1)

            c_label.width = Inches(2.5)
            c_val.width = Inches(4.3)

            set_cell_shading(c_label, COLOR_LIGHT_BG_HEX)
            set_cell_margins(c_label, top=100, bottom=100, left=150, right=150)
            set_cell_margins(c_val, top=100, bottom=100, left=150, right=150)

            p_l = c_label.paragraphs[0]
            r_l = p_l.add_run(label)
            r_l.font.name = "Calibri"
            r_l.font.size = Pt(10)
            r_l.font.bold = True
            r_l.font.color.rgb = RGB_PRIMARY

            p_v = c_val.paragraphs[0]
            r_v = p_v.add_run(val)
            r_v.font.name = "Calibri"
            r_v.font.size = Pt(10)
            r_v.font.color.rgb = RGB_DARK_TEXT
            if label.startswith("Evaluation"):
                r_v.font.bold = True

        set_table_borders(tbl_student, color=COLOR_BORDER_HEX, sz="4")

        # Page break after cover
        self.doc.add_page_break()

    def _add_section_header(self, title: str, level: int = 1):
        """Add styled section header."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16 if level == 1 else 10)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True

        run = p.add_run(title)
        run.font.name = "Georgia" if level == 1 else "Calibri"
        run.font.size = Pt(13 if level == 1 else 11.5)
        run.font.bold = True
        run.font.color.rgb = RGB_PRIMARY if level == 1 else RGB_SECONDARY

        # Add horizontal decorative rule under level 1 headers
        if level == 1:
            pPr = p._p.get_or_add_pPr()
            pbdr = parse_xml(
                f'<w:pBdr {nsdecls("w")}>'
                f'<w:bottom w:val="single" w:sz="8" w:space="4" w:color="{COLOR_SECONDARY_HEX}"/>'
                f'</w:pBdr>'
            )
            pPr.append(pbdr)

    def _add_aim_section(self):
        """Add aim and objectives."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15

        r_label = p.add_run("Aim: ")
        r_label.font.name = "Calibri"
        r_label.font.size = Pt(10.5)
        r_label.font.bold = True
        r_label.font.color.rgb = RGB_PRIMARY

        r_text = p.add_run(self.config.aim)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(10.5)
        r_text.font.color.rgb = RGB_DARK_TEXT

    def _add_requirements_section(self):
        """Add software and hardware requirements."""
        for req in self.config.software_requirements:
            p = self.doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15

            parts = req.split(":", 1)
            if len(parts) == 2:
                r1 = p.add_run(parts[0] + ": ")
                r1.font.name = "Calibri"
                r1.font.size = Pt(10)
                r1.font.bold = True
                r1.font.color.rgb = RGB_PRIMARY

                r2 = p.add_run(parts[1])
                r2.font.name = "Calibri"
                r2.font.size = Pt(10)
                r2.font.color.rgb = RGB_DARK_TEXT
            else:
                r = p.add_run(req)
                r.font.name = "Calibri"
                r.font.size = Pt(10)
                r.font.color.rgb = RGB_DARK_TEXT

    def _add_compliance_table(self):
        """Add structured table mapping faculty syllabus requirements to implementation."""
        if not self.config.faculty_requirements:
            return

        table = self.doc.add_table(rows=len(self.config.faculty_requirements) + 1, cols=3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        headers = ["Faculty Syllabus Requirement", "Implementation File", "Code Evidence & Technical Verification"]
        widths = [Inches(1.8), Inches(1.5), Inches(3.5)]

        # Header Row
        hdr_row = table.rows[0]
        for idx, (cell, title, w) in enumerate(zip(hdr_row.cells, headers, widths)):
            cell.width = w
            set_cell_shading(cell, COLOR_PRIMARY_HEX)
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(title)
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Content Rows
        for r_idx, item in enumerate(self.config.faculty_requirements, start=1):
            row = table.rows[r_idx]
            bg_color = COLOR_LIGHT_BG_HEX if r_idx % 2 == 1 else "FFFFFF"

            vals = [item["requirement"], item["implementation"], item["evidence"]]
            for cell, text, w in zip(row.cells, vals, widths):
                cell.width = w
                set_cell_shading(cell, bg_color)
                set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                run = p.add_run(text)
                run.font.name = "Calibri"
                run.font.size = Pt(9)
                run.font.color.rgb = RGB_DARK_TEXT

        set_table_borders(table, color=COLOR_BORDER_HEX, sz="4")

    def _add_procedure_section(self):
        """Add step-by-step procedural steps."""
        for step in self.config.procedure_steps:
            p = self.doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15

            parts = step.split(":", 1)
            if len(parts) == 2:
                r1 = p.add_run(parts[0] + ": ")
                r1.font.name = "Calibri"
                r1.font.size = Pt(10)
                r1.font.bold = True
                r1.font.color.rgb = RGB_SECONDARY

                r2 = p.add_run(parts[1])
                r2.font.name = "Calibri"
                r2.font.size = Pt(10)
                r2.font.color.rgb = RGB_DARK_TEXT
            else:
                r = p.add_run(step)
                r.font.name = "Calibri"
                r.font.size = Pt(10)
                r.font.color.rgb = RGB_DARK_TEXT

    def _add_evidence_section(self, evidence_list: List[Dict[str, Any]]):
        """Add output screenshots, captions, and deep technical explanations."""
        for i, ev in enumerate(evidence_list, 1):
            # Subsection Heading
            title = ev.get("title") or ev["name"].replace("_", " ").title()
            self._add_section_header(f"Demonstration 5.{i}: {title}", level=2)

            # Metadata Pill Table
            meta_tbl = self.doc.add_table(rows=1, cols=2)
            meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            meta_tbl.autofit = False

            c1, c2 = meta_tbl.rows[0].cells
            c1.width = Inches(4.5)
            c2.width = Inches(2.3)
            set_cell_shading(c1, COLOR_LIGHT_BG_HEX)
            set_cell_shading(c2, COLOR_LIGHT_BG_HEX)
            set_cell_margins(c1, top=60, bottom=60, left=120, right=120)
            set_cell_margins(c2, top=60, bottom=60, left=120, right=120)

            p1 = c1.paragraphs[0]
            r1 = p1.add_run(f"Requirement Tag: {ev.get('requirement_tag', 'Faculty Requirement')}")
            r1.font.name = "Calibri"
            r1.font.size = Pt(8.5)
            r1.font.bold = True
            r1.font.color.rgb = RGB_PRIMARY

            p2 = c2.paragraphs[0]
            p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            status = ev.get("status", "PASSED")
            r2 = p2.add_run(f"Status: {status}")
            r2.font.name = "Calibri"
            r2.font.size = Pt(8.5)
            r2.font.bold = True
            r2.font.color.rgb = RGBColor(0x28, 0xA7, 0x45) if "PASS" in status else RGBColor(0xDC, 0x35, 0x45)

            set_table_borders(meta_tbl, color=COLOR_BORDER_HEX, sz="4")

            # Screenshot insertion
            image_path = ev.get("image_path")
            if image_path and Path(image_path).exists():
                p_img = self.doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(8)
                p_img.paragraph_format.space_after = Pt(4)
                p_img.paragraph_format.keep_with_next = True

                # Limit width to 6.2 inches to remain comfortably within 0.8" margins on 8.5" paper
                self.doc.add_picture(str(image_path), width=Inches(6.2))

                # Caption
                p_cap = self.doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_after = Pt(8)
                p_cap.paragraph_format.keep_with_next = True

                r_cap_num = p_cap.add_run(f"Figure 5.{i}: ")
                r_cap_num.font.name = "Calibri"
                r_cap_num.font.size = Pt(9)
                r_cap_num.font.bold = True
                r_cap_num.font.color.rgb = RGB_PRIMARY

                r_cap_txt = p_cap.add_run(ev.get("caption", "Output Screenshot"))
                r_cap_txt.font.name = "Calibri"
                r_cap_txt.font.size = Pt(9)
                r_cap_txt.font.italic = True
                r_cap_txt.font.color.rgb = RGB_DARK_TEXT
            else:
                p_err = self.doc.add_paragraph()
                r_err = p_err.add_run(f"[!] Screenshot evidence unavailable: {ev.get('status', 'Failed to capture')}")
                r_err.font.name = "Calibri"
                r_err.font.size = Pt(9.5)
                r_err.font.color.rgb = RGBColor(0xDC, 0x35, 0x45)

            # Technical Explanation
            p_desc = self.doc.add_paragraph()
            p_desc.paragraph_format.space_after = Pt(14)
            p_desc.paragraph_format.line_spacing = 1.15

            r_desc_label = p_desc.add_run("Technical Explanation & Demonstrated Behavior: ")
            r_desc_label.font.name = "Calibri"
            r_desc_label.font.size = Pt(9.5)
            r_desc_label.font.bold = True
            r_desc_label.font.color.rgb = RGB_SECONDARY

            r_desc = p_desc.add_run(ev.get("description", ""))
            r_desc.font.name = "Calibri"
            r_desc.font.size = Pt(9.5)
            r_desc.font.color.rgb = RGB_DARK_TEXT

    def _add_conclusion_section(self):
        """Add academic conclusion."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15

        r_text = p.add_run(self.config.conclusion)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(10)
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
            rq.font.size = Pt(10)
            rq.font.bold = True
            rq.font.color.rgb = RGB_PRIMARY

            p_a = self.doc.add_paragraph()
            p_a.paragraph_format.space_after = Pt(6)
            p_a.paragraph_format.line_spacing = 1.15

            ra_label = p_a.add_run("Answer: ")
            ra_label.font.name = "Calibri"
            ra_label.font.size = Pt(9.5)
            ra_label.font.bold = True
            ra_label.font.color.rgb = RGB_SECONDARY

            ra = p_a.add_run(qa["answer"])
            ra.font.name = "Calibri"
            ra.font.size = Pt(9.5)
            ra.font.color.rgb = RGB_DARK_TEXT

    def _add_source_code_appendix(self):
        """Include the complete, unmodified source code for all project files in the appendix."""
        p_intro = self.doc.add_paragraph()
        p_intro.paragraph_format.space_after = Pt(12)
        p_intro.paragraph_format.line_spacing = 1.15
        r_intro = p_intro.add_run(
            "This appendix contains the complete, unabridged source code for all implementation files "
            "comprising this assignment. Every HTML document, stylesheet, and JavaScript interaction "
            "module is documented below with its relative path and functional responsibility."
        )
        r_intro.font.name = "Calibri"
        r_intro.font.size = Pt(9.5)
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

            line_count = len(code_content.splitlines())

            # File Header Box
            tbl_hdr = self.doc.add_table(rows=1, cols=2)
            tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
            tbl_hdr.autofit = False

            c_left, c_right = tbl_hdr.rows[0].cells
            c_left.width = Inches(5.0)
            c_right.width = Inches(1.8)

            set_cell_shading(c_left, COLOR_PRIMARY_HEX)
            set_cell_shading(c_right, COLOR_PRIMARY_HEX)
            set_cell_margins(c_left, top=80, bottom=80, left=140, right=140)
            set_cell_margins(c_right, top=80, bottom=80, left=140, right=140)

            p_l = c_left.paragraphs[0]
            r_fn = p_l.add_run(f"File 8.{idx}: {src_spec.relative_path}")
            r_fn.font.name = "Consolas"
            r_fn.font.size = Pt(9.5)
            r_fn.font.bold = True
            r_fn.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

            r_role = p_l.add_run(f"  ({src_spec.role})")
            r_role.font.name = "Calibri"
            r_role.font.size = Pt(8.5)
            r_role.font.italic = True
            r_role.font.color.rgb = RGBColor(0xD0, 0xE0, 0xF0)

            p_r = c_right.paragraphs[0]
            p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r_meta = p_r.add_run(f"{line_count} lines · {src_spec.language.upper()}")
            r_meta.font.name = "Consolas"
            r_meta.font.size = Pt(8.5)
            r_meta.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

            set_table_borders(tbl_hdr, color=COLOR_PRIMARY_HEX, sz="4")

            # Description Paragraph
            p_desc = self.doc.add_paragraph()
            p_desc.paragraph_format.space_before = Pt(4)
            p_desc.paragraph_format.space_after = Pt(6)
            r_desc = p_desc.add_run(f"Purpose: {src_spec.description}")
            r_desc.font.name = "Calibri"
            r_desc.font.size = Pt(9)
            r_desc.font.italic = True
            r_desc.font.color.rgb = RGB_MUTED

            # Monospace Code Box Table
            tbl_code = self.doc.add_table(rows=1, cols=1)
            tbl_code.alignment = WD_TABLE_ALIGNMENT.CENTER
            tbl_code.autofit = False

            code_cell = tbl_code.rows[0].cells[0]
            code_cell.width = Inches(6.8)
            set_cell_shading(code_cell, COLOR_CODE_BG_HEX)
            set_cell_margins(code_cell, top=100, bottom=100, left=120, right=120)

            p_code = code_cell.paragraphs[0]
            p_code.paragraph_format.space_before = Pt(0)
            p_code.paragraph_format.space_after = Pt(0)
            p_code.paragraph_format.line_spacing = 1.0

            r_code = p_code.add_run(code_content)
            r_code.font.name = "Consolas"
            r_code.font.size = Pt(7.5)
            r_code.font.color.rgb = RGB_DARK_TEXT

            set_table_borders(tbl_code, color=COLOR_BORDER_HEX, sz="4")

            # Spacing between files
            p_sep = self.doc.add_paragraph()
            p_sep.paragraph_format.space_before = Pt(12)
            p_sep.paragraph_format.space_after = Pt(12)
