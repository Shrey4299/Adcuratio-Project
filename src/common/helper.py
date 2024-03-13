import json

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

    # Function to extract post data from a page


def extract_post_data(soup):
    home_titles = soup.find_all(class_="home-title")
    home_descs = soup.find_all(class_="home-desc")
    home_images = soup.find_all(class_="home-img-src lazyload")
    home_urls = soup.find_all(class_="story-link")

    post_data = []

    for i in range(len(home_titles)):
        title = home_titles[i].text.strip()
        desc = home_descs[i].text.strip()
        image_src = (
            home_images[i]["data-src"]
            if home_images[i].has_attr("data-src")
            else home_images[i]["src"]
        )
        url = home_urls[i]["href"]

        post_data.append(
            {
                "title": title,
                "description": desc,
                "image_source": image_src,
                "url": url,
            }
        )

    return post_data


# Function to create generalized description using NLTK stopwords
def create_generalised_description(description):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(description)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)


def create_description_word_count(description):
    ignore_chars = {".", ",", ":", ";", "'", '"', "`"}

    hmap = {}
    desc_list = description.split()

    for word in desc_list:
        # Ignore word if it contains any of the ignore characters
        if any(char in ignore_chars for char in word):
            continue

        # Otherwise, count the word
        if word not in hmap:
            hmap[word] = 1
        else:
            hmap[word] += 1

    # Sort the dictionary based on values (word counts) in descending order
    sorted_hmap = dict(sorted(hmap.items(), key=lambda item: item[1], reverse=True))

    return sorted_hmap
