from aiogram.filters import BaseFilter
from aiogram.types import Message
import re

class EntryName(BaseFilter):
    pattern = re.compile(r'.+?;\D+?;\d+')
    async def __call__(self, message:Message):
        return self.pattern.match(message.text)

