import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
VAULT_DIR = BASE_DIR / "my_vault"
SHADOW_DIR = BASE_DIR / ".shadow_backup"
DB_PATH = BASE_DIR / "vault_state.db"

# Agent Thresholds
SUSPICIOUS_INTERVAL_SECONDS = 2
SUSPICIOUS_BURST_COUNT = 3

def ensure_directories():
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    SHADOW_DIR.mkdir(parents=True, exist_ok=True)
    # Hide shadow backup directory on Windows
    if os.name == 'nt':
        import ctypes
        FILE_ATTRIBUTE_HIDDEN = 0x02
        try:
            ctypes.windll.kernel32.SetFileAttributesW(str(SHADOW_DIR), FILE_ATTRIBUTE_HIDDEN)
        except Exception:
            pass
