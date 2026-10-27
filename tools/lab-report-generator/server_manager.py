"""
Process and server lifecycle manager for WAF Lab Report Generator.
Discovers free ports, spawns servers cleanly, waits for readiness,
and strictly shuts down only the processes started by the generator.
"""

import atexit
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional, List


def find_free_port(preferred_port: int = 8000) -> int:
    """Find an available TCP port, attempting preferred_port first."""
    # Test preferred port first
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferred_port))
            return preferred_port
        except OSError:
            pass

    # If preferred port is busy, get an ephemeral free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        return s.getsockname()[1]


class ServerManager:
    """Manages the lifecycle of an application server subprocess."""

    def __init__(
        self,
        workspace_root: Path,
        assignment_dir: Path,
        server_type: str = "static_http",
        server_dir: Optional[Path] = None,
        default_port: int = 8000
    ):
        self.workspace_root = workspace_root
        self.assignment_dir = assignment_dir
        self.server_dir = server_dir or assignment_dir
        self.server_type = server_type
        self.port = find_free_port(default_port) if server_type != "none" else default_port
        self.process: Optional[subprocess.Popen] = None
        self._is_stopped = False

        # Register cleanup to ensure no orphan processes remain
        atexit.register(self.stop)

    def start(self, custom_command: Optional[List[str]] = None, entry_url: str = "/index.html", timeout_secs: float = 15.0) -> str:
        """Start the server and wait for the entry point to become responsive."""
        if self.server_type == "none":
            print(f"[*] Server type is 'none'. No background server required.")
            return ""

        if self.process is not None:
            return f"http://localhost:{self.port}"

        print(f"[*] Starting {self.server_type} server for '{self.server_dir.name}' on port {self.port}...")

        cwd = self.server_dir
        env = os.environ.copy()
        env["PORT"] = str(self.port)

        if custom_command:
            cmd = [arg.replace("{port}", str(self.port)) for arg in custom_command]
        elif self.server_type == "static_http":
            # Use current Python interpreter to run http.server
            cmd = [
                sys.executable,
                "-m",
                "http.server",
                str(self.port),
                "--directory",
                str(self.server_dir)
            ]
        elif self.server_type in ("express", "node_express"):
            # For Express or Node applications, dynamically locate entry file
            if (cwd / "server.js").exists():
                cmd = ["node", "server.js"]
            elif (cwd / "app.js").exists():
                cmd = ["node", "app.js"]
            elif (cwd / "api" / "server.js").exists():
                cmd = ["node", "api/server.js"]
            else:
                cmd = ["node", "server.js"]
        else:
            raise ValueError(f"Unsupported server type: {self.server_type}")

        # Start subprocess
        self.process = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        )

        base_url = f"http://localhost:{self.port}"
        target_url = f"{base_url}{entry_url}"
        print(f"[*] Waiting for server readiness at {target_url}...")

        start_time = time.time()
        ready = False
        last_error = None

        while time.time() - start_time < timeout_secs:
            # Check if process died prematurely
            if self.process.poll() is not None:
                _, stderr = self.process.communicate()
                raise RuntimeError(
                    f"Server process terminated unexpectedly with exit code {self.process.returncode}. "
                    f"Stderr: {stderr.decode('utf-8', errors='ignore')}"
                )

            try:
                req = urllib.request.Request(
                    target_url,
                    headers={"User-Agent": "WAF-LabReportGenerator-HealthCheck"}
                )
                with urllib.request.urlopen(req, timeout=1.0) as response:
                    if response.status in (200, 304):
                        ready = True
                        break
            except Exception as e:
                last_error = e
                time.sleep(0.2)

        if not ready:
            self.stop()
            raise TimeoutError(
                f"Server failed to become responsive at {target_url} within {timeout_secs}s. "
                f"Last error: {last_error}"
            )

        print(f"[+] Server is ready and responsive at {base_url}")
        return base_url

    def stop(self):
        """Cleanly terminate only the process spawned by this manager."""
        if self._is_stopped or self.process is None:
            return

        self._is_stopped = True
        pid = self.process.pid
        print(f"[*] Shutting down server process (PID: {pid})...")

        try:
            if os.name == "nt":
                # On Windows, kill the process tree to avoid orphan children
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False
                )
            else:
                self.process.terminate()
                self.process.wait(timeout=3)
        except Exception as e:
            try:
                self.process.kill()
            except Exception:
                pass
        finally:
            self.process = None
            print(f"[+] Server process (PID: {pid}) terminated successfully.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
