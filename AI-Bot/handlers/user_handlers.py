from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
import whisper
from pydub import AudioSegment

from services.services import AI_transformation_text

router: Router = Router()

@router.message()
async def command_start(message:Message,
                        bot:Bot):
    # model = whisper.load_model("base")
    voice = message.voice
    file = await bot.get_file(voice.file_id)
    voice_file = await bot.download_file(file.file_path)
    res_voice = AI_transformation_text.voice_answer(voice_file=voice_file)
    await message.answer_voice(res_voice)

