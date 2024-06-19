from dash import Dash,html,dcc,Output,Input
import pandas as pd 
import seaborn as sns
import locale
import plotly.express as px
import constants

bike_df = pd.read_csv('./assets/Sales.csv',parse_dates=['Date'])
bike_df.reset_index(drop=True,inplace=True)
app = Dash(__name__,external_stylesheets=['./assets/style.css'])

transaction_month = px.histogram(bike_df,x='Month',y='Revenue',color='Product_Category',barmode='group',title="Transactions Per Month",color_discrete_map=constants.CATEGORY_COLORS,histfunc='sum')
transaction_month.update_layout(
    paper_bgcolor = constants.SECTION_BG,
    plot_bgcolor = constants.SECTION_BG,
    yaxis=dict(
        title='Sum of revenue($)',
        title_font=dict(size=14, color='black'),  # Y-axis title font properties
        tickfont=dict(size=12, color='black'),  # Y-axis tick label properties
        gridcolor= constants.SECTION_BG
    ), 
    xaxis=dict(
        title='Years',
        title_font=dict(size=14, color='black'),  # X-axis title font properties
        tickfont=dict(size=12, color='black'),
        title_standoff=20,# X-axis tick label properties
        gridcolor= constants.SECTION_BG
    ),
    legend=dict(
        title='Product Category',
        bgcolor="orange", 
        font=dict(
            size = 10,
            color="White"  # Text color of the legend
        )
    )
)
transaction_month.update_traces(
    textfont_color = 'white',
    texttemplate='%{x}',  # Display value inside the bar
    textposition='inside',  # Position of the text
    insidetextanchor='middle',  # Anchor text in the middle of the bar
    textfont= dict(color='#f0f0f0')
)
app.layout = html.Main(
    children=[
        html.Section(
            id= 'summarySection',
            children=[
                dcc.Graph(figure=transaction_month)
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)