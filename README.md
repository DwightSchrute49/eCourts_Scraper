# eCourts Scraper

A Python project to fetch court listings from [eCourts](https://services.ecourts.gov.in/ecourtindia_v6/) with a simple Flask web interface.  
It allows checking case details using a **CNR number**, viewing court name and serial number, and downloading cause lists or case PDFs (simulated).

---

## Features

- Fetch court details using a **CNR number**.
- Check if a case is **listed today or tomorrow**.
- View **court name** and **serial number**.
- Optionally **download case PDFs** (simulated).
- Download **entire cause list for today** (simulated JSON).
- REST API endpoints for easy integration or testing.

---

## Project Structure

```
ecourts_scraper/
│
├─ ecourts_scraper.py      # Main Python scraper module
├─ app.py                  # Flask web interface
├─ web_results/            # Output folder for JSON and PDFs
└─ README.md               # Project documentation
```

---

## Installation

1. Clone the repository or unzip the project folder.
2. Install required Python packages:

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**

```
Flask==2.3.6
requests==2.32.1
selenium==4.15.0
```

3. Ensure **Python 3.10+** is installed.
4. Optional: Install ChromeDriver for Selenium if real scraping is needed.

---

## Usage

### 1. Run the Flask Web Server

```bash
python app.py
```

Open a browser at: `http://127.0.0.1:5000/`  
You’ll see a confirmation message:

```
Flask server is running! Use /check_cnr or /download_cause_list
```

---

### 2. Check CNR via API

**POST** request to `/check_cnr` (e.g., via Postman):

```json
{
  "cnr": "DLND010012342020",
  "today": true,
  "tomorrow": false,
  "download_pdf": false
}
```

**Response example:**

```json
{
  "details": {
    "Court Name": "District Court, New Delhi",
    "Next Hearing Date": "16-10-2025",
    "Serial Number": "12"
  },
  "messages": ["CNR DLND010012342020 is listed today ✅"]
}
```

- JSON and simulated PDF (if requested) are saved in `web_results/`.

---

### 3. Download Cause List

**GET** request to `/download_cause_list`:

```
http://127.0.0.1:5000/download_cause_list
```

**Response:**

```json
{
  "message": "Simulated cause list saved",
  "path": null
}
```

- Actual cause list JSON saved in `web_results/cause_list_<date>.json`.

---

## Notes

- The project uses **simulated PDFs and cause lists** for demonstration.
- Real CNR numbers are required for live testing with actual eCourts data.
- Modular design: `ecourts_scraper.py` handles scraping, `app.py` handles the web/API interface.
- Can be extended in the future to include a React or React Native frontend.
