from enum import Enum
import config
import praw

class State(Enum):
    finded = 0
    invested = 1
    validated = 2
    finished = 3

class Investment:
    def __init__(self, submission):
        self.id = submission.id
        self.submission = submission
        self.bot_comment = find_bot_comment(submission)
        self.invested_comment = find_invested_comment(self.bot_comment)
        if self.invested_comment:
            self.state = len(self.invested_comment.comments) + 1  #TODO
        else:
            self.state = State.finded

    def find_bot_comment(submission):
        for comment in submission.comments:
            if comment.author == "MemeInvestor_Bot":
                return comment

    def find_invested_comment(bot_comment):
        for comment in bot_comment.comments:
            if comment.author == config.reddit["username"]:
                return comment

    def invest(self, amount):
        self.submission.downvote()
        self.invested_comment = self.bot_comment.reply("!invest " + str(amount))
        self.state = State.invested
        print(str(amount) + " invested in https://reddit.com" + self.invested_comment.permalink)

    def check_investment(self):
        self.invested_comment.refresh()
        for reply in self.invested_comment.replies:
            if reply.author == "MemeInvestor_Bot":
                print("Reply of " + comment.submission.title)
                self.submission.upvote()
                self.state = State.validated
                break
