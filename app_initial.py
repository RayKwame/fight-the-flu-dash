import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

import pandas as pd
import dash
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html


import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots



# Reading in the data 
df = pd.read_csv('data/Flu_Shot_Data_cleaned_2.csv')

data = df.groupby(["h1n1_concern","h1n1_vaccine"],as_index=True)["opinion_h1n1_risk"].count().reset_index(name="count")
data['Percentage'] = (data['count'] /data['count'].sum()*100).round()

data1 = df.groupby(["h1n1_vaccine"],as_index=True)["h1n1_vaccine"].count().reset_index(name="count")
data1['Percentage'] = (data1['count'] /data1['count'].sum()*100).round()

data2 = df.groupby(["seasonal_vaccine"],as_index=True)["seasonal_vaccine"].count().reset_index(name="count")
data2['Percentage'] = (data2['count'] /data2['count'].sum()*100).round()

data3 = df.groupby(["doctor_recc_h1n1","h1n1_vaccine"],as_index=True)["doctor_recc_h1n1"].count().reset_index(name="count")
data3['Percentage'] = (data3['count'] /data3['count'].sum()*100).round()

df_dist_h1n1 = df.h1n1_vaccine.value_counts(normalize=True).round(2).rename_axis('Vacc').reset_index(name='counts')
df_dist_seas = df.seasonal_vaccine.value_counts(normalize=True).round(2).rename_axis('Vacc').reset_index(name='counts')

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# this is needed by gunicorn command in procfile
server = app.server


'''def get_figure(filter= None):
    chart_data =[]
  
    if filter == "not_vaccinated":
        chart_data = [
        go.Bar(name='Not vaccined', x=data.query('h1n1_vaccine == 0')['h1n1_concern'], y=data.query('h1n1_vaccine == 0')['Percentage']),
    ]

    elif filter == "vaccinated":
        chart_data = [
        go.Bar(name='Vaccined', x=data.query('h1n1_vaccine == 1')['h1n1_concern'], y=data.query('h1n1_vaccine == 1')['Percentage'])
    ]

    else: 
        chart_data = [
        go.Bar(name='Not vaccined', x=data.query('h1n1_vaccine == 0')['h1n1_concern'], y=data.query('h1n1_vaccine == 0')['Percentage']),
        go.Bar(name='Vaccined', x=data.query('h1n1_vaccine == 1')['h1n1_concern'], y=data.query('h1n1_vaccine == 1')['Percentage'])
    ]

    fig_plot = go.Figure(data=chart_data,
    layout=go.Layout(template="simple_white"))

    # Change the bar mode
    fig_plot.update_layout(barmode='group')
    fig_plot.update_xaxes(title='Concern of H1N1',
        ticktext=['Not at all concerned 1', 'Not very concerned', 'Somewhat concerned', 'Very concerned'],
        tickmode='array', tickvals = [0,1, 2, 3])
    fig_plot.update_yaxes(title='Percentage of vaccinations')
        
    return fig_plot

fig = get_figure()
'''

def get_figure(filter= None):
    chart_data =[]

    if filter == "h1n1_vaccines":
        chart_data = [
        go.Bar(name="H1N1 vaccines", x=df_dist_h1n1.Vacc, y=df_dist_h1n1.counts, 
        marker_color='rgb(25,25,112)', text=df_dist_h1n1.counts, textposition='auto')
        ]

    elif filter == "seasonal_flu_vaccine":
        chart_data = [
        go.Bar(name="Seasonal flu vaccine", x=df_dist_seas.Vacc, y=df_dist_seas.counts, 
        marker_color='rgb(188,143,143)', text=df_dist_seas.counts, textposition='auto')
        ]  

    else: 
        chart_data = [
        go.Bar(name="H1N1 vaccines", x=df_dist_h1n1.Vacc, y=df_dist_h1n1.counts, 
        marker_color='rgb(25,25,112)', text=df_dist_h1n1.counts, textposition='auto'),
        
        go.Bar(name="Seasonal flu vaccine", x=df_dist_seas.Vacc, y=df_dist_seas.counts, 
        marker_color='rgb(188,143,143)', text=df_dist_seas.counts,textposition='auto')
        ]

    fig_plot = go.Figure(data=chart_data,
        layout=go.Layout(template="simple_white"))


    # Change the bar mode
    fig_plot.layout = dict(title='Vaccination Status in Sample', 
    # This code removes the 3.0 from the plot (which was shown although value was dropped):
    #xaxis = dict(type="category", categoryorder='category ascending')
    )
    fig_plot.update_xaxes( 
        ticktext=["Not vaccinated", "Vaccinated"], 
        tickmode='array', tickvals = [0,1],
        tickangle=0,tickfont_size=14
        )
    fig_plot.update_yaxes(title='Share within sample')

    return fig_plot

fig = get_figure()





# Creating plots for the distribution of our target(H1N1) variables 


'''def get_figure_targets_H1N1():
    fig = go.Figure(data=[
    go.Bar(name='Not vaccinated', x=data1.query('h1n1_vaccine == 0')['h1n1_vaccine'], y=data1.query('h1n1_vaccine == 0')['Percentage']),
    go.Bar(name='Vaccinated', x=data1.query('h1n1_vaccine == 1')['h1n1_vaccine'], y=data1.query('h1n1_vaccine == 1')['Percentage'])
],
    layout=go.Layout(template="simple_white"))

    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_xaxes(title='Distribution of the H1N1 Target',
        ticktext=['Vaccinated', 'Not Vaccinated'],
        tickmode='array', tickvals = [1, 0])
    fig.update_yaxes(title='Percentage')
            
    return fig

fig_targets_H1N1 = get_figure_targets_H1N1()'''




'''# Creating plots for the distribution of our target(Seasonal) variables 

def get_figure_targets_Seas():
    fig = go.Figure(data=[
    go.Bar(name='Not vaccinated', x=data2.query('seasonal_vaccine == 0')['seasonal_vaccine'], y=data2.query('seasonal_vaccine == 0')['Percentage']),
    go.Bar(name='Vaccinated', x=data2.query('seasonal_vaccine == 1')['seasonal_vaccine'], y=data2.query('seasonal_vaccine == 1')['Percentage'])
],
    layout=go.Layout(template="simple_white"))

    # Change the bar mode
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_xaxes(title='Distribution of the Seasonal Flu Target',
        ticktext=['Vaccinated', 'Not Vaccinated'],
        tickmode='array', tickvals = [1, 0])
    fig.update_yaxes(title='Percentage')
            
    return fig

fig_targets_Seas = get_figure_targets_Seas()'''


# Creating plots for the distribution of people with recommendation that shows both vaccinated and not vaccinated


def get_figure_targets_doc_recc():
    fig = go.Figure(data=[
    go.Bar(name='Not vaccinated', x=data3.query('h1n1_vaccine == 0')['doctor_recc_h1n1'], y=data3.query('h1n1_vaccine == 0')['Percentage']),
    go.Bar(name='Vaccinated', x=data3.query('h1n1_vaccine == 1')['doctor_recc_h1n1'], y=data3.query('h1n1_vaccine == 1')['Percentage'])
],
    layout=go.Layout(template="simple_white"))

    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_xaxes(title='Distribution of people with doctor´s recommendation for H1N1',
        ticktext=['Recommended', 'Not Recommended'],
        tickmode='array', tickvals = [1, 0])
    fig.update_yaxes(title='Percentage')
            
    return fig

fig_targets_H1N1_doc_recc = get_figure_targets_doc_recc()


def get_default_bar(data):
    return px.bar(data)

default_bar= get_default_bar(data)


default_bar = get_figure()
app.layout = html.Div(
    

    children=[
        
        html.H2(
            id="title",
            children="Flushot Interactive Dashboard",
        ),
        html.H1(children=""),
        html.Div(
            children=[
                html.H2("Inputs"),
                html.Div(
                    children=[
                        html.P("Vaccination_Distribution"),
                        dcc.Dropdown(
                            id="Distribution-dropdown",
                            options=[
                                {"label": "Both", "value": "both"},
                                {"label": "H1N1 vaccines", "value": "h1n1_vaccines"},
                                {"label": "Seasonal flu vaccine", "value": "seasonal_flu_vaccine"},
                            ],
                            value="both",
                        ),
                    ],
                ),
               
            ],

               # mit style kann man CSS-Formatierungen verwenden
            style={
                "backgroundColor": "#DDDDDD",
                "maxWidth": "800px",
                "padding": "10px 20px",
            },
        ),           
        html.Div(
            children=[
                html.H2("bar-chart"),
                dcc.Graph(id="bar-chart", figure=default_bar),
            ],
           
        ),


        #html.Button("Submit", id="textarea-state-example-button", n_clicks=0),
        #html.
        html.Div(id="textarea-state-example-output", style={"whiteSpace": "pre-line"}),
        #dcc.Graph(id="bar-chart", figure=fig),
        #dcc.Graph(id="bar-chart_1", figure=fig_targets_H1N1),
        #dcc.Graph(id="bar-chart_2", figure=fig_targets_Seas),
        #dcc.Graph(id="bar-chart_3", figure=fig_targets_H1N1_doc_recc),
    ]
)

# https://dash.plotly.com/basic-callbacks
@app.callback(
    
    #Output("textarea-state-example-output", "children"),
    Output("bar-chart", "figure"),
    
    Input("Distribution-dropdown", "value"), #Input("n-input", "value")],
    #State("Distribution-dropdown", "value"),
)
def update_output(value):

    return get_figure(value)



# Add the server clause:
if __name__ == "__main__":
    app.run_server()






    
