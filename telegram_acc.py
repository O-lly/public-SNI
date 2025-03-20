import asyncio, json, os
from telethon import TelegramClient

# Credenciais do Telegram
CREDENTIALS_PATH="credentials/telegram_acc.json"
with open(CREDENTIALS_PATH, "r") as credentials_file:
    credentials=json.load(credentials_file)

API_ID=credentials["api_id"]
API_HASH=credentials["api_hash"]
SESSION_NAME=credentials["session_name"]
PHONE=credentials["phone"]

# Cria o cliente do Telegram
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Arquivo para armazenar media
MEDIA_PATH="media/telegram"
os.makedirs(MEDIA_PATH, exist_ok=True)

# Armazena id de posts já visualizados
CHECKED_POSTS_PATH="telegram_checked_posts.txt"
if not os.path.exists(CHECKED_POSTS_PATH):
    open(CHECKED_POSTS_PATH, "w").close()

async def start_session():
    if not client.is_connected():
        await client.start(phone=PHONE)
        print("✅ Sessão do Telegram iniciada!")

async def end_session():
    if client.is_connected():
        await client.disconnect()
        print("❌ Sessão do Telegram finalizada.")

async def list_dialogs():
    await start_session()
    async for dialog in client.iter_dialogs():
        print(dialog.id, dialog.title)
    await end_session()

async def collect_messages(chat_identifier, limit=1):
    await start_session()
    # Obtém a entidade do grupo
    chat = await client.get_entity(chat_identifier)
    
    # Itera sobre as mensagens do grupo
    async for message in client.iter_messages(chat, limit):
        print(f"ID da Mensagem: {message.id}")
        print(f"Texto: {message.text}")

        if message.media:
            file_path = await client.download_media(message, file=f"{MEDIA_PATH}/{message.id}/")
            print(f"✅ Mídia salva em: {file_path}")
        print("-" * 40)
    
    await end_session()

async def send_message(chat_identifier, message_text="", media_gallery=[]):
    await start_session()
    await client.send_message(chat_identifier, message_text)
    print("✅ Mensagem enviada com sucesso!")
    await end_session()

async def collect_new_posts(chat_identifier, limit=1):
    await start_session()
    # Obtém a entidade do grupo
    chat = await client.get_entity(chat_identifier)

    with open(CHECKED_POSTS_PATH, "r") as checked_posts_file:
        checked_posts=checked_posts_file.read().splitlines()

    # Itera sobre as mensagens do grupo
    async for message in client.iter_messages(chat, limit):
        if str(message.id) in checked_posts:
            continue
        print(f"ID da Mensagem: {message.id}")
        print(f"Texto: {message.text}")

        if message.media:
            file_path = await client.download_media(message, file=f"{MEDIA_PATH}/{message.id}")
            print(f"✅ Mídia salva em: {file_path}")
        print("-" * 40)

    with open(CHECKED_POSTS_PATH, "a") as checked_posts_file:
        checked_posts_file.write(f"{message.id}\n")
    
    await end_session()

asyncio.run(collect_new_posts(-4795461865))