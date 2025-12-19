import tkinter as tk
from tkinter import ttk, messagebox
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
import csv
import threading

# ================= READ API KEY =================
with open("api_key.txt", "r") as f:
    API_KEY = f.read().strip()

youtube = build("youtube", "v3", developerKey=API_KEY)

comments_data = []

# ================= VIDEO ID =================
def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    elif parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return None

# ================= SCRAPER =================
def scrape_comments():
    video_url = link_entry.get().strip()
    video_id = get_video_id(video_url)

    if not video_id:
        messagebox.showerror("Error", "Invalid YouTube Link")
        return

    comments_data.clear()
    progress["value"] = 0
    status_label.config(text="🔍 Initializing Extraction...")

    def run():
        next_page_token = None
        count = 0

        while True:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response["items"]:
                top = item["snippet"]["topLevelComment"]["snippet"]
                comments_data.append({
                    "type": "Comment",
                    "author": top["authorDisplayName"],
                    "text": top["textDisplay"],
                    "likes": top["likeCount"]
                })
                count += 1

                if "replies" in item:
                    for reply in item["replies"]["comments"]:
                        r = reply["snippet"]
                        comments_data.append({
                            "type": "Reply",
                            "author": r["authorDisplayName"],
                            "text": r["textDisplay"],
                            "likes": r["likeCount"]
                        })
                        count += 1

                progress["value"] = min(100, progress["value"] + 2)
                status_label.config(text=f"💾 Extracted {count} comments...")

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        progress["value"] = 100
        status_label.config(text="✅ Extraction Completed Successfully")

    threading.Thread(target=run).start()

# ================= EXPORT =================
def export_file(file_type):
    name = filename_entry.get().strip()
    if not name:
        messagebox.showwarning("Warning", "Enter file name")
        return

    if file_type == "csv":
        with open(f"{name}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["type", "author", "text", "likes"]
            )
            writer.writeheader()
            writer.writerows(comments_data)
        messagebox.showinfo("Done", f"{name}.csv saved successfully")

    else:
        with open(f"{name}.txt", "w", encoding="utf-8") as f:
            for c in comments_data:
                f.write(f"[{c['type']}]\n")
                f.write(f"Author: {c['author']}\n")
                f.write(f"Likes: {c['likes']}\n")
                f.write(f"Text: {c['text']}\n")
                f.write("-"*50 + "\n")
        messagebox.showinfo("Done", f"{name}.txt saved successfully")

# ================= UI =================
root = tk.Tk()
root.title("Youtube Comment Scraper | AashishCyberH4CKS")
root.geometry("720x520")
root.configure(bg="black")

style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="black", foreground="#00ff9c", font=("Consolas", 10))
style.configure("TButton", background="black", foreground="#00ff9c", font=("Consolas", 10))
style.configure("TEntry", fieldbackground="black", foreground="#00ff9c")
style.configure("TProgressbar", troughcolor="black", background="#00ff9c")

# ================= HEADER =================
header = tk.Label(
    root,
    text="YOUTUBE COMMENT SCRAPER\nCreated by AashishCyberH4CKS",
    fg="#00ff9c",
    bg="black",
    font=("Consolas", 16, "bold")
)
header.pack(pady=15)

# ================= INPUT =================
frame = tk.Frame(root, bg="black")
frame.pack(pady=10)

ttk.Label(frame, text="🔗 YouTube Video Link").grid(row=0, column=0, sticky="w")
link_entry = ttk.Entry(frame, width=60)
link_entry.grid(row=1, column=0, pady=5)

ttk.Button(frame, text="🚀 Start Extraction", command=scrape_comments).grid(row=2, column=0, pady=10)

# ================= PROGRESS =================
progress = ttk.Progressbar(root, length=500)
progress.pack(pady=10)

status_label = ttk.Label(root, text="🟢 Waiting...")
status_label.pack()

# ================= EXPORT =================
export_frame = tk.Frame(root, bg="black")
export_frame.pack(pady=15)

ttk.Label(export_frame, text="📁 File Name").grid(row=0, column=0)
filename_entry = ttk.Entry(export_frame, width=30)
filename_entry.grid(row=1, column=0, pady=5)

ttk.Button(export_frame, text="💾 Export CSV", command=lambda: export_file("csv")).grid(row=2, column=0, pady=5)
ttk.Button(export_frame, text="📄 Export TXT", command=lambda: export_file("txt")).grid(row=3, column=0)

# ================= RUN =================
root.mainloop()
