from world_bank_data_app import app
import json, plotly
from flask import render_template, request, Response, jsonify
from wrangling_scripts.wrangle_data import prepare_data


countries_dict = {
    "Italy": "ITA",
    "Egypt": "EGY",
    "Czech Republic": "CZE",
    "Brazil": "BRA",
    "Germany": "DEU",
    "United Arab Emirates": "ARE",
    "Spain": "ESP",
    "United State of America": "USA",
    "Japan": "JPN"
}

indicators_dict = {
    "Population (total)": "SP.POP.TOTL",
    "Forest Area (sq. KM)": "AG.LND.FRST.K2",
    "Population Growth Annual": "SP.POP.GROW",
    "CO2 Emissions (Kilo Ton)": 'EN.ATM.CO2E.KT'
}



@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():

    if (request.method == 'POST') and request.form:
        figures = prepare_data(request.form, indicators_dict)
        countries_selected = []

        for country in request.form.lists():
            countries_selected.append(country[1][0])

    else:
        figures = prepare_data(countries_dict, indicators_dict)
        countries_selected = []

        for keys, values in countries_dict.items():
            countries_selected.append(values)

    countries_code = list(map(list, countries_dict.items()))
    print("Countries code are", countries_code)

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                           all_countries=countries_code,
                           countries_selected=countries_selected)


@app.route('/contact_me')
@app.route('/contact_me.html')
def contact_me():
    return render_template('/contact_me.html')
