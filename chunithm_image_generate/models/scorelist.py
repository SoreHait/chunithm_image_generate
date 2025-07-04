from dataclasses import dataclass
from typing import List
from decimal import Decimal
from .api_models import louis
from . import player


@dataclass
class ScoreListItem:
    constant: Decimal
    judge_status: str
    difficulty: int
    music_id: int
    score: Decimal


@dataclass
class ScoreList:
    nickname: str
    score_list: List[ScoreListItem]

    @classmethod
    def from_louis(cls, player_model: player.Player, score_data: list, song_info: dict) -> "ScoreList":
        score_model: louis.LouisScoreList = louis.LouisScoreList.parse_obj(score_data)
        score_list: List[ScoreListItem] = []
        for record in score_model.__root__:
            score_list.append(ScoreListItem(
                constant=Decimal(song_info[str(record.music_id)][str(record.level_index)]),
                judge_status=record.judge_status,
                difficulty=record.level_index,
                music_id=record.music_id,
                score=record.score,
            ))
        return cls(nickname=player_model.nickname, score_list=score_list)

    @classmethod
    def from_louis_all(cls, player_model: player.Player, score_data: list, song_info: dict, query_level: str) -> "ScoreList":
        score_model: louis.LouisScoreList = louis.LouisScoreList.parse_obj(score_data)
        score_list: List[ScoreListItem] = []
        for music_id, info in song_info.items():

