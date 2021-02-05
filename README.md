# Final Project - Capstone

## iMeteoStation

### DESCRIPTION

iMeteoStation is an application that is used to search and save weather conditions for cities around the world. Data displayed in the application comes from two external services:

* [OpenWeatherMap API](https://openweathermap.org/)

* [Airly API](https://airly.org/en/)

Application allows users to create `accounts`, display the `current weather`, `five-day weather forecast`, `air quality`. Users can save measurements and manage them on profile page. The project uses the [XlsxWriter](https://xlsxwriter.readthedocs.io/) library which allows users to save data in an excel files.

### PROJECT STRUCTURE OVERVIEW

The structure of the project folder is as follows:
```
capstone
|── capstone
|── saved_data
|── weatherdata
|── db.sqlite3
|── manage.py
|── README.md
|── requirements.txt
```

`saved_data` folder contains all excel files saved by user. It is a main directory where all files are saved.

`weatherdata` folder is a main application directory of a project and the structure is as follows:
```
weatherdata
|── __pycache__
|── migrations
|── static
|── templates
|── __init__.py
|── admin.py
|── apps.py
|── forms.py
|── models.py
|── tests.py
|── urls.py
|── util.py
|── views.py
```

`static` folder contains all static files for the application:
  * `scripts.js` file contains several `javascript` functions, e.g.:
    * `showAlert(message)`: function takes a `message` parameter and displays the alert on the page
    * `sendDataToServer(url, data)`: function takes two parameters: `url`, `data` and sends  data to the server

  * `styles.scss` file which contains main styles for application, written with `SASS` preprocessor and compiled to `styles.css` file.

`templates` folder contains all HTML templates for the application views:
  * `layout.html`
  * `index.html`
  * `login.html`
  * `register.html`
  * `current_weather.html`
  * `five_day_weather.html`
  * `air_quality.html`
  * `nearest_installations.html`
  * `profile_page.html`

`forms.py` file contains a `UserRegisterForm` class used for creating users.

`models.py` file contains the application models:
  * `CurrentWeather` class represents weather data
  * `CurrentAirQuality` class represents air quality data

`util.py` file contains all utility functions for the application:
  * `list_filenames()`: function returns a list of file names in 'saved_data' directory
  * `list_files_info()`: function returns a list of dictionaries for each file
    in 'saved_data' directory. Each file contains file name,
    created time and modified time
  * `save_as_excel_file(filename, data)`: function for saving data in Excel file, takes two arguments:
    filename which is a name of the saved file and data which is
    a list of dictionaries contains data to be saved in Excel file
  * `open_file(filename)`: function that opens file form 'saved_data' directory by filename
  * `delete_file(filename)`: function that deletes file from 'saved_data' directory by filename

`views.py` file contains all function-based views with logic for application and several functions for receiving data from the frontend side:

  * `index`: displaying homepage of the application
  * `current_weather`: displays current weather conditions for a given city or town
  * `five_day_weather`: displays five-day weather forecast for a given city or town
  * `nearest_installations`: displays nearest air sensors for a given city or town within 3km
  * `current_air_quality`: displays current air quality data for a given city or town
  * `save_data_in_db`: function that receives data from the frontend and saves it in the database
  * `delete_single_weather_data`: function that deletes single weather measurement from the profile page table
  * `delete_all_weather_data`: function that deletes all weather measurements from the profile page table
  * `delete_single_air_data`: function that deletes single air quality measurement from the profile page table
  * `delete_all_air_data`: function that deletes all air quality measurements from the profile page table
  * `profile_page`: displays logged user profile page
  * `save_weatherdata_in_file`: function that saves weather measurements in excel file
  * `save_airdata_in_file`: function that saves air measurements in excel file
  * `open_excel_file`: function that opens excel file from the profile page view
  * `delete_excel_file`: function that deletes excel file from the profile page view
  * `login_view`
  * `logout_view`
  * `register`

### SPECIFICATION

* **Current weather**: Display weather data by typing city or town name. Data comes from `OpenWeatherMap API` after sending a request to `current weather` endpoint. If the input is empty, city name is incorrect or there is no data for a given city, appropriate alert appears, else weather data is displayed.

* **Five day forecast**: Display five day forecast including weather data every 3 hours. Displayed data includes `measurement date and time, temperature, humidity and weather description`. If input is empty or incorrect, appropriate alert appears.

* **Current air quality**: Display air quality data for a given city or town name.
  Data comes from `Airly API`, measurement values are searched by geographical location, to achieve this the Google `Geocode API` is used to get `latitude` and `longitude` for a given city or town name. Endpoint returns data for sensor within 3 km from the given location. If there is no data for a given city or town name, appropriate alert appears.

* **Nearest sensor installations**: Display nearest sensor installations for a given city or town name within `3 km`. Displayed data includes `sensor id, address, sponsor, additional info and sponsor site`.

* **Save data**: After search and display weather or air data user can save data in database without reloading the page using `javascript fetch` and display it on user profile page. There is a dashboard where user can check saved measurements. User have option to delete single measurement or delete all measurements from both weather and air tables.

* **Export to Excel**: User can export data to excel file by clicking `Save in Excel file` button. After clicking save button, modal is displayed where user can set the file name. If input is empty or filename already exist, appropriate alert appears. All functions that provides file operations and exporting data to Excel are included in `weatherdata/util.py` file. All excel files are saved locally in `saved_data` folder in main project directory. At the bottom of the profile page there's a `SAVED DATA` section where each user sees his saved excel files. In files table user can see `file name`, `creation time` and `modification time`. Files can be opened from the page by clicking a selected `file name`. Files can also be deleted from the application level.  

* **Responsive web design**: Main styles for the application are located in `weatherdata/static/weatherdata/styles.scss` file and written with SASS preprocessor. To make application responsive, media queries are added to the file.     
