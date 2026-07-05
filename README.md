# Stahovač videí z webu Moje Autoškola

Skript je určený pro uživatele webu [Moje Autoškola](https://www.moje-autoskola.cz/). Slouží ke stáhnutí libovolného videa ze sekce Studovna na vlastní disk.

## Požadavky

- Předplacená/zpřístupněná služba Studovna
- Nainstalovaný jazyk Python
- Nainstalovaný PIP
- Nainstalované všechny knihovny z `requirements.txt`

# Instalace a spuštění

1. Stáhnout všechny nutné knihovny (`pip install requirements.txt`)
2. Exportovat/zkopírovat `ma_session` a `PHPSESSID` cookies z prohlížeče
3. Vytvořit soubor `.env`
    - SUBDOMAIN=`[subdoména pro vaši autoškolu]`
    - MA_SESSION=`[ma_session]`
    - PHPSESSID=`[PHPSESSID]`
4. Spustit skript `mojeautoskola_video_downloader.py`
5. Zadat ID videa (např. 203, v URL stránky videa)

# Poznámky

Video bude uloženo v CWD jako `autoskola_video.mp4`.