from agno.agent import Agent
from agno.models.google import Gemini
import json
import os
from .deception import DeceptionAgent
from core.state_manager import StateManager
from core.healing import SelfHealer

class ReasoningAgent:
    def __init__(self, state_manager: StateManager):
        self.state = state_manager
        self.healer = SelfHealer()
        self.deception = DeceptionAgent(state_manager)
        
        # We use a Gemini model via agno. Adjust the ID if needed.
        self.agent = Agent(
            model=Gemini(id="gemini-2.0-flash"),
            description="You are a brilliant cybersecurity reasoning agent. Your job is to analyze file system events and determine if they represent a threat.",
            instructions=[
                "Analyze the provided JSON list of recent file events.",
                "CRITICAL: If you see ANY 'deleted' events, you MUST immediately flag it as 'Suspicious'.",
                "If you see multiple file creations in a short time, flag it as 'Suspicious'.",
                "Only if it is a single file read or modification, flag it as 'Normal'.",
                "Respond strictly in JSON format: {\"status\": \"Normal\" or \"Suspicious\", \"reasoning\": \"...\"}"
            ],
            markdown=False
        )

    def analyze_events(self, events: list):
        if not events:
            return

        events_json = json.dumps(events, default=str)
        prompt = f"Analyze these recent file events: {events_json}"
        
        self.state.log_thought("ReasoningAgent", f"Analyzing {len(events)} recent events...")
        try:
            response = self.agent.run(prompt)
            content = response.content.strip()
            
            # Simple JSON extraction
            import re
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                extracted = match.group(0)
            else:
                extracted = content
                
            try:
                decision = json.loads(extracted)
                status = decision.get("status", "Normal")
                reasoning = decision.get("reasoning", "No reasoning provided.")
            except:
                # Failsafe if it still didn't generate valid JSON
                status = "Suspicious" if "Suspicious" in content else "Normal"
                reasoning = content
            
            self.state.log_thought("ReasoningAgent", f"Decision: {status}. Reasoning: {reasoning}")
            
            # If status changed to Suspicious, trigger defenses
            current_status = self.state.get_status()
            if status == "Suspicious" and current_status != "Suspicious":
                self.state.update_status("Alert")
                self.state.log_thought("ReasoningAgent", "Threat detected. Activating Deception and Healing protocols.")
                
                # Deploy decoys
                self.deception.deploy_decoys()
                self.state.update_status("Suspicious")
                
            elif status == "Normal" and current_status != "Normal":
                # Maybe cool down over time, but for now we just log it
                pass

            # Handle Healing proactively
            if status == "Suspicious":
                deleted_events = [e for e in events if e.get("event_type") == "deleted"]
                for e in deleted_events:
                    fname = os.path.basename(e.get("file_path"))
                    self.healer.restore_file(fname)

        except Exception as e:
            self.state.log_thought("ReasoningAgent", f"Error during analysis: {str(e)}")
