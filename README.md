# CommScrape - YouTube Comment & Reply Extractor
<img width="897" height="583" alt="Screenshot 2025-12-19 145432" src="https://github.com/user-attachments/assets/72708ba1-84a4-4dcb-bbe4-f5defe1120a2" />


A Python-based tool that extracts **comments and replies** from any **public YouTube video** using the official **YouTube Data API v3**, and exports the data into **CSV or TXT** format with a clean and structured layout.

This tool is useful for research, data analysis, moderation review, sentiment studies, and educational purposes.

---

## 🚀 Features

- Extracts **top-level comments** and **their replies**
- Works with **any public YouTube video**
- Uses **official YouTube Data API v3**
- Structured export to:
  - CSV
  - TXT
- Progress indicator during extraction
- Custom file naming before export
- Simple and user-friendly interface
- Safe and API-compliant (no scraping)

---

## 🧰 Requirements

- Python 3.8 or higher
- Google YouTube Data API v3 enabled
- Internet connection

---

## 📁 Project Structure

CommentScraperUI/
│── api_key.txt
│── commscrape.py
│── requirements.txt
│── README.md


---

## 🔑 API Setup

1. Go to Google Cloud Console
2. Create a new project
3. Enable **YouTube Data API v3**
4. Generate an API key
5. Save the API key in a file named `api_key.txt` in the project folder


---

## 📦 Installation

Install required dependencies using:

```bash
pip install -r requirements.txt

▶️ How to Run
python commscrape.py

📝 Usage
Launch the application
Paste the public YouTube video link
Start the extraction process
Wait until extraction completes
Choose export format (CSV or TXT)
Enter a file name
File will be saved in the same directory

⚠️ Notes

Only public videos are supported.
Comments disabled on a video cannot be extracted.
API quota limits apply as per Google policy.

📜 License
This project is intended for educational and research purposes only.
Users are responsible for complying with YouTube’s terms of service.

👤 Author

Created by AashishCyberH4CKS
