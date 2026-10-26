"""
render_docx.py: Utility to render DOCX files to PDF using native Microsoft Word COM,
and export PDF pages to PNG images for visual inspection using pypdfium2.
"""

import os
import sys
import argparse
from pathlib import Path

def docx_to_pdf(docx_path: Path, pdf_path: Path) -> bool:
    try:
        import win32com.client
    except ImportError:
        # Fallback to subprocess via PowerShell COM if pywin32 not installed
        pass

    docx_abs = str(docx_path.resolve())
    pdf_abs = str(pdf_path.resolve())

    # Use PowerShell script execution for reliable Word COM automation
    ps_script = f"""
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
    if "RENDER_PDF_SUCCESS" in res.stdout:
        return True
    else:
        print("Word conversion failed:", res.stderr or res.stdout, file=sys.stderr)
        return False

def pdf_to_images(pdf_path: Path, output_dir: Path) -> list:
    import pypdfium2 as pdfium
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf = pdfium.PdfDocument(str(pdf_path))
    image_paths = []
    
    for i, page in enumerate(pdf):
        # Render at 150 DPI for fast crisp inspection
        image = page.render(scale=150 / 72).to_pil()
        out_path = output_dir / f"page_{i + 1:02d}.png"
        image.save(out_path)
        image_paths.append(out_path)
        
    return image_paths

def render_and_inspect(docx_path: str, output_dir: str = None):
    docx = Path(docx_path)
    if not docx.exists():
        print(f"File not found: {docx}")
        return None, []
        
    if output_dir is None:
        out_dir = docx.parent / "rendered_pages"
    else:
        out_dir = Path(output_dir)
        
    pdf_path = docx.parent / f"{docx.stem}.pdf"
    print(f"Converting {docx.name} -> {pdf_path.name} via Microsoft Word...")
    success = docx_to_pdf(docx, pdf_path)
    if not success:
        return None, []
        
    print(f"Rendering pages to PNG in {out_dir}...")
    pages = pdf_to_images(pdf_path, out_dir)
    print(f"Rendered {len(pages)} pages successfully.")
    return pdf_path, pages

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render DOCX to PDF and PNGs")
    parser.add_argument("docx", help="Path to DOCX file")
    parser.add_argument("--outdir", default=None, help="Output directory for PNGs")
    args = parser.parse_args()
    
    render_and_inspect(args.docx, args.outdir)
