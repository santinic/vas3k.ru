import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../vas3k"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vas3k.settings")

import re
from datetime import datetime
import urllib
import django
import requests
from TwitterAPI import TwitterAPI
from stories.models import Story, Memory

django.setup()


def clear_text(text):
    text = re.sub(r'(http://[^ ]+)', "", text)
    text = text.replace("RT @vas3k: ", "")
    text = re.sub(r"(https?://[\S]+)", "", text)
    return text


def extract_place(tweet):
    twitter_place = None
    if "place" in tweet and tweet["place"]:
        twitter_place = tweet["place"]
    elif "retweeted_status" in tweet and "place" in tweet["retweeted_status"] and tweet["retweeted_status"]["place"]:
        twitter_place = tweet["retweeted_status"]["place"]

    if twitter_place:
        geo = {
            "name": twitter_place["full_name"]
        }
        coordinates = twitter_place.get("bounding_box", {}).get("coordinates")
        if coordinates:
            geo["latitude"] = coordinates[0][0][1]
            geo["longitude"] = coordinates[0][0][0]
        return {
            "geo": geo
        }
    return None


def instagram_oembed(url):
    response = requests.get("http://api.instagram.com/oembed?url=%s" % url)
    print("Instagram response: %s" % response.text)
    return response.json()["thumbnail_url"]


def start_story(tweet):
    command, code, title = tweet["text"].split(" ", 2)
    print("Start story: %s" % code)
    group, created = Story.objects.get_or_create(
        slug=code,
        type="events",
        defaults=dict(
            author="vas3k",
            title=clear_text(title)
        )
    )
    if created:
        print("OK")
    else:
        print("SKIP")


def add_to_story(tweet):
    command, type, text = tweet["text"].split(" ", 2)
    text = re.sub(r'(http://[^ ]+)', "", text).replace("RT @vas3k: ", "")
    print("Add to last story: %s" % type)
    last_story = Story.objects.filter(type="events").order_by("-created_at").first()
    data = extract_place(tweet)
    for url in tweet["entities"]["urls"]:
        if url["expanded_url"].startswith("http://i.vas3k.ru"):
            image = url["expanded_url"]
            memory, created = Memory.objects.get_or_create(
                slug=tweet["id_str"],
                defaults=dict(
                    type=type,
                    icon="icon-photobucket",
                    title=clear_text(text),
                    image=image,
                    image_preview=image.replace("i.vas3k.ru/", "i.vas3k.ru/400/"),
                    text=clear_text(text),
                    data=json.dumps(data) if data else None,
                    story=last_story,
                    url=image.replace("i.vas3k.ru/", "i.vas3k.ru/full/") if image else "http://twitter.com/vas3k/status/%s" % tweet["id_str"],
                    latitude=data["geo"].get("latitude") if data and "geo" in data else None,
                    longitude=data["geo"].get("longitude") if data and "geo" in data else None
                )
            )
            if created:
                Story.objects.filter(id=last_story.id).update(created_at=datetime.now())
                print("OK")
            else:
                print("SKIP")


def add_image_to_last_story(tweet, image, type="picmedium", icon="icon-photobucket", url=None):
    print("Add image to last story: %s" % image)
    last_story = Story.objects.filter(type="events").order_by("-created_at").first()
    data = extract_place(tweet)
    memory, created = Memory.objects.get_or_create(
        slug=tweet["id_str"],
        defaults=dict(
            type=type,
            icon=icon,
            title=clear_text(tweet["text"]),
            image=image,
            image_preview=image.replace("i.vas3k.ru/", "i.vas3k.ru/500/"),
            text=clear_text(tweet["text"]),
            story=last_story,
            data=json.dumps(data) if data else None,
            url=url,
            latitude=data["geo"].get("latitude") if data and "geo" in data else None,
            longitude=data["geo"].get("longitude") if data and "geo" in data else None
        )
    )
    if created:
        Story.objects.filter(id=last_story.id).update(created_at=datetime.now())
        print("OK")
    else:
        print("SKIP")


def add_text_to_last_story(tweet):
    print("Add text to last story: %s" % tweet["text"])
    last_story = Story.objects.filter(type="events").order_by("-created_at").first()
    data = extract_place(tweet)
    memory, created = Memory.objects.get_or_create(
        slug=tweet["id_str"],
        defaults=dict(
            type="text",
            text=clear_text(tweet["text"]),
            story=last_story,
            data=json.dumps(data) if data else None,
            url="http://twitter.com/vas3k/status/%s" % tweet["id_str"],
            latitude=data["geo"].get("latitude") if data and "geo" in data else None,
            longitude=data["geo"].get("longitude") if data and "geo" in data else None
        )
    )
    if created:
        Story.objects.filter(id=last_story.id).update(created_at=datetime.now())
        print("OK")
    else:
        print("SKIP")


COMMANDS = {
    "add": add_to_story,
    "start": start_story
}


twitter = TwitterAPI(
    consumer_key="",
    consumer_secret="",
    access_token_key="",
    access_token_secret=""
)

tweets = twitter.request("statuses/user_timeline", {
    "count": 50,
    "trim_user": True,
    "exclude_replies": True,
    "include_rts": True
})

for tweet in reversed(list(tweets)):
    print("Tweet: %s" % tweet)
    is_processed = False
    for command, action in COMMANDS.items():
        if tweet["text"].startswith(command):
            action(tweet)
            is_processed = True
            break

    if not is_processed:
        for url in tweet["entities"]["urls"]:
            if url["expanded_url"].startswith("http://i.vas3k.ru"):
                url_big = url["expanded_url"].replace("http://i.vas3k.ru/", "http://i.vas3k.ru/full/")
                add_image_to_last_story(tweet, url["expanded_url"], url=url_big)
                is_processed = True

            if url["expanded_url"].startswith("https://instagram.com") or url["expanded_url"].startswith("http://instagram.com"):
                add_image_to_last_story(tweet, instagram_oembed(url["expanded_url"]), type="picsquare", icon="icon-instagramtwo", url=url["expanded_url"])
                is_processed = True

        for url in tweet["entities"].get("media", []):
            url_big = url["media_url"]
            if url_big.startswith("http://i.vas3k.ru/"):
                url_big = url["media_url"].replace("http://i.vas3k.ru/", "http://i.vas3k.ru/full/")
            add_image_to_last_story(tweet, url["media_url"], url=url_big)
            is_processed = True

    if not is_processed:
        add_text_to_last_story(tweet)

