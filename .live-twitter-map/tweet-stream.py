from django.db import models
import credentials
import tweepy
import json
import psycopg2
import psqldbcredentials as db
import random
import time
# Create your models here.
class MyStreamListener(tweepy.StreamListener):

    # def __init__(self, api=None):
    #     super(MyStreamListener, self).__init__()
    #     self.num_tweets = 0
    #     self.file = open(file_name, mode)
    #     self.max_tweets = max_tweets

    def on_status(self,status):

        # print(".")
        
        # t = status._json
        cursor = mydb.cursor()
        try: 
            # l = centre_bb(t['place']['bounding_box'])
            # time.sleep(10)    
            add_tweet = "INSERT INTO tweets (text,tweet_id,lon,lat,timestamp_ms) VALUES (%s,%s,%s,%s,%s)"
            text = remove_emoji(status.text)
            # print(status)
            # print((text,status.id,status.timestamp_ms))
            #print(status.place.bounding_box.coordinates
            centre = centre_bb(status.place.bounding_box)
            # print(centre)
            dt  = (text,status.id,centre[0],centre[1],status.timestamp_ms)
            try:
                cursor.execute(add_tweet,dt)
                mydb.commit()
            except:
                print("Error: tweet not added to db")
            finally:
                print(dt)
            # cursor.commit()
        except:
            print('no location')




        #credentials.ACCESS_SECRET


def centre_bb(bb): # Takes bounding box and calculates centre point
    c1,c2 = [bb.coordinates[0][i] for i in (0,2)]
    # centre = [(c1[1] + c2[1] )/2,(c1[0] + c2[0] )/2]
    centre = [random.triangular(c1[1],c2[1]),random.triangular(c1[0],c2[0])] # Randomises to minimise stacking 
    return centre

def remove_emoji(text): # Removes emoji from text for database compatability
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

if __name__ == "__main__":
    while True:
        time.sleep(5)

        mydb = psycopg2.connect(
            host=db.host,
            user=db.user,
            password=db.passwd,
            dbname = db.database
            )

        print(mydb)
        auth  = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_SECRET)
        api = tweepy.API(auth)
        region = [-7.0,49.0, 2.0,61.0]

        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        myStream.filter(locations=region)
        # Close the MySQL connection as it finished
        # However, this won't be reached as the stream listener won't stop automatically
        # Press STOP button to finish the process.
        mydb.close() 
        print("db closed")
