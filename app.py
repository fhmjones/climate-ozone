# Ozone at YVR and Abbotsford
# -*- coding: utf-8 -*-

# Run this app with `python app3.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/ 

# based on ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line

from flask import Flask
from os import environ

import pandas as pd
import dash
from dash import dcc
from dash import html

# plotly express could be used for simple applications
# but this app needs to build plotly graph components separately 
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)

# load intro and source text files
intro = open('introduction.md', 'r')
intro_md = intro.read()
intro = open('sources.md', 'r')
sources_md = intro.read()

# read in the data from the prepared CSV file. 
# Data are assumed to be in the custom formatted CSV file `YVR and Abbotsford 2017.csv`, stored in the folder `data`. 

all_O3 = pd.read_csv("YVR-Abb-2017.csv",index_col=0, parse_dates=['date_pst'])

# rolling n-point moving average (hence the .mean()); data points are 1hr apart, hence 24/day or 168/wk.
days = 7
hrs = 24*days
YVR_smoothed = all_O3.YVR_ppb.rolling(hrs, center=True, min_periods=6).mean() 
Abb_smoothed = all_O3.Abbotsford_ppb.rolling(hrs, center=True, min_periods=6).mean() 

# add this as columns to the dataframe
all_O3['YVR_smoothed']=YVR_smoothed
all_O3['Abb_smoothed']=Abb_smoothed

# rolling 8hr moving "average" (hence the .mean()); points are 1hr apart
yvr_8hr_O3 = all_O3.YVR_ppb.rolling(8,min_periods=6).mean()
abb_8hr_O3 = all_O3.Abbotsford_ppb.rolling(8,min_periods=6).mean()

# resample result by "day" (the 'D'), choosing the max value. 
YVR_max8hrsavg=yvr_8hr_O3.resample('D').max()
Abb_max8hrsavg=abb_8hr_O3.resample('D').max()

# Dash starts by defining dashboard controls at the same time as 
# placing them on the page using layout functions.
# HTML can be used, but it's easier to just have Dash translate MarkDown.
# For more control over layout, HTML and a chosen CSS template will be needed.
# YVR = Vancouver airport
# Abb = Abbotsford
# MDA8 = maximum daily 8 hour average

app.layout = html.Div([
# Start the page with introductory text and instructions.
    html.Div([
        dcc.Markdown(
            children=intro_md
        ),
    ]),

    html.Div([
# CheckList can define all checkboxes together but then the logic becomes 
# more awkward for this simple task. So each box is a separate CheckBox of this situation.

# Layout intention is to have 3 columns, 2 with checkboxes and a third with the dropdown.
# result is not ideal (dropdown is too low).
# The solution involves manipulating CSS but it is probably better to use BootStrap classes.
# That can be pursued later as it is "cosmetics" not functionality.
        dcc.Markdown('''
        **Select YVR components**
        '''),
        dcc.Checklist(
            id='yvrr_chkbox',
            options=[
                {'label': 'YVR raw', 'value': 'yvrr'}
            ],
            value=['yvrr']
        ),
        dcc.Checklist(
            id='yvrs_chkbox',
            options=[
                {'label': 'YVR smoothed', 'value': 'yvrs'}
            ],
            value=[]
        ),
        dcc.Checklist(
            id='yvrm_chkbox',
            options=[
                {'label': 'YVR MDA8', 'value': 'yvrm'}
            ],
            value=[]
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        dcc.Markdown('''
        **Select Abb. components**
        '''),
        dcc.Checklist(
            id='abbr_chkbox',
            options=[
                {'label': 'Abb raw', 'value': 'abbr'}
            ],
            value=[]
        ),
        dcc.Checklist(
            id='abbs_chkbox',
            options=[
                {'label': 'AbbR smoothed', 'value': 'abbs'}
            ],
            value=[]
        ),
        dcc.Checklist(
            id='abbm_chkbox',
            options=[
                {'label': 'Abb MDA8', 'value': 'abbm'}
            ],
            value=[]
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        dcc.Markdown('''
        Plot type for Abbotsford data only
        '''),
        dcc.Dropdown(
            id='linetype',
            options=[
                {'label': 'Lines', 'value': 'lines'},
                {'label': 'Markers', 'value': 'markers'},
                {'label': 'Lines & markers', 'value': 'lines+markers'}
            ],
            value='lines'
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),

# after controls, place the figure
    dcc.Graph(id='indicator-graphic'),

# then the text for instruction or to define the assignment.
    html.Div ([
        dcc.Markdown(
            children=sources_md
        )
    ])

], style={'width': '900px'})

# The callback function with it's app.callback wrapper.
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('yvrr_chkbox', 'value'),
    Input('yvrs_chkbox', 'value'),
    Input('yvrm_chkbox', 'value'),
    Input('abbr_chkbox', 'value'),
    Input('abbs_chkbox', 'value'),
    Input('abbm_chkbox', 'value'),
    Input('linetype', 'value'),
    )
def update_graph(yvrr_chkbox, yvrs_chkbox, yvrm_chkbox, abbr_chkbox, abbs_chkbox, abbm_chkbox, linetype):
# constructing all the figure's components
    fig = go.Figure()
    if yvrr_chkbox == ['yvrr']:
        fig.add_trace(go.Scatter(x=all_O3.index, y=all_O3.YVR_ppb,
                    mode='lines', line=dict(color='MediumTurquoise'), name="YVR raw"))
        fig.layout.title = "Vancouver Airport"
    if abbr_chkbox == ['abbr']:
        fig.add_trace(go.Scatter(x=all_O3.index, y=all_O3.Abbotsford_ppb,
                    mode=linetype, line=dict(color='SandyBrown'), name="Abb raw"))
        fig.layout.title = "Abbotsford"
    if yvrs_chkbox == ['yvrs']:
        fig.add_trace(go.Scatter(x=all_O3.index, y=all_O3.YVR_smoothed, 
                    mode="lines", line=dict(color='green'), name="YVR 7-day average"))
        fig.layout.title = "Vancouver Airport"
    if abbs_chkbox == ['abbs']:
        fig.add_trace(go.Scatter(x=all_O3.index, y=all_O3.Abb_smoothed, 
                    mode=linetype, line=dict(color='red'), name="Abb 7-day average"))
        fig.layout.title = "Abbotsford"
# different "x" because mda8 has daily values, not hourly values. 
    if yvrm_chkbox == ['yvrm']:  
        fig.add_trace(go.Scatter(x=YVR_max8hrsavg.index, y=YVR_max8hrsavg, 
                    mode="lines", line=dict(color='blue', width=2), name="YVR max daily 8hr avg"))
        fig.layout.title = "Vancouver Airport"
    if abbm_chkbox == ['abbm']:
        fig.add_trace(go.Scatter(x=YVR_max8hrsavg.index, y=Abb_max8hrsavg, 
                    mode=linetype, line=dict(color='firebrick', width=2), name="Abb max daily 8hr avg"))
        fig.layout.title = "Abbotsford"
    
    if (yvrr_chkbox == ['yvrr'] or yvrs_chkbox == ['yvrs'] or yvrm_chkbox == ['yvrm']) and (abbr_chkbox == ['abbr']or abbs_chkbox == ['abbs'] or abbm_chkbox == ['abbm']):
        fig.layout.title = "Vancouver Airport and Abbotsford"
    fig.update_layout(xaxis_title='Time', yaxis_title='ppb')

    return fig    

# dubugging on causes the active page to refresh as soon as edits are saved. 
# Python will quite if there are syntax errors, but if not the app will 
# throw error messages directly into the running browser window. 
# This is a very efficient workflow.
if __name__ == '__main__':
    app.run_server(debug=True)

# I'm not sure if it's more efficient to turn off debug; needs researching. 
    #app.run_server(debug=False)
