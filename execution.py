import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

MODE = sys.argv[1] if len(sys.argv) > 1 else ""

if MODE=="cli":
    from interfaces.cli import main
    main()
elif MODE=="gui":
    import subprocess,os
    subprocess.run(["streamlit", "run", str(ROOT / "interfaces" / "gui.py")],env = {**os.environ, "PYTHONPATH": str(ROOT)})
else:
    print("""Unrecognized mode,usage is either:
          uv run python execution.py cli
          uv run python execution.py gui
          """)