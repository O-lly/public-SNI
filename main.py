import reddit, twitter, mail, schedule, time, os, telegram_acc, asyncio 

RUNNING=True

TWITTER_POSTS_FILE=twitter.CHECKED_POSTS_PATH
REDDIT_POSTS_FILE=reddit.CHECKED_POSTS_PATH
TELEGRAM_POSTS_FILE=telegram_acc.CHECKED_POSTS_PATH

REDDIT_TELEGRAM=False
REDDIT_TWITTER=False
TWITTER_TELEGRAM=False
TELEGRAM_TWITTER=False


async def monitor_twitter_telegram():
    return

async def monitor_telegram_twitter():
    return

async def monitor_reddit_twitter(limit=3):
    with open(TWITTER_POSTS_FILE, "r") as twitter_posts_file:
        twitter_post_list=twitter_posts_file.read().splitlines()

    posts=reddit.check_posts(limit)
    # Se houver posts novos no reddit, deve executar o passo do Twitter
    for post in posts:
        if post["id"] not in twitter_post_list:
            time.sleep(1)
            twitter.send_post(post)
            with open(TWITTER_POSTS_FILE, "a") as twitter_posts_file:
                twitter_posts_file.write(f"{post['id']}\n")
    return

async def monitor_reddit_telegram():
    return

async def menu():
    global REDDIT_TELEGRAM, REDDIT_TWITTER, TWITTER_TELEGRAM, TELEGRAM_TWITTER
    print("Opções\n",
          "\t1. Ativar monitoramento Reddit-Telegram\n",
          "\t2. Ativar monitoramento Reddit-Twitter\n",
          "\t3. Ativar monitoramento Twitter-Telegram\n",
          "\t4. Ativar monitoramento Telegram-Twitter\n")
    
    op = int(input("Opção: "))

    match op:
        case 1:
            print("Ativando monitoramento Reddit-Telegram")
            REDDIT_TELEGRAM=True
        case 2:
            print("Ativando monitoramento Reddit-Twitter")
            REDDIT_TWITTER=True
        case 3:
            print("Ativando monitoramento Twitter-Telegram")
            TWITTER_TELEGRAM=True
        case 4:
            print("Ativando monitoramento Telegram-Twitter")
            TELEGRAM_TWITTER=True
        case _:
            print("Opção inválida. Encerrando programa.")
            exit()
            

async def run():
    if REDDIT_TELEGRAM: await monitor_reddit_telegram()
    if REDDIT_TWITTER: await monitor_reddit_twitter()
    if TWITTER_TELEGRAM: await monitor_twitter_telegram()
    if TELEGRAM_TWITTER: await monitor_telegram_twitter()

async def schedule_tasks():
    tempo = 0
    while RUNNING:
        tempo += 1
        schedule.run_pending()
        await asyncio.sleep(1)
        if tempo % 10 == 0:
            print(f"Tempo: {tempo} segundos.")
        if tempo == 200:
            break

async def main():
    await menu()
    # Agenda a execução da função run
    schedule.every(1).minutes.do(lambda: asyncio.create_task(run()))
    await schedule_tasks()  

if __name__ == "__main__":
    asyncio.run(main())  # ✅ Chama `asyncio.run()` apenas aqui