from dataclasses import dataclass
from typing import List, Tuple
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
        all_music: List[Tuple[int, int]] = []
        for music_id, constant_info in song_info.items():
            for level_index, level_constant in constant_info.items():
                if level_index == 'title':
                    continue
                constant = Decimal(level_constant)
                if f'{int(constant)}{"+" if constant % 1 >= 0.5 else ""}' == query_level:
                    all_music.append((int(music_id), int(level_index)))

        for record in score_model.__root__:
            score_list.append(ScoreListItem(
                constant=Decimal(song_info[str(record.music_id)][str(record.level_index)]),
                judge_status=record.judge_status,
                difficulty=record.level_index,
                music_id=record.music_id,
                score=record.score,
            ))
            all_music.remove((record.music_id, record.level_index))

        for music_id, level_index in all_music:
            score_list.append(ScoreListItem(
                constant=Decimal(song_info[str(music_id)][str(level_index)]),
                judge_status='',
                difficulty=level_index,
                music_id=music_id,
                score=Decimal('-1'),
            ))

        return cls(nickname=player_model.nickname, score_list=score_list)
