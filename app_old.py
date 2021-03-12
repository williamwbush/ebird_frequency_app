import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.validator_cache
from dash.dependencies import Input, Output
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('all_species_frequency_all_years_7f3d.csv')
df_counties = pd.read_csv('all_species_cfrequency.csv')
df_fchange = pd.read_csv('frequency_change2.csv')
df_irr = pd.read_csv('irr.csv')
df_inc = pd.read_csv('species_increasing.csv')
df_dec = pd.read_csv('species_decreasing.csv')
df_common = pd.read_csv('most_common.csv')
df_rarest = pd.read_csv('rarest_2020.csv')

winter_s = ''
species_s = ''

app.layout = html.Div([

    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Photos", href="photos", style={'color':'white'})),
            dbc.NavItem(dbc.NavLink("Tables", href="tables", style={'color':'white'})),
        ],
        brand="Home",
        brand_href="/",
        dark=True,
        color='dark',
        sticky='top'
    ),
    
    html.Br(),
    html.Br(),

    html.H1('Bird Frequency in Illinois Since 2000', style={'text-align': 'center'}),

    html.P('Data: eBird', style={'text-align': 'center'}),

    html.Br(),

    html.H6('Choose Year and Species', style={'text-align': 'center'}),

    dcc.Dropdown(id='select_winter',
                 options=[{'label': f'{c}/{c+1}', 'value': f'{c}/{c+1}'} for c in range(2020,1999,-1)],
                 placeholder='select years...',
                 multi=True,
                 value=['2020/2021','2019/2020','2018/2019','2017/2018','2016/2017','2015/2016','2014/2015','2013/2014','2012/2013',
                        '2011/2012','2010/2011','2009/2010','2008/2009','2007/2008','2006/2007','2005/2006','2004/2005','2003/2004',
                        '2002/2003','2001/2002','2000/2001'],
                 style={'width': '65%', 'margin':'auto'},
                 optionHeight=20,
                 persistence=True,
                 persistence_type='session'
                 ),
    dcc.Dropdown(id='select_species',
                 options=[{'label':f'{species.title()}','value':f'{species}'} for species in sorted(list(set(df['COMMON NAME'])))],
                 placeholder='select species...',
                 multi=True,
                 value=['Common Redpoll'],
                 style={'width': '65%', 'margin':'auto'},
                 optionHeight=20,
                 persistence=True,
                 persistence_type='session'
                 ),
    
    html.Br(),

    html.H5('Frequency 7-Day Average with Concurrent Years', style={'text-align': 'center'}),

    dcc.Graph(id='species_graph', figure={}),

    html.H5('Frequency 7-Day Average with Sequential Years', style={'text-align': 'center'}),

    dcc.Graph(id='single_timeline', figure={}),

    html.H5('Frequency by County', style={'text-align': 'center'}),

    html.Br(),

    dcc.Dropdown(id='map_species',
        options=[{'label':f'{species.title()}','value':f'{species}'} for species in sorted(list(set(df['COMMON NAME'])))],
        placeholder='select species...',
        multi=False,
        value='Common Redpoll',
        style={'width': '45%', 'margin':'auto'},
        optionHeight=20,
        persistence=True,
        persistence_type='session'
        ),
    
    html.Br(),

    html.H6('Month', style={'text-align': 'center'}),

    # html.Div(id='outer_container', children=[], style={'text-align':'center'}),

    dcc.Dropdown(id='month_dropdown',
        options=[{'label':'January','value':7}, {'label':'February','value':8}, {'label':'March','value':9}, {'label':'April','value':10}, {'label':'May','value':11}, 
                 {'label':'June','value':12}, {'label':'July','value':1}, {'label':'August','value':2}, {'label':'September','value':3}, {'label':'October','value':4}, 
                 {'label':'November','value':5}, {'label':'December','value':6}],
        placeholder='select month...',
        multi=False,
        value=7,
        style={'width': '40%', 'margin':'auto'},
        optionHeight=20,
        persistence=True,
        persistence_type='session'
        ),

    # dcc.Slider(
    #     id='month_slider',
    #     min=1,
    #     max=12,
    #     step=1,
    #     value=7,
    # ),

    dcc.Graph(id='county_choropleth', figure={}),

    html.Br(),

    html.H5('Average Yearly Frequency', style={'text-align': 'center'}),
    
    dcc.Graph(id='frequency_bar', figure={}),

    html.H5('Percent Change in Average Yearly Frequency', style={'text-align': 'center'}),

    dcc.Graph(id='frequency_change', figure={}),

    html.Br(),

    html.H5('Most Irruptive Species', style={'text-align': 'center'}),
    
    html.Br(),

    dcc.Graph(id='irruptive', figure={}),

    # px.bar(df_irr, x='RANK', y='MAX MIN RATIO',
    #        hover_data=['COMMON NAME', 'MAX MIN RATIO', 'MAX', 'MIN'], color='MAX MIN RATIO', height=400),

    dash_table.DataTable(
        id='irr_table',
        style_table={'width':'50%', 'margin':'auto'},
        columns=[{"name": i, "id": i} for i in df_irr.columns],
        data=df_irr.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="light grey"),
        style_data=dict(backgroundColor="lavender"),
        style_cell_conditional=[
        {'if': {'column_id': 'RANK'},
         'width': '30px'},
        {'if': {'column_id': 'COMMON NAME'},
         'width': '50px'},
        {'if': {'column_id': 'MAX MIN RATIO'},
         'width': '30px'},
        {'if': {'column_id': 'MAX'},
         'width': '30px'},
        {'if': {'column_id': 'MIN'},
         'width': '30px'},
        {'if': {'column_id': 'DIFF'},
         'width': '30px'},
    ]),

    html.Br(),
    html.Br(),

    html.H5('Species with Declining Frequencies', style={'text-align': 'center'}),
    
    html.P('(species with greatest percent decrease in frequency between 2001–2003 and 2018–2020)', style={'text-align': 'center'}),

    html.Br(),

    dash_table.DataTable(
        id='dec_table',
        style_table={'width':'50%', 'margin':'auto'},
        columns=[{"name": i, "id": i} for i in df_dec.columns],
        data=df_dec.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="light grey"),
        style_data=dict(backgroundColor="lavender"),
        style_cell_conditional=[
        {'if': {'column_id': 'RANK'},
         'width': '30px'},
        {'if': {'column_id': 'COMMON NAME'},
         'width': '50px'},
        {'if': {'column_id': 'FREQUENCY PCT DECREASE'},
         'width': '30px'},
        {'if': {'column_id': 'MAX'},
         'width': '30px'},
        {'if': {'column_id': 'MIN'},
         'width': '30px'},
        {'if': {'column_id': 'DIFF'},
         'width': '30px'},
    ]),

    html.Br(),
    html.Br(),

    html.H5('Species with Increasing Frequencies', style={'text-align': 'center'}),

    html.P('(species with greatest percent increase in frequency between 2001–2003 and 2018–2020)', style={'text-align': 'center'}),

    html.Br(),

    dash_table.DataTable(
        id='inc_table',
        style_table={'width':'50%', 'margin':'auto'},
        columns=[{"name": i, "id": i} for i in df_inc.columns],
        data=df_inc.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="light grey"),
        style_data=dict(backgroundColor="lavender"),
        style_cell_conditional=[
        {'if': {'column_id': 'RANK'},
         'width': '30px'},
        {'if': {'column_id': 'COMMON NAME'},
         'width': '50px'},
        {'if': {'column_id': 'FREQUENCY PCT INCREASE'},
         'width': '30px'},
    ]),

    html.Br(),
    html.Br(),

    html.H5('Most Common Species In My Checklists', style={'text-align': 'center'}),

    html.Br(),

    dash_table.DataTable(
        id='common',
        style_table={'width':'50%', 'margin':'auto'},
        columns=[{"name": i, "id": i} for i in df_common.columns],
        data=df_common.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="light grey"),
        style_data=dict(backgroundColor="lavender"),
        style_cell_conditional=[
        {'if': {'column_id': 'RANK'},
         'width': '30px'},
        {'if': {'column_id': 'COMMON NAME'},
         'width': '50px'},
        {'if': {'column_id': 'CHECKLISTS'},
         'width': '30px'},
    ]),

    html.Br(),
    html.Br(),

    html.H5('Rarest Species I Observed in 2020', style={'text-align': 'center'}),

    html.P('(species with lowest frequency in 2020)', style={'text-align': 'center'}),

    html.Br(),

    dash_table.DataTable(
        id='rarest',
        style_table={'width':'50%', 'margin':'auto'},
        columns=[{"name": i, "id": i} for i in df_rarest.columns],
        data=df_rarest.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="light grey"),
        style_data=dict(backgroundColor="lavender"),
        style_cell_conditional=[
        {'if': {'column_id': 'RANK'},
         'width': '20px'},
        {'if': {'column_id': 'COMMON NAME'},
         'width': '30px'},
        {'if': {'column_id': 'FREQUENCY'},
         'width': '30px'},
    ]),
    
    html.Br(),
    html.Br(),

    html.P('eBird Basic Dataset. Version: EBD_relJan-2021. Cornell Lab of Ornithology, Ithaca, New York. Jan 2021.', style={'text-align': 'center'})
])


@app.callback(
    [Output(component_id='species_graph', component_property='figure'),
     Output(component_id='single_timeline', component_property='figure'),
     Output(component_id='county_choropleth', component_property='figure'),
     Output(component_id='frequency_change', component_property='figure'),
     Output(component_id='frequency_bar', component_property='figure'),
     Output(component_id='irruptive', component_property='figure')],
    [Input(component_id='select_winter', component_property='value'),
     Input(component_id='select_species', component_property='value'),
     Input(component_id='month_dropdown', component_property='value'),
     Input(component_id='map_species', component_property='value')]
)


def update_graph(winter_selected, species_selected, month_selected, map_species):
    
    dfc = df.copy()
    
    # fig = px.line()
    
    # fig_timeline = fig

    if species_selected and winter_selected and map_species:
        dfc = dfc[(dfc['OBSERVATION WINTER'].isin(winter_selected)) & (dfc['COMMON NAME'].isin(species.upper() for species in species_selected))]
    else:
        return dash.no_update

    # GRAPH DAILY FREQUENCY YEARS COMBINED

    if len(species_selected) > 1:
        color = 'COMMON NAME'
    else:
        color = 'NAME AND YEARS'

    fig = px.line(dfc, x='DAY OF SEASON', y='FREQUENCY 7 DAY RA', color=color, line_group='NAME AND YEARS')

    fig.update_layout(
                    xaxis_title='Date',
                    yaxis_title='Frequency (Percent of Checklists)',
                    xaxis=dict(tickmode='array',
                                tickvals=[0,31,62,92,123,153,184,215,243,274,304,335,365],
                                ticktext=['July','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul']),
                    hoverlabel=dict(
                                font_size=12,
                                font_family="Rockwell"))

    # GRAPH DAILY FREQUENCY YEARS SEPARATED

    fig_timeline = px.line(dfc, x='OBSERVATION DATE', y='FREQUENCY 7 DAY RA', color=color, line_group='NAME AND YEARS')

    fig_timeline.update_layout(
                    xaxis_title='Date',
                    yaxis_title='Frequency (Percent of Checklists)',
                    hoverlabel=dict(
                                    font_size=12,
                                    font_family="Rockwell"))

    # GRAPH FREQUENCY BY COUNTY WITH CHOROPLETH

    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month_selected = ((month_selected + 6) % 12) or 12

    df_counties_s = df_counties[df_counties['COMMON NAME'] == map_species.upper()]

    df_counties_m = df_counties_s[df_counties_s['OBSERVATION MONTH'] == month_selected]

    fmax = list(df_counties_s['FREQUENCY'])
    fmax = max(fmax)
    
    fig_choropleth = px.choropleth(df_counties_m, geojson=counties, locations='FIPS', color='FREQUENCY',
                           color_continuous_scale="Viridis",
                           range_color=(0, fmax),
                           scope="usa",
                           labels={'COUNTY':'county','FREQUENCY':'frequency'},
                          )
    fig_choropleth.update_geos(fitbounds="locations", visible=False)
    fig_choropleth.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # GRAPH YEARLY FREQUENCY
    
    fchange_species = df_fchange[df_fchange['COMMON NAME'].str.lower().isin(species.lower() for species in species_selected)]
    fig_fchange_bar = px.bar(fchange_species, x='YEAR',y='FREQUENCY', color='COMMON NAME', barmode='group')

    # GRAPH YEARLY FREQUENCY CHANGE

    fig_fchange = px.bar(fchange_species, x='YEAR', y='FREQUENCY CHANGE', color='COMMON NAME', barmode='group')

    # GRAPH TABLE OF TOP IRRUPTIVE SPECIES

    irruptive_species = px.bar(df_irr, x='RANK', y='MAX MIN RATIO', log_y=True,
           hover_data=['COMMON NAME', 'MAX MIN RATIO', 'MAX', 'MIN'], color='MAX MIN RATIO', height=400)


      
    return fig, fig_timeline, fig_choropleth, fig_fchange, fig_fchange_bar, irruptive_species


if __name__ == '__main__':
    app.run_server(debug=True)