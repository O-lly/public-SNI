import tweepy, json, os

REDDIT_MEDIA_PATH="media/reddit"

HISTORY_PATH="history/twitter"
os.makedirs(HISTORY_PATH, exist_ok=True)

CHECKED_POSTS_PATH=f"{HISTORY_PATH}/twitter_checked_posts.txt"
if not os.path.exists(CHECKED_POSTS_PATH):
    open(CHECKED_POSTS_PATH, "w").close()

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

def send_post(content="", media_gallery=[]):
    media_ids = []
    media_chunks = []

    # Verifica se há mídia e divide em grupos de até 4 (limite do Twitter)
    if media_gallery:
        media_chunks = [media_gallery[i:i+4] for i in range(0, len(media_gallery), 4)]

    # Enviar o primeiro grupo de mídia com o tweet principal
    if media_chunks:
        for media_path in media_chunks[0]:
            media = api_v1.media_upload(media_path)
            media_ids.append(media.media_id)

    # Posta o tweet principal
    if media_ids:
        response = client.create_tweet(text=content, media_ids=media_ids)
    else:
        response = client.create_tweet(text=content)

    print("✅ Tweet principal postado:", response.data)
    main_tweet_id = response.data["id"]

    # Postar tweets de resposta com os grupos de mídia adicionais (se houver)
    if len(media_chunks) > 1:
        for chunk_index, chunk in enumerate(media_chunks[1:], start=1):
            media_ids = []  # Resetar lista de media_ids para cada resposta
            for media_path in chunk:
                media = api_v1.media_upload(media_path)
                media_ids.append(media.media_id)
            
            response = client.create_tweet(
                text="",  # Deixa em branco para não repetir conteúdo
                media_ids=media_ids,
                in_reply_to_tweet_id=main_tweet_id
            )

            print(f"✅ Resposta postada (parte {chunk_index}):", response.data)
            main_tweet_id = response.data["id"]  # Atualiza ID para o próximo reply

    return response.data