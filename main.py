from dash import Dash,html,dcc,Output,Input,callback
import pandas as pd 
import seaborn as sns
import locale
import plotly.express as px
import plotly.graph_objects as go
import constants


locale.setlocale(locale.LC_ALL,'')

bike_df = pd.read_csv('./assets/Sales.csv',parse_dates=['Date'])
bike_df.reset_index(drop=True,inplace=True)

app = Dash(__name__,external_stylesheets=['./assets/style.css',constants.FONT_AWESOME])

customer_count = bike_df['Revenue'].count()
total_profit =  bike_df['Profit'].sum()
total_quantity =  bike_df['Order_Quantity'].sum()

highest_month_group = bike_df.groupby(by='Month')['Revenue'].sum().reset_index()
highest_month = highest_month_group.loc[highest_month_group['Revenue'] == highest_month_group['Revenue'].max()]
highest_month


transaction_month = px.histogram(bike_df,x='Month',y='Revenue',color='Product_Category',barmode='group',title="Transactions Per Month",color_discrete_map=constants.CATEGORY_COLORS,histfunc='sum',labels='Revenue',height=370)
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
        bgcolor="#D5F0FF", 
        font=dict(
            size = 10,
            color="black"  # Text color of the legend
        )
    )
)


sub_cat = bike_df.groupby(by='Sub_Category')['Revenue'].sum().reset_index()
print(sub_cat)

country = px.line(bike_df, x='Year',y='Revenue',color='Country')
country.update_traces(mode="markers+lines", hovertemplate=None)
country.update_layout(hovermode='x')

country_list = bike_df['Country'].unique()

@callback(
    Output(component_id='country-val', component_property='children'),
    Input(component_id='country-dropdown', component_property='value')
)
def update_output_div(input_value):
    print(input_value)
    return f'Output: {input_value}'

@callback(
    Output(component_id='country-val', component_property='children'),
    Input(component_id='year-slider',component_property='children')
)
def update_year(input_value):
    return input_value

app.layout = html.Main(
    children=[
        html.Section(
            children=[
                dcc.Dropdown(
                    options=[{'label': country, 'value': country} for country in country_list], value=None,
                    id='country-dropdown'
                    ), 
                dcc.RangeSlider(
                    min=bike_df['Year'].min(), 
                    max=bike_df['Year'].max(),
                    id='year-slider' ,
                    step=None,
                    marks={str(year): str(year) for year in bike_df['Year'].unique()},
                    
                )
            ]
            ),
        html.Section(
            id= 'summarySection',
            children=[
                html.Div(
                    id='monthlyTransaction',
                    children=[dcc.Graph(figure=transaction_month)]
                ), 
                html.Div(
                    id='totalSection',
                    children=[
                        html.Div(
                            id='totalOne',
                            children=[
                                html.I(
                                    id='icons',
                                    className='fa fa-user'
                                ),
                                html.H4(
                                    id='totalLabel',
                                    children=['Total Customer']
                                ),
                                html.H1(
                                    id='totalValue',
                                    children=[f'${locale.format_string('%d',customer_count,grouping=True)}']
                                ),
                            ]
                        ),
                        html.Div(
                            id='totalTwo',
                            children=[
                                html.I(
                                    id='icons',
                                    className='fa fa-dollar'
                                ),
                                html.H4(
                                    id='totalLabel',
                                    children=['Total Profit']
                                ),
                                html.H1(
                                    id='totalValue',
                                    children=[f'${locale.format_string('%d',total_profit,grouping=True)}']
                                ),
                            ]
                        ),
                        html.Div(
                            id='totalThree',
                            children=[
                                html.I(
                                    id='icons',
                                    className='fa fa-calculator'
                                ),
                                html.H4(
                                    id='totalLabel',
                                    children=['Total Quantity']
                                ),
                                html.H1(
                                    id='totalValue',
                                    children=[f'${locale.format_string('%d',total_quantity,grouping=True)}']
                                ),
                            ]
                        ),
                        html.Div(
                            id='totalFour',
                            children=[
                                html.I(
                                    id='icons',
                                    className='fa fa-calendar'
                                ),
                                html.H4(
                                    id='totalLabel',
                                    children=['Highest Month']
                                ),
                                html.H1(
                                    id='totalValue',
                                    children=[f'{highest_month['Month'].values[0]}']
                                ),
                            ]
                        ),
                    ]
                )
            ]
        ),
        html.H3(
            id='country-val',
            children=[]
                ),
        
    ]
)

@callback(
    Output(component_id='country-val', component_property='children'),
    Input(component_id='country-dropdown', component_property='value')
)
def update_output_div(input_value):
    print(input_value)
    return f'Output: {input_value}'

@callback(
    Output(component_id='country-val', component_property='children'),
    Input(component_id='year-slider',component_property='value')
)
def update_year(input_value):
    return input_value

if __name__ == '__main__':
    app.run(debug=True)