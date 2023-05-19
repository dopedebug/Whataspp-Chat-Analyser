import pandas as pd 
import re
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)    
    d = []
    for date in dates:
        a = re.split("-",date)
        d.append(a[0])
    dates = d
    df = pd.DataFrame({'User_message':messages,'message_date':dates})

    df['message_date']
    df['message_date'] = pd.to_datetime(df['message_date'],infer_datetime_format = True)

    df.rename(columns = {'message_date':'date'},inplace=True)
    users = []
    messages = []
    for message in df['User_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notifications')
            messages.append(entry[0])

    df['User'] = users
    df['Message'] = messages

    df.drop(columns= ['User_message'],inplace=True)  
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['day_name'] = df['date'].dt.day_name()
    df['minute'] = df['date'].dt.minute   
    period= []
    for hours in df[['day_name','hour']]['hour']:
        if hours =='23':
            period.append(str(hours)+'-'+'00')
        elif hours=='0':
            period.append('00' +'-'+'1')
        else:
            period.append(str(hours)+'-'+str(hours+1))
    df['period'] = period
    return df