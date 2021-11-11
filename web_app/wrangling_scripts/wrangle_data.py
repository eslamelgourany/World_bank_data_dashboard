import pandas as pd
import requests
import plotly.graph_objs as go


def prepare_data(countries_dict, indicators_dict):

    '''
    Args:
        countries_dict: Dictionary of countries that you need to process, keys are strings and values are 3 iso code
        indicators_dict: Dictionary of indicators that you need to process, keys are strings and values are
        indicators code from the world data bank.

    Returns:
        figures: List of figures that has cleaned data and layout
    '''

    countries_iso_lst = list()
    data_frames = list()

    # Create list of iso countries and prepare it for the API call.
    for country, iso_code in countries_dict.items():
        countries_iso_lst.append(iso_code.lower())
    all_countries = ';'.join(countries_iso_lst)

    # Loop through the dict and get the URls
    for keys, values in indicators_dict.items():
        url = f'http://api.worldbank.org/v2/countries/{all_countries}/indicator/{values}/?date=2010:2018&per_page=1000&format=json'
        r = requests.get(url)
        data = r.json()[1]
        for i, value in enumerate(data):
            value['indicator'] = value['indicator']['value']
            value['country'] = value['country']['value']

        # Append the data to data_frames list
        data_frames.append(data)

    # Chart 1: Total population for the targeted countries per defined year frame.
    graph_one = []
    df_one = pd.DataFrame(data_frames[0])
    country_list = df_one.country.unique().tolist()

    for country in country_list:
        x_val = df_one[df_one['country'] == country].date.tolist()
        y_val = df_one[df_one['country'] == country].value.tolist()
        graph_one.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country
            )
        )

    layout_one = dict(title='Total Population for countries per year', xaxis=dict(title='Year',
                      autotick=True, tick0=2010, dtick=5), yaxis=dict(title='Population (total)'))

    # Chart 2: Forest Areas for countries per year 2018
    graph_two = []
    df_two = pd.DataFrame(data_frames[1])
    df_two.sort_values('value', ascending=False, inplace=True)
    df_two = df_two[df_two['date'] == '2018']
    graph_two.append(
        go.Bar(
            x=df_two.country.tolist(),
            y=df_two.value.tolist(),
        )
    )

    layout_two = dict(title='Forest Areas (sq. KM) in 2018',
                      xaxis=dict(title='Country'), yaxis=dict(title='sq. KM'))

    # Chart 3: Annual Population Growth per year
    graph_three = []
    df_three = pd.DataFrame(data_frames[2])
    for country in country_list:
        x_val = df_three[df_three['country'] == country].date.tolist()
        y_val = df_three[df_three['country'] == country].value.tolist()
        graph_three.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country
            )
        )

    layout_three = dict(title='Annual population growth per year', xaxis=dict(title='Year', autotick=True, tick0=2010, dtick=5)
                        , yaxis=dict(title='Population growth (annual%)'))

    # Chart 4: CO2 Emissions per year for list of countries
    graph_four = []
    df_four = pd.DataFrame(data_frames[3])
    for country in country_list:
        x_val = df_four[df_four['country'] == country].date.tolist()
        y_val = df_four[df_four['country'] == country].value.tolist()
        graph_four.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country
            )
        )

    layout_four = dict(title='CO2 Emission for countries per year', xaxis=dict(title='Year', autotick=True, tick0=2010, dtick=5),
                       yaxis=dict(title='kiloton of CO2'))

    # Chart 5: CO2 Emissions for Germany per year
    graph_five = []
    df_five = pd.DataFrame(data_frames[3])
    print("unique is", df_five['country'].unique())
    df_five = df_five[df_five['country'] == 'Germany']

    graph_five.append(
        go.Bar(
            x=df_five.date.tolist(),
            y=df_five.value.tolist(),
        )
    )

    layout_five = dict(title='CO2 Emission in Germany per year', xaxis=dict(title='Year'),
                       yaxis=dict(title='(kTon)'))

    # Append graphs and layouts in dict to prepare it for the Frontend.
    figures = list()
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))

    return figures
