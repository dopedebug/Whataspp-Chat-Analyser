import streamlit as st
import pandas as pd
import preprocesser
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('UTF-8')
    df = preprocesser.preprocess(data)

    user_list = df['User'].unique().tolist()
    user_list.remove('Group Notifications')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Show analysis wrt:',user_list)


    if st.sidebar.button('Show analysis'):
        words,num_messages,media,link = helper.helper(selected_user,df)   
        st.title('Top Statitics')
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header('Total messages')
            st.header(num_messages)
        with col2:
            st.header('Total Words')
            st.header(words)
        with col3:
            st.header('Media shared')
            st.header(media)
        with col4:
            st.header('Links shared')
            st.header(link)
        st.title('Activity map')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Monthly Activity')
            monthly_timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(monthly_timeline['time'],monthly_timeline['Message'],color='green')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.header('Daily timeline')
            daily_time = helper.daily_timeline(selected_user,df)
            plt.figure(figsize=(18,10))
            fig,ax = plt.subplots()
            ax.plot(daily_time['only_date'],daily_time['Message'],color='red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        # activity map
        col1,col2 = st.columns(2)
        
        with col1:

            st.header('Most Busy Days')
            week_ac = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(week_ac.index,week_ac.values,color='red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Months')
            month_ac = helper.monthly_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(month_ac.index,month_ac.values,color='orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        st.title('Weekly HeatMap')
        act_table = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(act_table)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most busy users')
            u_list = helper.fetch_most_busy_user(df)
            fig,ax = plt.subplots()
            col1,col2  = st.columns(2)
            with col1:
                ax.bar(u_list.index, u_list.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(round((df['User'].value_counts().drop('Group Notifications')/df.shape[0])*100,2).reset_index().rename(columns = {'index':"Name","User":"Percent"}))
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        st.header('word_frequency')
        word_freq = helper.word_freq(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(word_freq['Words'],word_freq['frequency'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        col1,col2 = st.columns(2)
        with col1:
            emoji = helper.emoji_analyser(selected_user,df)
            st.title('Emoji Analysis')
            st.dataframe(emoji)
        with col2:
            fig,ax = plt.subplots()
            try:
                ax.pie(emoji['frequency'],labels = emoji['emojis'],autopct = '%0.2f')
            except Exception as e:
                st.header(e)
            st.pyplot(fig)



