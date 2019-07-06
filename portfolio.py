from investment import Investment

class Portfolio:
    def __init__(self, auth_config):
        self.reddit = praw.Reddit(**auth_config)
        self.refresh_balance()
        self.sub_all = reddit.subreddit('All')
        self.sub_meme = reddit.subreddit('MemeEconomy')
        self.investments = []
        self.find_investments()

    def refresh_balance(self):
        post = Investment.find_bot_comment(self.reddit.subreddit('MemeEconomy').hot(limit=1)[0]).reply("!balance")
        while len(post.comments) == 0:
            sleep(10)
            post.refresh()
            #TODO
        self.balance = int(post.comments[0][34:-10])

    def find_worth(submissions, score = 0, age = 10):
        investments = []
        for submission in submissions:
            sub_age = (datetime.now() - datetime.fromtimestamp(submission.created_utc)).total_seconds() / (60 * 60);
            if submission.subreddit == "MemeEconomy" and sub_age <= age and submission.score >= score:
                investments.append(Investment(submission))
        return investments


    def find_investments(self):
        self.investments += find_worth(self.sub_all.hot(limit=1000), 100, 3)
        self.investments += find_worth(self.sub_meme.new(limit=1000), 30, 0.3)
