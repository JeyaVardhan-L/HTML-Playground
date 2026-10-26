"""
Browser automation and screenshot capture engine using Playwright.
Executes non-destructive navigation, interaction tests, and captures high-resolution screenshots.
"""

import time
from pathlib import Path
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright, Page, BrowserContext

from config import AssignmentConfig, ScreenshotScene


class BrowserRunner:
    """Orchestrates headless Chromium automation to test assignments and capture real output evidence."""

    def __init__(self, base_url: str, output_dir: Path):
        self.base_url = base_url.rstrip("/")
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_scenes(self, config: AssignmentConfig) -> List[Dict[str, Any]]:
        """Run all scenes defined in config and return captured screenshot metadata."""
        captured_evidence: List[Dict[str, Any]] = []

        print(f"[*] Launching Playwright Chromium to execute {len(config.scenes)} evidence scenes...")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--font-render-hinting=none"]
            )

            for i, scene in enumerate(config.scenes, 1):
                print(f"  [{i}/{len(config.scenes)}] Capturing scene '{scene.name}'...")
                screenshot_filename = f"{scene.name}.png"
                screenshot_path = self.output_dir / screenshot_filename

                # Create an isolated context per scene with requested viewport and device scale factor
                vp = scene.viewport
                context: BrowserContext = browser.new_context(
                    viewport={"width": vp.get("width", 1440), "height": vp.get("height", 900)},
                    device_scale_factor=2.0  # High DPI for crisp print quality
                )

                page: Page = context.new_page()

                try:
                    full_target_url = f"{self.base_url}{scene.url_path}"
                    page.goto(full_target_url, wait_until="networkidle", timeout=15000)

                    # Wait for selector if specified
                    if scene.wait_selector:
                        page.wait_for_selector(scene.wait_selector, timeout=5000)

                    # Execute custom actions
                    self._execute_actions(page, scene.actions)

                    # Ensure fonts and rendering settle
                    page.wait_for_timeout(500)

                    # Capture screenshot
                    page.screenshot(
                        path=str(screenshot_path),
                        full_page=scene.full_page
                    )

                    captured_evidence.append({
                        "name": scene.name,
                        "title": scene.title,
                        "caption": scene.caption,
                        "description": scene.description,
                        "requirement_tag": scene.requirement_tag,
                        "image_path": screenshot_path,
                        "url": full_target_url,
                        "status": "PASSED"
                    })
                    print(f"      [OK] Saved: {screenshot_path.name}")

                except Exception as e:
                    print(f"      [FAIL] Failed to capture scene '{scene.name}': {e}")
                    captured_evidence.append({
                        "name": scene.name,
                        "caption": scene.caption,
                        "description": f"FAILED CHECK: {scene.description}. Error: {str(e)}",
                        "requirement_tag": scene.requirement_tag,
                        "image_path": None,
                        "url": full_target_url,
                        "status": f"FAILED: {e}"
                    })
                finally:
                    context.close()

            browser.close()

        print(f"[+] All scenes executed. Successfully captured {sum(1 for e in captured_evidence if e['image_path'])} screenshots.")
        return captured_evidence

    def _execute_actions(self, page: Page, actions: List[Dict[str, Any]]):
        """Execute action sequence on page or within iframe."""
        for action in actions:
            action_type = action.get("type")

            if action_type == "wait_time":
                page.wait_for_timeout(action.get("ms", 500))

            elif action_type == "click":
                selector = action["selector"]
                page.wait_for_selector(selector, timeout=5000)
                page.click(selector)

            elif action_type == "fill":
                selector = action["selector"]
                page.wait_for_selector(selector, timeout=5000)
                page.fill(selector, action["value"])

            elif action_type == "iframe_action":
                frame_selector = action["frame_selector"]
                sub = action["sub_action"]
                sub_type = sub.get("type")
                frame = page.frame_locator(frame_selector)

                if sub_type == "fill":
                    target_sel = sub["selector"]
                    frame.locator(target_sel).fill(sub["value"])

                elif sub_type == "click":
                    target_sel = sub["selector"]
                    frame.locator(target_sel).click()

                elif sub_type == "fill_survey":
                    # Specialized non-destructive survey form filling
                    name_input = frame.locator("#studentName")
                    if name_input.count() > 0:
                        name_input.fill(sub.get("name", "Jey"))

                    email_input = frame.locator("#studentEmail")
                    if email_input.count() > 0:
                        email_input.fill(sub.get("email", "student@gitam.in"))

                    fav_model = frame.locator("#favModel")
                    if fav_model.count() > 0:
                        fav_model.select_option(label=sub.get("model", "Anthropic Claude 3.5 Sonnet"))

                    use_case = frame.locator("#primaryUseCase")
                    if use_case.count() > 0:
                        use_case.select_option(label=sub.get("use_case", "Software Engineering & Coding"))

                    exp = sub.get("experience", "Advanced")
                    exp_radio = frame.locator(f'input[name="experience"][value="{exp}"]')
                    if exp_radio.count() > 0:
                        exp_radio.check()

                    # Checkboxes
                    for cap in sub.get("capabilities", []):
                        cb = frame.locator(f'input[name="capabilities"][value="{cap}"]')
                        if cb.count() > 0:
                            cb.check()

                    comments = frame.locator("#surveyComments")
                    if comments.count() > 0:
                        comments.fill(sub.get("comments", "Verified via automated test runner."))

                    # Submit form
                    submit_btn = frame.locator('button[type="submit"]')
                    if submit_btn.count() > 0:
                        submit_btn.click()

                    # Wait for feedback card to appear and ensure it is scrolled into view
                    page.wait_for_timeout(600)
                    result_card = frame.locator("#surveyResultCard")
                    if result_card.count() > 0:
                        result_card.scroll_into_view_if_needed()
                    page.wait_for_timeout(500)
