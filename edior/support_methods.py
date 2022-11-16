import logging
import wikipedia

from demotivator import Demotivator

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message, File

from db_ops import *



# logging.basicConfig(level=logging.DEBUG)


def get_wiki_note(request: str):
    try:
        wikipedia.set_lang("ru")
        # notes = wikipedia.search(request)

        pg = wikipedia.page(request)
        return "\n".join([pg.title, "\n", pg.url, "\n", pg.content[0:2000] + "..."])
    except Exception as e:
        return f"Что-то пошло не так. Возможно нет статьи с таким названием не сущесвтует. Можете отрпавить баг-репорт, вот текст ошибки: \n {e}."


async def switch_types(message, file_id, type: str, phrase):

    new_bind = add_new_bind(
        chat_id=message.chat.id,
        type=type,
        phrase=phrase,
        answer=file_id)
    await message.reply(new_bind)

async def make_demotivator(path, text):
    if "|" in text:
        elements = text.split("|")
        Demotivator(path, elements[0], elements[1])
    else: Demotivator(path, text)