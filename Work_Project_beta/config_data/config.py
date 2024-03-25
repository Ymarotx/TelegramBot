from environs import Env
from dataclasses import dataclass

@dataclass
class Tg_Bot:
    token : str
    admin_id: list[int]

@dataclass
class Config:
    tg_bot: Tg_Bot

def load_config(path: str | None=None):
    env = Env()
    env.read_env(path)
    return Config(tg_bot=Tg_Bot(token=env('BOT_TOKEN'),admin_id=list(map(int,env.list('ADMIN_ID')))))