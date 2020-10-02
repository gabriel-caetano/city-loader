# City Loader Script

Developed to create .sql dumps from .csv files

## Requirements

- Create a local mysql database

- Set the mysql connection configs inside the file

  - host

  - user

  - password

  - database name

- Load the dump 'municipios_e_secoes.sql' into the local database

- Download [this files](https://drive.google.com/drive/folders/1y-q3S5rZPwQ2POAuKzZQwYIf6Zbow5J8?usp=sharing) into the 'votos' and 'wider' folders

## How to use it

- Create an instance of the CityLoader class with the city name and the state initials as params

- Call one or more of the available methods to read and create the dumps

- Finally call the method finish() that create the file with all the dumps and close the db connection

Obs.: Tha bigger the city the longer it takes to load everythong (specially the votes)
