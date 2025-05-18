# TubeSnatcher 🎣 - Because Copy-Pasting URLs is Too Much Work

Welcome to **TubeSnatcher**, the app for people who want to download YouTube videos without touching the command line, or using actual brain cells.  
Built with ✨ CustomTkinter ✨ so it looks like you actually tried.

## 🤔 What Even Is This?

TubeSnatcher is a glorified YouTube downloader with:

- 🎵 Audio download (because we’re still vibing to YouTube-to-mp3 in 2025)
- 📹 Video download (in case screen recording just ain’t cutting it)
- 📂 Saves files in sensible places (unlike your download folder)

It’s basically `yt-dlp`, but make it ✨ GUI ✨.

## 🔥 Features (aka Stuff We Flex About)

| Feature | Why You Should Care |
|--------|---------------------|
| ✅ CustomTkinter GUI | Because plain Tkinter is uglier than your browser history |
| ✅ Threaded Downloads | App won’t freeze like your ex’s heart |
| ✅ Audio/Video Mode | You choose, we pretend to care |
| ✅ FFmpeg Integration | Auto-converts audio like a nerdy magician |
| ✅ Smart Save Paths | Music goes to Music. Video goes to Video. Shocking, I know. |
| ✅ Logging | So you can stare at your failures in style |

## 🕸️ Internet? Checked Like a Pro.

Other apps be like: “requests.get('https://google.com')”  
Mee app be like: **"Let’s get down to the TCP level with socket"**

Why?  
Because you don’t just *check* for internet like a basic browser.  
You **handshake Google** like a man and say “Oi, you there?”

No fake positives. No request timeouts. Just raw, low-level ping — like the alpha dev you are. 💪🔥

## 🔁 Resume Like a Boss

Started a download and got distracted by reels? Power cut? Mom closed your laptop mid-download?  
Don’t cry, ra. Open the app again, paste the **same URL**, and boom — **continues like nothing happened.**  
Because this app has better memory than your brain when in exam. 💅

## 🚀 How To Use (Like A Pro, Or At Least Pretend To)

> Step 0: Install Python. Yes, seriously. Don’t skip this.

1. Clone the repo like you mean it:
   ```bash
   git clone https://github.com/itz-mr-voidwalker/TubeSnatcher.git
   cd TubeSnatcher
   ```

2. Install dependencies, coz nothing works out of the box anymore:
   ```
   pip install -r requirements.txt
   ``` 
3. Run the thing
    ```
    python main.py
    ```
# 📦 Requirements
- Python 3.9+ (anything older is basically medieval)

- yt-dlp, ffmpeg(comes with git), customtkinter, requests, and other fancy pip stuff

- A working brain (optional, but helpful)

# 🎯 What It Doesn’t Do
- Won’t download private videos, sorry stalkers.

- Won’t download full playlists unless you say yes when prompted.

# 💡 Why Though?
Because typing yt-dlp -x --audio-format mp3 <URL> is apparently too much effort for some of y’all.
So I wrapped it in a GUI. You're welcome.

# 📜 License
MIT License or something. Basically, use it, break it, but don’t blame me.

## 👑 Author 

Made by Sai Vignesh — just another Python guy who talks to his code more than people.

Writes code like it’s poetry, and breaks it like it’s a Monday morning.

🎧 Music is always playing, errors are always displaying.

📍 Currently somewhere between Tkinter hell and CustomTkinter heaven.

📬 Insta? Yeah, stalk away: [@itz_mr.voidwalker](https://instagram.com/itz_mr.voidwalker)
