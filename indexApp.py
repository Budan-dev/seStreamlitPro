import streamlit as st 
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf



st.title("S&P 500 App")


st.markdown("""
This app retrieves the list of the **S&P 500** (From Wikipedia) and its corresponding **Stock Closing Price** (year-to-date)!

* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn

* **Data Source:** [Wikipedia](https://www.wikipedia.org/).


""")

st.sidebar.header("User Input Features")

#Web Scraping S&P 500 data

#Using Streamlit Cache to save after scraping  

@st.cache_data
#Using python function to scrape through wikipedia
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby("GICS Sector")


#Sidebar - Sector Selection
sorted_sector_unique = sorted( df["GICS Sector"].unique() )
default_select_con = sorted_sector_unique[0]
selected_sector = st.sidebar.multiselect("Sector", sorted_sector_unique, default_select_con)


#Filtering data
df_selected_sector = df[ (df["GICS Sector"].isin(selected_sector))]


st.header("Display Companies in Selected Sector")
st.write("Data Dimension: ", str(df_selected_sector.shape[0]), "Data columns", str(df_selected_sector.shape[1]))
st.dataframe(df_selected_sector)



# To download the Web scraped data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)



# https: //pypi.org/project/yfinance
data = yf.download(
    tickers = list(df_selected_sector[:10].Symbol),
    period = "ytd",
    interval = "1d",
    group_by = "ticker",
    auto_adjust = True,
    prepost = True,
    threads = True,
    proxy = None
)



st.set_option('deprecation.showPyplotGlobalUse', False)

def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df["Date"] = df.index
    plt.fill_between(df.Date, df.Close, color="skyblue", alpha=0.3)
    plt.plot(df.Date, df.Close, color= "skyblue", alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight="bold")
    plt.xlabel("Date", fontweight="bold")
    plt.ylabel("Closing Price", fontweight="bold")
    return st.pyplot()


num_company = st.sidebar.slider("Number Of Companies", 1, 5)


if st.button("Show Plots"):
    st.header("Stock Closing Price")
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)