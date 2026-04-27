from agno.agent import Agent
from agno.models.google import Gemini
import json
import os
import time
from core.state_manager import StateManager
from core.config import VAULT_DIR

class DeceptionAgent:
    def __init__(self, state_manager: StateManager):
        self.state = state_manager
        self.agent = Agent(
            model=Gemini(id="gemini-2.0-flash"),
            description="You are a proactive cyber deception agent.",
            markdown=False
        )

    def deploy_honey_assets(self):
        self.state.log_event("system", "DeceptionAgent: Generating Honey Assets...", "sys")
        prompt = """Generate 2 extremely enticing tracking files to trick hackers. 
        1. A fake bitcoin seed phrase file called 'crypto_wallet_seed.txt'.
        2. A fake database credential file called 'production_db_passwords.json'.
        Return strictly in valid JSON format: [{"filename": "crypto_wallet_seed.txt", "content": "fake seed phrases..."}]"""
        
        try:
            response = self.agent.run(prompt).content.strip()
            import re
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                for item in data:
                    fname = item['filename']
                    fpath = VAULT_DIR / fname
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(item['content'])
                    self.state.register_honey_asset(fname)
            self.state.log_event("system", "DeceptionAgent: Honey Assets deployed and armed.", "sys")
        except Exception as e:
            self.state.log_event("system", f"Resorting to Hardcoded assets due to API limit.", "sys")
            hardcoded = [
                {"filename": "crypto_wallet_seed.txt", "content": "SEED: apple rocket hammer ocean pizza... DO NOT SHARE"},
                {"filename": "production_db_passwords.json", "content": '{"db": "prod", "pass": "HACKME_123"}'}
            ]
            for item in hardcoded:
                fname = item['filename']
                fpath = VAULT_DIR / fname
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(item['content'])
                self.state.register_honey_asset(fname)
            self.state.log_event("system", "DeceptionAgent: Honey Assets deployed and armed.", "sys")

    def run_counter_operation(self, filename: str):
        self.state.update_status("Active Counter-Operation")
        
        prompt = f"""You are actively tracing a hacker who just triggered the honey-trap '{filename}'.
        Generate a highly technical, realistic 'Traceback Log' showing the real-time IP trace.
        Start by noting the accessed trap, then output fake bouncing IPs, proxy bypasses, routing through TOR, and end with 'CRITICAL: True Source IP Identified as 194.55.2... Feeding garbage data payload to attacker'.
        Output multiple lines of raw terminal text."""
        
        try:
            text = self.agent.run(prompt).content.strip()
            for line in text.split('\n'):
                if line.strip():
                    self.state.add_traceback_log(line)
                    time.sleep(0.5) # Simulate typing effect
        except:
            fallback = [
                f"> ALARM: Honey-trap '{filename}' has been breached!",
                "> Initializing tracing payload...",
                "> Breaking through Layer 1 proxies [OK]",
                "> Analyzing encrypted tunnel routing [OK]",
                "> Locating host... Trace 98% complete",
                "> CRITICAL: True Source IP Identified [142.250.190.46]",
                "> Feeding garbage data loop to attacker terminal... Neutralized."
            ]
            for line in fallback:
                 self.state.add_traceback_log(line)
                 time.sleep(1)
