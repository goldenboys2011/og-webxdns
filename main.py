from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from datetime import datetime
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify allowed origins like ["https://yourapp.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load domains from file
def load_domains():
    with open("domains.json", "r") as f:
        return json.load(f)

# Transform a domain entry into the target format
def transform_domain(entry):
    name_parts = entry["url"].split(".")
    if len(name_parts) < 2:
        return None

    return {
        "owned_by": {
            "registrar": "webx-plus",
            "user": "user_2vfgnTfYM0BHgy9v1beXpFTOhkx",
            "history": [
                "545fb839-1d67-4061-9aca-3d9284e77ab6",
                "user_2vm12eWHkvmuj3XX7TdngcHXLMk"
            ]
        },
        "_id": str(uuid4()),
        "tld": name_parts[-1],
        "name": ".".join(name_parts[:-1]),
        "target": entry.get("ip", "https://default.url/"),
        "records": [],
        "created_at": "2024-06-01T10:53:41.036Z",
        "updated_at": "2025-06-14T20:22:41.207Z",
        "adopted": False,
        "suspended": False,
        "searchable": True,
        "note": "<img src=\"\" onerror=\"alert(1)\">\n",
        "resolved_at": datetime.utcnow().isoformat() + "Z"
    }

# Endpoint: /dns/domains
@app.get("/domains")
def get_domains():
    raw = load_domains()
    transformed = [transform_domain(d) for d in raw if transform_domain(d) is not None]
    return {
        "success": True,
        "data": transformed
    }

@app.get("/domain/{name}/{tld}")
def get_single_domain(name: str, tld: str):
    raw = load_domains()
    for d in raw:
        if d.get("url") == f"{name}.{tld}":
            return {
                "ip": d.get("ip", f"https://{d.get('url')}"),
                "source": "wxp_dns"
            }
    raise HTTPException(status_code=404, detail="Domain not found")
    raise HTTPException(status_code=404, detail="Domain not found")
