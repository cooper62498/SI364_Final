import re

import plotly.graph_objs as go
import plotly.plotly as py
from plotly.offline import plot

from ski.models import Geography, Mountain


def plot_map():
    state_abbr_dict = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
    }

    geo = Geography.objects.values()
    data = []
    for x in geo:
        data.append(
            (x["latitude"], x["longitude"], Mountain.objects.get(id=x["mountain_id"]))
        )

    max_snow = max([float(x[2].new_snow) for x in data])
    data = [
        go.Scattergeo(
            locationmode="USA-states",
            lon=[x[1] for x in data if float(x[2].new_snow) > 0],
            lat=[x[0] for x in data if float(x[2].new_snow) > 0],
            text=[
                '{} ({}) <br>{}"'.format(
                    x[2].name, state_abbr_dict[str(x[2].state_name)], x[2].new_snow
                )
                for x in data
                if float(x[2].new_snow) > 0
            ],
            hoverinfo="text",
            mode="markers",  #'markers+text'
            marker=dict(
                size=8,
                opacity=0.8,
                reversescale=True,
                autocolorscale=False,
                symbol="square",
                line=dict(width=1, color="rgba(102, 102, 102)"),
                cmax=max_snow,
                cmin=0,
                color=[float(x[2].new_snow) for x in data if float(x[2].new_snow) > 0],
                colorbar=dict(title="New Snowfall"),
                colorscale="Jet",
            ),
        )
    ]

    layout = dict(
        title="Hover over the marker for each mountains name and snowfall<br>Locations with No New snowfall are not shown",
        autosize=True,
        geo=dict(
            scope="usa",
            projection=dict(type="albers usa"),
            showland=True,
            landcolor="rgb(250, 250, 250)",
            subunitcolor="rgb(217, 217, 217)",
            countrycolor="rgb(217, 217, 217)",
            countrywidth=0.5,
            subunitwidth=0.5,
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    # url = py.plot(fig, filename='US-Ski-Mountains',auto_open=False)
    plot_div = plot(fig, output_type="div", include_plotlyjs=True, auto_open=False)
    res = re.search('<div id="([^"]*)"', plot_div)
    div_id = res.groups()[0]
    return (plot_div, div_id)
