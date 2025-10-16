from flask import Flask, request, jsonify
from ecourts_scraper import fetch_cnr_details, check_listing, save_results, download_pdf, download_cause_list

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask server is running! Use /check_cnr or /download_cause_list"

@app.route("/check_cnr", methods=["POST"])
def check_cnr():
    data = request.get_json()
    cnr = data.get("cnr")
    today_flag = data.get("today", False)
    tomorrow_flag = data.get("tomorrow", False)
    download_pdf_flag = data.get("download_pdf", False)

    if not cnr:
        return jsonify({"error": "CNR is required"}), 400

    result = fetch_cnr_details(cnr)
    if not result:
        return jsonify({"message": f"No details found for CNR {cnr}."})

    listed_today, listed_tomorrow = check_listing(result)
    messages = []
    if today_flag and listed_today:
        messages.append(f"CNR {cnr} is listed today ✅")
    if tomorrow_flag and listed_tomorrow:
        messages.append(f"CNR {cnr} is listed tomorrow ✅")
    if not messages:
        messages.append(f"CNR {cnr} is not listed today or tomorrow ❌")

    save_results(result, cnr, "web_results")

    if download_pdf_flag:
        download_pdf(cnr, "web_results")
        messages.append(f"Simulated PDF saved for {cnr}")

    return jsonify({"messages": messages, "details": result})

@app.route("/download_cause_list", methods=["GET"])
def download_cause():
    path = download_cause_list("web_results")
    return jsonify({"message": "Simulated cause list saved", "path": path})

if __name__ == "__main__":
    app.run(debug=True)
