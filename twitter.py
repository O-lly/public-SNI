import tweepy, json, os

MEDIA_PATH="reddit_media"

# Credenciais do Twitter/X
CREDENTIALS_PATH="credentials/twitter_credentials.json"
with open(CREDENTIALS_PATH, "r") as credentials_file:
    credentials=json.load(credentials_file)

API_KEY=credentials["api_key"]
API_SECRET=credentials["api_secret"]
CLIENT_ID=credentials["client_id"]
CLIENT_SECRET=credentials["client_secret"]
ACCESS_TOKEN=credentials["access_token"]
ACCESS_TOKEN_SECRET=credentials["access_token_secret"]

# Autenticação para API v1.1
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api_v1 = tweepy.API(auth)

# Autenticação para a API v2
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def send_post(post):
    id = post["id"]
    author = post["author"]
    title = post["title"]
    content = post["content"]
    attachments=[]
    
    media_ids=[]
    media_chunks=[]

    # Lista todos os arquivos no diretório
    media_files = os.listdir(MEDIA_PATH)

    for file_name in media_files:
        if id in file_name:
            attachments.append(file_name)
    
    if attachments: # Verifica se attachments não está vazia
        # Divide os arquivos em grupos de 4 (limite do Twitter)
        media_chunks = [attachments[i:i+4] for i in range(0, len(attachments), 4)]

        # Enviar o primeiro chunck no principal
        if media_chunks and len(media_chunks) > 0:
            for file in media_chunks[0]:
                media = api_v1.media_upload(f"{MEDIA_PATH}/{file}")
                media_ids.append(media.media_id)
        else:
            print("Nenhum chunk de mídia encontrado")
    else:
        print("Nenhum anexo encontrado, pulando upload de mídia")

    # Postar tweet com mídia usando API v2
    tweet_text = title

    if media_ids:  # Se houver pelo menos um media_id
        response = client.create_tweet(text=tweet_text, media_ids=media_ids)
    else:
        response = client.create_tweet(text=tweet_text)

    main_tweet_id = response.data["id"]
    print("✅ Tweet principal postado:", response.data)

    # Postar tweets de resposta com os chuncks adicionais
    if len(media_chunks) > 1:
        for chunk_index, chunk in enumerate(media_chunks[1:], start=1):
            for file in chunk:
                media = api_v1.media_upload(f"{MEDIA_PATH}/{file}")
                media_ids.append(media.media_id)
            
            # Texto opcional nos tweets de resposta
            reply_text = ""

            # Criar o tweet como uma resposta ao principal
            response = client.create_tweet(
                text=reply_text,
                media_ids=media_ids,
                in_reply_to_tweet_id=main_tweet_id
            )

            print(f"✅ Resposta postada (parte {chunk_index}):", response.data)

    print("✅ Tweet postado:", response.data)