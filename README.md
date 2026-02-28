# Quran Kol Youm

"The best of you are those who learn the Quran and teach it." - Prophet Muhammad (peace be upon him) [Narrated by Al-Bukhari]

A Python-based automation tool that automatically posts pages of the Holy Quran to a Facebook Page. It posts pages sequentially from 1 to 606 (completing a Khatma), along with a beneficial supplication (Duaa).

**Live Demo:** [See the bot's page on facebook here ](https://www.facebook.com/qurankolyoum43)

## Purpose
This project serves as a **Sadaqah Jariyah**. It automates the daily posting of Quran pages to remind people to read the Quran and share religious content on social media.

## Features
- **Sequential Posting:** Page 1 → Page 606.
- **Auto-Reset:** Restarts from Page 1 automatically after finishing the Quran.
- **Smart Captions:** Random beneficial Duaa from `duaa.json`.
- **Zero Maintenance:** Runs entirely on the cloud (GitHub Actions).

---

## How to Use (For Non-Coders)
**You do not need to install Python or code anything.** Just follow these steps:

1.  **Fork the Repository:** Click the "Fork" button at the top right of this page to copy this project to your account.
2.  **Get Facebook Credentials:** Follow the guide in [FACEBOOK_SETUP.md](FACEBOOK_SETUP.md) to get your `PAGE_ID` and `ACCESS_TOKEN`.
3.  **Add Secrets:**
    *   Go to your forked repository **Settings** → **Secrets and variables** → **Actions**.
    *   Click **New repository secret**.
    *   Add `FACEBOOK_PAGE_ID` (Value: Your Page ID).
    *   Add `FACEBOOK_ACCESS_TOKEN` (Value: Your Token).
4.  **Start From Zero:** Delete `posted_pages.json` and the script will create it again & start from zero
4.  **Enable Automation:**
    *   Go to the **Actions** tab.
    *   If you see a warning, click **"I understand my workflows, go ahead and enable them"**.
    *   The bot will now run automatically according to the schedule!

---

## Installation (For Developers)
If you want to run the script locally on your machine:

### 1. Clone & Install
```bash
git clone https://github.com/avax43/quranKolYoum.git
cd quranKolYoum
pip install -r requirements.txt
```

### 2. Configure
Create a `.env` file:
```ini
FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_ACCESS_TOKEN=your_token
```

### 3. Run
```bash
python quran_kol_youm.py
```

## Contributing
We welcome everyone! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Contact Me
If you need any help or have any questions, feel free to contact me 
- **Telegram:** [@Avax43](https://t.me/Avax43)

## License
This project is open-source. You are free to use, modify, and distribute it for any beneficial cause.
```

