from yattag import Doc

# Create header data and title for HTML data
def InitializeHTML():
    WeatherInHTML = open("WeatherPredictionTemplate.html","a")
    doc, tag, text = Doc().tagtext()

    with tag('head'):
        with tag('style'):
            text('th, td {padding-top: 0px; padding-bottom: 0px; padding-left: 10px; padding-right:10px}')    
            text('th, td {border: 1px solid white; border-collapse: collapse; background-color: #96D4D4}')
            text('.grid-container {display: grid; grid-template-columns: 30% 70%;}')
            text('table {margin: 0px auto; white-space: pre-line"}')

    with tag('h1', style = "background: #96D4D4;", align = "center"):
        text("Automated Weather Report")
    
    #with tag("p", align = 'center'):
    #    text('')

    WeatherInHTML.write(doc.getvalue())
    WeatherInHTML.close()    