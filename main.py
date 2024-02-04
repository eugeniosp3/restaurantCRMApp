# pragmaticoders
# escapingtutorialhell.com

from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

# External scripts for Tailwind CSS CDN
external_scripts = [{'src': 'https://cdn.tailwindcss.com'}]

app = Dash(__name__, external_scripts=external_scripts)
df = pd.read_csv("cleaned_historic_inspections.csv")
df["Roadway Dimensions (Area)"] = df["Roadway Dimensions (Area)"].fillna(
    0).astype(float)
columnsLowercase = ["Qualify Alcohol",
                    "Landmark District or Building", "Approved for Sidewalk Seating", 'Approved for Roadway Seating']
for column in columnsLowercase:
    df[column] = df[column].str.title()
mapDF = df
restaurantData = pd.DataFrame()

matchingFacilityHeader = "text-sm text-slate-50 font-medium"
matchingFacilityObject = "text-xs text-slate-50"
matchingFacilityBodyLayout = "flex flex-col items-start gap-1"
restaurantsAvailable = ["Select Restaurant"]

# TODO: turn this into a function i can import to keep code clean
fig = px.scatter_mapbox(mapDF, lat="Latitude", lon="Longitude",
                        color="Qualify Alcohol", size="Roadway Dimensions (Area)",
                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                        mapbox_style="carto-positron")

# Update the figure properties
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
    )
)

# Main Layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        # our drop downs are going to go
                        dcc.Dropdown(mapDF['Borough'].unique(), id='Borough',
                                     multi=False, value=mapDF['Borough'].unique()[0], className="w-[200px] text-slate-600"),
                        dcc.Dropdown(mapDF['Qualify Alcohol'].unique(), id='AlcoholYN',
                                     multi=False, value=mapDF['Qualify Alcohol'].unique()[0], className="w-[200px] text-slate-600"),
                        dcc.Dropdown(mapDF['Landmark District or Building'].unique(), id='LandmarkYN',
                                     multi=False, value=mapDF['Landmark District or Building'].unique()[0], className="w-[200px] text-slate-600"),
                        dcc.Dropdown(mapDF['Seating Interest (Sidewalk/Roadway/Both)'].unique(), id='SeatingInterest',
                                     multi=False, value=mapDF['Seating Interest (Sidewalk/Roadway/Both)'].unique()[0], className="w-[200px] text-slate-600"),
                        dcc.Dropdown(mapDF['Approved for Sidewalk Seating'].unique(), id='SidewalkOptions',
                                     multi=False, value=mapDF['Approved for Sidewalk Seating'].unique()[0], className="w-[200px] text-slate-600"),
                        dcc.Dropdown(mapDF['Approved for Roadway Seating'].unique(), id='RoadwayOptions',
                                     multi=False, value=mapDF['Approved for Sidewalk Seating'].unique()[1], className="w-[200px] text-slate-600"),
                        # text in our header goes here
                        html.Div([
                            html.P("Records Matching",
                                   className=matchingFacilityHeader),
                            html.Div(id="recordsMatchingBeforeRestaurant",
                                     className=matchingFacilityObject),
                        ],
                        )
                    ],
                    className="w-full h-[10%] bg-slate-800 text-white text-center flex justify-evenly items-center",
                ),
                html.Div([
                    html.Div([dcc.Graph(id='map', figure=fig, style={'height': '850px'})],
                             className="h-full w-full", id="mapHolderDiv",
                             ),
                    html.Div(
                        [
                            # our drop downs are going to go
                            dcc.Dropdown(restaurantsAvailable, id='RestaurantSelection',
                                         multi=False, value=restaurantsAvailable[0], className="w-[325px] text-slate-600"),
                            # text in our header goes here
                            html.Div([
                                html.P(
                                    className="text-md text-slate-50 font-semibold", id="desiredRestaurant"),

                            ],
                                className="",
                                id="RestaurantNameText"),
                            # location and contact info
                            html.Div([
                                html.P("Business Address",
                                       className=matchingFacilityHeader),
                                html.P(
                                    className=matchingFacilityObject, id="postcode"),
                                html.P(
                                    className=matchingFacilityObject, id="nta"),
                                html.P(
                                    className=matchingFacilityObject, id="boro"),
                                html.P(
                                    className=matchingFacilityObject, id="lat-long"),

                            ],
                                className=matchingFacilityBodyLayout,
                                id="RestaurantLocationInfo"),
                            # legal and compliance info
                            html.Div([
                                html.P("Legal and Compliance",
                                       className=matchingFacilityHeader),
                                html.P(
                                    className=matchingFacilityObject, id="hlthcompliance"),
                                html.P(
                                    className=matchingFacilityObject, id="dba"),
                                html.P(
                                    className=matchingFacilityObject, id="foodsvc"),
                                html.P(
                                    className=matchingFacilityObject, id="lglbizname"),

                            ],
                                className=matchingFacilityBodyLayout,
                                id="legalAndComplianceInfo"),

                            # alcohol info
                            html.Div([
                                html.P("Alcohol Licensure Information",
                                       className=matchingFacilityHeader),
                                html.P(
                                    className=matchingFacilityObject, id="qlfyalcohol"),
                                html.P(
                                    className=matchingFacilityObject, id="slalicense"),
                                html.P(
                                    className=matchingFacilityObject, id="slaserial"),

                            ],
                                className=matchingFacilityBodyLayout,
                                id="RestaurantAlcoholInfo"),

                            # sales info
                            html.Div([
                                html.P("Sales Realated Information",
                                       className=matchingFacilityHeader),
                                html.P(
                                    className=matchingFacilityObject, id="lndmrkOrBldg"),
                                html.P(
                                    className=matchingFacilityObject, id="lndmrkDistTrms"),
                                html.P(
                                    className=matchingFacilityObject, id="seatintrst-options"),
                                html.P(
                                    className=matchingFacilityObject, id="rdwyApproved"),
                                html.P(
                                    className=matchingFacilityObject, id="rdwyDimArea"),
                                html.P(
                                    className=matchingFacilityObject, id="rdwyDimLength"),
                                html.P(
                                    className=matchingFacilityObject, id="rdwyDimWidth"),
                                html.P(
                                    className=matchingFacilityObject, id="sidewalkseating"),
                                html.P(
                                    className=matchingFacilityObject, id="sidewalkDimArea"),
                                html.P(
                                    className=matchingFacilityObject, id="sidewalkDimLength"),
                                html.P(
                                    className=matchingFacilityObject, id="sidewalkDimWidth"),
                            ],
                                className=matchingFacilityBodyLayout,
                                id="SalesRelevantInfo"),

                            # past appliations submitted and when
                            html.Div([
                                html.P("Previous NYC Applications Submitted",
                                       className=matchingFacilityHeader),
                                html.P(
                                    className=matchingFacilityObject, id=""),
                                html.P(
                                    className=matchingFacilityObject, id=""),
                                html.P(
                                    className=matchingFacilityObject, id=""),
                                html.P(
                                    className=matchingFacilityObject, id=""),
                                html.P(
                                    className=matchingFacilityObject, id=""),
                            ],
                                className=matchingFacilityBodyLayout,
                                id="pastApplicationsSubmittedInfo")
                        ],
                        className="w-[25%] h-full bg-slate-400 text-white text-center flex flex-col items-start p-8 gap-2 overflow-scroll",
                    )], className="w-full h-[90%] flex flex-row ")],
            className="w-full h-full flex flex-col items-end ",),



    ],
    className="w-full h-screen bg-slate-50 overflow-hidden"
)


@app.callback(
    [Output("desiredRestaurant", "children"),
     Output('recordsMatchingBeforeRestaurant', 'children'),
     Output('RestaurantSelection', 'options'),
     Output('postcode', 'children'),
     Output('nta', 'children'),
     Output('boro', 'children'),
     Output('lat-long', 'children'),
     Output('hlthcompliance', 'children'),
     Output('dba', 'children'),
     Output('foodsvc', 'children'),
     Output('lglbizname', 'children'),
     Output('qlfyalcohol', 'children'),
     Output('slalicense', 'children'),
     Output('slaserial', 'children'),
     Output('lndmrkOrBldg', 'children'),
     Output('lndmrkDistTrms', 'children'),
     Output('seatintrst-options', 'children'),
     Output('rdwyApproved', 'children'),
     Output('rdwyDimArea', 'children'),
     Output('rdwyDimLength', 'children'),
     Output('rdwyDimWidth', 'children'),
     Output('sidewalkseating', 'children'),
     Output('sidewalkDimArea', 'children'),
     Output('sidewalkDimLength', 'children'),
     Output('sidewalkDimWidth', 'children')
     ],
    [Input('Borough', 'value'),
     Input('AlcoholYN', 'value'),
     Input('LandmarkYN', 'value'),
     Input('SeatingInterest', 'value'),
     Input('SidewalkOptions', 'value'),
     Input('RoadwayOptions', 'value'),
     Input('RestaurantSelection', 'value'),


     ]
)
def dataframeSlicers(borough, alcoholyn, landmarkyn, seatinginterest, sidewalkOptions, roadwayOptions, restaurantSelection):
    """
    function docstring

    Args:
        borough ([type]): [description]
        alcoholyn ([type]): [description]
        landmarkyn ([type]): [description]
        seatinginterest ([type]): [description]
        sidewalkOptions ([type]): [description]
        roadwayOptions ([type]): [description]
        restaurantSelection ([type]): [description]

    Returns:
        [type]: [description]

    """
    # filter the dataframe
    dfFiltering = mapDF[mapDF["Borough"] == borough]
    print(dfFiltering.shape[0])
    dfFiltering = dfFiltering[dfFiltering["Qualify Alcohol"] == alcoholyn]
    print(dfFiltering.shape[0])

    dfFiltering = dfFiltering[dfFiltering["Landmark District or Building"]
                              == landmarkyn]
    print(dfFiltering.shape[0])

    dfFiltering = dfFiltering[dfFiltering["Seating Interest (Sidewalk/Roadway/Both)"]
                              == seatinginterest]
    print(dfFiltering.shape[0])

    dfFiltering = dfFiltering[dfFiltering["Approved for Sidewalk Seating"]
                              == sidewalkOptions]
    print(dfFiltering.shape[0])

    dfFiltering = dfFiltering[dfFiltering["Approved for Roadway Seating"]
                              == roadwayOptions]
    print(dfFiltering.shape[0])

    # Update restaurantsAvailable based on filtered DataFrame
    restaurantsAvailable = [{'label': name, 'value': name}
                            for name in dfFiltering['Restaurant Name'].unique()]

    # Check to ensure there is always a default or a placeholder option
    if not restaurantsAvailable:
        restaurantsAvailable = [{'label': 'Select Restaurant', 'value': ''}]
    print("Restaurant Selection: ", restaurantSelection)

    restaurantfilter = dfFiltering[dfFiltering["Restaurant Name"]
                                   == restaurantSelection]
    # if the restaurantfilter has more than one option just return the first
    if restaurantfilter.shape[0] > 1:
        restaurantfilter = restaurantfilter.iloc[0]
    restaurantfilter.reset_index().to_csv("aRestaurant.csv", index=False)

    # Return the number of records found and the list of restaurants for the dropdown
    return restaurantSelection, dfFiltering.shape[0], restaurantsAvailable, restaurantfilter["Postcode"], restaurantfilter["NTA"], restaurantfilter["Borough"], (restaurantfilter["Latitude"], restaurantfilter["Longitude"]), restaurantfilter["healthCompliance_terms"], restaurantfilter["Doing Business As (DBA)"], restaurantfilter["Food Service Establishment Permit #"], restaurantfilter["Legal Business Name"], restaurantfilter["Qualify Alcohol"], restaurantfilter["SLA License Type"], restaurantfilter["SLA Serial Number"], restaurantfilter["Landmark District or Building"], restaurantfilter["landmarkDistrict_terms"], restaurantfilter["Seating Interest (Sidewalk/Roadway/Both)"], restaurantfilter["Approved for Roadway Seating"], restaurantfilter["Roadway Dimensions (Area)"], restaurantfilter["Roadway Dimensions (Length)"], restaurantfilter["Roadway Dimensions (Width)"], restaurantfilter["Approved for Sidewalk Seating"], restaurantfilter["Sidewalk Dimensions (Area)"], restaurantfilter["Sidewalk Dimensions (Length)"], restaurantfilter["Sidewalk Dimensions (Width)"]


if __name__ == "__main__":
    app.run_server(debug=True)
