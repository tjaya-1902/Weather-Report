import UnitConversion

def create_table_daily_progression(weather_data, selected_index):
    # Prepare column names once
    col_names = ["Hour"]
    columns_map = [
        ("temp", "Tmp [°C]", UnitConversion.FahrenheitToCelcius),
        ("windspeed", "Wind Spd [kmh]", UnitConversion.MphToKpH),
        ("humidity", "Humidity [%]", None)
    ]

    for idx, (_, col_name, _) in enumerate(columns_map):
        if selected_index[idx] == 1:
            col_names.append(col_name)

    days = weather_data.get('days', [])
    weather_14_days = []

    for day in days[:15]:
        hours = day.get('hours', [])
        weather_24_hours = []

        for hour_data in hours[:24]:
            weather_1_hour = [hour_data.get('datetime', '')[:-3]]  # Remove last 3 chars from time string

            for idx, (key, _, converter) in enumerate(columns_map):
                if selected_index[idx] == 1:
                    value = hour_data.get(key, '')
                    if converter and value != '':
                        value = converter(value)
                    weather_1_hour.append(value)

            weather_24_hours.append(weather_1_hour)

        weather_14_days.append(weather_24_hours)
        
        date = day['datetime']
        weather_24_hours.append(date)
        

    return weather_14_days, col_names