import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ETL scripts in execution order
scripts = [
    "etl/load.py",
    "etl/load_date.py",
    "etl/load_fact.py"
]

print("=" * 50)
print("SALES DATA WAREHOUSE - ETL PIPELINE")
print("Started:", datetime.now())
print("=" * 50)

for script in scripts:

    print(f"\nRunning: {script}", flush=True)

    subprocess.run(
        [sys.executable, script],
        cwd=PROJECT_ROOT,
        check=True
    )

    print(f"Completed: {script}", flush=True)

print("\n" + "=" * 50)
print("ETL PIPELINE COMPLETED SUCCESSFULLY")
print("Finished:", datetime.now())
print("=" * 50)