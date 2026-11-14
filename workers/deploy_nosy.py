"""Deploy the updated Nosy worker (interview-workerjs) to Cloudflare.

Mirrors the custom.cloudflare helper's call_form, but targets
interview-workerjs with minimal metadata (main_module + compatibility_date,
no bindings - the worker only reads the ANTHROPIC_API_KEY secret, which
lives at the service level and is NOT touched by a script upload).

Usage: python3 deploy_nosy.py <script-path>
"""
import json, subprocess, sys
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import dynamic_credential_entry

BASE = "https://api.cloudflare.com/client/v4"
ACCOUNT = "701117dde6af00d42bac3c4058b660be"
SCRIPT_NAME = "interview-workerjs"

def main():
    script_path = sys.argv[1]
    entry = dynamic_credential_entry("custom.cloudflare", "access_token")
    hdr = f"Authorization: Bearer {str(entry['surrogate']).strip()}"
    metadata = {
        "main_module": "worker.mjs",
        "compatibility_date": "2026-11-04",
    }
    r = subprocess.run(
        ["curl", "-sS", "-m", "60", "-X", "PUT",
         "-H", hdr,
         "-F", f"metadata={json.dumps(metadata)};type=application/json",
         "-F", f"worker.mjs=@{script_path};filename=worker.mjs;type=application/javascript+module",
         BASE + f"/accounts/{ACCOUNT}/workers/scripts/{SCRIPT_NAME}"],
        capture_output=True, text=True, timeout=70,
    )
    print("curl exit:", r.returncode)
    print(r.stdout[:3000])
    print(r.stderr[:500])

if __name__ == "__main__":
    main()
