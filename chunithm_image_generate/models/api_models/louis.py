from pydantic import BaseModel
from typing import List
from decimal import Decimal
import re


class LouisRecordItem(BaseModel):
    music_id: int
    level_index: int
    score: Decimal
    judge_status: str

    class Config:
        alias_generator = lambda s: re.sub('_(.)', lambda m: m.group(1).upper(), s)


class LouisRecentsRecordItem(BaseModel):
    music_id: int
    difficulty: str
    score: Decimal
    judge_status: str

    class Config:
        alias_generator = lambda s: re.sub('_(.)', lambda m: m.group(1).upper(), s)


class LouisBestsRecords(BaseModel):
    b30: List[LouisRecordItem]
    n20: List[LouisRecentsRecordItem]


class LouisBests(BaseModel):
    nickname: str
    records: LouisBestsRecords


class LouisScoreList(BaseModel):
    __root__: List[LouisRecordItem]


class LouisPlayer(BaseModel):
    nickname: str
    friend_code: str

    class Config:
        alias_generator = lambda s: re.sub('_(.)', lambda m: m.group(1).upper(), s)
