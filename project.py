import tweepy
import csv
import pandas as pd
from gtts import gTTS 
from playsound import playsound  
from translate import Translator
import os


consumer_key='MCx7op7xDAuX1FYjjpzmAGfhr'
consumer_secret='bgSBGDbMjRYSHpcGLQxKT5IiEjGMejq9vTAejg00KF5iOVZeso'
access_token='1311546887829241856-kk64OO0x6rhFkS9MUkloYvNnScozSG'
access_token_secret='eKSGE52eK6cFcGo3MBa07xhyQDDEtI9MhohrF5pOy9FPx'
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

tweet_text=[]
tweet_list=[]
audio_list=[]
video_list=[]
public_tweets=api.user_timeline(id='@ChekuriKhushal')
#public_tweets=api.search('Codechella -filter:retweets',count=50,tweet_mode='extended',include_entities=True)
for tweets in public_tweets:
    
    try:
        if 'media' in tweets.entities:

        #print(tweets._json['extended_entities']['media'])
            for tweet_type in tweets.extended_entities['media']:

                if tweet_type['type']=='photo':

                    a=tweets._json['extended_entities']['media']
                    print("Its a photo")
                    
                    tweet_list.append(a[0]['media_url'])
                    #imagecaptioning(a[0]['media_url'])
                    
                elif tweet_type['type']=='video':
             
                    
                    video=tweet_type['video_info']['variants']
                    if len(video)==4:
                        audio_url=video[0]['url']
                        audio_list.append(audio_url)
                        #audiotransciption(video[0]['url'])
                    elif len(video)==3:
                        video_url=video[0]['url']
                        video_list.append(video_url)
                        #videocaptioning(video[0]['url'])
                    
                elif tweet_type['type']=='animated_gif':
                    print("its an animated gif")
                    video=tweet_type['video_info']['variants']
                    animated_url=video[0]['url']
                    tweet_list.append(animated_url)
                    
        elif 'retweeted_status' in tweets._json:

            #print(tweets._json['retweeted_status']['full_text'])
            print('--------')
            
        else:
            #print(tweets.text)
            
            translator= Translator(to_lang="French")
            translation = translator.translate(tweets.text)
            print(translation)
            tweet_text.append((tweets.text,translation))
            print(tweet_text)  
# Here are converting in English Language  
            language = 'en'  
   
            obj = gTTS(text=tweets.text, lang=language, slow=False)  
  
  #Here we are saving the transformed audio in a mp3 file named  
            filename=tweets.created_at + ".mp3"
            obj.save(filename)  
  
# Play the  file  
            playsound(filename)
            #os.remove()   



    except:
        pass

try:
    urldata=pd.DataFrame(tweet_list,columns=['url'])
    urldata.to_csv("urlsheet.csv",index=None,columns=['url'],encoding='utf-8')
    tweetdata=pd.DataFrame(tweet_text,columns=['tweet','translation'])
    tweetdata.to_csv("tweets.csv",index=None,columns=['tweet','translation'],encoding='utf-8')
    audio_list_data=pd.DataFrame(audio_list,columns='audio_url')
    audio_list_data.to_csv("audio_list.csv",index=None,columns=['audio_url'],encoding='utf-8')
    video_list_data=pd.DataFrame(video_list,columns=['video_url'])
    video_list_data.to_csv("video_list.csv",index=None,columns=['video_url'],encoding='utf-8')
except:
    pass
