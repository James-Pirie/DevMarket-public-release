# DevMarket
A tool which collects and displays job listing data from Seek.com in relevant and interesting ways.

- /data_collection is a beautiful soup web scraper. Collects listing information from seek.co.nz [more info here](https://devmarket.nz/about)
- /database schema for our sql database
- /flask_web a modular flask web application [see live here](https://devmarket.nz/)
## Installation

**Installation via requirements.txt**

**Windows**
```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution
To run the scraper a sql database will need to be setup, instructions to follow
1. Setup SQL DB Server
2. Change connection objects in data_collection/database_setup.y and /data_collection/main.py
3. Run database_setup.py
4. Change conenction string in flask_web/database/connect.py
5. Configure ports and flask server for flask application
5. Run wsgi flask server on local machine 
