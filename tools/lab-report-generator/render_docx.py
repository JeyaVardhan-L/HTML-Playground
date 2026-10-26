"""
render_docx.py: Utility to render DOCX files to PDF using native Microsoft Word COM,
and export PDF pages to PNG images for visual inspection using pypdfium2.
"""

import os
import sys
import argparse
from pathlib import Path

def docx_to_pdf(docx_path: Path, pdf_path: Path) -> bool:
    """
    Convert DOCX to PDF using native Microsoft Word COM via PowerShell.
    Explicitly raises RuntimeError if conversion fails or output is invalid.
    """
    docx_path = Path(docx_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    if not docx_path.exists():
        raise FileNotFoundError(f"Source DOCX file not found: {docx_path}")
    if docx_path.stat().st_size == 0:
        raise ValueError(f"Source DOCX file is empty (0 bytes): {docx_path}")

    # Ensure target parent directory exists and remove any stale output file
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if pdf_path.exists():
        try:
            pdf_path.unlink()
        except Exception as e:
            raise RuntimeError(f"Unable to remove existing target PDF {pdf_path}: {e}")

    docx_abs = str(docx_path)
    pdf_abs = str(pdf_path)

    # PowerShell script for reliable Word COM automation
    ps_script = f"""
$ErrorActionPreference = "Stop"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {{
    $doc = $word.Documents.Open("{docx_abs}")
    $doc.SaveAs([ref]"{pdf_abs}", [ref]17)
    $doc.Close([ref]0)
    Write-Host "RENDER_PDF_SUCCESS"
}} catch {{
    Write-Error $_
    exit 1
}} finally {{
    $word.Quit()
}}
"""
    import subprocess
    res = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_script],
        capture_output=True,
        text=True
    )

    if res.returncode != 0 or "RENDER_PDF_SUCCESS" not in res.stdout:
        err_msg = res.stderr.strip() or res.stdout.strip() or f"Process exited with code {res.returncode}"
        raise RuntimeError(f"Microsoft Word PDF conversion failed: {err_msg}")

    if not pdf_path.exists():
        raise RuntimeError(f"PDF conversion completed without error, but output PDF was not found at {pdf_path}")

    if pdf_path.stat().st_size < 1024:
        raise RuntimeError(f"Generated PDF file at {pdf_path} is suspiciously small ({pdf_path.stat().st_size} bytes)")

    return True


def pdf_to_images(pdf_path: Path, output_dir: Path) -> list:
    """Render PDF pages to 150 DPI PNG images for visual inspection."""
    import pypdfium2 as pdfium
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf = pdfium.PdfDocument(str(pdf_path))
    image_paths = []

    for i, page in enumerate(pdf):
        # Render at 150 DPI for crisp visual inspection
        image = page.render(scale=150 / 72).to_pil()
        out_path = output_dir / f"page_{i + 1:02d}.png"
        image.save(out_path)
        image_paths.append(out_path)

    return image_paths


def render_and_inspect(docx_path: str, output_dir: str = None, pdf_path: str = None):
    """
    High-level utility to convert DOCX to PDF and export page preview images.
    Raises explicit exceptions on failure so calling processes never proceed with stale files.
    """
    docx = Path(docx_path).resolve()
    if not docx.exists():
        raise FileNotFoundError(f"File not found: {docx}")

    if pdf_path is None:
        target_pdf = docx.parent / f"{docx.stem}.pdf"
    else:
        target_pdf = Path(pdf_path).resolve()

    if output_dir is None:
        out_dir = docx.parent / "preview_pages"
    else:
        out_dir = Path(output_dir).resolve()

    print(f"[*] Converting {docx.name} -> {target_pdf.name} via Microsoft Word COM...")
    docx_to_pdf(docx, target_pdf)

    print(f"[*] Rendering PDF pages to PNG preview in {out_dir}...")
    pages = pdf_to_images(target_pdf, out_dir)
    print(f"[+] Rendered {len(pages)} pages successfully.")
    return target_pdf, pages

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render DOCX to PDF and PNGs")
    parser.add_argument("docx", help="Path to DOCX file")
    parser.add_argument("--outdir", default=None, help="Output directory for PNGs")
    args = parser.parse_args()
    
    render_and_inspect(args.docx, args.outdir)
