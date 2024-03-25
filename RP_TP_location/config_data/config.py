from environs import Env
from dataclasses import dataclass

@dataclass
class TgBot:
    token: str
    admin_id: list[int]

@dataclass
class Config:
    tg_bot: TgBot



def load_config(path: str | None = None):
    env =Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),admin_id=list(map(int,env.list('ADMIN_ID')))))
