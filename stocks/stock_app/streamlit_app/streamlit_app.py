import streamlit as st
import datetime
import yfinance as yf
from plotly import graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly,plot_components_plotly
from matplotlib import style
import pandas as pd

html="""
           <head>
    <title>Stocks Forecasting</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid" style="display: flex;">
          <div class="navbar-brand d-flex justify-content-left" style="width: 100vw;">
             
                <span class="navbar-text hello-msg justify-content-center">
                  Hello, {{ request.user }} 
                </span>
          </div>
          <div></div>
          <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav hello-msg ml-auto">
                <li class="nav-item">
                  <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                </li>
              </ul>
          </div>
        </div>
      </nav>
   
      </body>
           """

       
st.set_page_config( layout = "wide",
    initial_sidebar_state = "collapsed",
)
START=datetime.datetime(2009,1,1)
TODAY=datetime.date.today()
style.use('dark_background')
df=pd.read_csv('./listing_status.csv')
stock=df['symbol']
stocks =list(stock)
st.title("Stock Prediction")
selected_stock=st.selectbox('Select stock for prediction',stocks)
n_years=st.slider('Years of Prediction',1,5)
period=n_years*365
@st.cache_data
def load_data(ticker):
   data=yf.download(ticker,START,TODAY)
   data.reset_index(inplace=True)
   return data

data_load_state=st.text('Loading data...')
data=load_data(selected_stock)
st.subheader('Raw Data')
st.write(data.tail())

def plot_raw_data():
   fig=go.Figure()
   fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='stack_open'))
   fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='stock_close'))
   fig.layout.update(title_text='Time Series Data',xaxis_rangeslider_visible=True)
   fig.update_traces(
         line=dict(color='#af68de')
        )
   st.plotly_chart(fig)

plot_raw_data()    

df_train=data[['Date','Close']]
df_train=df_train.rename(columns={'Date':'ds','Close':'y'})
model=Prophet()
model=model.fit(df_train)
future = model.make_future_dataframe(periods=period)  
predictions=model.predict(future)
st.subheader('Forecast data')
st.write(predictions.tail())
st.markdown('\n\n')
st.write(f'Forecast plot for {n_years} years')
    
fig1 =plot_plotly(model,predictions)
fig1.layout.update(xaxis_rangeslider_visible=True,
                       width=50,height=550)
fig1.update_traces(
      line=dict(color='#af68de')
    )
st.plotly_chart(fig1,use_container_width=True)
st.write("Forecast components")
fig2 =plot_components_plotly(model,predictions)
fig2.layout.update(xaxis_rangeslider_visible=True,
                       width=1000,height=1100,
                       margin=dict(l=0, r=0, t=20, b=0),)
fig2.update_traces(
       line=dict(color='#af68de')
    )
st.write(fig2)
    
