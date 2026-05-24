# Setup
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),
                                html.Br(),

                                # Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 100: '100'},
                                value=[min_payload, max_payload]),

                                # Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='Launch Site', 
        title='Success Count for all launch sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df,
                    names='class', 
                    title=f'Total Success Launches for the site {entered_site}')
        return fig

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, payload):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,
        x='Payload Mass (kg)', y="class",
        color="Booster Version Category",
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = filtered_df[(filtered_df['Launch Site'] == entered_site)
        & (filtered_df['Payload Mass (kg)'] >= payload[0])
        & (filtered_df['Payload Mass (kg)'] <= payload[1])
        ]
        
        fig = px.scatter(filtered_df,
        x='Payload Mass (kg)', y="class",
        color="Booster Version Category",
        title='Correlation between Payload and Success for the site {entered_site}') 

        return fig


# Run the app
if __name__ == '__main__':
# Scope: Only accessible from the local machine
#    app.run()   # default port: 8050

# The port might be already in use. Try a different port:
# Scope: Only accessible from the local machine
     #app.run(port=8051, debug=True)

     # Scope: Accessible from local machine AND other devices on the network
     app.run(host='0.0.0.0', port=8050, debug=True) # (using 0.0.0.0 instead of 127.0.0.1), TO run http://localhost:8050 in browser.
