import pydantic
async def delete_messages(bot,lists:list,chat_id:int):
    for message_id in lists:
        await bot.delete_message(chat_id=chat_id,message_id=message_id)
