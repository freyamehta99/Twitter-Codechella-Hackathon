import tweepy
import csv
import pandas as pd
from gtts import gTTS 
from playsound import playsound  
from translate import Translator
import os

#content_type': 'video/mp4', 
#'url': 'https://video.twimg.com/ext_tw_video/1329874886953615362/pu/vid/480x270/I9K5DTOXLvEPQ9at.mp4?tag=10'}, {'content_type': 'application/x-mpegURL',
#'url': 'https://video.twimg.com/ext_tw_video/1329874886953615362/pu/pl/EWp3PLmAQc31TbhV.m3u8?tag=10'


consumer_key='MCx7op7xDAuX1FYjjpzmAGfhr'
consumer_secret='bgSBGDbMjRYSHpcGLQxKT5IiEjGMejq9vTAejg00KF5iOVZeso'
access_token='1311546887829241856-kk64OO0x6rhFkS9MUkloYvNnScozSG'
access_token_secret='eKSGE52eK6cFcGo3MBa07xhyQDDEtI9MhohrF5pOy9FPx'
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)
audio_tweet=api.user_timeline(id='@ChekuriKhushal')
for tweet in audio_tweet:
    #print(tweet)

    print(".............")
    if 'media' in tweet.entities:
        print(tweet._json['extended_entities'])
        print("111111111111111111111111111111")
        for tweet_t in tweet.extended_entities['media']:
            if tweet_t['type']=='video':
                v=tweet_t['video_info']['variants']
                v_url=v[2]['content_type']
                print(v[0]['url'])
                if (len(v))==4:
                    print("its audio tweet")
                else:
                    print("its a video")
                    

tweet_text=[]
tweet_list=[]
audio_list=[]
video_list=[]
public_tweets=api.search('Codechella -filter:retweets',count=50,tweet_mode='extended',include_entities=True)
for tweets in public_tweets:
    #print(twets)
    try:
        if 'media' in tweets.entities:

        #print(tweets._json['extended_entities']['media'])
            for tweet_type in tweets.extended_entities['media']:

                if tweet_type['type']=='photo':

                    a=tweets._json['extended_entities']['media']
                    print("Its a photo")
                    tweet_list.append(a[0]['media_url'])
                elif tweet_type['type']=='video':
             
                    print("its a video")
                    video=tweet_type['video_info']['variants']
                    if len(video)==4:
                        audio_url=video[0]['url']
                        audio_list.append(audio_url)
                    elif len(video)==3:
                        video_url=video[0]['url']
                        video_list.append(video_url)
                    
                elif tweet_type['type']=='animated_gif':
                    print("its an animated gif")
                    video=tweet_type['video_info']['variants']
                    animated_url=video[0]['url']
                    tweet_list.append(animated_url)
                    
        elif 'retweeted_status' in tweets._json:

            #print(tweets._json['retweeted_status']['full_text'])
            print('--------')
            
        else:
            #print(tweets.full_text)
            tweet_text.append(tweets.full_text)
            #translator= Translator(to_lang="German")
            #translation = translator.translate(tweets.full_text)
            #print(translation)  
# Here are converting in English Language  
            language = 'en'  
   
            obj = gTTS(text=tweets.full_text, lang=language, slow=False)  
  
  #Here we are saving the transformed audio in a mp3 file named  
   
            obj.save("tweet.mp3")  
  
# Play the  file  
            playsound("tweet.mp3")
            os.remove("tweet.mp3")   


            print('--------')



    except:
        pass

urldata=pd.DataFrame(tweet_list)
urldata.to_csv("urlsheet.csv",encoding='utf-8')
tweetdata=pd.DataFrame(tweet_text)
tweetdata.to_csv("tweets.csv",encoding='utf-8')
audio_list_data=pd.DataFrame(audio_list)
audio_list_data.to_csv("audio_list.csv",encoding='utf-8')
video_list_data=pd.DataFrame(video_list)
video_list_data.to_csv("video_list.csv",encoding='utf-8')