"""
cli_runner.py: CLI and Terminal Evidence Capture Engine.
Executes real Node.js and MongoDB script commands, captures genuine terminal
outputs (stdout, stderr, exit code), and renders high-resolution terminal cards
via Playwright for inclusion in academic lab reports.
"""

import html
import os
import re
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright

from config import CliCommandSpec


class CliRunner:
    """Executes CLI commands and captures authentic output evidence."""

    def __init__(self, workspace_root: Path, output_dir: Path):
        self.workspace_root = Path(workspace_root).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_commands(
        self,
        commands: List[CliCommandSpec],
        assignment_dir: Optional[Path] = None
    ) -> List[Dict[str, Any]]:
        """Execute a list of CLI command specs and return evidence records."""
        assignment_dir = assignment_dir or self.workspace_root
        evidence_records: List[Dict[str, Any]] = []

        print(f"[*] Executing {len(commands)} CLI evidence commands...")

        for idx, spec in enumerate(commands, start=1):
            print(f"  [{idx}/{len(commands)}] Executing CLI spec '{spec.name}'...")

            cwd = assignment_dir
            if spec.cwd_relative:
                cwd = (assignment_dir / spec.cwd_relative).resolve()

            cmd_str = " ".join(spec.command)
            env = os.environ.copy()
            if spec.env_vars:
                env.update(spec.env_vars)

            start_t = time.time()
            try:
                res = subprocess.run(
                    spec.command,
                    cwd=str(cwd),
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=20,
                    encoding="utf-8",
                    errors="replace",
                    shell=(os.name == "nt")
                )
                elapsed = time.time() - start_t
                stdout_text = res.stdout.strip()
                stderr_text = res.stderr.strip()
                returncode = res.returncode
            except Exception as e:
                elapsed = time.time() - start_t
                stdout_text = ""
                stderr_text = f"Command execution failed: {e}"
                returncode = 1

            combined_output = stdout_text
            if stderr_text:
                combined_output = (stdout_text + "\n" + stderr_text).strip() if stdout_text else stderr_text

            # Strip ANSI escape sequences (e.g. colors from vite/npm/chalk)
            combined_output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', combined_output)

            # Save raw output text log
            txt_filename = f"{spec.name}.txt"
            txt_path = self.output_dir / txt_filename
            txt_path.write_text(combined_output, encoding="utf-8")

            # Render crisp terminal card image via Playwright
            png_filename = f"{spec.name}.png"
            png_path = self.output_dir / png_filename

            try:
                self._render_terminal_card(
                    command_str=cmd_str,
                    output_text=combined_output,
                    target_image=png_path,
                    title=spec.title,
                    returncode=returncode,
                    elapsed_sec=elapsed
                )
                status_str = "PASSED" if returncode == 0 else f"FAILED (Exit Code {returncode})"
            except Exception as render_err:
                print(f"      [!] Warning: Failed to render terminal card for '{spec.name}': {render_err}")
                png_path = None
                status_str = f"EXEC_OK_RENDER_FAIL: {render_err}"

            evidence_records.append({
                "name": spec.name,
                "title": spec.title,
                "caption": spec.caption,
                "description": spec.description,
                "requirement_tag": spec.requirement_tag,
                "image_path": png_path,
                "command": cmd_str,
                "terminal_output": combined_output,
                "status": status_str
            })
            print(f"      [{'OK' if returncode == 0 else 'FAIL'}] Saved: {png_filename if png_path else txt_filename}")

        print(f"[+] CLI execution complete. Processed {len(evidence_records)} command evidence records.")
        return evidence_records

    def _render_terminal_card(
        self,
        command_str: str,
        output_text: str,
        target_image: Path,
        title: str,
        returncode: int,
        elapsed_sec: float
    ):
        """Render command and output into an authentic, high-DPI terminal card."""
        safe_cmd = html.escape(command_str)
        safe_title = html.escape(title)
        safe_output = html.escape(output_text) if output_text else "<i>(No console output returned)</i>"

        badge_color = "#28a745" if returncode == 0 else "#dc3545"
        badge_text = "EXIT: 0 (SUCCESS)" if returncode == 0 else f"EXIT: {returncode} (FAILED)"

        # Cap lines to fit comfortably without excessive vertical stretching
        lines = safe_output.splitlines()
        if len(lines) > 35:
            safe_output = "\n".join(lines[:35]) + f"\n\n... [{len(lines) - 35} lines truncated for report presentation] ..."

        card_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background-color: transparent;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 16px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  .terminal-window {{
    width: 900px;
    background-color: #1e1e24;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    overflow: hidden;
    border: 1px solid #333340;
  }}
  .window-bar {{
    background-color: #16161c;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #2a2a36;
  }}
  .window-dots {{
    display: flex;
    gap: 7px;
  }}
  .dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }}
  .dot-red {{ background-color: #ff5f56; }}
  .dot-yellow {{ background-color: #ffbd2e; }}
  .dot-green {{ background-color: #27c93f; }}
  .window-title {{
    flex: 1;
    text-align: center;
    color: #9ba1b0;
    font-size: 12px;
    font-family: "Consolas", monospace;
    font-weight: 500;
    margin-right: 48px;
  }}
  .terminal-body {{
    padding: 18px 22px;
    color: #e2e4ea;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 13.5px;
    line-height: 1.5;
  }}
  .prompt-row {{
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px dashed #343444;
  }}
  .prompt-symbol {{
    color: #4ec9b0;
    font-weight: bold;
    margin-right: 10px;
  }}
  .command-text {{
    color: #f1f2f6;
    font-weight: 600;
    flex: 1;
  }}
  .badge {{
    font-size: 11px;
    font-weight: bold;
    padding: 2px 8px;
    border-radius: 4px;
    background-color: {badge_color};
    color: #ffffff;
    margin-left: 8px;
  }}
  .output-pre {{
    white-space: pre-wrap;
    word-break: break-all;
    color: #d1d5db;
    font-size: 12.5px;
    max-height: 520px;
  }}
</style>
</head>
<body>
  <div class="terminal-window">
    <div class="window-bar">
      <div class="window-dots">
        <div class="dot dot-red"></div>
        <div class="dot dot-yellow"></div>
        <div class="dot dot-green"></div>
      </div>
      <div class="window-title">{safe_title} — Terminal Session ({elapsed_sec:.2f}s)</div>
    </div>
    <div class="terminal-body">
      <div class="prompt-row">
        <span class="prompt-symbol">$</span>
        <span class="command-text">{safe_cmd}</span>
        <span class="badge">{badge_text}</span>
      </div>
      <pre class="output-pre">{safe_output}</pre>
    </div>
  </div>
</body>
</html>"""

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 960, "height": 800}, device_scale_factor=2.0)
            page.set_content(card_html, wait_until="networkidle")
            card_elem = page.locator(".terminal-window")
            card_elem.screenshot(path=str(target_image))
            browser.close()
