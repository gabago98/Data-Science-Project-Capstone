# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load SpaceX data into a pandas DataFrame
spacex_df = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv',
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str}
)

# Get minimum and maximum payload values for slider settings
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create Dash application instance
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    # Title for the dashboard
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown for selecting launch sites (Task 1)
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',  # Default to 'All Sites'
        placeholder="Select a Launch Site",
        searchable=True
    ),
    
    html.Br(),
    
    # Pie chart for success count by site (Task 2)
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),
    
    # Label for the payload slider
    html.P("Payload range (Kg):"),
    
    # Range slider for selecting payload range (Task 3)
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),
    
    # Scatter plot for payload vs. success (Task 4)
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for updating the pie chart based on selected site
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    # Filter data for successful launches
    success_df = spacex_df[spacex_df['class'] == 1]
    if selected_site == 'ALL':
        # Show total success count by site if 'ALL' is selected
        fig = px.pie(
            success_df, 
            values='class', 
            names='Launch Site', 
            title='Total Successful Launches by Site'
        )
    else:
        # Show success vs failure counts for the selected site
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(
            site_df, 
            names='class', 
            title=f'Launch Outcomes for {selected_site}'
        )
    return fig

# Callback for updating scatter plot based on site and payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    # Filter data by selected payload range
    low, high = payload_range
    payload_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site == 'ALL':
        # Plot for all sites if 'ALL' is selected
        fig = px.scatter(
            payload_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category',
            title='Payload vs. Success Outcomes for All Sites'
        )
    else:
        # Plot for a specific site
        site_df = payload_df[payload_df['Launch Site'] == selected_site]
        fig = px.scatter(
            site_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category',
            title=f'Payload vs. Success Outcomes for {selected_site}'
        )
    return fig

# Run the application
if __name__ == '__main__':
    app.run_server()
