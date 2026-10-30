import subprocess
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
scratch_dir = BASE_DIR / 'scratch'
scratch_dir.mkdir(exist_ok=True)

edge_exe = r"C:\Program Files (x86)\Microsoft\EdgeCore\156.0.4314.50\msedge.exe"
if not os.path.exists(edge_exe):
    print(f"Error: Edge binary not found at {edge_exe}")
    exit(1)

targets = [
    {
        "url": "http://127.0.0.1:5001/",
        "output": str(scratch_dir / "staging_home_desktop.png"),
        "size": "--window-size=1280,800",
        "desc": "Desktop Homepage (1280x800)"
    },
    {
        "url": "http://127.0.0.1:5001/",
        "output": str(scratch_dir / "staging_home_mobile.png"),
        "size": "--window-size=390,844",
        "desc": "Mobile Viewport Homepage (390x844)"
    },
    {
        "url": "http://127.0.0.1:5001/auth/login",
        "output": str(scratch_dir / "staging_login.png"),
        "size": "--window-size=1280,800",
        "desc": "Login Page (1280x800)"
    },
    {
        "url": "http://127.0.0.1:5001/events/1",
        "output": str(scratch_dir / "staging_event_detail.png"),
        "size": "--window-size=1280,800",
        "desc": "Event Detail Page (1280x800)"
    }
]

print(f"Executing Microsoft Edge Core Headless QA...")
print(f"Edge Binary: {edge_exe}")

for t in targets:
    cmd = [
        edge_exe,
        "--headless=new",
        "--disable-gpu",
        f"--screenshot={t['output']}",
        t["size"],
        t["url"]
    ]
    print(f"Capturing: {t['desc']} -> {t['output']}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(t["output"]):
        size = os.path.getsize(t["output"])
        print(f"  [OK] Saved ({size} bytes)")
    else:
        print(f"  [FAIL] Could not capture screenshot. Stderr: {res.stderr[:200]}")

print("Microsoft Edge QA capture complete.")

