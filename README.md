# This project aims for visualizing Indo-Aryan language family via digitalize and interactive map.
## Directory structure-:
1. assets folder-: Contains update.geojson, which is the geo data files containing coordinates for various districts used in this project.
2. combine.py-: Main file for running the app. Basically contains all the code to generate all the interactive map.
3. filter.py-: This is the source code for filtering and reducing the refined.geojson and storing it in under assets folder. It is to note that filtering is necessary for faster rendering and also as this code also capitalize all the names which exist in refined.geojson.
4. home_page.py-: this is the Home Page of our app.
5. physical_streamlit.py-: source code to generate physical map and storing it with physical_streamlit.html, which is finallly used to render in dash.
6. tree_data.py-: Data file for the Indo-Aryan family tree, contains almost all the language which are there under this family.
7. data_refined.csv-: Data file containing State, District and the major language spoken there.
8. lang_dialects.csv-: Data file containing all the other sub-dialects of major languages. 
9. indo_aryan_boundaries.json-: Coordinate file for the lines drawn in physical map (physical_streamlit.py / physical_streamlit.html)
10. physical_languages.json-: Data file containing position and degree value for various languages which are displayed in physical map.
11. refined.geojson-: Original data coordinate file for various districts. Change this file as it is much easy to with this file and then filter it to get update.geojson. REFER to point 3.
12. physical_streamlit.html-: physical map file, can be opened by double clicking on it as it is just a normal html file, generated from physical_streamlit.py
13. coordinates.js-: File to generate randome samples for coordinate, See NOTE section below to understand it better.

## Instructions to use it:
1. First install all the requirements as mentioned in requirement.txt
2. Then come inside Final directory by using command: cd Final
3. Then launch the app by: python combine.py
4. There in terminal comes a link for local host. ctrl+click or copy and paste in any browser to launch it.

## Instructions to change data files:
1. To change coordinate file, change only refined.geojson, then filter it via filter.py
2. To change major language spoken-: Change data_refined.csv
3. To change sub-dialects of a language-: change lang_dialects.csv
4. To change lines of physical map-: change indo_aryan_boundaries.json file
5. To change orientation and location of languages in physical map-: change physical_languages.json file

**NOTE-:** To find the coordinates for any line use-: https://codepen.io/jhawes/pen/xxBVZY?editors=1111 link to generate random samples and change its javascript(js) code with coordinates.js
