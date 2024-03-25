from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    def __init__(self,admin_id: list[int]):
        self.admin_id = admin_id

    async def __call__(self, message:Message) -> bool:
        return message.from_user.id in self.admin_id