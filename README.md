# 🎬 YouTube Downloader PRO

A simple yet powerful **YouTube video/audio downloader** built with Python, Tkinter, and `yt-dlp`.

Supports:

* ✅ MP4 video downloads
* ✅ MP3 audio extraction
* ✅ Queue system (download multiple links automatically)
* ✅ Progress tracking
* ✅ Clean GUI

---

## 🚀 Features

* Add multiple YouTube links to a **queue**
* Download videos sequentially (no crashes)
* Choose between:

  * 🎥 MP4 (video)
  * 🎵 MP3 (audio)
* Real-time **progress bar**
* Select custom download folder
* Remove or clear queue items

---

## 📸 Preview

```
[ GUI Window ]
- Input URL
- Add to Queue
- Queue List
- Format Selection
- Download Button
- Progress Bar
```

---

## 🧰 Requirements

Make sure you have:

* Python 3.8+
* pip

Install dependencies:

```bash
pip install yt-dlp
```

---

## ⚙️ FFmpeg Installation (IMPORTANT)

FFmpeg is required for:

* MP4 merging (video + audio)
* MP3 conversion

### 🔗 Download FFmpeg

* 🌐 Official site: https://ffmpeg.org/download.html
* 🪟 Windows builds: https://www.gyan.dev/ffmpeg/builds/

### 🪟 Windows Setup

1. Download ZIP (release build)
2. Extract it
3. Go to:

   ```
   ffmpeg/bin
   ```
4. Copy the path
5. Add it to **Environment Variables → PATH**

Test:

```bash
ffmpeg -version
```

---

### 🐧 Linux (Kali / Ubuntu)

```bash
sudo apt install ffmpeg
```

---

### 🍎 macOS

```bash
brew install ffmpeg
```

---

## ▶️ How to Run

```bash
python your_script_name.py
```

---

## 🧠 How It Works

1. Add YouTube URLs to queue
2. Click **Start Download**
3. App processes links one-by-one
4. Uses `yt-dlp` internally
5. Progress updates in real-time

---

## ⚠️ Notes

* MP3 conversion requires FFmpeg
* Some videos may fail due to:

  * region restrictions
  * private videos
  * YouTube changes

---

## 📦 Build to EXE (Optional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed your_script_name.py
```

Output:

```
dist/your_script_name.exe
```

---

## 📜 Disclaimer

This tool is for **educational purposes only**.

Please respect:

* YouTube Terms of Service
* Copyright laws

---

## 💡 Future Improvements

* Parallel downloads
* Playlist support
* Pause / Resume
* Dark mode UI
* Download history

---

## 👨‍💻 Author

Built by Barthez
---
