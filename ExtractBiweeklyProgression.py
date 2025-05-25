import UnitConversion

def create_table_biweekly_progression(weather_data, selected_index):
    weather_14_days = []

    # Prepare column names once based on selected indices
    col_names = ["Dates"]
    columns_map = [
        ("tempmax", "Max Tmp [°C]", UnitConversion.FahrenheitToCelcius),
        ("tempmin", "Min Tmp [°C]", UnitConversion.FahrenheitToCelcius),
        ("windspeed", "Wind Spd [kmh]", UnitConversion.MphToKpH),
        ("precipprob", "Precip. Prob. [%]", None),
        ("humidity", "Humidity [%]", None),
        ("sunrise", "Sunrise", lambda x: x[:-3]),
        ("sunset", "Sunset", lambda x: x[:-3]),
        ("conditions", "Condition", None)
    ]

    for idx, (key, col_name, converter) in enumerate(columns_map):
        if selected_index[idx] == 1:
            col_names.append(col_name)

    days = weather_data.get('days', [])
    for i in range(min(15, len(days))):
        day_data = days[i]
        weather_1_day = [day_data.get('datetime', '')]

        for idx, (key, _, converter) in enumerate(columns_map):
            if selected_index[idx] == 1:
                value = day_data.get(key, '')
                if converter and value != '':
                    value = converter(value)
                weather_1_day.append(value)

        weather_14_days.append(weather_1_day)

    return weather_14_days, col_names