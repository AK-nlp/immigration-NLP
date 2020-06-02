# scripts for extracting tweets containing some keyword
import glob
import pandas as pd
import pickle
import re


def read_keywords(keyword_filename):
    """
    read the keywords from file
    :param keyword_filename: file that contains keywords
    :return:
    """
    file = open(keyword_filename)
    keywords = []
    for line in file:
        keywords.append(line.strip())
    file.close()
    return keywords


def read_previousley_processed_files(tracking_filename):
    """
    read list of files that were previously processed
    :param tracking_filename: file that contains list of previously processed
    :return:
    """
    processed_files = []
    file = open(tracking_filename)
    for line in file:
        processed_files.append(line.strip())
    file.close()
    return processed_files


def extract_from_file(tweet_filename, keywords):
    """
    extracting tweets in tweet_filename that contain any of the keyword

    :param tweet_filename:
    :param keywords:
    :return:
    """
    try:
        tweet_id_arr = []
        created_at_arr = []
        lang_arr = []
        full_text_arr = []
        usr_id_arr = []
        screen_name_arr = []

        infile = open(tweet_filename, 'rb')
        user_tweets = pickle.load(infile)
        for user, tweets in user_tweets.items():
            if tweets == 'No result':  # particular case when we cannot crawl tweets from this user
                continue
            for tweet in tweets:
                tweet_id_arr.append(tweet['id'])
                usr_id_arr.append(tweet['user']['id'])
                screen_name_arr.append(tweet['user']['screen_name'])
                lang_arr.append(tweet['lang'])
                created_at_arr.append(tweet['created_at'])
                full_text_arr.append(tweet['full_text'])
        infile.close

        df = pd.DataFrame.from_dict({'tweet_id': tweet_id_arr, 'user_id': usr_id_arr, 'screen_name': screen_name_arr,
                                     'lang': lang_arr, 'created_at': created_at_arr, 'full_text': full_text_arr})

        keyword_str = '|'.join(keywords)
        print('keywords = ', keyword_str)
        selected_tweets = df[df['full_text'].str.contains(keyword_str, flags=re.IGNORECASE, na=False, regex=True)]
        return selected_tweets
    except Exception as e:
        print(e)
        return None


def extract_tweets(raw_tweet_path, keyword_filename, save_path, tracking_filename):
    """
    
    :param raw_tweet_path:
    :param keyword_filename:
    :param save_path:
    :param tracking_filename:
    :return:
    """
    raw_files = glob.glob('{}/*.pkl'.format(raw_tweet_path))  # get list of .pkl files
    keywords = read_keywords(keyword_filename)

    # get list of previously processed files
    previously_processed_files = read_previousley_processed_files(tracking_filename)
    # turn into set for faster membership checking
    previously_processed_files = set(previously_processed_files)

    extracted_tweets = None
    processed_files = []
    save_count = 0

    for filename in raw_files:
        print('processing file {}'.format(filename))
        if filename in previously_processed_files:
            # ignore the files that were previously processed
            continue
        selected_tweets = extract_from_file(filename, keywords)
        print('\t extract {} tweets'.format(selected_tweets.shape[0]))
        if selected_tweets is None:
            # there is something wrong with the file, just ignore it for now
            continue
        if extracted_tweets is None:
            extracted_tweets = selected_tweets
        else:
            extracted_tweets = pd.concat([extracted_tweets, selected_tweets], axis=0)
        #
        processed_files.append(filename)

        #
        if extracted_tweets.shape[0] >= 50000:
            extracted_tweets.to_pickle('{}/{}.pkl'.format(save_path, save_count))
            #
            track = open(tracking_filename, 'a+')
            for f in processed_files:
                track.write(f + '\n')
            track.close()
            # restart the containers
            extracted_tweets = None
            processed_files = []
            save_count += 1

    # last processed files
    if extracted_tweets is not None:
        extracted_tweets.to_pickle('{}/{}.pkl'.format(save_path, save_count))
        #
        track = open(tracking_filename, 'a+')
        for f in processed_files:
            track.write(f + '\n')
        track.close()


raw_tweet_directory = '/home/hoang/data/tweets/eu_core_users_top_followers'
keyword_filename = 'selected_keywords.txt'
save_directory = '/home/hoang/mirror/extracted_tweets'
tracking_filename = 'tweet_extraction_tracking.txt'

extract_tweets(raw_tweet_directory, keyword_filename, save_directory, tracking_filename)
