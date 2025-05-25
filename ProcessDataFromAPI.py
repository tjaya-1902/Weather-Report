import os
import json

import ExtractAlerts
import ExtractDailyProgression
import ExtractBiweeklyProgression

import OutputAlerts
import OutputBiweeklyReport
import OutputDailyReport

import InitHTML

from pathlib import Path

class API_Data:

    WEATHER_JSON = 'WeatherData.json'
    WEATHER_HTML = 'WeatherPrediction.html'
    WEATHER_TEMPLATE = 'WeatherPredictionTemplate.html'

    def __init__(self, CityName, IndexBiweekly, IndexDaily, IndexOutputFormat):
        self.CityName = CityName 
        self.IndexBiweekly = IndexBiweekly
        self.IndexDaily = IndexDaily
        self.IndexOutputFormat = IndexOutputFormat
        
        with open(self.WEATHER_JSON, 'r') as file:
            self.ExtractedAPI_Data = json.load(file)[0]

    def _reset_html_files(self):
        Path(self.WEATHER_HTML).unlink(missing_ok=True)
        Path(self.WEATHER_TEMPLATE).unlink(missing_ok=True)
        

    def ProcessDataFromAPI_BiweeklyProgression(self, Target):
        biweekly_data, biweekly_cols = ExtractBiweeklyProgression.create_table_biweekly_progression(self.ExtractedAPI_Data, self.IndexBiweekly)
        alerts_data, alerts_cols = ExtractAlerts.create_table_alerts(self.ExtractedAPI_Data)

        biweekly_report = OutputBiweeklyReport.ProcessedBiweeklyReport(self.CityName, biweekly_data, biweekly_cols, self.IndexBiweekly)
        alerts_report = OutputAlerts.ProcessedAlerts(alerts_data, alerts_cols)

        if Target == "UI_Figure":
            if sum(self.IndexBiweekly) == 0:
                return None
            return biweekly_report.create_plot_biweekly_progression(graph_format="Matplotlib")

        if Target == "Program Output":
            self._reset_html_files()

            InitHTML.InitializeHTML()
            if self.IndexOutputFormat[0] == 1:
                biweekly_report.output_biweekly_progression_to_console()
                alerts_report.OutputAlertsToConsole()

            if self.IndexOutputFormat[1] == 1 or self.IndexOutputFormat[2] == 1:
                biweekly_report.output_biweekly_progression_to_html()
                alerts_report.OutputAlertsToHTML()

    def ProcessDataFromAPI_DailyProgression(self, Target):
        daily_data, daily_cols = ExtractDailyProgression.create_table_daily_progression(self.ExtractedAPI_Data, self.IndexDaily)
        daily_report = OutputDailyReport.ProcessedDailyReport(self.CityName, daily_data, daily_cols, self.IndexDaily)

        if Target == "UI":
            if sum(self.IndexDaily) == 0:
                return None
            return daily_report.create_plot_daily_progression(graph_format="Matplotlib")

        if Target == "Program Output":
            if sum(self.IndexBiweekly) == 0:
                self._reset_html_files()
                InitHTML.InitializeHTML()
            else:
                Path(self.WEATHER_TEMPLATE).unlink(missing_ok=True)

            
            if self.IndexOutputFormat[0] == 1:
                daily_report.output_daily_progression_to_console()

            if self.IndexOutputFormat[1] == 1 or self.IndexOutputFormat[2] == 1:
                daily_report.output_daily_progression_to_html()

            Path(self.WEATHER_TEMPLATE).unlink(missing_ok=True)