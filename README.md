# City Loader Script

Developed in Python to create .sql dumps from .csv files with pre-defined structures.

## Requirements

- Python 3 Installed;

- MySQL Installed;

- MySQL Python Connector:

`python -m pip install mysql-connector-python`

- Module Unidecode Installed: - python -m pip install unidecode

- Create a local mysql database;

- Set the mysql connection configs inside the file config.py:

  - host;

  - user;

  - password;

  - database name;

- Load the dump 'municipios.sql' and 'secoes\_(year).sql' from [here](https://drive.google.com/drive/folders/1mc0ybopl-KnEg7XdyOoR74Vhda-lpiNR?usp=sharing) into the local database;

- Download [this files](https://drive.google.com/drive/folders/1y-q3S5rZPwQ2POAuKzZQwYIf6Zbow5J8?usp=sharing) into the 'votos' and 'wider' folders.
  Obs.: It’s good to have an editor to work with code like VSCode.

## How to use it

- Create an instance of the CityLoader class with the city name and the state initials as params;

`loader = CityLoader("Santa Maria", "RS")`

- Call one or more of the available methods to read and create the dumps;
- Finally call the method finish() that create the file with all the dumps and close the db connection;

`loader.finish()`

- Methods to read and create the:

  - `loader.dumpSingle(year, table)`

    Pass the year and the table as params to create the dump of the specified table;
    year must be 2012, 2014, 2016, 2018, representing the election years available
    table must be a string "votes" or "profiles"

  - `loader.dumpProfilesSumary()`
    Use to dump profiles tables of all years;

  - `loader.dumpVotes()`
    Use to dump votes tables of all years;

  - `loader.dumpYear(year)`
    Pass the year as param (same as above) to dump tables of the year;

  - `loader.dumpCity()`
    Dump all tables of the city;

## How to run the code

In the cmd/terminal use the following command:
`python ~path/CityLoader.py`

Obs.: The bigger the city the longer it takes to load everything (specially the votes)
