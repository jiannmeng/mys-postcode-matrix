`pip install -r requirements.txt`
Preferably in a virtual environment.

If you use Poetry, just `poetry install` instead and you're good to go.

You also need to copy the .env.example file, rename to .env, and paste your Google Maps API key.
Google Maps API permissions needed: Geocode API (for notebook 2), Distance Matrix (for notebook 3)

Structure:

data - Pos Malaysia input file
output - files generated throughout the notebooks
responses - storage area for all responses from Google Maps API. These cost money, so it's good to cache them.
src - python files

Notebooks:

#1 - Clean the Pos Malaysia data, and generate some master postcodes / distance matrix.
#2 - Can ignore for now. Investigating if the Pos Malaysia postcodes coordinates are close to Google Maps' coordinates
#3 - Use the Google Maps API to get the estimated time taken from one postcode coordinate to another.

