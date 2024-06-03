import os

from pydantic_settings import BaseSettings
from environs import load_dotenv

load_dotenv()

class BotSettings(BaseSettings):
    TelegramApiToken: str
    OpenAIToken:str

class Config:
    bot_token = os.environ.get('BOT_TOKEN')
    openai_token = os.environ.get('OPENAITOKEN')
    settings = BotSettings(TelegramApiToken=bot_token,OpenAIToken=openai_token)
    APIToken = settings.TelegramApiToken
    OpenAIToken = settings.OpenAIToken


