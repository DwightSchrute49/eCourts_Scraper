import argparse
import json
import os
from datetime import datetime, timedelta
import random

# -------------------
# Mock data for testing
# -------------------

# Example CNR database (you can add more)
MOCK_CNR_DATA = {
    "DLND010012342020": {
        "Next Hearing Date": (datetime.today() + timedelta(days=0)).strftime("%d-%m-%Y"),
        "Court Name": "District Court, New Delhi",
        "Serial Number": "12"
    },
    "MHND020034562021": {
        "Next Hearing Date": (datetime.today() + timedelta(days=1)).strftime("%d-%m-%Y"),
        "Court Name": "Mumbai Civil Court",
        "Serial Number": "34"
    }
}

# Mock cause list for today
MOCK_CAUSE_LIST = [
    {"CNR": "DLND010012342020", "Court": "District Court, New Delhi", "Serial": "12"},
    {"CNR": "MHND020034562021", "Court": "Mumbai Civil Court", "Serial": "34"},
    {"CNR": "TNND030056782022", "Court": "Chennai Court", "Serial": "56"},
]


# -------------------
# Functions
# -------------------

def fetch_cnr_details(cnr):
    """Simulate fetching CNR details."""
    return MOCK_CNR_DATA.get(cnr, {})


def check_listing(result):
    """Check if the case is listed today or tomorrow."""
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)
    listed_today = listed_tomorrow = False

    next_hearing_str = result.get("Next Hearing Date", "")
    if next_hearing_str:
        try:
            hearing_date = datetime.strptime(next_hearing_str, "%d-%m-%Y").date()
            listed_today = hearing_date == today
            listed_tomorrow = hearing_date == tomorrow
        except:
            pass
    return listed_today, listed_tomorrow


def save_results(result, cnr, outdir):
    os.makedirs(outdir, exist_ok=True)
    filename = os.path.join(outdir, f"{cnr}.json")
    with open(filename, "w") as f:
        json.dump(result, f, indent=4)
    print(f"Saved results to {filename}")


def download_pdf(cnr, outdir):
    """Simulate PDF download."""
    os.makedirs(outdir, exist_ok=True)
    pdf_file = os.path.join(outdir, f"{cnr}.pdf")
    with open(pdf_file, "w") as f:
        f.write(f"PDF for CNR {cnr} (simulated)")
    print(f"Simulated PDF saved: {pdf_file}")


def download_cause_list(outdir):
    """Simulate downloading entire cause list for today."""
    os.makedirs(outdir, exist_ok=True)
    filename = os.path.join(outdir, f"cause_list_{datetime.today().strftime('%Y%m%d')}.json")
    with open(filename, "w") as f:
        json.dump(MOCK_CAUSE_LIST, f, indent=4)
    print(f"Saved simulated cause list: {filename}")


# -------------------
# Main
# -------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnr", help="CNR number to fetch")
    parser.add_argument("--today", action="store_true", help="Check if listed today")
    parser.add_argument("--tomorrow", action="store_true", help="Check if listed tomorrow")
    parser.add_argument("--download-pdfs", action="store_true", help="Download case PDF (simulated)")
    parser.add_argument("--causelist", action="store_true", help="Download full cause list for today (simulated)")
    parser.add_argument("--outdir", default="myresults", help="Output directory")
    args = parser.parse_args()

    if args.cnr:
        cnr_details = fetch_cnr_details(args.cnr)
        if not cnr_details:
            print(f"No details found for CNR {args.cnr}.")
        else:
            listed_today, listed_tomorrow = check_listing(cnr_details)
            if args.today and listed_today:
                print(f"CNR {args.cnr} is listed today ✅")
            if args.tomorrow and listed_tomorrow:
                print(f"CNR {args.cnr} is listed tomorrow ✅")
            if not listed_today and not listed_tomorrow:
                print(f"CNR {args.cnr} is not listed today or tomorrow ❌")

            save_results(cnr_details, args.cnr, args.outdir)

            if args.download_pdfs:
                download_pdf(args.cnr, args.outdir)

    if args.causelist:
        download_cause_list(args.outdir)
