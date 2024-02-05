#%%
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#%%
from src.utils import config

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent)
#%%
subreddit = reddit.subreddit('CroIT')

for post in subreddit.top(limit=10):  # You can use .hot(), 
    print(post.title)  

#%%
analyzer = SentimentIntensityAnalyzer()

for post in subreddit.top(limit=10):
    sentiment = analyzer.polarity_scores(post.title)
    print(f"{post.title}: {sentiment}")

#%%

#%%

#%%

#%%
