import os
import UserInterface as UI
import ProcessDataFromAPI
import SendEmail


OUTPUT_FILES = [
    "WeatherPrediction.html",
    "WeatherPredictionTemplate.html",
    "WeatherPrediction.pdf"
]

def main():
    # Clean up existing output files
    for file in OUTPUT_FILES:
        if os.path.exists(file):
            os.remove(file)

    # Initialize GUI and get user input
    ui_values = UI.UI_Values()
    selected_biweekly, selected_daily, selected_output, selected_email = ui_values.Invoke_UI()
    city_name = ui_values.Input_CityName.get()

    # Process weather data
    api_data = ProcessDataFromAPI.API_Data(city_name, selected_biweekly, selected_daily, selected_output)

    if any(selected_biweekly):
        api_data.ProcessDataFromAPI_BiweeklyProgression(Target="Program Output")

    if any(selected_daily):
        api_data.ProcessDataFromAPI_DailyProgression(Target="Program Output")

    # Send email if selected
    if selected_output[2] and (any(selected_biweekly) or any(selected_daily)):
        SendEmail.SendWeatherReport(selected_email)

    input("Press Enter to exit;")

if __name__ == "__main__":
    main()

# pyinstaller --onefile Main.py


