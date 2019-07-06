#!/usr/bin/env python3

import praw
from datetime import datetime
from time import sleep
import config
from investment import Investment, State
from portfolio import Portfolio

def background_check():
	while len(my_investments) != 0:
		sleep(2 * 60)
		print("I have " + str(len(my_investments)) + " comments")
		for comment in my_investments[:]:
			post_invests(comment)
			my_investments.remove(comment)

def print_portfolio(portfolio):
	print("\n\n")
	print("MemeCoins:" + str(portfolio.balance))
	nb_investment = len(portfolio.investments)
	print("Number of Investment :" + str(nb_investment))
	if (nb_investment):
		for investment in portfolio.investments:
			print_investment(investment)

def print_investment(investment):
		# print("\thttps://reddit.com" + investment.submission.permalink)
		print("\thttps://reddit.com" + investment.bot_comment.permalink)
		print("\t" + str(investment.state))
		print("\t\tSubmission score: " + str(investment.submission.score))
		print("\t\tSubmission age:   " + str((datetime.now() - datetime.fromtimestamp(investment.submission.created_utc)).total_seconds() / (60 * 60)) + " hours")
		print("\n")

def main():
	portfolio = Portfolio(config.reddit)
	print_portfolio(portfolio)
	loop_on = 1
	while loop_on:
		loop_on = 0
		for investement in portfolio.investments:
			investement.invest(portfolio, 10)
		sleep(20)
		for investement in portfolio.investments:
			investement.check_investment()
		portfolio.find_investments()
		for investment in portfolio.investments:
			if investment.state != State.validated:
				if investment.state != State.finished:
					loop_on = 1
		print_portfolio(portfolio)


if __name__ == "__main__":
	main()
