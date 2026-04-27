import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.state_manager import StateManager
from core.config import VAULT_DIR
from agents.deception import DeceptionAgent
import threading

class VaultSensor(FileSystemEventHandler):
    def __init__(self, state_manager: StateManager, deception_agent: DeceptionAgent):
        self.state = state_manager
        self.deception = deception_agent
        self.armed = True

    def _process(self, event):
        if event.is_directory: return
        fname = os.path.basename(event.src_path)
        
        if fname.endswith('~') or fname.endswith('.tmp'): return
        
        self.state.log_event("access", f"File touched: {fname}", "unknown")
        
        # Check if they touched the Honey Asset!
        if self.armed and self.state.is_honey_asset(fname):
            self.armed = False # Prevent multi-triggers from opening multiple files
            self.state.log_event("system", f"!!! HONEY TRAP ACTIVATED BY {fname} !!!", "sys")
            # Run the autonomous Counter-OPTrace asynchronously
            threading.Thread(target=self.deception.run_counter_operation, args=(fname,)).start()

    def on_modified(self, event): self._process(event)
    def on_deleted(self, event): self._process(event)

def start_sensor(state_manager: StateManager, deception_agent: DeceptionAgent):
    obs = Observer()
    handler = VaultSensor(state_manager, deception_agent)
    obs.schedule(handler, str(VAULT_DIR), recursive=False)
    obs.start()
    return obs
