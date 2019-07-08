from investment import Investment
import config
import praw
from time import sleep
from datetime import datetime

PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class Portfolio:
	def __init__(self, auth_config):
		self.uptime = datetime.now()
		print("Asking for Reddit OAuth...")
		self.reddit = praw.Reddit(**auth_config)
		self.user = self.reddit.redditor(config.reddit["username"])
		self.sub_all = self.reddit.subreddit('All')
		self.sub_meme = self.reddit.subreddit('MemeEconomy')
		self.investments = []
		print("Done")
		self.balance = 0
		self.refresh_balance()
		self.balance_update = datetime.now()
		self.invest_scale = int(self.balance / 4) + 1

	def refresh_balance(self):
		post = None
		GREEN = '\033[92m'
		print(GREEN)
		print("RESET BALANCE:")
		print("Checking last sent orders...")
		print(BLUE)
		for comment in self.user.comments.new(limit=50):
			if comment.body.find("!invest") >= 0:
				break;
			if comment.body.find("!balance") >= 0:
				if len(comment.replies) == 0:
					print("Cant access last orders...")
				for reply in comment.replies:
					print(comment.body)
					if comment.body.find("account balance") >= 0:
						self.balance = int(comment.body[38:-13].replace(',', ''))
						break
		if self.balance == 0:
			print(RED)
			print("Asking for balance...")
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
		print(GREEN)
		print("New balance: " + str(self.balance))
