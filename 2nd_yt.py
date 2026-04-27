import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import threading
import yt_dlp
import os

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader PRO")
        self.root.geometry("600x450")

        self.queue = []
        self.is_downloading = False

        self.build_ui()

    # ================= UI =================
    def build_ui(self):
        tk.Label(self.root, text="YouTube URL").pack()
        self.url_entry = tk.Entry(self.root, width=70)
        self.url_entry.pack(pady=5)

        tk.Button(self.root, text="Add to Queue", command=self.add_to_queue).pack()

        self.queue_listbox = tk.Listbox(self.root, width=80, height=8)
        self.queue_listbox.pack(pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Remove Selected", command=self.remove_selected).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear Queue", command=self.clear_queue).pack(side="left", padx=5)

        self.format_var = tk.StringVar(value="MP4")
        tk.Radiobutton(self.root, text="MP4", variable=self.format_var, value="MP4").pack()
        tk.Radiobutton(self.root, text="MP3", variable=self.format_var, value="MP3").pack()

        tk.Button(self.root, text="Choose Folder", command=self.choose_folder).pack()
        self.path_label = tk.Label(self.root, text="No folder selected")
        self.path_label.pack()

        tk.Button(self.root, text="Start Download", bg="green", fg="white",
                  command=self.start_download).pack(pady=10)

        self.progress_bar = Progressbar(self.root, length=400)
        self.progress_bar.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Idle")
        self.status_label.pack()

    # ================= UTIL =================
    def safe_ui(self, func):
        self.root.after(0, func)

    def set_status(self, text):
        self.safe_ui(lambda: self.status_label.config(text=text))

    def set_progress(self, value):
        self.safe_ui(lambda: self.progress_bar.config(value=value))

    def update_queue_display(self):
        self.queue_listbox.delete(0, tk.END)
        for item in self.queue:
            self.queue_listbox.insert(tk.END, item)

    # ================= FILE =================
    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_label.config(text=folder)

    # ================= QUEUE =================
    def add_to_queue(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        if url in self.queue:
            messagebox.showwarning("Duplicate", "URL already in queue")
            return

        self.queue.append(url)
        self.update_queue_display()
        self.url_entry.delete(0, tk.END)

    def remove_selected(self):
        try:
            index = self.queue_listbox.curselection()[0]
            self.queue.pop(index)
            self.update_queue_display()
        except IndexError:
            messagebox.showwarning("Warning", "No item selected")

    def clear_queue(self):
        if not self.queue:
            return
        if messagebox.askyesno("Confirm", "Clear entire queue?"):
            self.queue.clear()
            self.update_queue_display()

    # ================= DOWNLOAD =================
    def start_download(self):
        if self.is_downloading:
            messagebox.showinfo("Info", "Download already in progress")
            return

        if not self.queue:
            messagebox.showerror("Error", "Queue is empty")
            return

        thread = threading.Thread(target=self.process_queue, daemon=True)
        thread.start()

    def process_queue(self):
        self.is_downloading = True

        save_path = self.path_label.cget("text")
        if save_path == "No folder selected":
            save_path = os.path.join(os.path.expanduser("~"), "Downloads")

        while self.queue:
            url = self.queue[0]

            try:
                self.set_status("Fetching video info...")

                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Unknown')

                self.set_status(f"Downloading: {title}")

                self.download_single(url, save_path)

            except Exception as e:
                self.set_status("Error occurred")
                self.safe_ui(lambda: messagebox.showerror("Download Error", str(e)))

            finally:
                self.queue.pop(0)
                self.safe_ui(self.update_queue_display)

        self.set_status("All downloads completed")
        self.set_progress(0)
        self.is_downloading = False

    def download_single(self, url, save_path):
        selected_format = self.format_var.get()
        outtmpl = os.path.join(save_path, '%(title)s.%(ext)s')

        if selected_format == "MP4":
            ydl_opts = {
                'outtmpl': outtmpl,
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'progress_hooks': [self.progress_hook],
            }
        else:
            ydl_opts = {
                'outtmpl': outtmpl,
                'format': 'bestaudio/best',
                'progress_hooks': [self.progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except yt_dlp.utils.DownloadError as e:
            raise Exception(f"Download failed: {e}")

    # ================= PROGRESS =================
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
            try:
                percent = float(percent_str)
            except:
                percent = 0
            self.set_progress(percent)

        elif d['status'] == 'finished':
            self.set_progress(100)

# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()