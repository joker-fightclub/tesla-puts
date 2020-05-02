import tweepy
import twitter
import sys
from datetime import datetime, date, time, timedelta
from tweepy import Cursor
from collections import Counter
import sys
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
import yahoofinancials
import json
import api_key # returns internal api key
import plotly.graph_objects as go
import plotly.express as px


# initialize date and time for stock prices
style.use('ggplot')
start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()

#set up api key info
consumer_key, consumer_secret, access_token, access_token_secret = api_key.return_api_key()

#set up api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')
api = tweepy.API(auth)


account_list = ['elonmusk']
def account_summary(account_list):
    if (len(sys.argv) > 1):
      account_list = sys.argv[1:]
    else:
      print("Please provide a list of usernames at the command line.")
      sys.exit(0)
    if len(account_list) > 0:
      for target in account_list:
        print("Getting data for " + target)
        item = api.get_user(target)
        print("name: " + item.name)
        print("screen_name: " + item.screen_name)
        print("description: " + item.description)
        print("statuses_count: " + str(item.statuses_count))
        print("friends_count: " + str(item.friends_count))
        print("followers_count: " + str(item.followers_count))
        tweets = item.statuses_count
        account_created_date = item.created_at
        delta = datetime.utcnow() - account_created_date
        account_age_days = delta.days
        print("Account age (in days): " + str(account_age_days))
        if account_age_days > 0:
          print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))
        hashtags = []
        mentions = []
        tweet_count = 0
        end_date = datetime.utcnow() - timedelta(days=30)
        for status in Cursor(api.user_timeline, id=target).items():
          tweet_count += 1
          if hasattr(status, "entities"):
            entities = status.entities
            if "hashtags" in entities:
              for ent in entities["hashtags"]:
                if ent is not None:
                  if "text" in ent:
                    hashtag = ent["text"]
                    if hashtag is not None:
                      hashtags.append(hashtag)
            if "user_mentions" in entities:
              for ent in entities["user_mentions"]:
                if ent is not None:
                  if "screen_name" in ent:
                    name = ent["screen_name"]
                    if name is not None:
                      mentions.append(name)
          if status.created_at < end_date:
            break

def print_latest_elon_rant():
    elon = api.user_timeline('elonmusk')
    status = elon[0]
    json_str = json.loads(json.dumps(status._json))
    latest_post = json_str['text']
    return latest_post

def print_most_recent_tweets():
    elon = api.user_timeline('elonmusk', count = 1000)
    status = elon[0:100]
    pd.read_json(elon)
    statuses = pd.DataFrame()
    statuses["created_at"] = 0
    statuses["tweet"] = 0




i = 0
elon = api.user_timeline('elonmusk', count = 1000)
for status in elon:
    json_str = json.loads(json.dumps(status._json))
    if '@' not in json_str["text"]:
        statuses.loc[i, 'created_at'] = json_str['created_at']
        statuses.loc[i, 'tweet'] = json_str['text']
        i = i+1
    id = json_str['id']
    while int(json_str['created_at'].split(" ")[-1]) > 2019:
        elon = api.user_timeline('elonmusk', count = 1000)
        for status in tqdm(elon):
            json_str = json.loads(json.dumps(status._json))
            if '@' not in json_str["text"]:
                statuses.loc[i, 'created_at'] = json_str['created_at']
                statuses.loc[i, 'tweet'] = json_str['text']
                i = i+1


json_str['id']



json_str['created_at'].astype(date) < 2019
tesla_data = json_str['created_at']
datetime.strptime(tesla_data, '%Y')

int(json_str['created_at'].split(" ")[-1]) < 2019

len(statuses)
statuses


'@' in json_str["text"]

statuses

json_str["text"][0]

latest_tweet = print_latest_elon_rant()

print(print_latest_elon_rant())


''' import tesla stocks if not already saved'''
tsla_df = yf.download('TSLA', start='2019-01-01', end='2020-04-01', interval = '60m', progress=False)
tsla_df.head()
len(tsla_df)
tsla_df.columns
tsla_df.to_csv('tesla_stonks.csv')

'''read_csv'''
tsla_df = pd.read_csv('tesla_stonks.csv')
tsla_df.head()

# plot Stock Price - High
fig = px.line(tsla_df, x='Datetime', y='High')
fig.show()

# plot Stock Price - Low
fig = go.Figure()
fig.add_trace(go.Scatter(x=tsla_df.index, y=tsla_df.High, mode='lines', name = "High"))
fig.add_trace(go.Scatter(x=tsla_df.index, y=tsla_df.Low, mode='lines', name = "Low"))


# plot Stock Price - close - open
fig = go.Figure()
fig.add_trace(go.Scatter(x=tsla_df['Datetime'], y=tsla_df["Close"] - tsla_df["Open"], mode='lines', name = "Close - Open"))



set_of_buy = [] # fill with words that typicall yindicate a reduction in stock price
set_of_sell = [] # fill with words that typicall yindicate a rise in stock price


import plotly.io as pio
pio.renderers.default = "browser"

BEarer token
#AAAAAAAAAAAAAAAAAAAAAE8UEAEAAAAAwmm8fp1WnkDAjFYIbexsVdCk4yY%3DDNodCsTPddcyQOntyleBX1ppdDfxHOuzORagTDMc9Y0A5dfBKQ
