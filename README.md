# SEO-Keywords-Planner

## Overview
SEO Keywords Planner is a web application designed to provide keyword performance visualizations. Businesses can use the web app for Search Engine Optimization SEO. It is built from flask with serpApi.

## Data Collection and Processing
- **Data Source for Demonstration**: The application utilizes the demo_json_data to display the demonstration. It uses the keyword "cityu" as the demo data.
- **Data Source for Live Search**: The application utilizes the serpi API to fetch real-time keyword performance data. 
- **Data Transformation**:
1. When the value returned is less than 1 (<1), it is replaced by 0.
2. (Region search)Based on the locations returned, the continent of the location is searched with the sata frame in Get.Continent.py.

## Running the Application
1. **Setup Environment**:
    - Ensure Python 3.9 is installed on your system.
    - Install required Python libraries: `pip install Flask`, `pip install pandas`, `pip install google-search-results`, `pip install matplotlib`
      
2. **Starting the App**:
    - Run the application using `py app.py`(for Windows OS) or `python app.py` (for Mac OS).
    - Access the app in a web browser at `localhost:5000`.

3. **Using the App**:
    - Search "cityu" on the demo page to preview how the web app runs.
    - Sign up for an account and log in for live search.
    - Search for keywords to view real-time data and visualizations.
    - Download the chart image for later reference.
