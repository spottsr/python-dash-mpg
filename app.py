from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import seaborn as sns


# Load data into Dataframe
df = sns.load_dataset('mpg')
df['model_year'] = df['model_year'] + 1900

app = Dash(__name__)
app.layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H2("Seaborn MPG Dataset App"),
                html.H5("Robert Spotts")    
            ],
            width=True,
            ),
        
        dbc.Row([
            html.Div([
                dcc.Graph(id='graph-with-slider'),
                dcc.Slider(
                    df['model_year'].min(),
                    df['model_year'].max(),
                    step=None,
                    value=df['model_year'].max(),
                    marks={str(year): str(year) for year in df['model_year'].unique()},
                    id='year-slider')
            ]),
            html.Div([
                dash_table.DataTable(id='filtered-datatable', page_size=25)
            ])

        ]),
        ])
    ])  
])

# Callback for slider to update graph
@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.model_year <= selected_year]

    fig = px.scatter(filtered_df, x="horsepower", y="mpg", color="origin", title="Relationship Between Horsepower vs MPG", log_x=False, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

# Callback for slider to update dattable
@callback(
    Output('filtered-datatable', 'data'),
    Input('year-slider', 'value'))
def update_table(selected_year):
    filtered_df = df[df.model_year <= selected_year]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)
