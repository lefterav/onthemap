import pandas as pd
import plotly.express as px
from tqdm import (tqdm)
from geopy.geocoders import Nominatim
import time
import json
from argparse import ArgumentParser

# List of cities and institutions
locations = [
    "Reykjavik, Iceland", "Amsterdam, Netherlands", "Athens, Greece", "Bilbao, Spain", "Pittsburgh, USA",
    "Prague, Czech Republic", "Copenhagen, Denmark", "Dublin, Ireland", "Rabat, Morocco", "Edinburgh, UK",
    "Ghent, Belgium", "Groningen, Netherlands", "Hildesheim, Germany", "Paris, France", "Lisbon, Portugal",
    "Baltimore, USA", "Nancy, France", "Ann Arbor, USA", "Boston, USA", "Ottawa, Canada", "Oslo, Norway",
    "Philadelphia, USA", "Montreal, Canada", "Seoul, South Korea", "Saarbrücken, Germany", "Surrey, UK",
    "Tilburg, Netherlands", "Dublin, Ireland", "Darmstadt, Germany", "Zurich, Switzerland", "London, UK", "Kara, Togo",
    "Barcelona, Spain", "Tokyo, Japan", "Trento, Italy", "Helsinki, Finland", "Thessaloniki, Greece", "Roma, Italy",
    "Gothenburg, Sweden", "Lucerne, Switzerland", "Salzburg, Austria", "Melbourne, Australia",
    "Abu Dhabi, United Arab Emirates",  "Hangzhou, China", "Palo Alto, USA", "Mountain View, USA", "Hyderabad, India"
]


def get_geo_data(locations):
    global geo_data
    # Geocode cities
    geolocator = Nominatim(user_agent="collab_mapper")
    geo_data = []

    for city in tqdm(locations):
        try:
            location = geolocator.geocode(city)
            if location:
                geo_data.append({
                    "City": city,
                    "Latitude": location.latitude,
                    "Longitude": location.longitude
                })
            time.sleep(1)  # To respect rate limits
        except Exception as e:
            print(f"Error geocoding {city}: {e}")


    with open('data.json', 'w') as f:
        json.dump(geo_data, f)
    return geo_data


def plot_on_the_map(geo_data):



    # Create DataFrame
    df = pd.DataFrame(geo_data)

    # Plot map
    fig = px.scatter_geo(df,
                         lat='Latitude',
                         lon='Longitude',
                         hover_name='City',
                         title='University Collaborations by City',
                         projection='mercator',
                         width=1200,  # Increase width
                         height=800)  # Increase height
    fig.update_geos(
        showland=True, landcolor="rgb(240, 240, 240)",
        showocean=True, oceancolor="rgb(200, 230, 255)",
        showlakes=True, lakecolor="rgb(200, 230, 255)",
        showrivers=True, rivercolor="rgb(180, 210, 230)",
        showcountries=True, countrycolor="rgb(200, 200, 200)"
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    fig.show()
    fig.write_image("university_collaborations_map.png")
    fig.write_html("university_collaborations_map.html")


if __name__ == "__main__":

    parser = ArgumentParser(description="Geocode locations and plot them on a map.")
    parser.add_argument("--plot_locations", type=str, nargs="*", help="Plot geodata given in json format")
    args = parser.parse_args()

    if args.plot_locations:
        with open(args.plot_locations[0], 'r') as f:
            geo_data = json.load(f)
        plot_on_the_map(geo_data)
    else:
        geo_data = get_geo_data(locations)
        plot_on_the_map(geo_data)
