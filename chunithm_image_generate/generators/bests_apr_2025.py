from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple
from ..models import bests
from . import util
import random
from decimal import Decimal
from PIL.ImageFont import FreeTypeFont


BASE_PATH = os.path.split(__file__)[0]
RESOURCE_PATH = os.path.join(BASE_PATH, 'res', 'aprilres')
JACKET_PATH = os.path.join(BASE_PATH, 'res', 'jacketpng')

def get_diff_text(level_index: int) -> str:
    return ['基础', '进阶', '专家', '大师', '终极'][level_index]

def draw_two_digit_rating_apr(base_im_draw: ImageDraw.ImageDraw, ra: Decimal,
                           main_font: FreeTypeFont, sub_font: FreeTypeFont, position: Tuple[int, int],
                           sub_text_shift: int) -> int:
    text_width = sub_text_shift
    ra_str = f'{ra:.2f}'
    text_main = ra_str[:-2]
    text_sub = ra_str[-2:]
    base_im_draw.text(position, text=text_main, fill='red', font=main_font, anchor='lt')
    ra_text_main_width = main_font.getmask(text_main).getbbox()[2]
    text_width += ra_text_main_width
    base_im_draw.text((position[0]+ra_text_main_width+sub_text_shift, position[1]), text=text_sub, fill='red',
                      font=sub_font, anchor='lt')
    text_width += sub_font.getmask(text_sub).getbbox()[2]
    return text_width

class ChuniAprilGenerate2025:
    @staticmethod
    def generate_song_card(record: bests.RecordItem, im: Image.Image, at: Tuple[int, int], index: int):
        try:
            jacket = Image.open(os.path.join(JACKET_PATH, f"{record.music_id}.png"))
        except FileNotFoundError:
            print("chuni 曲绘未找到:", f"{record.music_id}.png")
            jacket = util.get_dummy_jacket(record.music_id)

        im_draw = ImageDraw.Draw(im)
        jacket = jacket.resize((120, 120))
        im.paste(jacket, ((188 - 120) // 2 + at[0], (188 - 120) // 2 + at[1]))

        font = ImageFont.truetype(os.path.join(RESOURCE_PATH, 'simhei.ttf'), 24)
        im_draw.text((at[0] + 18, at[1] + 16), str(index),
                     'black', font=font, anchor='lm', stroke_width=1)
        im_draw.text((at[0] + 55, at[1] + 16), get_diff_text(record.difficulty),
                     util.get_diff_color(record.difficulty), font=font, anchor='lm', stroke_width=1)
        im_draw.text((at[0] + 165, at[1] + 16), str(record.constant),
                     'red', font=font, anchor='rm', stroke_width=1)
        font = font.font_variant(size=18)
        im_draw.text((at[0] + 10, at[1] + 150), util.wrap_text(record.title, font, 180),
                     'black', font=font, anchor='lm', stroke_width=2, stroke_fill='white')
        im_draw.text((at[0] + 10, at[1] + 170), f'{record.score:,}',
                     'black', font=font, anchor='lm', stroke_width=2, stroke_fill='white')

        pricetag = Image.open(os.path.join(RESOURCE_PATH, f'pricetag{random.randint(1, 4)}.png'))
        pricetag = pricetag.resize((180, 180))
        im.paste(pricetag, (at[0] + 60, at[1] + 70), pricetag)

        font = ImageFont.truetype(os.path.join(RESOURCE_PATH, 'DSN-SiRin.ttf'), 48)
        font_small = ImageFont.truetype(os.path.join(RESOURCE_PATH, 'DSN-SiRin.ttf'), 36)
        draw_two_digit_rating_apr(im_draw, record.ra_2dg, font, font_small, (at[0] + 123, at[1] + 148), 0)


    @staticmethod
    def generate_bests_layout(bests_data: bests.Bests, api: str) -> Image.Image:
        if len(bests_data.bests) == 0:
            raise ValueError(f"User Bests has no records. Using API: {api}")
        bests_data.bests.sort(key=lambda x: x.ra_precise, reverse=True)

        starting_pos = (10, 210)
        gap = 10
        card_size = (188, 188)

        bg = Image.open(os.path.join(RESOURCE_PATH, 'bgapr2025.png'))

        for idx, item in enumerate(bests_data.bests):
            pos = (starting_pos[0] + (idx % 5) * (card_size[0] + gap), starting_pos[1] + (idx // 5) * (card_size[1] + gap))
            ChuniAprilGenerate2025.generate_song_card(item, bg, pos, idx + 1)

        bg_draw = ImageDraw.Draw(bg)
        font = ImageFont.truetype(os.path.join(RESOURCE_PATH, 'DSN-SiRin.ttf'), size=90)
        nickname = util.wrap_text(bests_data.nickname, font, 310)
        bg_draw.text((650, 105), nickname, 'white', font, 'ls')
        bg_draw.text((650, 170), f'{bests_data.b30_avg_4dg:.4f}', fill='white', font=font, anchor='ls')

        return bg.convert("RGB")
