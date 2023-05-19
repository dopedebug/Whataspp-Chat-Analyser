import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji


def helper(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]
    
    # Number of Messages
    num_messages = df.shape[0]
    # Number of words
    words = []
    for messages in df['Message']:
            words.extend(messages.split())
    # media files
    num_media = df[df['Message']=="<Media omitted>\n"].shape[0]
    # links
    count= 0
    for i in df['Message']:
        if "www" in i or ".com" in i:
            count+=1
    link_num = count    
    
    return len(words),num_messages,num_media,link_num

def fetch_most_busy_user(df):
    x = df['User'].value_counts().head(n = 7).drop('Group Notifications')
    return x


def create_wordcloud(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User']==selected_user]

    
    temp = df[df['User'] != 'Group Notifications']
    temp  = temp[temp['Message'] !="<Media omitted>\n"]
    f = open('stop_words.txt','r')
    stop_words = f.read()

    words = []

    for messages in temp['Message']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc= wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc

def word_freq(selected_user,df):
    if selected_user != 'Overall':    
        df = df[df['User']==selected_user]
    

    temp = df[df['User'] != 'Group Notifications']
    temp  = temp[temp['Message'] !="<Media omitted>\n"]
    f = open('stop_words.txt','r')
    stop_words = f.read()

    words = []

    for messages in temp['Message']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)

    a = pd.DataFrame(Counter(words).most_common(10))
    a.rename(columns = {0:"Words",1:"frequency"},inplace = True)
    return a

def emoji_analyser(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]
    emojis = []

    for message in df['Message']:
        emojis.extend([em for em in message if em in emoji.distinct_emoji_list(em)])
    emo = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emo.rename(columns={0:'emojis',1:'frequency'},inplace = True)
    return emo
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':    
        df = df[df['User']==selected_user]
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year','month_num',"month"]).count()['Message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))   
    timeline['time'] = time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':    
        df = df[df['User']==selected_user]
    df['only_date'] = df['date'].dt.date
    daily_time = df.groupby(['year','only_date']).count()['Message'].reset_index()
    return daily_time

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':    
        df = df[df['User']==selected_user]
    return df['day_name'].value_counts()

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':    
        df = df[df['User']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':    
        df = df[df['User']==selected_user]
    act_table = df.pivot_table(index = 'day_name',columns ='period',values='Message',aggfunc='count').fillna(0)
    return act_table
