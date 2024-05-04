
document.onreadystatechange = function () {
	if (document.readyState == "complete") {
		console.log("document has fully loaded");
		console.log(hydro_data_TEMP_HUMIDITY);
		console.log(start_date);
		document.getElementById("date-from").value = start_date;

	}
  };
  

  var TEMP_HUMIDITY_DATA = hydro_data_TEMP_HUMIDITY.data;
  console.log(TEMP_HUMIDITY_DATA);
  const hydro_data = document.getElementById('hydroDataChart');
  const high_temp_element = document.getElementById('max-temp');
  const low_temp_element = document.getElementById('min-temp');
  const ave_temp_element = document.getElementById('ave-temp');
  const high_humid_element = document.getElementById('max-humidity');
  const low_humid_element = document.getElementById('min-humidity');
  const ave_humid_element = document.getElementById('ave-humidity');
  console.log("we have got the element for the new chart");

  var myHydroChart = new Chart(hydro_data, {
	  type: "bar",
	  data: {},
  });
  console.log("myHydroChart empty chart created");

  // hydro_data_TEMP_HUMIDITY 
  if (hydro_data_TEMP_HUMIDITY){
	  console.log("there is data in the variable hydro_data_TEMP_HUMIDITY");
	  var high_temp = hydro_data_TEMP_HUMIDITY.data_summary.high_temp;
	  var low_temp = hydro_data_TEMP_HUMIDITY.data_summary.low_temp;
	  var ave_temp = hydro_data_TEMP_HUMIDITY.data_summary.ave_temp;
	  var high_humid = hydro_data_TEMP_HUMIDITY.data_summary.high_humid;
	  var low_humid = hydro_data_TEMP_HUMIDITY.data_summary.low_humid;
	  var ave_humid = hydro_data_TEMP_HUMIDITY.data_summary.ave_humid;
  }else{
	  console.log("there is NO DATA in the variable hydro_data_TEMP_HUMIDITY");
  };





  if (high_temp && low_temp &&ave_temp && high_humid && low_humid && ave_humid) {
	  console.log("there is min mac and ave data");
	  high_temp_element.innerHTML = "Max Temperature: " + high_temp + "&deg; C";
	  low_temp_element.innerHTML = "Min Temperature: " + low_temp + "&deg; C";
	  ave_temp_element.innerHTML = "Ave Temperature: " + ave_temp + "&deg; C";
	  high_humid_element.innerHTML = "Max Humidity: " + high_humid + "%";
	  low_humid_element.innerHTML = "Min Humidity: " + low_humid + "%";
	  ave_humid_element.innerHTML = "Ave Humidity: " + ave_humid + "%";
  }else{
	  console.log("there is NO min mac and ave data");
	  high_temp_element.innerHTML = "Max Temperature: - &deg; C";
	  low_temp_element.innerHTML = "Min Temperature: - &deg; C";
	  ave_temp_element.innerHTML = "Ave Temperature: - &deg; C";
	  high_humid_element.innerHTML = "Max Humidity: - %";
	  low_humid_element.innerHTML = "Min Humidity: - %";
	  ave_humid_element.innerHTML = "Ave Humidity: - %";
  };
  myHydroChart.destroy();

  myHydroChart = new Chart(hydro_data, 
	  {
		  type: 'bar',
		  data: {
			  labels: TEMP_HUMIDITY_DATA.map(row => row.Time),
			  datasets: [
				  {
					  label: 'Temperature',
					  data: TEMP_HUMIDITY_DATA.map(row => row.Temperature),
					  borderWidth: 1,
					  backgroundColor:'rgba(214, 0, 0, 0.2)',
					  borderColor:'rgba(214, 0, 0)'
				  },
				  {
					  label: 'Humidity',
					  data: TEMP_HUMIDITY_DATA.map(row => row.Humidity),
					  borderWidth: 1,
					  backgroundColor:'rgba(23, 155, 255, 0.2)',
					  borderColor:'rgba(23, 155, 255)'
				  }
			  ]
		  },
		  options: {
			  scales: {
				  y: {
					  beginAtZero: true,
					  steps: 10,
					  stepValue: 1,
					  max: 100
				  }
			  },
			  plugins: {
				  title:{
					  display: true,
					  align:'center',
					  fullSize:true,
					  text: 'Temperature + Humidity Data: '+ start_date,
					  font: {
						  size: 30
					  }
				  }
			  }
		  }
	  });




// function addData(chart, label, newData) {
//     chart.data.labels.push(label);
//     chart.data.datasets.forEach((dataset) => {
//         dataset.data.push(newData);
//     });
//     chart.update();
// }




        // var hydro_data_TEMP_HUMIDITY = {{ page_data.temp_humidity_data }};
//        