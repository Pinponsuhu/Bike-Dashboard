from dash import Dash,html,dcc,Output,Input
import pandas as pd 
import seaborn as sns
import locale
import plotly.express as px
bike_df = pd.read_csv('./asset/Sales.csv',parse_dates=['Date'])
bike_df.reset_index(drop=True,inplace=True)
app = Dash(__name__,external_stylesheets=['./style/style.css'])
app.layout = html.Main(
    children=['Hello']
)

if __name__ == '__main__':
    app.run_server(debug=True)