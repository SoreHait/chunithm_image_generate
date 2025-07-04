from PIL import Image
from typing import Union
from . import api_handler
from .generators import bests_gen_2025, scorelist_gen_2025


def generate_louis_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_louis_bests(account, qq=qq)
    return bests_gen_2025.ChuniBestsGenerate2025.generate_bests_layout(model, 'louis')

def generate_louis_scorelist(account: Union[str, int], level: str, keep_all: bool = False, *, qq: bool) -> Image.Image:
    model = api_handler.get_louis_scorelist(account, level, keep_all, qq=qq)
    return scorelist_gen_2025.ChuniScoreListGenerate2025.generate_scorelist_layout(model, 'louis')

def generate_lxns_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_lxns_bests(account, qq=qq)
    return bests_gen_2025.ChuniBestsGenerate2025.generate_bests_layout(model, 'lxns')

def generate_divingfish_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_divingfish_bests(account, qq=qq)
    return bests_gen_2025.ChuniBestsGenerate2025.generate_bests_layout(model, 'divingfish')
