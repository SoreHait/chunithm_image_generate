from PIL import Image, ImageDraw, ImageFont
import os
from math import ceil
from . import util
from ..models import scorelist
from typing import Dict, List
from decimal import Decimal


BASE_PATH = os.path.split(__file__)[0]
RESOURCE_BASE_PATH = os.path.join(BASE_PATH, 'res', 'scorelist')
RESOURCE_CARD_PATH = os.path.join(RESOURCE_BASE_PATH, 'card')
RESOURCE_BACKGROUND_PATH = os.path.join(RESOURCE_BASE_PATH, 'bg2025')
FONT_PATH = os.path.join(BASE_PATH, 'res', 'fonts')
JACKET_PATH = os.path.join(BASE_PATH, 'res', 'jacketpng')


class ChuniScoreListGenerate2025:
    @staticmethod
    def generate_single_song(record: scorelist.ScoreListItem) -> Image.Image:
        base = Image.open(os.path.join(RESOURCE_CARD_PATH, f'{record.difficulty}_{util.get_fc_text_strip(record.judge_status, record.score)[0]}.png'))
        base_draw = ImageDraw.Draw(base)

        try:
            jacket = Image.open(os.path.join(JACKET_PATH, f"{record.music_id}.png"))
        except FileNotFoundError:
            print("chuni 曲绘未找到:", f"{record.music_id}.png")
            jacket = util.get_dummy_jacket(record.music_id)
        jacket = jacket.resize((600, 600))
        jacket_mask = Image.new('1', (600, 600))
        draw_mask = ImageDraw.Draw(jacket_mask)
        draw_mask.rounded_rectangle((0, 0, 600, 600), 120, fill='white')
        base.paste(jacket, (round((base.width - jacket.width) / 2), 126), jacket_mask)

        font = ImageFont.truetype(os.path.join(FONT_PATH, 'LINESeedJP_OTF_Bd.otf'), size=120)
        score_txt = f'{record.score:,}' if record.score >= 0 else 'N/P'
        base_draw.text((round(base.width / 2), 831), score_txt, fill='black', font=font, anchor='mm')

        return base

    @staticmethod
    def generate_scorelist_layout(score_list: scorelist.ScoreList, api: str) -> Image.Image:
        line_len = 9
        scale_to = (x := 235, 997 * x // 855)
        top_padding = 480
        bottom_padding = 290
        starting_at = (148, top_padding)
        spacing = 11
        y_compensate = 0
        category_compensate = 0

        if len(score_list.score_list) == 0:
            raise ValueError(f"User Bests has no records. Using API: {api}")
        score_list.score_list.sort(key=lambda s: s.score, reverse=True)
        _constant_categorized: Dict[Decimal, List[scorelist.ScoreListItem]] = {}
        for record in score_list.score_list:
            if record.constant not in _constant_categorized:
                _constant_categorized[record.constant] = []
            _constant_categorized[record.constant].append(record)
        constant_categorized: List[List[scorelist.ScoreListItem]] = sorted(_constant_categorized.values(), key=lambda s: s[0].constant, reverse=True)

        base = Image.open(os.path.join(RESOURCE_BACKGROUND_PATH, 'bg.png'))
        constant_background = Image.open(os.path.join(RESOURCE_BACKGROUND_PATH, 'constant.png'))
        total_height = top_padding + bottom_padding + len(constant_categorized) * (constant_background.height + category_compensate * 2)
        for group in constant_categorized:
            total_height += ceil(len(group) / line_len) * (scale_to[1] + spacing + y_compensate)
        base = base.resize((base.width, total_height))
        component = Image.open(os.path.join(RESOURCE_BACKGROUND_PATH, 'spot.png'))
        base.alpha_composite(component, (0, (base.height - component.height) // 2))
        component = Image.open(os.path.join(RESOURCE_BACKGROUND_PATH, 'topstripe.png'))
        base.alpha_composite(component)
        component = Image.open(os.path.join(RESOURCE_BACKGROUND_PATH, 'bottomstripe.png'))
        base.alpha_composite(component, (base.width - component.width, base.height - component.height))

        if base.height >= 4500:
            component = Image.open(os.path.join(RESOURCE_BACKGROUND_PATH, 'triangle.png'))
            base.alpha_composite(component, (0, (base.height - component.height) // 2))

        component = Image.open(os.path.join(RESOURCE_BACKGROUND_PATH, 'top.png'))
        base.alpha_composite(component)
        component = Image.open(os.path.join(RESOURCE_BACKGROUND_PATH, 'bottom.png'))
        base.alpha_composite(component, (base.width - component.width, base.height - component.height))

        base_draw = ImageDraw.Draw(base)
        font = ImageFont.truetype(os.path.join(FONT_PATH, 'LINESeedJP_OTF_Bd.otf'), size=80)
        current_y = -category_compensate
        sssp_counter = 0
        sss_counter = 0
        aj_counter = 0
        fc_counter = 0
        overlay = Image.new('RGBA', (base.width, base.height))
        overlay_draw = ImageDraw.Draw(overlay)
        for constant_group in constant_categorized:
            current_y += category_compensate
            overlay.paste(constant_background, (base.width // 2 - constant_background.width // 2, starting_at[1] + current_y))
            current_y += constant_background.height // 2
            overlay_draw.text((base.width // 2, starting_at[1] + current_y), f'{constant_group[0].constant:.1f}', fill='black', font=font, anchor='mm')
            current_y += constant_background.height // 2 + category_compensate
            for idx, record in enumerate(constant_group):
                if idx % line_len == 0 and idx != 0:
                    current_y += scale_to[1] + spacing + y_compensate
                song = ChuniScoreListGenerate2025.generate_single_song(record).resize(scale_to)
                paste_at = (starting_at[0] + idx % line_len * (song.width + spacing),
                            starting_at[1] + current_y + y_compensate)
                overlay.paste(song, paste_at)
                if 1007500 <= record.score <= 1008999:
                    sss_counter += 1
                elif 1009000 <= record.score <= 1010000:
                    sssp_counter += 1
                if record.judge_status == 'alljustice' or record.judge_status == 'alljusticecritical':
                    aj_counter += 1
                elif record.judge_status == 'fullcombo':
                    fc_counter += 1
            current_y += scale_to[1] + spacing + y_compensate
        base.alpha_composite(overlay)

        font = font.font_variant(size=43)
        source = util.get_api_name(api)
        base_draw.text((422, base.height - 143), source, 'black', font, 'ls')

        font = font.font_variant(size=55)
        base_draw.text((865, 395), f'SSS+:{sssp_counter} SSS:{sss_counter} AJ:{aj_counter} FC:{fc_counter}', 'black', font, 'mm')

        font = ImageFont.truetype(os.path.join(FONT_PATH, 'LINESeedJP_combined.otf'), size=96)
        nickname = util.wrap_text(score_list.nickname, font, 700)
        base_draw.text((780, 245), nickname, 'black', font, 'mm')

        base = base.resize(size=(int(base.width * 0.6), int(base.height * 0.6))).convert('RGB')
        return base
