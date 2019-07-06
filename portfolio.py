from investment import Investment

class Portfolio:
    investments = []

    def __init__(self, auth_config):
        self.reddit = praw.Reddit(**auth_config)
        refresh_balance(self)
        self.sub_all = reddit.subreddit('All')
        self.sub_meme = reddit.subreddit('MemeEconomy')

    def updates_investments(self, new_investments):
        self.investments += new_investments

    def refresh_balance(self):
        post = Investment.find_bot_comment(self.reddit.subreddit('MemeEconomy').hot(limit=1)[0]).reply("!balance")
        while len(post.comments) == 0:
            sleep(10)
            post.refresh()
            #TODO
        self.balance = int(post.comments[0][34:-10])

    def find_investments(self):
        investments += is_worth(self.sub_all.hot(limit=1000), 100, 3)
        investments += is_worth(self.sub_meme.new(limit=1000), 30, 0.3)
