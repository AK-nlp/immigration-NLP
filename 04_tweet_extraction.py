

import pandas as pd
import pickle
import glob
# import os
import re


#file_name = glob.glob("/aparup_test/test/*.pkl")
#file_name = glob.glob("/home/khatua/test1/*.pkl")
file_name = glob.glob("/home/hoang/mirror/data/tweets/eu_core_users_top_followers/*.pkl")

id_arr = []
created_at_arr = []
lang_arr = []
full_text_arr = []
usr_arr = []
i=1

for file in file_name:
    infile = open(file, 'rb')
    new_dict = pickle.load(infile)
    for key in new_dict:
        tweet_acess=new_dict[key]
        for tweet_data in tweet_acess:
            text_acess=tweet_data['full_text']
            full_text_arr.append(text_acess)
            text_acess=tweet_data['lang']
            lang_arr.append(text_acess)
            text_acess=tweet_data['created_at']
            created_at_arr.append(text_acess)
            text_acess=tweet_data['id']
            id_arr.append(text_acess)
    full_text_df = pd.DataFrame(full_text_arr)
    full_text_df.columns = ["full_text"]
    created_at_df = pd.DataFrame(created_at_arr) 
    created_at_df.columns = ["created_at"]
    tweet_lang_df = pd.DataFrame(lang_arr)
    tweet_lang_df.columns = ["tweet_lang"]
    id_df = pd.DataFrame(id_arr)  
    id_df.columns = ["id"]
    df_col = pd.concat([id_df,created_at_df,full_text_df,tweet_lang_df], axis=1)
    DF2 = df_col[df_col["full_text"].str.contains("asylum|immigrant|immigration|migrant|refugee|syria|germany",flags=re.IGNORECASE, na=False)]
    xx = ("extractedTweets_" + str(i) + ".pkl")
    DF2.to_pickle(xx)
    i=i+1
    id_arr = []
    created_at_arr = []
    lang_arr = []
    full_text_arr = []
    infile.close    
  
    

# full_text_df = pd.DataFrame(full_text_arr) 
# full_text_df.columns = ["full_text"]
# full_text_df 

# created_at_df = pd.DataFrame(created_at_arr) 
# created_at_df.columns = ["created_at"]

# tweet_lang_df = pd.DataFrame(lang_arr)
# tweet_lang_df.columns = ["tweet_lang"]

# id_df = pd.DataFrame(id_arr) 
# id_df.columns = ["id"]


# df_col = pd.concat([id_df,created_at_df,full_text_df,tweet_lang_df], axis=1)


# DF2 = df_col[df_col["full_text"].str.contains("asylum|immigrant|immigration|migrant|refugee|refugee#ImmigrantStories|#refugeecrisis|#RefugeeEconomics|#RefugeeForum|#RefugeesNotTerrorists|#RefugeesWelcome|#SyrianRefugees|#UN4RefugeesMigrants|#WelcomeRefugees|#WithRefugees",flags=re.IGNORECASE, na=False)]
# DF2.to_pickle('selectedTweets.pkl')