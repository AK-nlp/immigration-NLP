# scripts for extracting tweets containing some keyword


def extract_from_file(raw_tweet_file, keywords, path_2_save):
    """
    extracting tweets in raw_tweet_file that contain any of the keyword

    :param raw_tweet_file:
    :param keywords:
    :param path_2_save:
    :return:
    """


def extract_tweets(raw_tweet_directory, keywords, save_directory):
    """

    :param raw_tweet_directory:
    :param keywords:
    :param save_directory:
    :return:
    """
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    # for each file_name in raw_tweet_directory:
    #     extract_from_file(raw_tweet_directory/file_name, keywords,  save_directory/file_name)


raw_tweet_directory = "directory_of_the_raw_dataset"
keywords = "list of keywords"
save_directory = "directory to save the selected tweets"

extract_tweets(raw_tweet_directory, keywords, save_directory)
