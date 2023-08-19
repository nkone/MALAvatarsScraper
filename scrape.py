from bs4 import BeautifulSoup
import requests
import urllib.parse
import urllib.request
import os
import time
from tqdm import tqdm

HEADERS = {
        'Content-Type': 'text/html',
        'Retry-After': '60',
        }


def retry_request(url: str, retries: int, wait_time: int):
    content = ""
    for i in range(0, retries):
        content = requests.get(url, timeout=10, headers=HEADERS)
        if content.status_code > 300:
            print(f"Error requesting {url} status code: {content.status_code}")
            print(f"Waiting for {wait_time} for next request")
            time.sleep(wait_time)
        else:
            return content
        if i == (retries - 1):
            return ""
    return content


def find_search_url(search_str: str) -> str:
    mal_search_url = "https://myanimelist.net/search/all?cat=anime&q="
    mal_search_url += urllib.parse.quote_plus(search_str)
    print(f"Search url: {mal_search_url}")
    anime_link = ""
    search_page = retry_request(mal_search_url, 5, 30)
    if not search_page:
        return search_page
    soup = BeautifulSoup(search_page.content, "html.parser")
    article = soup.find("article")
    # articles = soup.find_all("article")
    # print(articles)
    # print(article)
    try:
        search_result = article.find_all("div", class_="list di-t w100")
        # print(search_result)
        # The use the first hyperlink to search for anime(bad)
        for result in search_result:
            # print(result)
            anime = result.find("a", class_="hoverinfo_trigger")
            anime_name = anime.find('img')['alt']
            print(anime_name)
            if anime_name.lower() == search_str.lower():
                anime_link = anime['href']
                return anime_link
            # print(anime[''])
    except AttributeError:
        print("Search string might be in correct or too short")
    return anime_link


def get_characters_images(anime_name: str):
    image_dir = \
            anime_name.replace(" ", "")\
            .replace('"', "").replace("/", '')\
            .replace(".", "").replace(",", "")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    else:
        print(f"Images might already downloaded for {image_dir}")
        return
    anime_url = find_search_url(anime_name)
    if not anime_url:
        raise ValueError(f"Anime url is empty for {anime_name}")
    print(anime_url)
    characters_url = anime_url + "/characters"
    page = retry_request(characters_url, 5, 30)
    soup = BeautifulSoup(page.content, "html.parser")
    characters_table = soup.find(
        "div", class_="anime-character-container js-anime-character-container"
    )
    # Collect all the characters name in the table
    characters_container = characters_table.find_all("a", class_="fw-n")
    # Wait 30 seconds for making more requests
    for character in tqdm(characters_container):
        # Go to ref link and download from there
        error = False
        time.sleep(1)
        character_page = retry_request(character['href'], 5, 60)
        character_name = character["href"].split("/")[-1].strip("_")
        try:
            soup = BeautifulSoup(character_page.content, 'html.parser')
            image_url = soup.find('img', class_="portrait-225x350")['data-src']
        except TypeError:
            tqdm.write(f"Character {character_name} might not have image")
            error = True
        except AttributeError:
            tqdm.write(f"Might have made too many reqs for {character_name}")
            error = True
        if not error:
            image_file = image_dir + "/"\
                + image_dir + '_' + character_name + ".jpg"
            tqdm.write(f"Downloading {character_name} from {anime_name}")
            # time.sleep(1)
            urllib.request.urlretrieve(image_url, image_file)


def main():
    with open('anime_list', encoding='utf-8') as anime_file:
        anime_list = anime_file.readlines()

    unique_anime_list = []
    dup_anime_list = []
    for anime in anime_list:
        anime = anime.strip()
        if anime not in unique_anime_list:
            unique_anime_list.append(anime)
        else:
            dup_anime_list.append(anime)

    for anime in unique_anime_list:
        try:
            get_characters_images(anime)
        except ValueError as error:
            print(f"Error {error}")
        except AttributeError as error:
            print(f"Error {error}")


if __name__ == "__main__":
    main()
