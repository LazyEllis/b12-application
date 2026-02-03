import json
import hmac
import hashlib
import os
import urllib.request
from datetime import datetime, timezone

NAME = "Emmanuel Danison"
EMAIL = "danisonemma@gmail.com"
RESUME_LINK = "https://raw.githubusercontent.com/LazyEllis/b12-application/main/resume/emmanuel-danison.pdf"
REPOSITORY_LINK = "https://github.com/LazyEllis/b12-application"
ACTION_RUN_LINK = os.environ.get("GITHUB_RUN_URL")

SIGNING_SECRET = b"hello-there-from-b12"
ENDPOINT = "https://b12.io/apply/submission"

# Payload
payload = {
    "action_run_link": ACTION_RUN_LINK,
    "email": EMAIL,
    "name": NAME,
    "repository_link": REPOSITORY_LINK,
    "resume_link": RESUME_LINK,
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
}

body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

# Signature
digest = hmac.new(SIGNING_SECRET, body, hashlib.sha256).hexdigest()
signature = f"sha256={digest}"

# POST Request
req = urllib.request.Request(
    ENDPOINT,
    data=body,
    headers={
        "Content-Type": "application/json",
        "X-Signature-256": signature,
    },
    method="POST",
)

with urllib.request.urlopen(req) as resp:
    response_body = resp.read().decode("utf-8")

print(response_body)