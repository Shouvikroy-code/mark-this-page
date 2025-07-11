import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def mark_page():
    title = request.args.get("title", "Untitled Page")
    page_url = request.args.get("page", "Unknown URL")

    # Prepare row data
    row_data = {
        "toTop": True,
        "cells": [
            {"columnId": int(os.environ.get("COL_ID_TITLE")), "value": title},
            {"columnId": int(os.environ.get("COL_ID_URL")), "value": page_url}
        ]
    }

    headers = {
        "Authorization": f"Bearer {os.environ.get('SMARTSHEET_API_TOKEN')}",
        "Content-Type": "application/json"
    }

    try:
        sheet_id = os.environ.get("SMARTSHEET_SHEET_ID")
        url = f"https://api.smartsheet.com/2.0/sheets/{sheet_id}/rows"
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps([row_data]),  # ✅ Send as a list, not wrapped in {"rows": [...]}
            verify=False
        )
        response.raise_for_status()
        return "✅ Page marked successfully.", 200
    except Exception as e:
        return f"❌ Error: {str(e)}", 500
