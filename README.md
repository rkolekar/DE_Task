
# Data Engineering Task

## Overview

This project consists of two data pipelines:

1. Copies tables from the source database to the destination database.
2. Monitors data quality of the source database and saves the report in our system.

## Prerequisites

- Install MySQL server on your local system.
- Create a database called `filmdata` in your local MySQL server.

## Setup

1. Update the `.env` file with the following changes:
- In the `DEST_CONN_STR` variable, update the username, password, and host credentials of your MySQL server.
- Update the value of `REPORT_FILENAME` variable. Create a folder in your system to save HTML reports of data quality.

2. Make the above changes in the Dockerfile where necessary.

## Dependencies

Install the required dependencies:

`pip install -r requirements.txt`


## Run the Code
To run the code, follow these steps:

Set the time in main.py line 37 to 3 minutes later than the current time.
Run the main.py file using your preferred IDE or command line.

**Note: The code is set to run automatically at 23:00 every day. Ensure that the time in main.py allows you to see the code run during testing.**

Feel free to use any IDE of your choice to execute the main.py file.