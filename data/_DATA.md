# Data Primer

## .sha256 Files

Each file has a corresponding .sha256 file with the same name. This contains the SHA-256 hash of the respective file, which was generated when the file was first obtained.

Occasionally, while working with these data files, we may accidentally make small changes to them. For example, we might hit save in Excel, or accidentally add a character in a .csv file without noticing.

To prevent this, we use the `src.utils` to store and check the hash of the file when importing. Use src.utils.store_hash to generate the hash, and use src.utils.check_hash before importing into a DataFrame to ensure that the file is exactly the same.

## Data Files

### Postcode - Lat Long.xlsx

A data file provided by Pos Malaysia ("PosM"). The data is mostly self explanatory:

- LOCATION
- POSTCODE
- POST_OFFICE - Probably district names, in CamelCase.
- POST_OFFICE_1 - This is similar to POST_OFFICE but with spaces between words.
- STATE
- DATEUPDATE
- POINT_X - Longitude in decimal degrees.
- POINT_Y - Latitude in decimal degrees.

We use Sheet2 only. Sheet1 appears to have the same data, but we haven't checked this.

When using pd.read_excel, for the POSTCODE column, we recommend passing in str to the dtype argument, or using src.utils.postcode_str to the converters argument. This forces the POSTCODE column to be a string instead of integer.

Do not expect any neat data in this file:

- Some STATES and POST_OFFICE/POST_OFFICE_1 values have inconsistent whitespace, capitalisation & `_x000D_` artifacts (an Excel newline marker), which need to be fixed/removed.
- A POSTCODE can appear multiple times, with different POST_OFFICE or even different STATE.
- A POSTCODE can have different POINT_X and POINT_Y coordinates if it appears multiple times, since one postcode could span multiple districts.
- Many different POSTCODES share the same POINT_X and POINT_Y coordinates.
- Some POSTCODEs have incorrect coordinates altogether. This is likely because the coordinates seem to be linked to the district; but certain STATEs have districts with the same name. The SQL / Vlookup used to generate this file probably matched on district name only, instead of (district, state) pairings.

To fix some of these issues, we have some manual corrections in:

- bad_postcode_data_Thev.xlsx
- ??

### dep_poskod_geo_web.csv

Data from the `postcode.my` website. Date of scraping is unknown. The data is self-explanatory:

- postcode
- state_given
- lat - Latitude in decimal degrees.
- lon - Longitude in decimal degrees.

The state-given strings are not exactly the same as the STATE column in PosM's data file. We will need to match the states manually.

postcode.my's postcodes are not exactly the same as PosM's postcodes. The coordinates may be different, and there are some postcodes in each file which are not in the other.

### bad_postcode_data_Thev.xslx

For PosM's data file, there are some POSTCODEs with outright incorrect coordinates. This file contains hand-corrected coordinates, which should be merged into the dataframe before further data analysis.

### json_1_states.json

A GeoJson file containing boundaries for each state. Note that the state names are not exactly the same as PosM's states, and will need some cleaning to match these up.

We use this to check that our given coordinates are really within a state's boundaries.

### [insert name here]

When checking whether postcode coordinates are within state boundaries, a few cropped in the wrong state. This file contains hand-corrected coordinates for these postcodes.