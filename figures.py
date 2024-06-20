from dash import Dash,html,dcc,Output,Input,callback
import pandas as pd 
import seaborn as sns
import locale
import plotly.express as px
import plotly.graph_objects as go
import constants

locale.setlocale(locale.LC_ALL,'')

class DashFigures():
    
    def __init__(self,bike_df):
        self.bike_df = bike_df
    
    def trans_month(self,input_value):
        if input_value != None:
            country_data = self.bike_df.loc[self.bike_df['Country'] == input_value]
            transaction_month = px.histogram(country_data,x='Month',y='Revenue',color='Product_Category',barmode='group',title=f"Transactions Per Month For {input_value}",color_discrete_map=constants.CATEGORY_COLORS,histfunc='sum',labels='Revenue',height=370)
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
            return transaction_month
        transaction_month = px.histogram(self.bike_df,x='Month',y='Revenue',color='Product_Category',barmode='group',title="Transactions Per Month",color_discrete_map=constants.CATEGORY_COLORS,histfunc='sum',labels='Revenue',height=370)
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
        return transaction_month
    
    def total_customer(self,input_value):
        if input_value != None:
            count_customer = self.bike_df.loc[self.bike_df['Country'] == input_value,'Revenue'].count()
            
            return f'{locale.format_string('%d',count_customer,grouping=True)}'
        else:
            count_customer = self.bike_df['Revenue'].count()
            
            return f'{locale.format_string('%d',count_customer,grouping=True)}'
        
    def total_Profit(self,input_value):
        if input_value != None:
            total_prof = self.bike_df.loc[self.bike_df['Country'] == input_value,'Profit'].sum()
            
            return f'${locale.format_string('%d',total_prof,grouping=True)}'
        else:
            total_prof = self.bike_df['Profit'].sum()
            
            return f'${locale.format_string('%d',total_prof,grouping=True)}'
        
        
    def total_quantity(self,input_value):
        if input_value != None:
            total_prof = self.bike_df.loc[self.bike_df['Country'] == input_value,'Order_Quantity'].sum()
            
            return f'{locale.format_string('%d',total_prof,grouping=True)}'
        else:
            total_prof = self.bike_df['Order_Quantity'].sum()
            
            return f'{locale.format_string('%d',total_prof,grouping=True)}'

    def highest_month(self,input_value):
        if input_value != None:
            country_df = self.bike_df.loc[self.bike_df['Country'] == input_value]
            grouped_month = country_df.groupby(by='Month')['Revenue'].sum().reset_index()
            highestMonth = grouped_month.loc[grouped_month['Revenue'] == grouped_month['Revenue'].max()]
            return highestMonth['Month']
        else:
            grouped_month = self.bike_df.groupby(by='Month')['Revenue'].sum().reset_index()
            highestMonth = grouped_month.loc[grouped_month['Revenue'] == grouped_month['Revenue'].max(),'Month']
            return highestMonth
            