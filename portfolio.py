from investment import Investment
import config
import praw
from time import sleep
from datetime import datetime

class Portfolio:
	def __init__(self, auth_config):
		self.reddit = praw.Reddit(**auth_config)
		self.balance = 10000
		self.user = self.reddit.redditor(config.reddit["username"])
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

	def find_worth(submissions, my_investments, score = 0, age = 10):
		print("\tSearching for: ")
		print("\t\t       " + "at least " + str(score) + " upvotes")
		print("\t\t       " + "and less " + str(age) + " hours")
		investments = []
		for submission in submissions:
			sub_age = (datetime.now() - datetime.fromtimestamp(submission.created_utc)).total_seconds() / (60 * 60);
			if submission.subreddit == "MemeEconomy":
				if sub_age <= age and submission.score >= score:
					no_double = 1
					for investment in my_investments:
						if (investment.submission.permalink == submission.permalink):
							no_double = 0
					if no_double:
						print("https://reddit.com" + submission.permalink)
						print("\tWith score of: " + str(submission.score))
						print("\tAnd age of: " + str(sub_age) + " hours")
						investments.append(Investment(submission))
		return investments


	def find_investments(self):
		print("Worth of ALL HOT:")
		self.investments += Portfolio.find_worth(self.sub_all.hot(limit=1000), self.investments, 100, 7)
		print("Worth of M_E NEW SMALL:")
		self.investments += Portfolio.find_worth(self.sub_meme.new(limit=1000), self.investments, 7, 0.1)
		print("Worth of M_E NEW BIG:")
		self.investments += Portfolio.find_worth(self.sub_meme.new(limit=1000), self.investments, 30, 2)
		print("Worth of M_E HOT SMALL:")
		self.investments += Portfolio.find_worth(self.sub_meme.hot(limit=1000), self.investments, 30, 2)
		print("Worth of M_E HOT BIG:")
		self.investments += Portfolio.find_worth(self.sub_meme.hot(limit=1000), self.investments, 100, 7)
		print("Worth of M_E RIS SMALL:")
		self.investments += Portfolio.find_worth(self.sub_meme.rising(limit=1000), self.investments, 30, 2)
		print("Worth of M_E RIS BIG:")
		self.investments += Portfolio.find_worth(self.sub_meme.rising(limit=1000), self.investments, 100, 7)
