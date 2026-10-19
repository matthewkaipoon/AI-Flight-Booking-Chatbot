import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_csv(filename: str, required_cols=None) -> pd.DataFrame:
    csv_path = DATA_DIR / filename

    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit("Error: Could not read CSV at {csv_path}")
    
    if required_cols:
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise SystemExit("Error: Missing columns {missing}")
        
    return df
    