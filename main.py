import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Constants (you can also use environment variables for security)
SMARTSHEET_API_TOKEN = "7CRwQ1P2GvPfQhTnwiroRPy6WavKC4QLqRxkA"
SHEET_ID = "6652447675076484"

# Column IDs from your Smartsheet
COLUMN_IDS = {
    "Name": 5861183523082116,
    "Email": 3609383709396868,
    "Topic": 8112983336767364,
    "Page URL": 794633942290308,
    "Status": 6503489439747972
}

@app.route("/", methods=["POST"])
def mark_page():
    try:
        data = request.get_json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        title = data.get("title", "").strip()
        page = data.get("page", "").strip()

        # Construct row data for Smartsheet
        row_data = [
            {"columnId": COLUMN_IDS["Name"], "value": name},
            {"columnId": COLUMN_IDS["Email"], "value": email},
            {"columnId": COLUMN_IDS["Topic"], "value": title},
            {"columnId": COLUMN_IDS["Page URL"], "value": page},
            {"columnId": COLUMN_IDS["Status"], "value": "No"}
        ]

        headers = {
            "Authorization": f"Bearer {SMARTSHEET_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "toBottom": True,
            "rows": [{"cells": row_data}]
        }

        url = f"https://api.smartsheet.com/2.0/sheets/{SHEET_ID}/rows"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return jsonify({"message": "✅ Page marked successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
