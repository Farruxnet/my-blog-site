from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


if __name__ == "__main__":
    script = ROOT / "scripts" / "build_post.py"
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "content" / "test-post.md"
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "post.html"
    raise SystemExit(subprocess.call([sys.executable, str(script), str(source), str(target)]))
