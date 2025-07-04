from PIL import Image
from typing import Union
from . import api_handler
from .generators import bests_apr_2025


def generate_louis_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_louis_bests(account, qq=qq)
    return bests_apr_2025.ChuniAprilGenerate2025.generate_bests_layout(model, 'louis')

def generate_lxns_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_lxns_bests(account, qq=qq)
    return bests_apr_2025.ChuniAprilGenerate2025.generate_bests_layout(model, 'lxns')

def generate_divingfish_bests(account: Union[str, int], *, qq: bool) -> Image.Image:
    model = api_handler.get_divingfish_bests(account, qq=qq)
    return bests_apr_2025.ChuniAprilGenerate2025.generate_bests_layout(model, 'divingfish')
