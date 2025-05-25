def create_table_alerts(weather_data):
    alerts = []
    
    if weather_data.get('alerts'):
        col_names = ["Event", "Onset", "Ends", "Description"]
        
        for alert in weather_data['alerts']:
            single_alert = [
                alert.get("event", ""),
                alert.get("onset", ""),
                alert.get("ends", ""),
                alert.get("description", "")
            ]
            alerts.append(single_alert)
    else:
        col_names = []

    return alerts, col_names
    