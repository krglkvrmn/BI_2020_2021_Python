import argparse
import os
import socket
import re
import sys
import time
from collections import defaultdict
import OpenSSL

import requests
from bs4 import BeautifulSoup


def get_start_point(path_to_file, sep):
    """Get start point from existing file"""
    if os.path.exists(path_to_file):
        with open(path_to_file) as file_in:
            for line in file_in:
                pass
            start_id = line.split(sep)[0]
        return int(start_id) + 1
    return 0


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", required=True, type=str, help="Output CSV file to save data")
parser.add_argument("-c", "--continue", default=False, action="store_true",
                    help="Allows continuation of script from the moment where it failed/stopped")
parser.add_argument("-s", "--sep", default=",", type=str, help="Field separator")
parser.add_argument("--start", default=0, type=int, help="ID to start parsing from (ignored if --continue specified)")
parser.add_argument("--end", default=50000, type=int, help="The last ID to parse")

args = vars(parser.parse_args())

BASE_URL = "https://myanimelist.net/anime/"
START, END = args["start"], args["end"]

data = defaultdict(list)
if args["continue"]:
    file_mode = "a"
    START = get_start_point(args["output"], args["sep"])
else:
    file_mode = "w"

with open(args["output"], file_mode) as file_out:
    # Iterate over anime_id which is unique identifier on myanimelist
    try:
        for anime_id in range(START, END):   # Random number much greater than possible total number of anime
            time.sleep(2)         # Avoid blocking due to high request rate
            while True:
                try:
                    resp = requests.get(BASE_URL + str(anime_id))
                    print(f"ID: {anime_id} code {resp.status_code}")
                    break
                except (OpenSSL.SSL.SysCallError, socket.gaierror) as exc:
                    print("Caught exception {exc}. Waiting 500 second and trying again...")
                    time.sleep(500)

            if resp.status_code == 404:
                continue
            anime_page_soup = BeautifulSoup(resp.text, "lxml")

            data["anime_id"].append(anime_id)

            try:
                title_english = anime_page_soup.find(class_="title-name h1_bold_none").text
                data["title_english"].append(title_english)
            except AttributeError:
                title_english = ""

            try:
                title_japanese = anime_page_soup.find("span", text="Japanese:").next_sibling.strip()
                data["title_japanese"].append(title_japanese)
            except AttributeError:
                title_japanese = ""

            try:
                synopsys = re.sub(r"[\n\r]+", " ", anime_page_soup.find(itemprop="description").text)
                data["synopsys"].append(synopsys)
            except AttributeError:
                synopsys = ""

            try:
                score = anime_page_soup.find(class_=re.compile("score-label.+")).text
                data["score"].append(score)
            except AttributeError:
                score = ""

            try:
                rating_count = anime_page_soup.find(itemprop="ratingCount").text
                data["rating_count"].append(rating_count)
            except AttributeError:
                rating_count = ""

            try:
                rank = anime_page_soup.find(class_="spaceit po-r js-statistics-info di-ib") \
                                      .contents[2].strip().strip("#")
                data["rank"].append(rank)
            except AttributeError:
                rank = ""

            try:
                popularity = anime_page_soup.find("span", text="Popularity:").next_sibling.strip().strip("#")
                data["popularity"].append(popularity)
            except AttributeError:
                popularity = ""

            try:
                favorites = anime_page_soup.find("span", text="Favorites:").next_sibling.strip().replace(",", "")
                data["favorites"].append(favorites)
            except AttributeError:
                favorites = ""

            try:
                type_ = anime_page_soup.find("span", text="Type:").next.next.next.text
                data["type"].append(type_)
            except AttributeError:
                type_ = ""

            try:
                episodes = anime_page_soup.find("span", text="Episodes:").next_sibling.strip()
                data["episodes"].append(episodes)
            except AttributeError:
                episodes = ""

            try:
                rating = anime_page_soup.find("span", text="Rating:").next_sibling.strip().split(" - ")[0]
                data["rating"].append(rating)
            except AttributeError:
                rating = ""

            try:
                duration = anime_page_soup.find("span", text="Duration:").next_sibling.strip()
                data["duration"].append(duration)
            except AttributeError:
                duration = ""

            try:
                studio = anime_page_soup.find("span", text="Studios:").next.next.next.text
                data["studio"].append(studio)
            except AttributeError:
                studio = ""

            try:
                season, year = anime_page_soup.find("span", text="Premiered:") \
                                              .find_next_sibling("a").text.strip().split()
            except AttributeError:
                season = year = ""

            genres = list(map(lambda x: x.text, anime_page_soup.find_all(itemprop="genre")))
            data["genres"].append(genres)

            print(anime_id, title_english, title_japanese, synopsys, score,
                  rating_count, rank, popularity, favorites, type_, episodes,
                  rating, duration, studio, season, year, ",".join(genres),
                  file=file_out, sep=args["sep"])
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
    except Exception as exc:
        print(exc)
        print("An error occurred. Exiting...")
        sys.exit(1)
