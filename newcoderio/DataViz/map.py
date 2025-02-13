import geojson

import parse as p

def create_map(data_file):
    """Creates a GeoJSON file.
    Returns a GeoJSON file that can be rendered in a GitHub
    Gist at gist.github.com.  Just copy the output file and
    paste into a new Gist, then create either a public or
    private gist.  GitHub will automatically render the GeoJSON
    file as a map.
    """

    # Define type of GeoJSON we're creating
    geo_map = {"type": "FeatureCollection"}

    # Define empty list to collect each point to graph
    item_list = []

    # Iterate over our data to create GeoJSOn document.
    # We're using enumerate() so we get the line, as well
    # the index, which is the line number.
    for index, line in enumerate(data_file):

        # Skip any zero coordinates as this will throw off
        # our map.
        if line['x'] == "0" or line['y'] == "0":
            continue

        # Setup a new dictionary for each iteration.
        data = {}

        # Assign line items to appropriate GeoJSON fields.
        data['type'] = 'Feature'
        data['id'] = index
        data['properties'] = {'Market Name': line['MarketName'],
                              'City': line['city'],
                              'Baked Goods': line['Bakedgoods'],
                              'Organic': line['Organic'],
                              'Wild Harvested': line['WildHarvested']}
        data['geometry'] = {'type': 'Point',
                            'coordinates': (line['x'], line['y'])}

        # Add data dictionary to our item_list
        item_list.append(data)

    # For each point in our item_list, we add the point to our
    # dictionary.  setdefault creates a key called 'features' that
    # has a value type of an empty list.  With each iteration, we
    # are appending our point to that list.
    for point in item_list:
        geo_map.setdefault('features', []).append(point)

    # Now that all data is parsed in GeoJSON write to a file so we
    # can upload it to gist.github.com
    with open('file_farmers.geojson', 'w') as f:
        f.write(geojson.dumps(geo_map))


def main():
    data = p.parse("farmers_market_data.csv", ",")

    return create_map(data)

if __name__ == '__main__':
    main()
