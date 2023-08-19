# MALAvatarsScraper

Purpose

I wanted to make a waifu tier list from animes I've watched but it takes time to find all the pictures. The idea of this script is to scrape pictures from [MAL](myanimelist.net) from a list of series supplied in anime_list text file. The script will create folder based on the names provided and download avatars from the character page. Granted, the names supplied has to be almost 100% correct otherwise it cannot find the page.

## Contrains

- There will be time out when MAL block the request since the script makes multiple URL requests in such short amount of time. It would then wait for like 2-3 mins to retry the operation.
- Sometimes, if search result directed to manga page, there will be error downloading.
- Folders already created will be skipped if share the same name.
- Inputting `oregairu` is not supported but its full name will `Yahari Ore no Seishun Love Comedy wa Machigatteiru`

## Dependencies

Script is tested to run on python 3.10.6. Running on WSL with Ubuntu 22.04

Requires BS4, and tqdm packages from Python.

```
pip install bs4 tqdm
```

No authentications needed for MAL

## How to run

```
python3 scrape.py
```

Sample outputs (see Horimiya folder):
![Remi](Horimiya/Horimiya_Remi_Ayasaki.jpg)
![Remi](Horimiya/Horimiya_Kyouko_Hori.jpg)
