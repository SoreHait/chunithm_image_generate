from PIL import Image, ImageDraw, ImageFont
import os
from math import ceil
from ..models import bests
from . import util


BASE_PATH = os.path.split(__file__)[0]
RESOURCE_PATH = os.path.join(BASE_PATH, 'res', 'bests')
FONT_PATH = os.path.join(BASE_PATH, 'res', 'fonts')
JACKET_PATH = os.path.join(BASE_PATH, 'res', 'jacketpng')


class ChuniBestsGenerate2025:
    @staticmethod
    def generate_song_card(record: bests.RecordItem, index: int) -> Image.Image:
        base = Image.open(os.path.join(RESOURCE_PATH, 'card_base.png'))
        base_draw = ImageDraw.Draw(base)

        try:
            jacket = Image.open(os.path.join(JACKET_PATH, f"{record.music_id}.png"))
        except FileNotFoundError:
            print("chuni 曲绘未找到:", f"{record.music_id}.png")
            jacket = util.get_dummy_jacket(record.music_id)

        jacket = jacket.resize((600, 600))
        jacket_mask = Image.new('1', (600, 600))
        draw_mask = ImageDraw.Draw(jacket_mask)
        draw_mask.rounded_rectangle((0, 0, 600, 600), 100, fill='white')
        base.paste(jacket, (150, 150), jacket_mask)

        font = ImageFont.truetype(os.path.join(FONT_PATH, 'LINESeedJP_OTF_Bd.otf'), size=80)
        base_draw.polygon([(1375, 75), (1275, 175), (875, 175), (975, 75)],
                          fill=util.get_diff_color(record.difficulty))
        base_draw.polygon([(1675, 75), (1575, 175), (1275, 175), (1375, 75)], fill='black')
        base_draw.text((1135, 127), text=record.level, fill='white', font=font, anchor='mm')
        base_draw.text((1475, 127), text=f'#{index}', fill='white', font=font, anchor='mm')

        scorestr = f'{record.score:,}'
        font = font.font_variant(size=176)
        base_draw.text((825, 450), text=scorestr, fill='black', font=font, anchor='lm')

        font = font.font_variant(size=100)
        title_text = util.wrap_text(record.title, font, 925)
        base_draw.text((825, 275), text=title_text, fill='black', font=font, anchor='lm')

        font = font.font_variant(size=120)
        font_small = font.font_variant(size=70)
        fc_str, fc_color = util.get_fc_text_strip(record.judge_status, record.score)
        if fc_color:
            base_draw.polygon([(1100, 575), (850, 825), (715, 825), (965, 575)], fill=fc_color)
        base_draw.text((930, 685), text=fc_str, fill='black', font=font, anchor='ms')

        base_draw.text((1225, 685), text=f'{record.constant:.1f}', fill='black', font=font_small, anchor='rs')
        util.draw_four_digit_rating(base_draw, record.ra_4dg, '', font, font_small, (1295, 685), 10)

        rating_color = util.get_ratingcolor(record.ra_precise)
        strip_area = [(1150, 775), (1100, 825), (1600, 825), (1650, 775)]
        if rating_color == 'colorful':
            step_width = ceil((strip_area[-1][0] - strip_area[0][0]) / 7)
            colors = ['#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF', '#9BF6FF', '#A0C4FF', '#BDB2FF']
            shift = strip_area[0][0] - strip_area[1][0]
            for idx, i in enumerate(range(strip_area[0][0], strip_area[-1][0], step_width)):
                base_draw.polygon([(i, strip_area[0][1]),
                                   (i-shift, strip_area[1][1]),
                                   (i-shift+step_width, strip_area[2][1]),
                                   (i+step_width, strip_area[3][1])], fill=colors[idx])
        else:
            base_draw.polygon(strip_area, fill=rating_color)

        return base.resize((380, 180))

    @staticmethod
    def generate_bests_layout(bests_data: bests.Bests, api: str) -> Image.Image:
        if len(bests_data.bests) == 0:
            raise ValueError(f"User Bests has no records. Using API: {api}")
        bests_data.bests.sort(key=lambda x: x.ra_precise, reverse=True)
        bests_data.recents.sort(key=lambda x: x.ra_precise, reverse=True)

        panel_gap = 50
        r10_layout = (1, 10)
        b30_layout = (3, 10)
        starting_pos = (50, 500)

        bg = Image.open(os.path.join(RESOURCE_PATH, 'bg2025.png'))
        base = Image.new('RGBA', (bg.width, bg.height))
        card = None
        for idx, item in enumerate(bests_data.bests):
            card = ChuniBestsGenerate2025.generate_song_card(item, idx + 1)
            row = idx // b30_layout[0]
            col = idx % b30_layout[0]
            if row >= b30_layout[1]:
                break
            base.paste(card, (starting_pos[0] + col * card.width, starting_pos[1] + row * card.height))
        r10_starting_pos = (starting_pos[0] + b30_layout[0] * card.width + panel_gap, starting_pos[1])
        for idx, item in enumerate(bests_data.recents):
            card = ChuniBestsGenerate2025.generate_song_card(item, idx + 1)
            row = idx // r10_layout[0]
            col = idx % r10_layout[0]
            if row >= r10_layout[1]:
                break
            base.paste(card, (r10_starting_pos[0] + col * card.width, r10_starting_pos[1] + row * card.height))

        bg_draw = ImageDraw.Draw(bg)
        font = ImageFont.truetype(os.path.join(FONT_PATH, 'LINESeedJP_combined.otf'), size=70)
        nickname = util.wrap_text(bests_data.nickname, font, 700)
        bg_draw.text((550, 160), nickname, 'black', font, 'mm')

        font = ImageFont.truetype(os.path.join(FONT_PATH, 'LINESeedJP_OTF_Bd.otf'), size=45)
        font_small = font.font_variant(size=25)
        trailing_white = 15
        bg_draw.text((325, 263), text=f'Rating', fill='black', font=font, anchor='lm')

        starting_pos = (520, 280)
        width = util.draw_four_digit_rating(bg_draw, bests_data.player_rating_4dg, '',
                                              font, font_small, starting_pos, 3)
        util.draw_four_digit_rating(bg_draw, bests_data.max_rating_4dg, '/ ',
                                      font, font_small, (starting_pos[0]+width+trailing_white, starting_pos[1]), 3)

        util.draw_four_digit_rating(bg_draw, bests_data.b30_avg_4dg, '', font, font_small, (380, 423), 3)
        util.draw_four_digit_rating(bg_draw, bests_data.r10_avg_4dg, '', font, font_small, (1030, 423), 3)

        font = font.font_variant(size=30)
        source = util.get_api_name(api)
        bg_draw.text((240, 2422), source, 'black', font, 'ls')

        pt = Image.alpha_composite(bg, base).convert('RGB')
        pt = pt.resize(size=(int(pt.width * 0.7), int(pt.height * 0.7)))
        return pt
