#!/bin/env python3

import praw
from datetime import datetime
from time import sleep
from config import config

my_comments = []

def invest(submission, investement):
    for comment in submission.comments:
        if comment.author == "MemeInvestor_Bot":
            my_reply = comment.reply("!invest " + str(investement))
            print(my_reply.permalink)
            my_comments.append((my_reply, submission))
            break

def main():
    reddit = praw.Reddit(**config)

    sub_all = reddit.subreddit('All')
    sub_meme = reddit.subreddit('MemeEconomy')

    for submission in sub_all.hot(limit=1000):
        if submission.subreddit == "MemeEconomy":
            hour = (datetime.now() - datetime.fromtimestamp(submission.created_utc)).total_seconds() / (60 * 60);
            print(submission.title, submission.permalink, submission.score, hour)
            submission.downvote()
            invest(submission, 1)

    while len(my_comments) != 0:
        sleep(20)
        print("I have " + str(len(my_comments)) + " comments")
        for comment, submission in my_comments[:]:
            comment.refresh()
            for replie in comment.replies:
                if comment.author == "MemeInvestor_Bot":
                    submission.upvote()
                    my_comments.remove((comment, submission))
                    break


if __name__ == "__main__":
    main()
