from enum import Enum
import config
import praw
from praw.models import MoreComments

PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class State(Enum):
	finded = 0
	invested = 1
	validated = 2
	finished = 3

class Investment:
	def __init__(self, submission):
		self.id = submission.id
		self.submission = submission
		self.bot_comment = Investment.find_bot_comment(submission)
		self.invested_comment = Investment.find_invested_comment(self.bot_comment)
		if self.invested_comment:
			self.state = len(self.invested_comment.comments) + 1  #TODO
		else:
			self.state = State.finded

	def find_bot_comment(submission):
		for comment in submission.comments:
			if comment.author == "MemeInvestor_bot":
				return comment

	def find_invested_comment(bot_comment):
		comment_forest = bot_comment.replies.replace_more(limit=0)
		for comment in comment_forest:
			if isinstance(comment, MoreComments):
				continue
			if comment.author == config.reddit["username"]:
				return comment

	def invest(self, portfolio, amount):
		if self.state == State.finded:
			for comment in portfolio.user.comments.new(limit=50):
				if comment.body.find("!invest") >= 0:
					if comment.submission == self.submission:
						self.state = State.invested
						self.invested_comment = comment
						break
		if self.state == State.finded:
			self.submission.downvote()
			if portfolio.balance / 100 < amount and portfolio.balance > amount:
				self.invested_comment = self.bot_comment.reply("!invest " + str(int(amount)))
				portfolio.balance -= int(amount)
			elif portfolio.balance * (10 / 100) > 100:
				self.invested_comment = self.bot_comment.reply("!invest 10%")
				portfolio.balance -= int(portfolio.balance * (10 / 100))
			elif portfolio.balance * (1 / 100) > 100:
				self.invested_comment = self.bot_comment.reply("!invest 1%")
				portfolio.balance -= int(portfolio.balance * (1 / 100))
			else:
				self.invested_comment = self.bot_comment.reply("!invest 100")
				portfolio.balance -= 100
			self.state = State.invested
			print(GREEN)
			print("\t" + str(amount) + " ivested at https://reddit.com" + self.invested_comment.permalink)

	def check_investment(self, portfolio):
		a = 0
		if self.state == State.invested or self.state == State.validated:
			self.invested_comment.refresh()
			for reply in self.invested_comment.replies:
				if reply.author == "MemeInvestor_bot":
					if reply.body.find("minimum") >= 0:
						self.state = State.finded
						a = -1
						print(RED)
						print("https://reddit.com" + self.invested_comment.permalink)
						print(reply.body)
						print(RESET)
						#TODO
					elif reply.body.find("UPDATE") >= 0:
						if self.state == State.validated:
							print(GREEN)
							print("https://reddit.com" + self.invested_comment.permalink)
							print(reply.body)
							print(RESET)
							portfolio.balance = int(comment.body[reply.body.find("Your new balance is **"):reply.body.find(" MemeCoins**.")].replace(',', ''))
							portfolio.balance_update = datetime.now()
						self.state = State.finished
						#TODO
					else:
						self.submission.upvote()
						self.state = State.validated
					return a
		return 0
