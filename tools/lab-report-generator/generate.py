#!/usr/bin/env python3
"""
Master CLI Entry Point for WAF Lab Report Generator.
Orchestrates assignment discovery, server startup, browser automation,
evidence capture, and Word document generation.

Usage:
    python tools/lab-report-generator/generate.py --assignment 2
    python tools/lab-report-generator/generate.py --assignment 2 --student-name "Jey" --roll-no "9057"
"""

import argparse
import shutil
import sys
import time
from pathlib import Path

# Configure stdout and stderr for UTF-8 encoding
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add current directory to sys.path to allow clean imports
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from config import get_assignment_config, ASSIGNMENT_REGISTRY
from server_manager import ServerManager
from browser_runner import BrowserRunner
from doc_builder import LabReportDocBuilder


def resolve_workspace_root() -> Path:
    """Find the root directory of the HTML-Playground repository."""
    # Current script is at: HTML-Playground/tools/lab-report-generator/generate.py
    candidate = CURRENT_DIR.parent.parent
    if (candidate / "Assignment-2").is_dir():
        return candidate
    # Fallback to current working directory
    cwd = Path.cwd().resolve()
    if (cwd / "Assignment-2").is_dir():
        return cwd
    if (cwd / "HTML-Playground" / "Assignment-2").is_dir():
        return cwd / "HTML-Playground"
    return candidate


def main():
    parser = argparse.ArgumentParser(
        description="Automated WAF Lab Report Generator for HTML-Playground.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-a", "--assignment",
        type=int,
        required=True,
        help="Assignment number to generate report for (e.g. 2, 3, 4, 5, 6, 7)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=None,
        help="Custom output directory for the report (default: reports/Assignment-{id})"
    )
    parser.add_argument(
        "--student-name",
        type=str,
        default=None,
        help="Student name for report cover and headers"
    )
    parser.add_argument(
        "--roll-no",
        type=str,
        default=None,
        help="Student roll/registration number"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=None,
        help="Preferred port for the application server"
    )
    parser.add_argument(
        "--skip-render",
        action="store_true",
        help="Skip automatic PDF and visual QA rendering"
    )

    args = parser.parse_args()

    workspace_root = resolve_workspace_root()
    print("=" * 70)
    print("      WAF AUTOMATED LAB REPORT GENERATOR")
    print("=" * 70)
    print(f"[*] Workspace Root: {workspace_root}")
    print(f"[*] Target Assignment: {args.assignment}")

    # Load configuration
    try:
        config = get_assignment_config(args.assignment)
    except Exception as e:
        print(f"[!] Configuration error: {e}")
        sys.exit(1)

    assignment_dir = workspace_root / config.folder_name
    if not assignment_dir.is_dir():
        print(f"[!] Error: Assignment folder '{config.folder_name}' not found at {assignment_dir}")
        sys.exit(1)

    # Resolve output directory & file
    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
    else:
        output_dir = workspace_root / "reports" / f"Assignment-{config.assignment_id}"

    output_dir.mkdir(parents=True, exist_ok=True)
    screenshots_dir = output_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    report_filename = f"WAF_Assignment_{config.assignment_id}.docx"
    pdf_filename = f"WAF_Assignment_{config.assignment_id}.pdf"
    final_docx_path = output_dir / report_filename
    final_pdf_path = output_dir / pdf_filename

    # Staging directory for atomic generation
    stage_dir = output_dir / ".stage"
    stage_dir.mkdir(parents=True, exist_ok=True)
    stage_docx = stage_dir / report_filename
    stage_pdf = stage_dir / pdf_filename
    stage_preview = stage_dir / "preview_pages"
    stage_preview.mkdir(parents=True, exist_ok=True)

    port = args.port or config.default_port
    start_time = time.time()

    # Step 1: Start Server
    with ServerManager(
        workspace_root=workspace_root,
        assignment_dir=assignment_dir,
        server_type=config.server_type,
        default_port=port
    ) as srv:
        base_url = srv.start(
            custom_command=config.server_command,
            entry_url=config.entry_url
        )

        # Step 2: Browser Automation & Screenshots
        runner = BrowserRunner(base_url=base_url, output_dir=screenshots_dir)
        evidence_list = runner.run_scenes(config)

    # Step 3: Document Generation to Staged Output
    print(f"\n[*] Generating report into staging area: {stage_docx}...")
    builder = LabReportDocBuilder(
        config=config,
        workspace_root=workspace_root,
        student_name=args.student_name,
        roll_no=args.roll_no
    )
    builder.build_report(evidence_list=evidence_list, output_path=stage_docx)

    # Step 4: Native Microsoft Word PDF Conversion & Visual Rendering
    rendered_pages = []
    if not args.skip_render:
        from render_docx import render_and_inspect
        try:
            print(f"[*] Rendering staged DOCX to PDF and page previews...")
            pdf_path, rendered_pages = render_and_inspect(
                docx_path=str(stage_docx),
                output_dir=str(stage_preview),
                pdf_path=str(stage_pdf)
            )
        except Exception as ren_err:
            print(f"[!] FATAL: Microsoft Word PDF conversion failed: {ren_err}")
            shutil.rmtree(stage_dir, ignore_errors=True)
            sys.exit(1)

    # Step 5: Automated Quality Assurance (QA) Audit
    print(f"[*] Running automated quality assurance audit...")
    from qa_checker import LabReportQAChecker
    qa = LabReportQAChecker(
        docx_path=stage_docx,
        pdf_path=stage_pdf,
        preview_dir=stage_preview,
        config=config,
        evidence_list=evidence_list,
        workspace_root=workspace_root
    )
    all_passed, qa_results = qa.run_all_checks()

    if not all_passed:
        print("[!] ERROR: Automated quality audit failed. Pre-existing report will NOT be replaced.")
        shutil.rmtree(stage_dir, ignore_errors=True)
        sys.exit(1)

    # Step 6: Atomic Replacement of Final Artifacts
    print(f"[*] QA audit passed. Performing atomic replacement of final report files...")
    shutil.copy2(stage_docx, final_docx_path)
    if stage_pdf.exists():
        shutil.copy2(stage_pdf, final_pdf_path)

    final_preview_dir = output_dir / "preview_pages"
    if stage_preview.exists() and list(stage_preview.glob("*.png")):
        if final_preview_dir.exists():
            shutil.rmtree(final_preview_dir, ignore_errors=True)
        shutil.copytree(stage_preview, final_preview_dir)

    # Clean up staging area
    shutil.rmtree(stage_dir, ignore_errors=True)

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print("               GENERATION & QA AUDIT COMPLETE")
    print("=" * 70)
    print(f"[+] Final Word Document:  {final_docx_path}")
    print(f"[+] Total Word Size:      {final_docx_path.stat().st_size / 1024:.1f} KB")
    if final_pdf_path.exists():
        print(f"[+] Final PDF Document:   {final_pdf_path}")
        print(f"[+] Total PDF Size:       {final_pdf_path.stat().st_size / 1024:.1f} KB")
    print(f"[+] Screenshots Captured: {len(evidence_list)} images in {screenshots_dir}")
    if rendered_pages:
        print(f"[+] Visual QA Preview:    {len(rendered_pages)} pages rendered to {final_preview_dir}")
    print(f"[+] Total Elapsed Time:   {elapsed:.1f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    main()
