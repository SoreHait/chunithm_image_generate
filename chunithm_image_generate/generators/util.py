from PIL.ImageFont import FreeTypeFont
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
from decimal import Decimal
import os


BASE_PATH = os.path.split(__file__)[0]
FONT_PATH = os.path.join(BASE_PATH, 'res', 'fonts')


def get_dummy_jacket(music_id: int) -> Image.Image:
    jacket = Image.new('RGBA', (600, 600), color='gray')
    jacket_draw = ImageDraw.Draw(jacket)
    font = ImageFont.truetype(os.path.join(FONT_PATH, 'LINESeedJP_OTF_Bd.otf'), size=300)
    jacket_draw.text((300, 220), '?', fill='black', font=font, anchor='mm')
    font = font.font_variant(size=100)
    jacket_draw.text((300, 430), str(music_id), fill='black', font=font, anchor='mm')
    return jacket

def get_diff_color(diff: int) -> str:
    return ['#029F76', '#EE7707', '#E02A2A', '#8118CE', '#303030'][diff]

def wrap_text(text: str, font: FreeTypeFont, wrap_width: int) -> str:
    text_width = font.getmask(text).getbbox()[2]
    if text_width > wrap_width:
        wrap_scale = text_width / wrap_width
        text = text[:int(len(text) // wrap_scale)]
        while font.getmask(text + '...').getbbox()[2] > wrap_width:
            text = text[:-1]
        text += '...'
    return text

def get_fc_text_strip(status: str, score: Decimal) -> Tuple[str, str]:
    if status == 'alljusticecritical' or score == 1010000:
        return 'AJC', '#FFABCF'
    elif status == 'alljustice':
        return 'AJ', '#ffae38'
    elif status == 'fullcombo' or status == 'fullchain' or status == 'fullchain2':
        return 'FC', '#00cd98'
    elif score == -1:
        return 'NP', ''
    else:
        return '--', ''

def draw_four_digit_rating(base_im_draw: ImageDraw.ImageDraw, ra: Decimal, text_prefix: str,
                           main_font: FreeTypeFont, sub_font: FreeTypeFont, position: Tuple[int, int],
                           sub_text_shift: int) -> int:
    text_width = sub_text_shift
    ra_str = f'{ra:.4f}'
    text_main = f'{text_prefix}{ra_str[:-2]}'
    text_sub = ra_str[-2:]
    base_im_draw.text(position, text=text_main, fill='black', font=main_font, anchor='ls')
    ra_text_main_width = main_font.getmask(text_main).getbbox()[2]
    text_width += ra_text_main_width
    base_im_draw.text((position[0]+ra_text_main_width+sub_text_shift, position[1]), text=text_sub, fill='black',
                      font=sub_font, anchor='ls')
    text_width += sub_font.getmask(text_sub).getbbox()[2]
    return text_width

def get_ratingcolor(rating: Decimal) -> str:
    if 0 <= rating < 4:
        ratingcolor = "#00BF40"
    elif 4 <= rating < 7:
        ratingcolor = "#FF6F00"
    elif 7 <= rating < 10:
        ratingcolor = "#FF4040"
    elif 10 <= rating < 12:
        ratingcolor = "#9326FF"
    elif 12 <= rating < 13.25:
        ratingcolor = "#D5510C"
    elif 13.25 <= rating < 14.5:
        ratingcolor = "#16A9E6"
    elif 14.5 <= rating < 15.25:
        ratingcolor = "#FFD937"
    elif 15.25 <= rating < 16:
        ratingcolor = "#FAD9A4"
    elif 16 <= rating < 17:
        ratingcolor = "16"
    elif rating >= 17:
        ratingcolor = "17"
    else:
        raise ValueError("Rating out of range")
    return ratingcolor

def get_api_name(api: str) -> str:
    if api == 'louis':
        return 'Louis'
    elif api == 'lxns':
        return 'Lxns'
    elif api == 'divingfish':
        return 'Diving-Fish'
    else:
        return 'Unknown'
