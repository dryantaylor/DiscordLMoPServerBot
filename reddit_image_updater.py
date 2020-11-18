import time
import praw
from cogs.redditCommands.code import load_reddit_API_info,subs,perSubPictureTotal

def update_pictures():
    while True:
        for subreddit,destination in subs:
            client_id, client_secret, user_agent = load_reddit_API_info()
            reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
            pictures = []
            x = 0
            for subbmission in reddit.subreddit(subreddit).hot(limit=1000):
                if subbmission.url.split(".")[-1] in ["png", "jpg", "jpeg"]:
                    pictures.append(subbmission.url)
                    x += 1
                if x == perSubPictureTotal:
                    break

                with open(f"./cogs/redditCommands/{destination}", "w") as file:
                    string = ""
                    for url in pictures:
                        string += f"{url}\n"
                    file.write(string)

                #  24hours = 86400 seconds
        time.sleep(86400)