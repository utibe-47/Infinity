from dash import html, dcc, Dash
from plotly import graph_objects as go, express as px


def create_table(data):
    fig = go.Figure(data=[go.Table(
        header=dict(values=data.columns, align='left'),
        cells=dict(values=data.values.T, align='left'))
    ]
    )
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0, "l": 0, "r": 0, "b": 0}, height=700)
    return fig


def _create_population_chart(data, continent="Asia", year=1952):
    filtered_df = data[(data.Continent == continent) & (data.Year == year)]
    filtered_df = filtered_df.sort_values(by="Population", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="Population", color="Country",
                 title="Country {} for {} Continent in {}".format("Population", continent, year),
                 text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def _create_gdp_chart(data, continent="Asia", year=1952):
    filtered_df = data[(data.Continent == continent) & (data.Year == year)]
    filtered_df = filtered_df.sort_values(by="GDP per Capita", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="GDP per Capita", color="Country",
                 title="Country {} for {} Continent in {}".format("GDP per Capita", continent, year),
                 text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def _create_life_exp_chart(data, continent="Asia", year=1952):
    filtered_df = data[(data.Continent == continent) & (data.Year == year)]
    filtered_df = filtered_df.sort_values(by="Life Expectancy", ascending=False).head(15)

    fig = px.bar(filtered_df, x="Country", y="Life Expectancy", color="Country",
                 title="Country {} for {} Continent in {}".format("Life Expectancy", continent, year),
                 text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def _create_choropleth_map(data, variable, year):
    filtered_df = data[data.Year == year]

    fig = px.choropleth(filtered_df, color=variable,
                        locations="ISO Alpha Country Code", locationmode="ISO-3",
                        color_continuous_scale="RdYlBu", hover_data=["Country", variable],
                        title="{} Choropleth Map [{}]".format(variable, year))
    fig.update_layout(dragmode=False, paper_bgcolor="#e5ecf6", height=600, margin={"l": 0, "r": 0})
    return fig


def update_app(app, data, continent_population, year_population, continent_gdp, year_gdp, continent_life_exp,
               year_life_exp, year_map, var_map):
    app.layout = html.Div([
        html.Div([
            html.H1("Regional Population Analysis", className="text-center fw-bold m-2"),
            html.Br(),
            dcc.Tabs([
                dcc.Tab([html.Br(),
                         dcc.Graph(id="dataset", figure=create_table(data))], label="Dataset"),
                dcc.Tab([html.Br(), "Continent", continent_population, "Year", year_population, html.Br(),
                         dcc.Graph(id="population")], label="Population"),
                dcc.Tab([html.Br(), "Continent", continent_gdp, "Year", year_gdp, html.Br(),
                         dcc.Graph(id="gdp")], label="GDP Per Capita"),
                dcc.Tab([html.Br(), "Continent", continent_life_exp, "Year", year_life_exp, html.Br(),
                         dcc.Graph(id="life_expectancy")], label="Life Expectancy"),
                dcc.Tab([html.Br(), "Variable", var_map, "Year", year_map, html.Br(),
                         dcc.Graph(id="choropleth_map")], label="Choropleth Map"),
            ])
        ], className="col-8 mx-auto"),
    ], style={"background-color": "#e5ecf6", "height": "100vh"})
    return app


def create_app():
    css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
    app = Dash(name="Dash Dashboard", external_stylesheets=css)
    return app


def create_widgets(continents, years):
    continent_population = dcc.Dropdown(id="cont_pop", options=continents, value="Asia", clearable=False)
    year_population = dcc.Dropdown(id="year_pop", options=years, value=1952, clearable=False)

    continent_gdp = dcc.Dropdown(id="cont_gdp", options=continents, value="Asia", clearable=False)
    year_gdp = dcc.Dropdown(id="year_gdp", options=years, value=1952, clearable=False)

    continent_life_exp = dcc.Dropdown(id="cont_life_exp", options=continents, value="Asia", clearable=False)
    year_life_exp = dcc.Dropdown(id="year_life_exp", options=years, value=1952, clearable=False)

    year_map = dcc.Dropdown(id="year_map", options=years, value=1952, clearable=False)
    var_map = dcc.Dropdown(id="var_map", options=["Population", "GDP per Capita", "Life Expectancy"],
                           value="Life Expectancy", clearable=False)
    return continent_population, year_population, continent_gdp, year_gdp, continent_life_exp, year_life_exp, year_map, var_map
