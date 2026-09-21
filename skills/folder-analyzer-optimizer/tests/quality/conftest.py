"""Make the quality folder itself importable so `from scoring import ...` works."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
