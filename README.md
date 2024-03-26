# Yelp crawler

The yelp crawler that scraps all the businesses from Yelp website

The crawler returned a file with json objects, each json representing a business from the given search results.
Each business have the following data:

● Business name
● Business rating
● Number of reviews
● Business yelp url
● Business website
● List of first 5 reviews, for each review:
    - Reviewer name
    - Review raiting
    - Review date

#### src
Consists of:
  - `app` - the files necessary for the application's operation are located in this directory;
    - `data_objects` - package contains the files responsible for the logic of forming search data.
    - `searchers` - package contains the files that provide the logic for searching raw data on Yelp resources
  - `crawler.py` - The file that consolidates the process of collecting and transforming data."

## Installation
- Ubuntu
- Python3.8

## Setup
Install virtualenv in project folder.
```shell script
[project_folder]$ python3 -m venv venv
``` 
```shell script
[project_folder]$ source  venv/bin/activate
``` 

Install the requirements:

[project_folder]$ pip install requirements.txt

The main scripts are specified in the `main.py` file.

#### Run script from console

`python main.py -q="contractors" -l="San Francisco, CA" -n=100"
` - main file for start main scrape.
- `-q="category"`: set category of business for parse (DEFAULT "San Francisco, CA")
- `-l="San Francisco, CA`: location of business (DEFAULT: "contractors")
- `-n=100`: limit of parse businesses, default 100 (DEFAULT: 10)

As a consequence of the task completion, a file named {category name}_in_{location}_data.json will be produced in the primary directory."









