import time
import os
import shutil

vault_dir = r"d:\honey_net\my_vault"

print("Simulating safe activity...")
notes_path = os.path.join(vault_dir, "notes.txt")
if os.path.exists(notes_path):
    with open(notes_path, "a", encoding="utf-8") as f:
        f.write("\nUser appending some normal notes.")
time.sleep(10)

print("Launching rapid abnormal activity (simulated threat)...")
for i in range(5):
    temp_path = os.path.join(vault_dir, f"malicious_drop_{i}.txt")
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write("encrypting...")
    time.sleep(0.1)

if os.path.exists(notes_path):
    print("Simulating malicious deletion of notes.txt...")
    os.remove(notes_path)

print("Attack finished. Defenses should activate now.")
