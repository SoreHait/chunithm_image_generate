from dataclasses import dataclass
from typing import List
from decimal import Decimal, ROUND_FLOOR
from .api_models import divingfish, louis, lxns
from . import player
import unicodedata


def cut_digits(num: Decimal, digit: int) -> Decimal:
    return num.quantize(Decimal(f'0.{"0" * (digit - 1)}1'), rounding=ROUND_FLOOR)


@dataclass
class RecordItem:
    constant: Decimal
    judge_status: str
    level: str
    difficulty: int
    music_id: int
    score: Decimal
    title: str

    @property
    def ra_precise(self) -> Decimal:
        if 500000 <= self.score <= 799999:
            return (self.score - 500000) * (self.constant - 5) / 2 / 300000
        elif 800000 <= self.score <= 899999:
            return (self.score - 800000) * (self.constant - 5) / 100000 + (self.constant - 5) / 2
        elif 900000 <= self.score <= 924999:
            return (self.score - 900000) * 2 / 25000 + (self.constant - 5)
        elif 925000 <= self.score <= 974999:
            return (self.score - 925000) * 3 / 50000 + (self.constant - 3)
        elif 975000 <= self.score <= 999999:
            return (self.score - 975000) * 1 / 25000 + self.constant
        elif 1000000 <= self.score <= 1004999:
            return (self.score - 1000000) * Decimal('0.5') / 5000 + (self.constant + 1)
        elif 1005000 <= self.score <= 1007499:
            return (self.score - 1005000) * Decimal('0.5') / 2500 + (self.constant + Decimal('1.5'))
        elif 1007500 <= self.score <= 1008999:
            return (self.score - 1007500) * Decimal('0.15') / 1500 + (self.constant + 2)
        elif 1009000 <= self.score <= 1010000:
            return self.constant + Decimal('2.15')
        else:
            return Decimal('0')

    @property
    def ra_4dg(self) -> Decimal:
        return cut_digits(self.ra_precise, 4)

    @property
    def ra_2dg(self) -> Decimal:
        return cut_digits(self.ra_precise, 2)


@dataclass
class Bests:
    nickname: str
    api: str
    bests: List[RecordItem]
    recents: List[RecordItem]

    @property
    def __b30_sum(self) -> Decimal:
        x = Decimal('0')
        for i in self.bests:
            x += i.ra_2dg
        return x

    @property
    def __r10_sum(self) -> Decimal:
        x = Decimal('0')
        for i in self.recents:
            x += i.ra_2dg
        return x

    @property
    def player_rating_4dg(self) -> Decimal:
        return cut_digits((self.__b30_sum + self.__r10_sum) / 40, 4)

    @property
    def b30_avg_4dg(self) -> Decimal:
        return cut_digits(self.__b30_sum / 30, 4)

    @property
    def r10_avg_4dg(self) -> Decimal:
        return cut_digits(self.__r10_sum / 10, 4)

    @property
    def max_rating_4dg(self) -> Decimal:
        if len(self.bests) == 0:
            raise ValueError(f"User Bests has no records. Using API: {self.api}")
        else:
            return cut_digits((self.__b30_sum + self.bests[0].ra_2dg * 10) / 40, 4)

    @classmethod
    def from_lxns(cls, player_model: player.Player, bests_data: dict, song_info: dict) -> "Bests":
        bests_model: lxns.LxnsBestsRecords = lxns.LxnsBestsRecords.parse_obj(bests_data)
        bests = []
        recents = []

        def __lxns_to_bests(l: lxns.LxnsBestsRecordItem) -> RecordItem:
            return RecordItem(
                constant=Decimal(song_info[str(l.id)][str(l.level_index)]),
                judge_status='' if l.full_combo is None else l.full_combo,
                level=l.level,
                difficulty=l.level_index,
                music_id=l.id,
                score=l.score,
                title=l.song_name
            )

        for record in bests_model.bests:
            bests.append(__lxns_to_bests(record))
        for record in bests_model.recents:
            recents.append(__lxns_to_bests(record))
        return cls(player_model.nickname, 'lxns', bests, recents)

    @classmethod
    def from_louis(cls, bests_data: dict, song_info: dict) -> "Bests":
        bests_model: louis.LouisBests = louis.LouisBests.parse_obj(bests_data)
        bests = []
        recents = []

        for record in bests_model.records.b30:
            constant = Decimal(song_info[str(record.music_id)][str(record.level_index)])
            bests.append(RecordItem(
                constant=constant,
                judge_status=record.judge_status,
                level=f'{constant // 1}{"+" if constant % 1 >= Decimal("0.5") else ""}',
                difficulty=record.level_index,
                music_id=record.music_id,
                score=record.score,
                title=song_info[str(record.music_id)]['title']
            ))
        for record in bests_model.records.r10:
            level_index = {'basic': 0, 'advanced': 1, 'expert': 2, 'master': 3, 'ultimate': 4}[record.difficulty]
            constant = Decimal(song_info[str(record.music_id)][str(level_index)])
            recents.append(RecordItem(
                constant=constant,
                judge_status=record.judge_status,
                level=f'{constant // 1}{"+" if constant % 1 >= Decimal("0.5") else ""}',
                difficulty=level_index,
                music_id=record.music_id,
                score=record.score,
                title=song_info[str(record.music_id)]['title']
            ))
        return cls(unicodedata.normalize('NFKC', bests_model.nickname), 'louis', bests, recents)

    @classmethod
    def from_divingfish(cls, bests_data: dict) -> "Bests":
        bests_model: divingfish.DivingfishBests = divingfish.DivingfishBests.parse_obj(bests_data)
        bests = []
        recents = []

        def __df_to_bests(l: divingfish.DivingfishBestsRecordItem) -> RecordItem:
            return RecordItem(
                constant=l.ds,
                judge_status=l.fc,
                level=l.level,
                difficulty=l.level_index,
                music_id=l.mid,
                score=l.score,
                title=l.title
            )
        for record in bests_model.records.b30:
            bests.append(__df_to_bests(record))
        for record in bests_model.records.r10:
            recents.append(__df_to_bests(record))
        return cls(bests_model.nickname, 'divingfish', bests, recents)
