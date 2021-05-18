import streamlit as st #to make web application
import yfinance as yf  #retrive all of stock data
import pandas as pd    #employee data frame
import cufflinks as cf #to create charts
import datetime        #to select datetime
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

# st.markdown('''
# # Stock Information
# ''')

#Sidebar panel
st.sidebar.subheader('Query Parameters')
start_date=st.sidebar.date_input("Start date",datetime.date(2020,1,1))
# end_date=st.sidebar.date_input("End date",datetime.date(2021,5,12))
end_date=st.sidebar.date_input("End date",datetime.date.today())

#Retriveing ticker data
ticker_list=['CBRE','AAPL','GOOG','FB','MSFT','AMZN','PLTR','U']
tickerSymbol=st.sidebar.selectbox('Stock Ticker',ticker_list)  #Select ticker
tickerData=yf.Ticker(tickerSymbol) #Get ticker data
tickerDf=tickerData.history(period='1d',start=start_date,end=end_date)
task=st.sidebar.radio('Summary',['Profile','Chart','Historical Data'])

if task=='Profile':
    #Ticker info <html placeholder %s> for logo image
    string_logo='<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo,unsafe_allow_html=True)

    string_name=tickerData.info['longName']
    st.subheader('**%s**' %string_name)
    st.write('***%s***' % tickerData.info['sector'])

    string_summmary=tickerData.info['longBusinessSummary']
    st.info(string_summmary)
    st.write(tickerData.info['website'])

if task=='Historical Data':
    #Ticker data
    st.subheader('**Ticker Data**')
    tickerDf.sort_index(axis=0,ascending=False)
    st.dataframe(tickerDf,800,700)
    #st.table(tickerDf)

if task=='Chart':
    #Chart: Bollinger bands
    #st.subheader('**Bollinger bands**')
    st.subheader(tickerSymbol)
    #qf=cf.QuantFig(tickerDf,title='QuantFig',legend='top',name='GS')
    qf=cf.QuantFig(tickerDf,legend='top')
    qf.add_bollinger_bands()
    #fig=qf.iplot(asFigure=True)
    #st.plotly_chart(fig)

    #qf.add_sma([10,20],width=2,color=['green','lightgreen'],legendgroup=True)
    #qf.add_rsi(periods=20,color='java')
    #qf.add_bollinger_bands(periods=30,boll_std=2,colors=['magenta','grey'],fill=True)
    qf.add_volume()
    #qf.add_macd()
    fig2=qf.iplot(asFigure=True)
    st.plotly_chart(fig2)

    # fig3=plt.plot(tickerDf['Close'],label='Close Price')
    # st.plotly_chart(fig3)

    ShortEMA=tickerDf['Close'].ewm(span=12).mean()
    longEMA=tickerDf['Close'].ewm(span=26).mean()
    tickerDf['MACD']=ShortEMA-longEMA

    chart_data=tickerDf['MACD']
    #st.line_chart(chart_data)
    st.area_chart(chart_data)
