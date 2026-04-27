import shutil
import os
from pathlib import Path
from .config import VAULT_DIR, SHADOW_DIR
from .state_manager import StateManager

class SelfHealer:
    def __init__(self):
        self.state = StateManager()

    def sync_to_shadow(self):
        """Copies all current files from vault to shadow, overriding existing."""
        for item in VAULT_DIR.iterdir():
            if item.is_file():
                shutil.copy2(item, SHADOW_DIR / item.name)

    def restore_file(self, file_name: str):
        """Restores a specific file from the shadow backup to the vault."""
        shadow_path = SHADOW_DIR / file_name
        vault_path = VAULT_DIR / file_name
        
        if shadow_path.exists():
            shutil.copy2(shadow_path, vault_path)
            self.state.log_thought("HealingAgent", f"Restored deleted/modified file: {file_name} from shadow backup.")
            return True
        else:
            self.state.log_thought("HealingAgent", f"Could not restore {file_name}: not found in shadow backup.")
            return False
