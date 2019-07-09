#!/usr/bin/env/ python3

import praw
from datetime import datetime
from time import sleep
import config
from investment import Investment, State
from portfolio import Portfolio

PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def print_portfolio(portfolio):
	print("\n\n")
	print(BLUE)
	print("MemeCoins:\t" + str(portfolio.balance))
	print("Base Investment: " + str(portfolio.invest_scale))
	nb_investment = len(portfolio.investments)
	print("Number of Investments:" + str(nb_investment))
	uptime = portfolio.balance_update
	print("Last balannce update: " + str(int((datetime.now() - uptime).total_seconds() / (60 * 60))) + " hours " + str(int((datetime.now() - uptime).total_seconds() / 60 % 60)) + " minutes " + str(int((datetime.now() - uptime).total_seconds()) % 60 % 60) + " seconds")
	if (nb_investment):
		for investment in portfolio.investments:
			print_investment(investment)

def print_investment(investment):
		# print("\thttps://reddit.com" + investment.submission.permalink)
		if investment.state == State.finished:
			return
		print(PURPLE)
		if investment.state == State.finded:
			print("https://reddit.com" + investment.bot_comment.permalink)
		else:
			print("https://reddit.com" + investment.invested_comment.permalink)
		print(str(investment.state))
		print("\tSubmission score: " + str(investment.submission.score) + " upvotes")
		uptime = datetime.fromtimestamp(investment.submission.created_utc)
		print("\tSubmission age:   " + str(int((datetime.now() - uptime).total_seconds() / (60 * 60))) + " hours " + str(int((datetime.now() - uptime).total_seconds() / 60 % 60)) + " minutes " + str(int((datetime.now() - uptime).total_seconds()) % 60 % 60) + " seconds")
		print(investment.submission.title)
		print(RESET)


def find_worth(submissions, my_investments, score = 0, age = 10):
	limit = 0
	print(YELLOW)
	print("\tSearching for:\t" + "at least      " + str(score) + " upvotes")
	print("\t\t\t"             + "and less than " + str(age)   + "   hours")
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
					mine_soon = Investment(submission)
					print_investment(mine_soon)
					investments.append(mine_soon)
	print(RESET)
	return investments

def find_investments(self):
	print(RESET)
	print("Worth of ALL HOT:")
	self.investments += find_worth(self.sub_all.hot(limit=1000), self.investments, 100, 7)
	print("Worth of M_E NEW SMALL:")
	self.investments += find_worth(self.sub_meme.new(limit=1000), self.investments, 7, 0.05)
	print("Worth of M_E NEW BIG:")
	self.investments += find_worth(self.sub_meme.new(limit=1000), self.investments, 30, 2)
	print("Worth of M_E HOT SMALL:")
	self.investments += find_worth(self.sub_meme.hot(limit=1000), self.investments, 30, 2)
	print("Worth of M_E HOT BIG:")
	self.investments += find_worth(self.sub_meme.hot(limit=1000), self.investments, 100, 7)
	print("Worth of M_E RIS SMALL:")
	self.investments += find_worth(self.sub_meme.rising(limit=1000), self.investments, 30, 2)
	print("Worth of M_E RIS BIG:")
	self.investments += find_worth(self.sub_meme.rising(limit=1000), self.investments, 100, 7)


	# loop_on = 1
	# while loop_on:
	# 	loop_on = 0
# for investment in portfolio.investments:
# 	if investment.state != State.validated:
# 		if investment.state != State.finished:
# 			loop_on = 1


def main():
	print(PURPLE)
	portfolio = Portfolio(config.reddit)
	print("Starting Invest are now:" + str(portfolio.invest_scale))
	while 1:
		print(BLUE)
		print("")
		print("New_loop:")
		if ((datetime.now() - portfolio.balance_update).total_seconds() / (60 * 60)) >= 4:
			print(GREEN)
			print("RESET BALANCE:")
			portfolio.refresh_balance()
			portfolio.invest_scale = int(portfolio.balance / 4) + 1
			print("Starting Invest are now:" + str(portfolio.invest_scale))
			portfolio.balance_update = datetime.now()
		print(BLUE)
		print("")
		print("Looking for investment...")
		print(YELLOW)
		find_investments(portfolio)
		for investement in portfolio.investments:
			investement.invest(portfolio, portfolio.invest_scale)
		print(RED)
		print("")
		print("Waiting for answer of MemeEconomy...")
		sleep(10)
		print(BLUE)
		print("Checking for answer of MemeEconomy...")
		print(RESET)
		for investement in portfolio.investments:
			if investement.check_investment(portfolio) < 0:
				portfolio.refresh_balance()
				portfolio.invest_scale = int(portfolio.balance / 4) + 1
				portfolio.balance_update = datetime.now()
				print("Starting Invest are now:" + str(portfolio.invest_scale))
		print("")
		print(RESET)
		print_portfolio(portfolio)
		print("")
		print(PURPLE)
		print("Uptime : script up since " + str(int((datetime.now() - portfolio.uptime).total_seconds() / (60 * 60))) + " hours " + str(int((datetime.now() - portfolio.uptime).total_seconds() / 60 % 60)) + " minutes " + str(int((datetime.now() - portfolio.uptime).total_seconds()) % 60 % 60) + " seconds")
		wait_duration = 5
		i = 0;
		while i < wait_duration:
			print("Waiting before next loop : " + str(i)  + "/" + str(wait_duration) + " minutes passed")
			sleep(60)
			i+=1



if __name__ == "__main__":
	main()
