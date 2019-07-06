from investment import Investment
import praw
from time import sleep
from datetime import datetime

class Portfolio:
    def __init__(self, auth_config):
        self.reddit = praw.Reddit(**auth_config)
        self.refresh_balance()
        self.sub_all = self.reddit.subreddit('All')
        self.sub_meme = self.reddit.subreddit('MemeEconomy')
        self.investments = []
        self.find_investments()

    def refresh_balance(self):
        post = None
        for submission in self.reddit.subreddit('MemeEconomy').hot(limit=1):
            post = Investment.find_bot_comment(submission).reply("!balance")
            break
        while len(post.replies) == 0:
            sleep(10)
            post.refresh()
            #TODO
        for reply in post.replies:
            self.balance = int(reply.body[38:-13].replace(',', ''))
            break
        print("New balance: " + str(self.balance))

    def find_worth(submissions, score = 0, age = 10):
        investments = []
        for submission in submissions:
            sub_age = (datetime.now() - datetime.fromtimestamp(submission.created_utc)).total_seconds() / (60 * 60);
            if submission.subreddit == "MemeEconomy" and sub_age <= age and submission.score >= score:
                investments.append(Investment(submission))
        return investments


    def find_investments(self):
        self.investments += Portfolio.find_worth(self.sub_all.hot(limit=1000), 100, 3)
        self.investments += Portfolio.find_worth(self.sub_meme.new(limit=1000), 30, 0.3)
