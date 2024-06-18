from functools import partial
from dash import callback, Input, Output

from dashboard.helper_functions import read_data
from dashboard.location_app_functions import (_create_population_chart, _create_gdp_chart,
                                              _create_life_exp_chart, _create_choropleth_map, update_app,
                                              create_app, create_widgets)

filename = 'location_statistics.csv'
data_df = read_data(filename)
data_df = data_df.round({'Life Expectancy': 2, 'GDP per Capita': 2, 'Centroid Longitude': 2, 'Centroid Latitude': 2})

create_population_chart = partial(_create_population_chart, data_df)
create_gdp_chart = partial(_create_gdp_chart, data_df)
create_life_exp_chart = partial(_create_life_exp_chart, data_df)
create_choropleth_map = partial(_create_choropleth_map, data_df)

continents = data_df.Continent.unique()
years = data_df.Year.unique()

[continent_population, year_population, continent_gdp,
 year_gdp, continent_life_exp, year_life_exp, year_map, var_map] = create_widgets(continents, years)

app = create_app()
app = update_app(app, data_df, continent_population, year_population, continent_gdp, year_gdp, continent_life_exp,
                 year_life_exp, year_map, var_map)


@callback(Output("population", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value"), ])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)


@callback(Output("gdp", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value"), ])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)


@callback(Output("life_expectancy", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value"), ])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)


@callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value"), ])
def update_map(var_map, year):
    return create_choropleth_map(var_map, year)


if __name__ == "__main__":
    app.run(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
