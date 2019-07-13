from bottle import template
import json

JSON_FOLDER = "./data"
AVAILABE_SHOWS = [
    "7",
    "66",
    "73",
    "82",
    "112",
    "143",
    "175",
    "216",
    "1371",
    "1871",
    "2993",
    "305",
]


def getVersion():
    return "0.0.1"


def getJsonFromFile(showName):
    try:
        return template(
            "{folder}/{filename}.json".format(folder=JSON_FOLDER, filename=showName)
        )
    except:
        return {}


def getShows(AVAILABE_SHOWS):
    shows_redefined = []
    for show in AVAILABE_SHOWS:
        shows_redefined.append(json.loads(getJsonFromFile(show)))
    return shows_redefined


def get_episode(show_id, episode_id):
    print("in get_episode")
    show = json.loads(getJsonFromFile(show_id))
    for episode in show["_embedded"]["episodes"]:
        if str(episode['id']) == str(episode_id):
            return episode
    return 'episode not found'
