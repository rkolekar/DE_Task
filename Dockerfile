# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install ODBC libraries
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV SOURCE_CONN_STR="mssql+pyodbc://de_candidate:1ntu5-d4t4@de-engineer-trial-intus.database.windows.net/FilmData?driver=ODBC Driver 17 for SQL Server&autocommit=true&timeout=30&protocol=TCP"
ENV DEST_CONN_STR="mysql+mysqlconnector://root:password@localhost/filmdata"
ENV REPORT_FILENAME="C:\Users\BhalchandraK\Desktop\DE task\Data Quality report\DataQualityReport_"

# Run main.py when the container launches
CMD ["python", "./pipeline/main.py"]
