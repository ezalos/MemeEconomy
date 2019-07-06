from enum import Enum
import config
import praw
from praw.models import MoreComments

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
		for comment in portfolio.user.comments.new(limit=50):
			if comment.submission == self.submission:
				self.state = State.invested
				self.invested_comment = comment
				print("We found an already invested meme at https://reddit.com" + self.invested_comment.permalink)
				print(self.invested_comment.body)
				break
		if self.state == State.finded:
			self.submission.downvote()
			self.invested_comment = self.bot_comment.reply("!invest " + str(amount) +"%")
			self.state = State.invested
			print(str(amount) + "% invested in https://reddit.com" + self.invested_comment.permalink)
			portfolio.balance -= portfolio.blance * (amount / 100)

	def check_investment(self):
		if self.state == State.invested:
			self.invested_comment.refresh()
			for reply in self.invested_comment.replies:
				if reply.author == "MemeInvestor_bot":
					print("Reply of " + reply.submission.title)
					print(reply.body)
					self.submission.upvote()
					self.state = State.validated
					break
