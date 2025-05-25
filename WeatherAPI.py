import requests, json
import os

# Download weather data from API
def GetWeatherData(CityName):

    # Enter your API key here
    API_Key = "KEY"
    
    # base_url variable to store url
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" 

    # complete url address
    complete_url = base_url + CityName + "?unitGroup=us&key=" + API_Key + "&contentType=json"
    
    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    if os.path.exists("WeatherData.json"):
        os.remove("WeatherData.json")

    DownloadSuccessful = False
    
    # convert json file to python dict
    try: 
        FileFromAPI = response.json()
        DownloadSuccessful = True
    except:
        print("City Name is invalid!")
        exit()

    # Save API data
    if DownloadSuccessful == True:
        try:
            with open("WeatherData.json", "r") as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            existing_data = []

        existing_data.append(FileFromAPI)

        with open("WeatherData.json", "w") as json_file:
            json.dump(existing_data, json_file, indent=4)

