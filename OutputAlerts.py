from tabulate import tabulate
from yattag import Doc

class ProcessedAlerts():

    def __init__(self, Data, ColNames):
        self.Data = Data
        self.ColNames = ColNames

    def OutputAlertsToConsole(self):
        print("Weather Alert")

        # Create weather alert table if there is any alert information
        if len(self.Data) > 0:
            print(tabulate(self.Data, headers = self.ColNames, tablefmt = "grid", maxcolwidths = [None, None, None, 70]))
        else:
            print("There is no weather alerts in this timeframe")    
        
        print("")

    def OutputAlertsToHTML(self):
        doc, tag, text = Doc().tagtext()
        
        with tag('body'):
            with tag('h1', align="center"):
                text('Weather Alert')

            if len(self.Data) > 0:
                doc.asis(str(tabulate(self.Data, headers=self.ColNames, tablefmt="html", maxcolwidths=[None, None, None, 70])))
            else:
                with tag('p', align = 'center'):
                    text('There is no weather alerts in this timeframe')

            with tag('div', style="break-after:page"):
                text("")

        with open("WeatherPrediction.html", "a", encoding="utf-8") as weather_in_html:
            weather_in_html.write(doc.getvalue())    