# ULTIMATE KEYLOGGER v4.0

> **Developer: Vishal Pentest**
>
> **For Authorized Penetration Testing & Security Research Only**
>
> **⚠️ Kanooni Chetavani:** Is tool ka unauthorized istemal karna kanuni jurm hai. Sirf authorized pentesting ke liye istemal karein.

---

## 📋 Vishal Pentest Ka Sandesh

> *"Yeh tool maine cybersecurity professionals aur authorized penetration testers ki madad ke liye banaya hai. Iska galat istemal na karein. Zimmedari se istemal karein aur hamesha permission lekar hi test karein. Ethical hacking ka matlab hai authorized hacking."*
>
> — **Vishal Pentest**

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [Technical Architecture](#-technical-architecture)
4. [Dependencies](#-dependencies-required-libraries)
5. [Installation](#-installation-step-by-step)
6. [Configuration](#-configuration)
7. [Usage](#-usage-kaise-use-karein)
8. [Sample Output](#-sample-output-telegram-par-kaise-dikhega)
9. [Detection & Evasion](#-detection--evasion-pata-kaise-nahi-lagta)
10. [Version History](#-version-history)
11. [Contributing](#-contributing)
12. [Contact](#-contact-developer)
13. [Legal Disclaimer](#-kanooni-chetavani-legal-disclaimer)

---

## 📋 Overview

**Ultimate Keylogger v4.0** ek comprehensive Windows surveillance aur monitoring tool hai jo **Vishal Pentest** dwara banaya gaya hai. Yeh tool authorized security assessments, red team operations, aur penetration testing engagements ke liye design kiya gaya hai. Yeh Telegram ko Command & Control (C2) channel ke roop mein integrate karta hai, jisse real-time exfiltration hoti hai.

### Kya Kya Data Exfiltrate Hota Hai:

| Type | Kya Capture Hota Hai |
|------|----------------------|
| ⌨️ Keystrokes | Har key jo user type karta hai, active window ke naam ke saath |
| 📸 Screenshots | Live desktop screenshot with timestamp overlay |
| 🎥 Webcam | Connected webcam se image capture |
| 📋 Clipboard | Jo bhi user copy karta hai (passwords, URLs, etc.) |
| 💻 System Info | Computer name, username, CPU usage, RAM usage |

---

## 🚀 Key Features

| # | Feature | Description | Interval |
|---|---------|-------------|----------|
| 1 | ⌨️ **Keystroke Logging** | Har key capture hoti hai active window ke naam ke saath. Jaise: `[14:23:05] <Chrome>: password123` | Real-time (instant) |
| 2 | 📸 **Screenshot Capture** | Desktop ki live screenshot li jaati hai aur Telegram par bheji jaati hai. Overlay mein timestamp aur window name hota hai | Har 20 seconds mein |
| 3 | 🎥 **Webcam Capture** | Connected webcam se image capture hoti hai aur Telegram par bheji jaati hai | Har 60 seconds mein |
| 4 | 📋 **Clipboard Monitoring** | Clipboard mein kuch bhi copy hota hai toh woh turant Telegram par bhej diya jata hai | Har 12 seconds mein check hota hai |
| 5 | 💻 **System Fingerprinting** | System ki complete information collect hoti hai jaise hostname, username, CPU %, RAM % | Har 4 minutes mein |
| 6 | 🔒 **Encrypted Buffer** | Local keystroke buffer Fernet encryption se secure hai. Koi bhi directly file read karke keys nahi dekh sakta | Flush hone par encrypt hota hai |
| 7 | 🤖 **Telegram C2** | Full bot integration. Saara data direct aapke Telegram bot par aata hai. Koi local file nahi banti | Continuous |
| 8 | 🕵️ **Stealth Mode** | Console window launch hote hi 1 second mein auto-hide ho jati hai. User ko pata bhi nahi chalega ki kuch chal raha hai | Instant |

---

## 🧠 Technical Architecture---

## 🔧 Dependencies (Required Libraries)

Yeh tool **sirf Windows operating system** par kaam karta hai kyunki ye `win32gui` use karta hai active window detection ke liye.

| Library | Version | Purpose |
|---------|---------|---------|
| **Python** | 3.8+ | Base programming language |
| **requests** | Latest | Telegram API se communicate karne ke liye |
| **pynput** | Latest | Keyboard ke har button press ko capture karne ke liye |
| **opencv-python** | Latest | Webcam se image capture karne ke liye |
| **numpy** | Latest | Image processing ke liye |
| **pyautogui** | Latest | Screenshots lene ke liye |
| **psutil** | Latest | System CPU/RAM usage nikalne ke liye |
| **pywin32** | Latest | Windows API se active window ka naam lene ke liye |
| **cryptography** | Latest | Fernet encryption ke liye |
| **Pillow** | Latest | Images manipulate karne aur overlay daalne ke liye |
| **pyperclip** | Latest | Clipboard read karne ke liye |

---

## 📦 Installation (Step-by-Step)

### Step 1: Python Install Karein

Agar Python nahi hai toh [python.org](https://python.org) se download karein.

Check karein:
```bash
python --version




