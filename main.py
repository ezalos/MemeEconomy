#!/usr/bin/env python3

import praw
from datetime import datetime
from time import sleep
import config
from investment import Investment, State

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

def find_worth(submissions, score = 0, age = 10):
    investments = []
    for submission in submissions:
        sub_age = (datetime.now() - datetime.fromtimestamp(submission.created_utc)).total_seconds() / (60 * 60);
        if submission.subreddit == "MemeEconomy" and sub_age <= age and submission.score >= score:
            investments.append(Investment(submission))
    return investments

def background_check():
    while len(my_investments) != 0:
        sleep(2 * 60)
        print("I have " + str(len(my_investments)) + " comments")
        for comment in my_investments[:]:
            post_invests(comment)
            my_investments.remove(comment)

def find_investments(reddit):
    sub_all = reddit.subreddit('All')
    sub_meme = reddit.subreddit('MemeEconomy')
    investments = []
    investments += is_worth(sub_all.hot(limit=1000), 100, 3)
    investments += is_worth(sub_meme.new(limit=1000), 30, 0.3)
    return investments

def main():
    reddit = praw.Reddit(**config.reddit)

    investments = find_investments(reddit)

    # invest_in_sub(sub_all.hot(limit=1000), 100, 3)
    # invest_in_sub(sub_meme.new(limit=1000), 30, 0.3)
    print("End of prospecting")
    background_check(investments)


if __name__ == "__main__":
    main()
