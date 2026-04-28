import os
import time
import subprocess
from core.config import ensure_directories, VAULT_DIR
from core.state_manager import StateManager
from agents.deception import DeceptionAgent
from agents.sensor import start_sensor

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    try:
                        k, v = line.strip().split('=', 1)
                        os.environ[k.strip()] = v.strip()
                    except ValueError:
                        pass
    if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

def main():
    load_env()
    ensure_directories()

    state = StateManager()
    state.update_status("Normal")
    
    deception = DeceptionAgent(state)
    print("Generating initial Honey Assets using Gemini...")
    deception.deploy_honey_assets()
    
    # Start Streamlit dashboard
    print("Starting Streamlit Dashboard...")
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.py')
    import sys
    port = os.environ.get("PORT", "8501")
    cmd = [sys.executable, "-m", "streamlit", "run", dashboard_path, "--server.port", port, "--server.address", "0.0.0.0", "--server.headless", "true"]
    streamlit_proc = subprocess.Popen(cmd)
    
    print("Vault Tripwire Armed. Waiting for Hacker...")
    observer = start_sensor(state, deception)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        streamlit_proc.terminate()
        observer.join()

if __name__ == "__main__":
    main()
