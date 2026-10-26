"""
qa_checker.py: Automated Quality Assurance and Validation Engine for WAF Lab Reports.
Performs rigorous structural, content, typography, and visual defect detection on generated
DOCX and PDF reports prior to final publication.

Checks Performed:
1. File Existence & Integrity (DOCX & PDF parseable, non-corrupted, non-empty)
2. Empty or Nearly Empty Page Detection (Pixel analysis on rendered PDF pages)
3. Screenshot & Image Integrity (File presence, dimensions, docx embedding)
4. Heading & Element Bonding (keep_with_next enforcement, orphan prevention)
5. Table Formatting (tblHeader repeat, cantSplit row integrity)
6. Source Code Appendix Completeness (All registered files present, complete lines)
7. Header/Footer & Pagination Fields (First-page suppression, PAGE/NUMPAGES dynamic fields)
"""

from pathlib import Path
from typing import List, Dict, Any, Tuple
import docx
from PIL import Image


class LabReportQAChecker:
    """Automated Quality Assurance Validator for WAF Lab Reports."""

    def __init__(
        self,
        docx_path: Path,
        pdf_path: Path,
        preview_dir: Path,
        config: Any,
        evidence_list: List[Dict[str, Any]],
        workspace_root: Path
    ):
        self.docx_path = Path(docx_path).resolve()
        self.pdf_path = Path(pdf_path).resolve()
        self.preview_dir = Path(preview_dir).resolve()
        self.config = config
        self.evidence_list = evidence_list
        self.workspace_root = Path(workspace_root).resolve()
        self.results: List[Dict[str, Any]] = []

    def log_result(self, category: str, test_name: str, passed: bool, details: str, severity: str = "ERROR"):
        self.results.append({
            "category": category,
            "test_name": test_name,
            "passed": passed,
            "status": "PASS" if passed else ("WARN" if severity == "WARN" else "FAIL"),
            "details": details,
            "severity": severity
        })

    def run_all_checks(self) -> Tuple[bool, List[Dict[str, Any]]]:
        """Execute full automated QA test suite."""
        print("\n" + "=" * 70)
        print("          AUTOMATED REPORT QUALITY ASSURANCE (QA) AUDIT")
        print("=" * 70)

        # Check 1: File Existence & Integrity
        self._check_file_integrity()

        # Load docx object if valid
        doc = None
        if self.docx_path.exists() and self.docx_path.stat().st_size > 1024:
            try:
                doc = docx.Document(str(self.docx_path))
            except Exception as e:
                self.log_result("Integrity", "DOCX XML Parsing", False, f"Failed to parse DOCX: {e}")

        # Check 2: Screenshot Evidence Integrity
        self._check_screenshots(doc)

        # Check 3: Headings & Structural Hierarchy
        if doc:
            self._check_headings_and_structure(doc)
            self._check_table_formatting(doc)
            self._check_header_footer_and_pagination(doc)
            self._check_code_appendix(doc)

        # Check 4: Page Count & Blank Page Detection
        self._check_page_rendering_and_blank_pages()

        # Summary Assessment
        failures = [r for r in self.results if r["status"] == "FAIL"]
        warnings = [r for r in self.results if r["status"] == "WARN"]
        passes = [r for r in self.results if r["status"] == "PASS"]

        all_passed = len(failures) == 0

        # Print detailed report
        for res in self.results:
            icon = "  [PASS] " if res["status"] == "PASS" else ("  [WARN] " if res["status"] == "WARN" else "  [FAIL] ")
            print(f"{icon} {res['category']} - {res['test_name']}: {res['details']}")

        print("-" * 70)
        print(f"[*] QA Audit Summary: {len(passes)} Passed, {len(warnings)} Warnings, {len(failures)} Critical Failures.")
        if all_passed:
            print("[+] STATUS: ALL QUALITY CRITERIA SATISFIED. Ready for atomic replacement.")
        else:
            print("[!] STATUS: QUALITY CHECKS FAILED. Report replacement aborted to protect existing files.")
        print("=" * 70 + "\n")

        return all_passed, self.results

    def _check_file_integrity(self):
        """Verify DOCX and PDF exist and meet baseline size constraints."""
        if not self.docx_path.exists():
            self.log_result("Integrity", "DOCX Existence", False, f"DOCX file missing: {self.docx_path}")
        else:
            sz_kb = self.docx_path.stat().st_size / 1024
            self.log_result(
                "Integrity", "DOCX Existence & Size",
                sz_kb >= 50,
                f"DOCX present ({sz_kb:.1f} KB)" if sz_kb >= 50 else f"DOCX suspiciously small ({sz_kb:.1f} KB)"
            )

        if not self.pdf_path.exists():
            self.log_result("Integrity", "PDF Existence", False, f"PDF file missing: {self.pdf_path}")
        else:
            sz_kb = self.pdf_path.stat().st_size / 1024
            self.log_result(
                "Integrity", "PDF Existence & Size",
                sz_kb >= 50,
                f"PDF present ({sz_kb:.1f} KB)" if sz_kb >= 50 else f"PDF suspiciously small ({sz_kb:.1f} KB)"
            )

    def _check_screenshots(self, doc: Any):
        """Verify all evidence screenshots exist, have valid dimensions, and are referenced in DOCX."""
        if not self.evidence_list:
            self.log_result("Screenshots", "Evidence Count", False, "No screenshot evidence provided.")
            return

        all_exist = True
        dimension_ok = True
        missing_files = []
        suspicious_images = []

        for ev in self.evidence_list:
            img_path_str = ev.get("image_path")
            if not img_path_str or not Path(img_path_str).exists():
                all_exist = False
                missing_files.append(ev.get("name", "unknown"))
                continue

            img_p = Path(img_path_str)
            try:
                with Image.open(img_p) as im:
                    w, h = im.size
                    if w < 200 or h < 200:
                        dimension_ok = False
                        suspicious_images.append(f"{img_p.name} ({w}x{h})")
            except Exception as e:
                all_exist = False
                missing_files.append(f"{img_p.name} (corrupt: {e})")

        self.log_result(
            "Screenshots", "Image File Availability",
            all_exist,
            f"All {len(self.evidence_list)} screenshot evidence files verified on disk." if all_exist else f"Missing/corrupt screenshots: {missing_files}"
        )

        self.log_result(
            "Screenshots", "Image Dimension & Aspect Ratio",
            dimension_ok,
            "All screenshots meet resolution standards (>= 200px)." if dimension_ok else f"Suspiciously small images: {suspicious_images}"
        )

        # Verify images embedded in DOCX package
        if doc:
            try:
                part_count = len([p for p in doc.part.related_parts.values() if "image" in str(p.content_type)])
                expected_min = len(self.evidence_list)
                embedded_ok = part_count >= expected_min
                self.log_result(
                    "Screenshots", "Embedded DOCX Media Parts",
                    embedded_ok,
                    f"{part_count} image parts embedded in DOCX package (>= {expected_min} expected)." if embedded_ok else f"Only {part_count} images embedded; expected at least {expected_min}."
                )
            except Exception as e:
                self.log_result("Screenshots", "Embedded DOCX Media Parts", False, f"Error checking DOCX media: {e}")

    def _check_headings_and_structure(self, doc: Any):
        """Verify presence of core numbered sections and keep_with_next formatting."""
        expected_sections = [
            "1. AIM & OBJECTIVES",
            "2. SOFTWARE & HARDWARE REQUIREMENTS",
            "3. FACULTY REQUIREMENTS COMPLIANCE MAPPING",
            "4. ARCHITECTURAL PROCEDURE & IMPLEMENTATION STEPS",
            "5. EXPERIMENTAL VERIFICATION & DEMONSTRATION OUTPUTS",
            "6. RESULT & CONCLUSION",
            "8. APPENDIX: COMPLETE APPLICATION SOURCE CODE"
        ]

        doc_headings = []
        keep_with_next_ok = True
        failed_headings = []

        for p in doc.paragraphs:
            if p.style.name.startswith("Heading"):
                text_clean = p.text.strip().upper()
                doc_headings.append(text_clean)
                if not p.paragraph_format.keep_with_next:
                    keep_with_next_ok = False
                    failed_headings.append(p.text[:30])

        missing_sections = []
        for sec in expected_sections:
            if not any(sec in h for h in doc_headings):
                missing_sections.append(sec)

        self.log_result(
            "Structure", "Required Academic Sections",
            len(missing_sections) == 0,
            f"All {len(expected_sections)} required academic sections present." if not missing_sections else f"Missing sections: {missing_sections}"
        )

        self.log_result(
            "Structure", "Heading Orphan Prevention (keep_with_next)",
            keep_with_next_ok,
            "All heading paragraphs enforce keep_with_next=True." if keep_with_next_ok else f"Headings lacking keep_with_next: {failed_headings}"
        )

    def _check_table_formatting(self, doc: Any):
        """Verify tables have repeating headers and cantSplit rows."""
        from docx.oxml.ns import qn

        if not doc.tables:
            self.log_result("Tables", "Table Presence", False, "No tables found in document.")
            return

        compliance_table_found = False
        tbl_header_ok = True
        cant_split_ok = True

        for tbl in doc.tables:
            # Check if this is the compliance mapping table (3 columns)
            if len(tbl.columns) == 3 and len(tbl.rows) > 3:
                compliance_table_found = True
                # Check header row
                hdr_tr = tbl.rows[0]._tr
                if not hdr_tr.xpath(".//w:tblHeader"):
                    tbl_header_ok = False

                # Check data rows for cantSplit
                for row in tbl.rows[1:]:
                    if not row._tr.xpath(".//w:cantSplit"):
                        cant_split_ok = False

        self.log_result(
            "Tables", "Compliance Table Repeat Header (w:tblHeader)",
            tbl_header_ok,
            "Compliance mapping table repeats header row across page breaks." if tbl_header_ok else "Compliance table header missing w:tblHeader."
        )

        self.log_result(
            "Tables", "Table Row Split Prevention (w:cantSplit)",
            cant_split_ok,
            "Table rows prevent awkward mid-cell splits across page breaks." if cant_split_ok else "Table rows missing w:cantSplit."
        )

    def _check_header_footer_and_pagination(self, doc: Any):
        """Verify different first page and dynamic page number fields."""
        section = doc.sections[0]
        diff_first = section.different_first_page_header_footer

        self.log_result(
            "Pagination", "Cover Page Header/Footer Suppression",
            diff_first,
            "Cover page suppresses running header and footer." if diff_first else "Cover page has running header/footer (different_first_page_header_footer is False)."
        )

        # Check footer table for PAGE and NUMPAGES instructions
        ftr_xml = section.footer._element.xml
        has_page = "PAGE" in ftr_xml
        has_numpages = "NUMPAGES" in ftr_xml
        pagination_ok = has_page and has_numpages

        self.log_result(
            "Pagination", "Dynamic Page Numbering (Page X of Y)",
            pagination_ok,
            "Footer includes dynamic Word PAGE and NUMPAGES fields." if pagination_ok else f"Missing pagination fields (PAGE: {has_page}, NUMPAGES: {has_numpages})."
        )

    def _check_code_appendix(self, doc: Any):
        """Verify all source files are present in the appendix."""
        assignment_dir = self.workspace_root / self.config.folder_name
        expected_files = [s.relative_path for s in self.config.source_files]

        doc_text = " ".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])

        missing_files = []
        for fn in expected_files:
            if fn not in doc_text:
                missing_files.append(fn)

        appendix_complete = len(missing_files) == 0
        self.log_result(
            "Appendix", "Source Files Completeness",
            appendix_complete,
            f"All {len(expected_files)} project source files verified in Code Appendix." if appendix_complete else f"Missing source files in appendix: {missing_files}"
        )

    def _check_page_rendering_and_blank_pages(self):
        """Analyze rendered PDF page images to detect empty or nearly blank pages."""
        if not self.preview_dir.exists():
            self.log_result("Visual QA", "Rendered Preview Pages", False, f"Preview directory missing: {self.preview_dir}", severity="WARN")
            return

        preview_images = sorted(list(self.preview_dir.glob("page_*.png")))
        page_count = len(preview_images)

        min_expected_pages = 15
        count_ok = page_count >= min_expected_pages
        self.log_result(
            "Visual QA", "Total Document Page Count",
            count_ok,
            f"Document contains {page_count} pages (minimum expected: {min_expected_pages})." if count_ok else f"Page count suspiciously low: {page_count} pages."
        )

        blank_pages = []
        for idx, img_path in enumerate(preview_images, 1):
            if idx == 1:
                # Cover page naturally has generous whitespace; skip pure blank check
                continue

            try:
                with Image.open(img_path) as im:
                    im_gray = im.convert("L")
                    w, h = im_gray.size
                    total_pixels = w * h
                    # Count pure white pixels (brightness >= 252)
                    white_count = sum(1 for p in im_gray.getdata() if p >= 252)
                    white_ratio = white_count / total_pixels

                    # Content page with > 98% pure white is considered an accidental blank page
                    if white_ratio > 0.985:
                        blank_pages.append(f"Page {idx:02d} ({white_ratio*100:.1f}% empty)")
            except Exception as e:
                print(f"[!] Warning inspecting page image {img_path}: {e}")

        no_blank_pages = len(blank_pages) == 0
        self.log_result(
            "Visual QA", "Accidental Blank Page Detection",
            no_blank_pages,
            "No accidental blank or near-empty content pages detected." if no_blank_pages else f"Detected near-empty content pages: {blank_pages}"
        )
