import os
import random
import json
import sys
import requests
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

log_handler = RotatingFileHandler(
    "app.log",
    maxBytes=512 * 1024, 
    backupCount=0,        
    encoding='utf-8'
)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        log_handler,
        logging.StreamHandler(sys.stdout)                
    ]
)

load_dotenv()
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

TOTAL_PAGES = 606
IMAGES_DIR = os.path.join("static", "images")
TRACKING_FILE = "posted_pages.json"
DUAS_FILE = "duaa.json"

def load_duas(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("duas", [])
    except FileNotFoundError:
        logging.error(f"Duaa file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in duaa file: {file_path}")
        return []

def load_state():
    """Load tracking state."""
    if not os.path.exists(TRACKING_FILE):
        return {"posted_pages": [], "used_duas": []}
    try:
        data = json.load(open(TRACKING_FILE, "r", encoding="utf-8"))
        if "posted" in data and "posted_pages" not in data:
            return {"posted_pages": data["posted"], "used_duas": []}
        return {
            "posted_pages": data.get("posted_pages", []),
            "used_duas": data.get("used_duas", [])
        }
    except (json.JSONDecodeError, AttributeError):
        return {"posted_pages": [], "used_duas": []}

def save_state(posted_pages, used_duas):
    """Save current state."""
    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "posted_pages": posted_pages,
            "used_duas": used_duas
        }, f, indent=2, ensure_ascii=False)

def get_next_page_sequential(posted_pages):
    """Determine next page number."""
    if not posted_pages:
        return 1
    
    last_page = max(posted_pages)
    next_page = last_page + 1
    
    if next_page > TOTAL_PAGES:
        logging.info("Khatma completed. Restarting from page 1.")
        return 1
    
    return next_page

def get_unique_dua(all_duas, used_duas):
    """Select an unused duaa."""
    available_duas = [d for d in all_duas if d not in used_duas]
    
    if not available_duas:
        logging.info("All duaas used. Resetting list.")
        used_duas = [] 
        available_duas = all_duas 
    
    selection = random.choice(available_duas)
    return selection, used_duas

def publish_to_facebook():
    logging.info("Starting publishing process...")
    if not PAGE_ID or not ACCESS_TOKEN:
        logging.critical("Missing FACEBOOK_PAGE_ID or ACCESS_TOKEN in .env")
        sys.exit(1)

    duas = load_duas(DUAS_FILE)
    if not duas:
        logging.error("No duaas found in duaa.json")
        sys.exit(1)

    state = load_state()
    posted_pages = state["posted_pages"]
    used_duas_list = state["used_duas"]
    page_number = get_next_page_sequential(posted_pages)
    
    if page_number == 1 and posted_pages:
        posted_pages = [] 

    dua_text, updated_used_duas = get_unique_dua(duas, used_duas_list)
    hashtags = "\n\n#القرآن_الكريم #ورد_يومي #تدبر #ختمة_القرآن"
    caption = f"ورد القرآن اليومي، صفحة {page_number}\n\n'{dua_text}'{hashtags}"

    image_path = os.path.join(IMAGES_DIR, f"page_{page_number}.jpg")

    if not os.path.exists(image_path):
        logging.error(f"Image not found: {image_path}")
        return

    logging.info(f"Publishing page: {page_number}")
    logging.info(f"Caption snippet: {caption[:50]}...")

    url = f"https://graph.facebook.com/v24.0/{PAGE_ID}/photos"
    params = {
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }

    try:
        with open(image_path, "rb") as img:
            files = {"source": img}
            resp = requests.post(url, params=params, files=files, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            logging.info(f"API Response: {result}")

            post_id = result.get("post_id") or result.get("id")
            if post_id:
                posted_pages.append(page_number)
                updated_used_duas.append(dua_text)
                
                save_state(posted_pages, updated_used_duas)
                logging.info(f"Success! https://facebook.com/{post_id}")
            else:
                logging.error(f"Failed: No post_id in response: {result}")

    except requests.exceptions.HTTPError:
        logging.error(f"HTTP Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")

if __name__ == "__main__":
    publish_to_facebook()
