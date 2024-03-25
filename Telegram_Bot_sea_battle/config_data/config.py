from environs import Env
from dataclasses import dataclass


@dataclass
class Tg_bot:
    token: str
    admin_ids: int

@dataclass
class Config:
    tg_bot: Tg_bot

def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(tg_bot=Tg_bot(token=env('BOT_TOKEN'),admin_ids=env('admin_id')))
