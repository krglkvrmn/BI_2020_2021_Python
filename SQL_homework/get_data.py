import socket
import re
import time
from collections import defaultdict
import OpenSSL
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://myanimelist.net/anime/"
START, END = int(sys.argv[1]), int(sys.argv[2])

data = defaultdict(list)

with open("raw_data.csv", "a") as file_out:
    # Iterate over anime_id which is unique identifier on myanimelist
    for anime_id in range(START, END):   # Random number much greater than possible total number of anime
        time.sleep(2)         # Avoid blocking due to high request rate
        while True:
            try:
                resp = requests.get(BASE_URL + str(anime_id))
                print(anime_id, resp.status_code)
                break
            except (OpenSSL.SSL.SysCallError, socket.gaierror) as exc:
                print("Catched exception {exc}. Waiting 500 second and trying again...")
                time.sleep(500)

        if resp.status_code == 404:
            continue
        anime_page_soup = BeautifulSoup(resp.text, "lxml")

        data["anime_id"].append(anime_id)

        try:
            title_english = anime_page_soup.find(class_="title-name h1_bold_none").text
            data["title_english"].append(title_english)
        except AttributeError:
            title_english = None

        try:
            title_japanese = anime_page_soup.find("span", text="Japanese:").next_sibling.strip()
            data["title_japanese"].append(title_japanese)
        except AttributeError:
            title_japanese = None

        try:
            synopsys = anime_page_soup.find(itemprop="description").text
            data["synopsys"].append(synopsys)
        except AttributeError:
            synopsys = None

        try:
            score = anime_page_soup.find(class_=re.compile("score-label.+")).text
            data["score"].append(score)
        except AttributeError:
            score = None

        try:
            rating_count = anime_page_soup.find(itemprop="ratingCount").text
            data["rating_count"].append(rating_count)
        except AttributeError:
            rating_count = None

        try:
            rank = anime_page_soup.find(class_="spaceit po-r js-statistics-info di-ib").contents[2].strip().strip("#")
            data["rank"].append(rank)
        except AttributeError:
            rank = None

        try:
            popularity = anime_page_soup.find("span", text="Popularity:").next_sibling.strip().strip("#")
            data["popularity"].append(popularity)
        except AttributeError:
            popularity = None

        try:
            favorites = anime_page_soup.find("span", text="Favorites:").next_sibling.strip().replace(",", "")
            data["favorites"].append(favorites)
        except AttributeError:
            favorites = None

        try:
            type_ = anime_page_soup.find("span", text="Type:").next.next.next.text
            data["type"].append(type_)
        except AttributeError:
            type_ = None

        try:
            episodes = anime_page_soup.find("span", text="Episodes:").next_sibling.strip()
            data["episodes"].append(episodes)
        except AttributeError:
            episodes = None

        try:
            rating = anime_page_soup.find("span", text="Rating:").next_sibling.strip().split(" - ")[0]
            data["rating"].append(rating)
        except AttributeError:
            rating = None

        try:
            duration = anime_page_soup.find("span", text="Duration:").next_sibling.strip()
            data["duration"].append(duration)
        except AttributeError:
            duration = None

        try:
            studio = anime_page_soup.find("span", text="Studios:").next.next.next.text
            data["studio"].append(studio)
        except AttributeError:
            studio = None

        try:
            season, year = anime_page_soup.find("span", text="Premiered:").find_next_sibling("a").text.strip().split()
        except AttributeError:
            season = year = None

        genres = list(map(lambda x: x.text, anime_page_soup.find_all(itemprop="genre")))
        data["genres"].append(genres)

        print(anime_id, title_english, title_japanese, synopsys, score, rating_count, rank, popularity, rating, type_, episodes, rating, duration, studio, season, year, ",".join(genres), file=file_out, sep="@")
