
<p align="center">
<a href="https://codecov.io/gh/AdamMisiak/Price_scraper"><img src="https://codecov.io/gh/AdamMisiak/Price_scraper/branch/master/graph/badge.svg" /></a>
</p>


# Price scraper

Website presenting actual prices(API) and value of users assets (Btc,Xrp,Gold) created with Flask. App was created as a project in TechLeaders.eu program.


## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Contact](#contact)

## Technologies
* Python version: 3.7

## Setup
To run app locally:
```
docker-compose up --build
```
After building 2 Dockerfiles app will be started.\
For main app:
```
http://localhost:12345/
```
For prices of assets in json format:
```
http://localhost:23456/
```
"CORS" browser plugin recomended for proper prices displaying.

## Contact
Created by Adam Misiak
