__author__ = 'Maria Gabriela Valdes'
__author__ = 'Jose Riera'

import os


def cleaning():
    base_path = '/Users/gaby/Documents/MIRI/3rd_Semester/IR/miri-ir2015/lab5/'

    for tf in os.listdir('../tweets/'):
        if tf != '.DS_Store':
            tweet_file = open(base_path + 'tweets/' + tf)
            clean_tweet_content = " ".join(filter(lambda x : not x.startswith("http"), tweet_file.read().split()))
            # clean_tweet_content = tweet_file.read().replace("http.*?", "")
            # re.sub('http.*?', '', tweet_file.read())

            if clean_tweet_content:
                clean_tweet_file = open(base_path + 'clean_tweets/' + tf, 'w')
                clean_tweet_file.write(clean_tweet_content)


def non_repeated_tweets():
    base_path = '/Users/gaby/Documents/MIRI/3rd_Semester/IR/miri-ir2015/lab5/'
    tweet_list = []

    for tf in os.listdir('../clean_tweets/'):
        if tf != '.DS_Store':
            tweet_file = open(base_path + 'clean_tweets/' + tf)
            tweet_list.append(tweet_file.read())

    non_repeated_tweet_list = set(tweet_list)
    non_repeated_tweet_index = 0

    for tweet in non_repeated_tweet_list:
        non_repeated_tweet_file = open(base_path + 'non_repeated_tweets/tweet' + str(non_repeated_tweet_index) + ".txt", 'w')
        non_repeated_tweet_file.write(tweet)
        non_repeated_tweet_index += 1


# cleaning()
non_repeated_tweets()