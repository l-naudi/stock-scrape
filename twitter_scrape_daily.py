from twitterscraper import query_tweets
import openpyxl
import os
import datetime as dt
import timeit
import pandas as pd
import shutil

class TwitterData:
    #run query for each company in array
    def get_data(self):
        timestamp = dt.datetime.now().strftime("%d-%m-%Y")
        start_time = timeit.default_timer()
        day_dir = 'C:\\Users\\12268\\stock-sentiment\\scrapes\\'+ timestamp
        #decides if to create new dir
        if os.path.isdir(day_dir):
            if os.path.isdir(day_dir + '_old'):
                shutil.rmtree(day_dir + '_old')
            shutil.move(day_dir,  day_dir + '_old')
            os.makedirs(day_dir)
            file_path =  day_dir + '\\'
        else:
            os.makedirs(day_dir)
            file_path =  day_dir + '\\'
        for i in range(len(arr)):
            ticker = arr[i][0] 
            company = arr[i][1]
            self.query_company(timestamp, ticker, company, file_path)
            end_time = timeit.default_timer()
        l = open(day_dir + '\\log.txt', 'w')
        l.write('Success! \r\nRuntime: ' + str(round(end_time, 2))-str(round(start_time, 2)) + ' seconds.')
        l.close()
   

    #search query fields
    def query_company(self, timestamp,  ticker, company, file_path):
        #* could create some sort of sting builder
        query = company + ' OR ' + '#'+company + ' OR ' + ticker + ' OR ' + '#'+ticker + ' OR ' + '$'+ticker 
        limit = 1000

        #gets tweets
        tweets = query_tweets(query, begindate=dt.date.today() - dt.timedelta(days=1), enddate=dt.date.today(), limit=limit, lang = 'english')
        #adds queried tweets to dataframe
        df = pd.DataFrame(tweets)

        #choose select columns from df for data
        data = df[['screen_name','username','timestamp','text','links','hashtags','has_media','img_urls','likes','retweets','replies','is_replied','is_reply_to']]
        #direct assignment for company name to
        data['company'], data['ticker'], data['scrape_date'] = company, ticker, timestamp
        #reorganizes dataframe
        data = data[['ticker','company','screen_name','username','timestamp','text','links','hashtags','has_media','img_urls','likes','retweets','replies','is_replied','is_reply_to','scrape_date']]

        #file fields
        file_ext = '.csv'
        file_name = ticker + '_' + timestamp
        file = file_path + file_name + file_ext

        #file writer
        data.to_csv(file)
        #print(pd.read_csv(file))

#company 2d array/list
arr = [['MSFT','Microsoft'], ['FB','Facebook'], ['GOOG', 'Google'], ['APPL', 'Apple'], ['NFLX', 'Netflix'], ['AMZN', 'Amazon'], ['DIS', 'Disney'], ['TSLA', 'Tesla'], ['MCD', 'McDonalds'], ['NKE', 'NIKE']]

td = TwitterData()
td.get_data()

