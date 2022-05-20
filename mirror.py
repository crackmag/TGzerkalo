from telethon.sessions import StringSession
from telethon.sync import TelegramClient
import time

import database

from config import (API_HASH, API_ID, SESSION_STRING,
                    CHANNELS_MAPPING, SOURCE_CHANNELS)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler_new_message(event):
    try:
        mirror_channel = CHANNELS_MAPPING.get(event.chat_id)
        if mirror_channel is None and len(mirror_channel) < 1:
            return
        sent = 0
        for c in mirror_channel:
            mirror_message_id = await client.send_message(c, event.message)
            database.insert({
                'mirror_message_id': mirror_message_id,
                'message_id': event.message.id,
                'mirror_channel_id': c,
                'channel_id': event.chat_id
            })
            sent += 1
            if sent > 50:
                sent = 0
                time.sleep(1)
    except Exception as e:
        print(e)

# Обработчик отредактированных сообщений
@client.on(events.MessageEdited(chats=SOURCE_CHANNELS))
async def handler_edit_message(event):
    try:
        messages_to_edit = database.find_by_id(event.message.id, event.chat_id)
        if messages_to_edit is not None and len(messages_to_edit) < 1:
            return
        sent = 0
        for message in messages_to_edit:
            await client.edit_message(message['mirror_channel_id'], message['mirror_message_id'], event.message.message)
            sent += 1
            if sent > 50:
                sent = 0
                time.sleep(1)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
