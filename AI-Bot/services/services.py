import io
from pathlib import Path

import whisper
from pydub import AudioSegment
import openai
from openai import OpenAI
from config_data.config import Config

class AI_transformation_text:
    @classmethod
    def get_text_from_voice(cls,voice_file):
        audio = AudioSegment.from_file(voice_file, format="ogg")
        mp3_file_path = f"exampl.mp3"
        audio.export(mp3_file_path, format="mp3")
        model = whisper.load_model("base")
        result = model.transcribe('exampl.mp3', fp16=False)
        print(result["text"])
        return result["text"]

    @classmethod
    def get_answer_for_question(cls,voice_file):
        openai.api_key = Config.OpenAIToken
        # openai.base_url = "https://..."
        # openai.default_headers = {"x-foo": "true"}
        text = cls.get_text_from_voice(voice_file)
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"{text}",
                },
            ],
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    @classmethod
    def voice_answer(cls,voice_file):
        text_answer_for_voice = cls.get_answer_for_question(voice_file)
        client = OpenAI(api_key=Config.OpenAIToken)
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=f"{text_answer_for_voice}"
        )
        response.stream_to_file(speech_file_path)
        with open('speech.mp3', "rb") as speech_file:
            voice_message = io.BytesIO(speech_file.read())
        return voice_message