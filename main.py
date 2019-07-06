#!/usr/bin/env python3

import praw
from datetime import datetime
from time import sleep
import config


my_investments = []


def pre_invest(submission, investment):
    for comment in comment.submission.comments:
        if comment.author == "MemeInvestor_Bot":
            comment.submission.downvote()
            my_reply = comment.reply("!invest " + str(investment))
            print("https://reddit.com" + my_reply.permalink)
            my_investments.append(my_reply)
            break


def post_invest(comment):
    comment.refresh()
    for reply in comment.replies:
        if reply.author == "MemeInvestor_Bot":
            print("Reply of " + comment.submission.title)
            comment.submission.upvote()
            break


def invest_in_sub(submissions, score = 0, age = 10):
    for submission in submissions:
        sub_age = (datetime.now() - datetime.fromtimestamp(submission.created_utc)).total_seconds() / (60 * 60);
        if submission.subreddit == "MemeEconomy" and sub_age <= age and submission.score >= score:
            print(submission.title, "https://reddit.com" + submission.permalink, submission.score, sub_age)
            pre_invest(submission, config.investment)

def background_check():
    while len(my_investments) != 0:
        sleep(2 * 60)
        print("I have " + str(len(my_investments)) + " comments")
        for comment in my_investments[:]:
            post_invests(comment)
            my_investments.remove(comment)

def main():
    reddit = praw.Reddit(**config.reddit)

    sub_all = reddit.subreddit('All')
    sub_meme = reddit.subreddit('MemeEconomy')

    invest_in_sub(sub_all.hot(limit=1000), 100, 3)
    invest_in_sub(sub_meme.new(limit=1000), 30, 0.3)
    print("End of prospecting")
    background_check()


if __name__ == "__main__":
    main()
