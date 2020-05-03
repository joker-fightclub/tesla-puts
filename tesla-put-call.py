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
from tqdm import tqdm
import sklearn
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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
def get_elon_tweets_2020():
    statuses = pd.DataFrame()
    statuses['created_at'] = 0
    statuses['tweet'] = 0
    i = 0
    elon = api.user_timeline('elonmusk', count = 1000)
    for status in elon:
        json_str = json.loads(json.dumps(status._json))
        if json_str["text"][0] != '@':
            statuses.loc[i, 'created_at'] = json_str['created_at']
            statuses.loc[i, 'tweet'] = json_str['text']
            i = i+1
        id = json_str['id']
    while int(json_str["created_at"].split(" ")[-1]) > 2019:
        elon = api.user_timeline('elonmusk', max_id = id, count = 1000)
        for status in tqdm(elon):
            json_str = json.loads(json.dumps(status._json))
            if json_str["text"][0] != '@':
                statuses.loc[i, 'created_at'] = json_str['created_at']
                statuses.loc[i, 'tweet'] = json_str['text']
                i = i+1
            id = json_str['id']
        print(json_str['created_at'].split(" ")[-1])
    return statuses
def load_tesla_stonks(interval):
    if interval == '60m':
        tsla_df = yf.download('TSLA', start='2019-01-01', end='2020-05-02', interval = '60m', progress=False)
    else:
        tsla_df = yf.download('TSLA', start='2019-01-01', end='2020-05-02', progress=False)
    if interval == '60m':
        tsla_df.to_csv('tesla_stonks_hourly.csv')
    else:
        tsla_df.to_csv('tesla_stonks_daily.csv')
    return tsla_df
def price_to_binary(x):
    if x>0:
        return 1
    else:
        return 0
def text_to_binary(x, y):
    if x in y:
        return 1
    else:
        return 0


'''load csv files'''
tsla_df = pd.read_csv('tesla_stonks_daily.csv')
tsla_df['close-open'] = tsla_df['Close'] - tsla_df['Open']
tsla_df.head()
tsla_df['movement'] = tsla_df['close-open'].astype(float).apply(lambda x: price_to_binary(x))
tsla_df.dtypes
tsla_df["date_time"] = pd.to_datetime(tsla_df["Date"], utc = False).dt.date


statuses = pd.read_csv("elon_tweets.csv").drop(columns = 'Unnamed: 0')
statuses.head()
statuses["date_time"] = pd.to_datetime(statuses['created_at'], utc = False).dt.date

merged_data = pd.merge(statuses, tsla_df, how = 'left', left_on = 'date_time', right_on = 'date_time')
merged_data = merged_data.dropna()

keywords = ['grimez', 'tesla', 'stock', 'high', 'vibe', 'anime', 'solar', 'corona', 'california', 'hospital', 'states', 'usa', 'america', 'rocket', 'free', 'texas', 'silicon', 'machine', 'mortality', 'hack']
for all in keywords:
    merged_data[all] = merged_data['tweet'].astype(str).apply(lambda x: text_to_binary(all, x.lower()))


X = merged_data[keywords]
y = merged_data['movement']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)


# fit model no training data
model = xgb.XGBClassifier(max_depth = 10)
eval_metric = ["auc","error"]
model.fit(X_train, y_train, eval_metric=eval_metric)

# test model
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))



# plots for Tesla Stock Price
fig = go.Figure()
fig.add_trace(go.Scatter(x=tsla_df.index, y=tsla_df.High, mode='lines', name = "High"))
fig.add_trace(go.Scatter(x=tsla_df.index, y=tsla_df.Low, mode='lines', name = "Low"))

tsla_df.columns
# plot Stock Price - close - open
fig = go.Figure()
fig.add_trace(go.Scatter(x=tsla_df['Date'], y=tsla_df["Close"] - tsla_df["Open"], mode='lines', name = "Close - Open"))
