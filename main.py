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


def main():
    portfolio = Portfolio(config.reddit)


if __name__ == "__main__":
    main()
