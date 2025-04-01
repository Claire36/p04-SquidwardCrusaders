# Saving the World by Squidward Crusaders

## Roster (roles TBD):  
Claire Song  
Linda Zheng  
Tanzeem Hasan  
Ben Rudinski

## Description of website/app
We will be finding the relationship between traffic congestion and the concentration of 4 air pollutants (O3, CO, SO2, and NO2) by comparing data from 2 datasets. Users will be able to pick an air pollutant upon logging in. Then, they will see maps of its concentration for each year from 2000 to 2011 alongside maps of traffic congestion over that same time period to see how changes in congestion affect the concentration of the air pollutant that they chose.

## Install Guide [w.i.p]

### Prerequisites
Ensure you have the following installed on your system:
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python 3](https://www.python.org/downloads/)

It's recommended to run this project in a virtual environment to avoid any potential conflicts with other packages. Obviously this doesn't apply to you Topher, but if your less advanced, refer to [this guide](https://novillo-cs.github.io/apcsa/tools/).

### Steps to Install and Run
1. Clone and move into this repository
```
$ git clone git@github.com:EndritIdrizi/p02.git
```
```
$ cd p01
```
3. Create a virtual environment
```
$ python3 -m venv foo
```

4. Activate the virtual environment: Linux/MacOS
```
$ . foo/bin/activate
```
4. Activate the virtual environment: Windows
```
$ foo\Scripts\activate
```
5. Install required packages
```
$ pip install -r requirements.txt
```
## Launch Codes: [w.i.p]
1. Run the database setup file
``` 
$ python3 app/setup_db.py
```
2. Locate and run the app file
``` 
$ cd app
```
``` 
$ python3 __init__.py
```
3. Access the Application: Open your browser and go to http://127.0.0.1:5000 or click the link that appears in your terminal output.
To stop the app, press CTRL + C
