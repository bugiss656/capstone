var save_weather_data_btn = document.querySelector('#save-weather-results')
var save_air_data_btn = document.querySelector('#save-air-results')
var open_file_btn = document.querySelectorAll('.open-file-link')


document.addEventListener('DOMContentLoaded', function() {

  if(save_weather_data_btn !== null) {
    save_weather_data_btn.addEventListener('click', () => {

      let weather_results = document.querySelector('#save-weather-results')
      let url = '/save_in_db'
      let weather_data = {
        'data_type': weather_results.dataset.dataType,
        'city_name': weather_results.dataset.cityName,
        'country': weather_results.dataset.country,
        'measurement_time': weather_results.dataset.measurementTime,
        'temperature': weather_results.dataset.temp,
        'feels_like': weather_results.dataset.feelsLike,
        'wind_speed': weather_results.dataset.windSpeed,
        'wind_direction': weather_results.dataset.windDirection,
        'pressure': weather_results.dataset.pressure,
        'humidity': weather_results.dataset.humidity,
        'visibility': weather_results.dataset.visibility,
        'main': weather_results.dataset.infoMain,
        'description': weather_results.dataset.infoDescription,
        'icon': weather_results.dataset.infoIcon
      }
      sendDataToServer(url, weather_data)
      showAlert('Weather data has been successfully saved.')
    })
  }


  if(save_air_data_btn !== null) {
    save_air_data_btn.addEventListener('click', () => {

      let air_results = document.querySelector('#save-air-results')
      let url = '/save_in_db'
      let air_data = {
        'data_type': air_results.dataset.dataType,
        'city_name': air_results.dataset.cityName,
        'measurement_time': air_results.dataset.measurementTime,
        'pm1': air_results.dataset.pm1,
        'pm25': air_results.dataset.pm25,
        'pm10': air_results.dataset.pm10,
        'index_value': air_results.dataset.indexValue,
        'index_level': air_results.dataset.indexLevel,
        'index_description': air_results.dataset.indexDescription,
        'index_color': air_results.dataset.indexColor,
      }

      sendDataToServer(url, air_data)
      showAlert('Air data has been successfully saved.')
    })
  }


  open_file_btn.forEach(open_file_btn => {
    open_file_btn.addEventListener('click', () => {
      var filename = open_file_btn.dataset.filename
      var url = '/open_file'

      sendDataToServer(url, filename)
    })
  })

})


function showAlert(message) {
  var alert = `
    <div class="alert alert-box success alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  `
  document.querySelector('.display-alert').innerHTML = alert
}


function sendDataToServer(url, data) {
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({data})
  })
  .then(response => response.json())
  .then(response => {})
}
