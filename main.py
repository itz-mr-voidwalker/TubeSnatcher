"""
TubeSnatcher - YouTube Music & Video Downloader with GUI
Author: Sai Vignesh
Built using: CustomTkinter, yt_dlp
"""

import customtkinter as ctk
from tkinter import messagebox
import yt_dlp
import os
import tkinter as tk
import re
import socket
import tempfile
import logging
import threading


class TubeSnatcherApp(ctk.CTk):
    """
    Main Application Class for TubeSnatcher.
    Provides GUI for downloading YouTube videos and music using yt_dlp.
    """

    def __init__(self) -> None:
        """Initializes the application window and sets up all components."""
        super().__init__()
        self.setup_logging()
        self.setup_window()
        self.create_widgets()
        logging.info("App Started....")
        
    def is_connected(self, host="8.8.8.8", port=53, timeout=3) -> bool:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    def setup_logging(self) -> None:
        """Sets up logging for error/info tracking in a temporary log file."""
        try:
            log_dir = os.path.join(tempfile.gettempdir(), "TubeSnatcher")
            os.makedirs(log_dir, exist_ok=True)
            logging.basicConfig(
                filename=os.path.join(log_dir, "TubeSnatcher.logs"),
                level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        except Exception as e:
            messagebox.showerror("Error", e)

    def setup_window(self) -> None:
        """Configures the appearance, title, size, and behavior of the main window."""
        try:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")
            self.title("TubeSnatcher")
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.geometry("520x520")
            self.last_percent = -1
            self.resizable(False, False)

            self.colors = {
                "background": "#121921",
                "card_bg": "#1e2738",
                "accent": "#4a90e2",
                "button_bg": "#3269b0",
                "button_hover": "#3e7ad9",
                "label_text": "#cfd6e4",
                "entry_bg": "#2b3749",
                "entry_text": "#e6ebf1"
            }
            self.configure(fg_color=self.colors["background"])
        except Exception as e:
            messagebox.showerror("Error", e)
            logging.error(e)

    def on_closing(self) -> None:
        """Handles graceful exit when the window is closed."""
        try:
            if messagebox.askyesno("Confirmation", "Do you want to quit the App?"):
                logging.info("App Closing...")
                self.destroy()
                os._exit(0)
        except Exception as e:
            logging.error(e)

    def create_widgets(self) -> None:
        """Creates and places all the GUI widgets on the main window."""
        try:
            # Main title
            self.title_label = ctk.CTkLabel(
                self,
                text="TubeSnatcher",
                font=ctk.CTkFont(family="Segoe UI", size=38, weight="bold"),
                text_color=self.colors["accent"]
            )
            self.title_label.pack(pady=(30, 20))

            # Card Frame
            self.card_frame = ctk.CTkFrame(
                master=self,
                fg_color=self.colors["card_bg"],
                corner_radius=18
            )
            self.card_frame.pack(padx=30, pady=10, fill="both", expand=False)
            self.card_frame.grid_columnconfigure(0, weight=1)

            # Dropdown
            self.dropdown_label = ctk.CTkLabel(
                self.card_frame,
                text="Select Type",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color=self.colors["label_text"]
            )
            self.dropdown_label.grid(row=0, column=0, sticky="w", padx=20, pady=(30, 10))

            self.type_var = tk.StringVar(value="YT Music")
            self.type_dropdown = ctk.CTkComboBox(
                master=self.card_frame,
                values=["YT Music", "YT Videos"],
                variable=self.type_var,
                fg_color=self.colors["entry_bg"],
                text_color=self.colors["entry_text"],
                button_color=self.colors["button_bg"],
                button_hover_color=self.colors["button_hover"],
                border_width=0,
                height=40,
                corner_radius=12,
                font=ctk.CTkFont(family="Segoe UI", size=13)
            )
            self.type_dropdown.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

            # URL Entry
            self.url_label = ctk.CTkLabel(
                self.card_frame,
                text="Enter URL",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color=self.colors["label_text"]
            )
            self.url_label.grid(row=2, column=0, sticky="w", padx=20, pady=(20, 10))

            self.url_entry = ctk.CTkEntry(
                master=self.card_frame,
                placeholder_text="https://youtube.com/...",
                fg_color=self.colors["entry_bg"],
                text_color=self.colors["entry_text"],
                placeholder_text_color="#7a7a8a",
                height=40,
                border_width=0,
                corner_radius=12,
                font=ctk.CTkFont(family="Segoe UI", size=13)
            )
            self.url_entry.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

            # Progress Bar
            self.progress_bar = ctk.CTkProgressBar(master=self.card_frame, progress_color="#EA440C", corner_radius=8)
            self.progress_bar.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
            self.progress_bar.set(0)
            self.progress_bar.grid_remove()

            # Submit Button
            self.submit_btn = ctk.CTkButton(
                master=self.card_frame,
                text="Submit",
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                fg_color=self.colors["accent"],
                hover_color="#3678f5",
                corner_radius=18,
                height=50,
                command=self.on_submit
            )
            self.submit_btn.grid(row=5, column=0, padx=20, pady=(0, 30), sticky="ew")
        except Exception as e:
            messagebox.showerror("Error", e)
            logging.error(e)

    def on_submit(self) -> None:
        """Handler for the submit button; validates inputs and starts download threads."""
        if not self.is_connected():
            messagebox.showerror("No internet!", "Internet is required to download your requirements")
            logging.error(e)
            return

        try:
            selected_type = self.type_var.get()
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showwarning("Missing URL", "Please enter a URL before submitting.")
                return

            self.submit_btn.configure(text="Downloading...", state="disabled")
            self.url_entry.configure(state="disabled")
            self.progress_bar.grid()
            self.progress_bar.set(0)

            if selected_type == "YT Videos":
                self.thread = threading.Thread(target=self.download, args=(url,))
            else:
                self.thread = threading.Thread(target=self.download_music, args=(url,))
            self.thread.start()

            thread_chk = threading.Thread(target=self.chk_thread)
            thread_chk.start()
        except Exception as e:
            logging.error(e)

    def chk_thread(self) -> None:
        """Monitors download thread and updates UI upon completion."""
        try:
            while self.thread.is_alive():
                pass
            messagebox.showinfo("Success", "Download Completed Successfully...")
            self.submit_btn.configure(text="Submit", state="normal")
            self.url_entry.configure(state="normal")
            self.url_entry.delete(0, 'end')
            self.progress_bar.grid_remove()
        except Exception as e:
            logging.error(e)
            messagebox.showerror("Error", e)

    def download_music(self, url: str) -> None:
        """Handles downloading music from YouTube."""
        try:
            is_playlist = messagebox.askyesno("Playlist?", "Are you downloading playlist?")
            messagebox.showinfo("Info", "Starting Download....")
            music_path = os.path.join(os.path.expanduser("~"), "Music", "TubeSnatcher")
            os.makedirs(music_path, exist_ok=True)

            ydl_opts = {
                'format': 'bestaudio/best',
                'ffmpeg_location': 'ffmpeg-7.1.1-essentials_build\\bin',
                'outtmpl': os.path.join(music_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': not is_playlist,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            messagebox.showerror("Error", "Pls Check url or your internet connectivity")
            
            logging.error(e)

    def download(self, url: str) -> None:
        """Handles downloading video from YouTube."""
        try:
            messagebox.showinfo("Info", "Starting Download....")
            videos_path = os.path.join(os.path.expanduser("~"), "Videos", "TubeSnatcher")
            os.makedirs(videos_path, exist_ok=True)

            ydl_opts = {
                'format': 'best',
                'progress_hooks': [self.progress_hook],
                'outtmpl': os.path.join(videos_path, '%(title)s.%(ext)s')
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            messagebox.showerror("Error", "Pls Check url or your internet connectivity")
            logging.error(e)

    def progress_hook(self, d: dict) -> None:
        """Progress callback for yt_dlp that updates the GUI progress bar."""
        try:
            if d['status'] == 'downloading':
                raw_percent = d.get('_percent_str', '0.0%')
                cleaned_percent = self.strip_ansi(raw_percent).replace('%', '').strip()

                try:
                    percent_float = float(cleaned_percent)
                    percent_int = int(percent_float)
                    if percent_int != self.last_percent:
                        self.progress_bar.set(percent_float / 100)
                        print(f"{percent_int}% Downloaded ✅")
                        self.last_percent = percent_int
                except Exception as e:
                    print(f"Can't get integer 🧨 Error: {e}")

            elif d['status'] == 'finished':
                self.progress_bar.set(1.0)
                print("🎉 Download complete bey!")
        except Exception as e:
            messagebox.showerror("Error", "Pls Check url or your internet connectivity")
            logging.error(e)

    def strip_ansi(self, string: str) -> str:
        """Removes ANSI escape sequences from strings."""
        try:
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            return ansi_escape.sub('', string)
        except Exception as e:
            messagebox.showerror("Error", e)
            logging.error(e)


def main():
    """Entry point to run the TubeSnatcher application."""
    try:
        app = TubeSnatcherApp()
        app.mainloop()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
