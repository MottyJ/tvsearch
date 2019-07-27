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


def get_version():
    return "0.0.1"


def get_json_from_file(show_name):
    try:
        return template(
            "{folder}/{filename}.json".format(folder=JSON_FOLDER, filename=show_name)
        )
    except:
        return {}


def get_shows(AVAILABE_SHOWS):
    shows_redefined = []
    for show in AVAILABE_SHOWS:
        shows_redefined.append(json.loads(get_json_from_file(show)))
    return shows_redefined

def get_show_episodes(show_id):
    show = json.loads(get_json_from_file(show_id))
    return show["_embedded"]["episodes"]

def get_episode(show_id, episode_id):
    show = json.loads(get_json_from_file(show_id))
    for episode in show["_embedded"]["episodes"]:
        if str(episode['id']) == str(episode_id):
            return episode
    return 'episode not found'

def search_episodes(search_value):
    shows = get_shows(AVAILABE_SHOWS)
    results = []
    for show in shows:
        for episode in show["_embedded"]["episodes"]:
            if (search_value.lower() in episode['name'].lower()):
                results.append({'showid':show['id'],'episodeid':episode['id'],'text':episode['name']})
            elif episode['summary'] and (search_value.lower() in episode['summary'].lower()):
                results.append({'showid': show['id'], 'episodeid': episode['id'], 'text': episode['name']})
    return results
