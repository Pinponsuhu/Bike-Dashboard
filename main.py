from dash import Dash,html,dcc,Output,Input
import pandas as pd 
import locale
import plotly.express as px
import plotly.graph_objects as go
import constants
import figures


locale.setlocale(locale.LC_ALL,'')

bike_df = pd.read_csv('./assets/Sales.csv',parse_dates=['Date'])
bike_df.reset_index(drop=True,inplace=True)

app = Dash(__name__,external_stylesheets=['./assets/style.css',constants.FONT_AWESOME])

sub_cat = bike_df.groupby(by='Country')['Revenue'].sum().reset_index()


sub_cat_pie = go.Figure(go.Bar(x=sub_cat['Country'],y=sub_cat['Revenue'], marker_color='#442BC7'))

country = px.line(bike_df, x='Year',y='Revenue',color='Country')
country.update_traces(mode="markers+lines", hovertemplate=None)
country.update_layout(hovermode='x')

country_list = bike_df['Country'].unique()

app.layout = html.Main(
    children=[
        html.Section(
            id='control',
            children=[
                html.Div(
                    children=[
                        dcc.Dropdown(
                        placeholder ='Select Country',
                        options=bike_df['Country'].unique(), value=None,
                        id='countryDropdown', 
                    ), 
                    ]
                ),
                html.Div(
                    children=[
                        html.Label(
                            id='slider-label',
                            children=['Year range']
                            ),
                        dcc.Slider(
                        min=bike_df['Year'].min(), 
                        max=bike_df['Year'].max(),
                        id='year-slider' ,
                        step=None,
                        marks={str(year): str(year) for year in bike_df['Year'].unique()},
                )
                    ]
                ), 
                html.Title(
                    children='Bike Sales Dashboard'
                )
            ]
            ),
        html.Section(
            id= 'summarySection',
            children=[
                html.Div(
                    id='monthlyTransactionDiv',
                    children=[
                        dcc.Graph(
                            id='monthlyTransaction',
                            )
                        ]
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
                                    id='totalCustomer',
                                    className='totalValue'
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
                                    id='totalProfit',
                                    className='totalValue',
                                    
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
                                    id='totalQuantity',
                                    className='totalValue',
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
                                    id='highestMonth',
                                    className='totalValue',
                                ),
                            ]
                        ),
                    ]
                )
            ]
        ),
        html.Section(
            id='sectionTwo',
            children=[
                html.Div(
                    id='countryChart',
                    children=[
                        dcc.Graph(
                            id='countryChart',
                        )
                    ]
                ),
                html.Div(
                    id='yearChart',
                    children=[
                        dcc.Graph(
                            id='sales_years'
                        )
                    ]
                    ),
            ]
        ),
        html.H4(
            id='country-val',
        )
        
    ]
)
fig_gen = figures.DashFigures(bike_df)

@app.callback(
    Output(component_id='totalCustomer', component_property='children'),
    Output(component_id='totalProfit', component_property='children'),
    Output(component_id='totalQuantity', component_property='children'),
    Output(component_id='highestMonth', component_property='children'),
    Output(component_id='monthlyTransaction', component_property='figure'),
    Output(component_id='sales_years', component_property='figure'),
    Input(component_id='countryDropdown', component_property='value'),
    allow_duplicate=True
    )

def update_hist(input_value):
    total= fig_gen.total_customer(input_value)
    totalProf= fig_gen.total_Profit(input_value)
    totalQuan= fig_gen.total_quantity(input_value)
    highestMonth = fig_gen.highest_month(input_value)
    trans= fig_gen.trans_month(input_value)
    saleYears= fig_gen.update_pie(input_value)
    return  total,totalProf,totalQuan,highestMonth,trans,saleYears

@app.callback(
    Output(component_id='country-val', component_property='children'),
    Output(component_id='countryChart', component_property='figure'),
    Input(component_id='year-slider', component_property='value')
)

def yearRange(input_value):
    country_chart = fig_gen.country_chart(input_value)
    return input_value, country_chart


if __name__ == '__main__':
    app.run(debug=True)