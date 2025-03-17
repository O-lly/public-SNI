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
    attachment=[]

    # Lista todos os arquivos no diretório
    media_files = os.listdir(MEDIA_PATH)

    for file_name in media_files:
        if id in file_name:
            attachment.append(file_name)
    
    for file in attachment:
        media = api_v1.media_upload(file)
    
    # Postar tweet com mídia usando API v2
    tweet_text = title
    response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    print("✅ Tweet postado:", response.data)