import json
import requests
import os
import shutil
from .constants import LOUIS_URL, LXNS_URL


BASE_PATH = os.path.split(__file__)[0]
CACHE_PATH = os.path.join(BASE_PATH, 'cache')
LOUIS_CACHE_FILE = os.path.join(CACHE_PATH, 'louis_cache.json')
LXNS_CACHE_FILE = os.path.join(CACHE_PATH, 'lxns_cache.json')

LOUIS_ENDPOINT = f"{LOUIS_URL}/api/resource/chunithm/song-list"
LXNS_ENDPOINT = f"{LXNS_URL}/api/v0/chunithm/song/list"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_louis_constant() -> dict:
    ensure_dir(CACHE_PATH)
    if os.path.exists(LOUIS_CACHE_FILE):
        with open(LOUIS_CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    resp = requests.get(LOUIS_ENDPOINT)
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError("Failed to get constants. Using API: louis")
    constant_list = {}
    for song in resp.json():
        constant_list[str(song['musicID'])] = {'title': song['title']}
        for key, value in song['charts'].items():
            if value is None or key == 'worldsend':
                continue
            level_index = {'basic': '0', 'advanced': '1', 'expert': '2', 'master': '3', 'ultima': '4'}[key]
            constant_list[str(song['musicID'])][level_index] = str(value["constant"])
    with open(LOUIS_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(constant_list, f, ensure_ascii=False, indent=4)
    return constant_list

def get_lxns_constant() -> dict:
    ensure_dir(CACHE_PATH)
    if os.path.exists(LXNS_CACHE_FILE):
        with open(LXNS_CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    resp = requests.get(LXNS_ENDPOINT)
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError("Failed to get constants. Using API: lxns")
    constant_list = {}
    for song in resp.json()["songs"]:
        constant_list[str(song["id"])] = {}
        for diff in song["difficulties"]:
            constant_list[str(song["id"])][str(diff["difficulty"])] = str(diff["level_value"])
    with open(LXNS_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(constant_list, f, ensure_ascii=False, indent=4)
    return constant_list

def remove_cache():
    if os.path.exists(CACHE_PATH):
        shutil.rmtree(CACHE_PATH)
