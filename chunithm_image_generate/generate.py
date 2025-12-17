from PIL import Image
from typing import Union
from . import api_handler
from .generators import bests_gen, scorelist_gen


def generate_louis_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_louis_bests(account, qq=qq)
    return bests_gen.ChuniBestsGenerate.generate_bests_layout(model, 'louis')

def generate_louis_scorelist(account: Union[str, int], level: str, keep_all: bool = False, *, qq: bool) -> Image.Image:
    model = api_handler.get_louis_scorelist(account, level, keep_all, qq=qq)
    return scorelist_gen.ChuniScoreListGenerate.generate_scorelist_layout(model, 'louis')

def generate_lxns_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_lxns_bests(account, qq=qq)
    return bests_gen.ChuniBestsGenerate.generate_bests_layout(model, 'lxns')

def generate_lxns_scorelist(account: Union[str, int], token: str, level: str, keep_all: bool = False, *, qq: bool) -> Image.Image:
    model = api_handler.get_lxns_scorelist(account, token, level, keep_all, qq=qq)
    return scorelist_gen.ChuniScoreListGenerate.generate_scorelist_layout(model, 'lxns')

def generate_divingfish_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_divingfish_bests(account, qq=qq)
    return bests_gen.ChuniBestsGenerate.generate_bests_layout(model, 'divingfish')
