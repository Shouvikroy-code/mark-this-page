import os
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def mark_page():
    title = request.args.get("title", "Untitled Page")
    page_url = request.args.get("page", "Unknown URL")

    # Prepare row data for Smartsheet
    row_data = [
        {"columnId": os.environ.get("COL_ID_TITLE"), "value": title},
        {"columnId": os.environ.get("COL_ID_URL"), "value": page_url}
    ]

    headers = {
        "Authorization": f"Bearer {os.environ.get('SMARTSHEET_API_TOKEN')}",
        "Content-Type": "application/json"
    }

    payload = {
        "toTop": True,
        "rows": [{"cells": row_data}]
    }

    try:
        sheet_id = os.environ.get("SMARTSHEET_SHEET_ID")
        url = f"https://api.smartsheet.com/2.0/sheets/{sheet_id}/rows"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return "✅ Page marked successfully.", 200
    except Exception as e:
        return f"❌ Error: {str(e)}", 500
