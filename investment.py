from enum import Enum
import config

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
