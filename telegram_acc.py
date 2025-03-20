import asyncio, json
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

async def list_dialogs():
    await client.start(phone=PHONE)
    async for dialog in client.iter_dialogs():
        print(dialog.id, dialog.title)
    client.disconnect()

async def collect_messages():
    # Inicia o cliente (irá solicitar o código, se necessário)
    await client.start(phone=PHONE)
    # Substitua pelo nome de usuário, link de convite ou ID do grupo
    group_identifier = -4795461865  
    # Aguarda a obtenção da entidade do grupo
    group = await client.get_entity(group_identifier)
    
    # Itera sobre as mensagens do grupo
    async for message in client.iter_messages(group, limit=5):
        print(f"ID da Mensagem: {message.id}")
        print(f"Texto: {message.text}")
        if message.media:
            file_path = await client.download_media(message)
            print(f"✅ Mídia salva em: {file_path}")
        print("-" * 40)
    
    await client.disconnect()

# Executa a função assíncrona
asyncio.run(collect_messages())