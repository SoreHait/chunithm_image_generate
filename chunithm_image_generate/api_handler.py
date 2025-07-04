import requests
from .constants import *
from .models import player, bests, scorelist
from typing import Union
from . import cache_manage


def get_louis_player(account: Union[str, int], *, qq: bool) -> player.Player:
    endpoint = f"{LOUIS_URL}/api/open/chunithm/user-info"
    body = {"qq" if qq else "username": account}
    resp = requests.post(endpoint, json=body, headers=LOUIS_HEADERS)
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError("Failed to get player info. Using API: louis")
    return player.Player.from_louis(resp.json())

def get_louis_scorelist(account: Union[str, int], level: str, keep_all: bool = False, *, qq: bool) -> scorelist.ScoreList:
    endpoint = f"{LOUIS_URL}/api/open/chunithm/filtered-info"
    body = {"qq" if qq else "username": account, "level": f"{level}-{level}"}
    resp = requests.post(endpoint, json=body, headers=LOUIS_HEADERS)
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError("Failed to get player scorelist. Using API: louis")
    player_model = get_louis_player(account, qq=qq)
    song_data = cache_manage.get_louis_constant()
    if keep_all:
        return scorelist.ScoreList.from_louis_all(player_model, resp.json(), song_data, level)
    return scorelist.ScoreList.from_louis(player_model, resp.json(), song_data)

def get_louis_bests(account: Union[str, int], *, qq: bool) -> bests.Bests:
    endpoint = f"{LOUIS_URL}/api/open/chunithm/basic-info"
    body = {"qq" if qq else "username": account}
    resp = requests.post(endpoint, json=body, headers=LOUIS_HEADERS)
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError("Failed to get player bests. Using API: louis")
    song_data = cache_manage.get_louis_constant()
    return bests.Bests.from_louis(resp.json(), song_data)

def get_divingfish_bests(account: Union[str, int], *, qq: bool) -> bests.Bests:
    endpoint = f"{DIVINGFISH_URL}/api/chunithmprober/query/player"
    body = {"qq" if qq else "username": account}
    resp = requests.post(endpoint, json=body, headers=DIVINGFISH_HEADERS)
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError("Failed to get player bests. Using API: divingfish")
    return bests.Bests.from_divingfish(resp.json())

def get_lxns_player(account: Union[str, int], *, qq: bool) -> player.Player:
    endpoint = f"{LXNS_URL}/api/v0/chunithm/player/qq/{account}" if qq else f"{LXNS_URL}/api/v0/chunithm/player/{account}"
    resp = requests.get(endpoint, headers=LXNS_HEADERS)
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError("Failed to get player info. Using API: lxns")
    return player.Player.from_lxns(resp.json()["data"])

def get_lxns_bests(account: Union[str, int], *, qq: bool) -> bests.Bests:
    player_model = get_lxns_player(account, qq=qq)
    endpoint = f"{LXNS_URL}/api/v0/chunithm/player/{player_model.friend_code}/bests"
    resp = requests.get(endpoint, headers=LXNS_HEADERS)
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError("Failed to get player bests. Using API: lxns")
    song_data = cache_manage.get_lxns_constant()
    return bests.Bests.from_lxns(player_model, resp.json()["data"], song_data)
