import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv
import os

session = requests.Session()

load_dotenv()

SUBDOMAIN = os.getenv("SUBDOMAIN") # eg. olomoucka.moje-autoskola.cz

MA_SESSION = os.getenv("MA_SESSION") # session ID
PHPSESSID = os.getenv("PHPSESSID") # # authentication token

if not SUBDOMAIN or not MA_SESSION or not PHPSESSID:
    raise RuntimeError("Chybějící parametry v .env souboru.")


# unique ID of the video
video_ID = input("Zadej ID videa: ")

if not video_ID.isdigit():
    raise ValueError("ID videa musí být číslo.")


base_url = f"https://{SUBDOMAIN}.moje-autoskola.cz/"
page_url = base_url + f"video_player.php?edit_id={video_ID}&autoplay=1"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": f"ma_session={MA_SESSION}; PHPSESSID={PHPSESSID}",
    "Referer": f"https://{SUBDOMAIN}.moje-autoskola.cz/zak_studovna_videa.php",
    "User-Agent": "Mozilla/5.0"
}

# load page (must be authenticated)
r = session.get(page_url, headers=headers)
r.raise_for_status()

if len(r.content) < 100:
    raise RuntimeError("Neplatné přihlašovací údaje.")

# extract video source
soup = BeautifulSoup(r.text, "html.parser")
source = soup.find("source")

if not source:
    raise RuntimeError("Video nenalezeno.")

# video stream URL
video_url = urljoin(base_url, source["src"])
# print("Video URL:", video_url)

# download request headers
video_headers = {
    "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": f"ma_session={MA_SESSION}; PHPSESSID={PHPSESSID}",
    "Range": "bytes=0-",
    "Referer": page_url,
    "User-Agent": "Mozilla/5.0"
}

# download in chunks
with session.get(video_url, headers=video_headers, stream=True) as resp:
    resp.raise_for_status()

    total = int(resp.headers.get("Content-Length", 0)) # video size in bytes
    downloaded = 0 # downloaded bytes

    with open("autoskola_video.mp4", "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

                downloaded += len(chunk)
                if total:
                    percent = downloaded * 100 / total
                    print(f"\rDownloaded: {percent:.2f}%", end="") #log downloaded part in percents

print(f"\nDone. ({total / 10**6} MB)")