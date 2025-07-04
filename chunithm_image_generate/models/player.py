from dataclasses import dataclass
from .api_models import louis, lxns
import unicodedata


@dataclass
class Player:
    nickname: str
    friend_code: str

    @classmethod
    def from_louis(cls, data: dict) -> "Player":
        model: louis.LouisPlayer = louis.LouisPlayer.parse_obj(data)
        return cls(nickname=unicodedata.normalize('NFKC', model.nickname), friend_code=model.friend_code)

    @classmethod
    def from_lxns(cls, data: dict) -> "Player":
        model: lxns.LxnsPlayer = lxns.LxnsPlayer.parse_obj(data)
        return cls(nickname=unicodedata.normalize('NFKC', model.name), friend_code=str(model.friend_code))
