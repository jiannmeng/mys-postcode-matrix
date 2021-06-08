# Getting started
## Dependencies
If you have Poetry installed on your computer, just run this command in the project root folder:
```
poetry install
```
If you prefer using pip (preferably in a virtual environment):
```
pip install -r requirements.txt
```

## API Key
If you are going to access the Google Maps API (notebook #4 in particular), you will need to obtain a Google Maps API key.

- Get your [API key](https://developers.google.com/maps/gmp-get-started). The key must have permission to use the Distance Matrix API.
- Copy the `.env.example` file, rename to `.env`, and paste in your Google Maps API key.

# Structure

- `data/` - Input data files with their hashes.
- `output/` - Data files from the notebooks.
- `responses/` - Storage area for all responses from Google Maps API. These cost money, so it's good to cache them.
- `src/` - python files

Notebooks are found in the root folder.

# Notebooks

We recommend going through the notebooks in numbered order:

1. Comparing the Pos Malaysia and postcode.my postcode databases. A simple heuristic is used to map missing postcodes from one set to the other.
2. Clean the Pos Malaysia data, and separate the postcodes into *master postcode* groupings.
3. Create a *distance matrix*: the distance between any two master postcodes in the same PPV region.
4. Use the Google Maps API to find the time taken to drive between any valid master postcode pair.
5. Take the API responses to create a *time matrix*: the time taken to drive between any valid master postcode pair.

# Key output files

The most important files in the `output/` folder:

- [`postcode.my-to-posm.csv`](./output/postcode.my-to-posm.csv) - A listing of all postcodes inside the postcode.my database, which are not in Pos Malaysia's database. For each of these, the most similar Pos Malaysia postcode is also given.
- [`posm-postcodes-core.csv`](./output/posm-postcodes-core.csv) - All Pos Malaysia postcodes, with their corresponding master postcode and state.
- [`time-matrix-sec.csv`](./output/time-matrix-sec.csv) - Time taken (in seconds) between any two master postcodes in the same PPV region. The [`minfloored`](./output/time-matrix-minfloored.csv) version is the same data but in minutes (rounded down).
