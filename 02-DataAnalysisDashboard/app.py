import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load Data
data = pd.read_csv("data/sales_data.csv")

# Create Dash App
app = Dash(__name__)
app.title = "Sales Data Analysis Dashboard"

# Layout
app.layout = html.Div([
    html.H1("📊 Sales Analysis Dashboard", style={'textAlign': 'center'}),
    html.P("Filter data by region:", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='region_filter',
        options=[{'label': region, 'value': region} for region in data['Region'].unique()],
        value=data['Region'].unique()[0],
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ),

    dcc.Graph(id='sales_chart'),
    dcc.Graph(id='profit_chart')
])

# Callbacks
@app.callback(
    [Output('sales_chart', 'figure'),
     Output('profit_chart', 'figure')],
    [Input('region_filter', 'value')]
)
def update_charts(selected_region):
    filtered = data[data['Region'] == selected_region]
    sales_fig = px.bar(filtered, x='Month', y='Sales', title='Monthly Sales')
    profit_fig = px.line(filtered, x='Month', y='Profit', title='Monthly Profit Trend')
    return sales_fig, profit_fig


if __name__ == "__main__":
    app.run(debug=True)
