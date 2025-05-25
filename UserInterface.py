from tkinter import *
import tkinter as tk
import ProcessDataFromAPI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import WeatherAPI

class UI_Values:

    def __init__(self):
        self.SelectedBiweeklyInfo = []
        self.SelectedDailyInfo = []
        self.SelectedOutputFormat = []
        self.UI_FigureIsPresent = False

    def Invoke_UI(self):
        
        # Create and append UI widgets
        self.Root = tk.Tk()
        self.Root.title(string = "Weather Prediction")

        Frame_Text = Frame(self.Root)
        Frame_Text.pack()

        Frame_CheckBox = Frame(self.Root)
        Frame_CheckBox.pack()

        Frame_Button = Frame(self.Root)
        Frame_Button.pack()

        # Enter city name and recipient email 
        self.Input_CityName = StringVar(value="Berlin")
        self.Email = StringVar()
        
        LabelCityName = Label(Frame_Text, text="City Name: ", anchor = 'w')
        EntryCityName = Entry(Frame_Text, textvariable = self.Input_CityName)

        LabelEmail = Label(Frame_Text, text="Email: ", anchor = 'w')
        EntryEmail = Entry(Frame_Text, textvariable = self.Email)

        LabelCityName.grid(row = 0, column = 0)
        EntryCityName.grid(row = 0, column = 1)
        LabelEmail.grid(row = 1, column = 0)
        EntryEmail.grid(row = 1, column = 1)

        # Checkboxes for basic biweekly informations 
        self.State_TempMax = IntVar(value=1)
        self.State_TempMin = IntVar(value=1)
        self.State_PrecipProb = IntVar(value=1)
        self.State_WindSpeed = IntVar(value=1)

        Label(Frame_CheckBox, 
              text="Biweekly Data (Basic):", 
              padx = 5, 
              pady = 5, 
              height = 1, 
              width = 25, 
              anchor = 'w').grid(row = 0, column = 0)
        
        CB_TempMax = Checkbutton(Frame_CheckBox, 
                                 text = "Max Temperature", 
                                 variable = self.State_TempMax, 
                                 onvalue = 1, 
                                 offvalue = 0, 
                                 height = 1, 
                                 width = 20, 
                                 anchor = 'w')
        CB_TempMax.grid(row = 1, column = 0)
        
        CB_TempMin = Checkbutton(Frame_CheckBox, 
                                 text = "Min Temperature", 
                                 variable = self.State_TempMin, 
                                 onvalue = 1, 
                                 offvalue = 0, 
                                 height = 1, 
                                 width = 20, 
                                 anchor = 'w')
        CB_TempMin.grid(row = 2, column = 0)

        CB_WindSpeed = Checkbutton(Frame_CheckBox, 
                                   text = "Wind Speed", 
                                   variable = self.State_WindSpeed, 
                                   onvalue = 1, 
                                   offvalue = 0, 
                                   height = 1, 
                                   width = 20, 
                                   anchor = 'w')
        CB_WindSpeed.grid(row = 3, column = 0)
        
        CB_PrecipProb = Checkbutton(Frame_CheckBox, 
                                    text = "Precipitation Probability", 
                                    variable = self.State_PrecipProb, 
                                    onvalue = 1, 
                                    offvalue = 0, 
                                    height = 1, 
                                    width = 20, 
                                    anchor = 'w')
        CB_PrecipProb.grid(row = 4, column = 0)
        
        # Checkboxes for extended biweekly informations 
        self.State_Humidity = IntVar(value=1)
        self.State_Sunrise = IntVar(value=1)
        self.State_Sunset = IntVar(value=1)
        self.State_Condition = IntVar(value=1)

        Label(Frame_CheckBox, 
              text="Biweekly Data (Extended):", 
              padx = 5, 
              pady = 5, 
              height = 1, 
              width = 25, 
              anchor = 'w').grid(row = 0, column = 1)
        
        CB_Humidity = Checkbutton(Frame_CheckBox, 
                                  text = "Humidity", 
                                  variable = self.State_Humidity, 
                                  onvalue = 1, 
                                  offvalue = 0, 
                                  height = 1, 
                                  width = 20, 
                                  anchor = 'w')
        CB_Humidity.grid(row = 1, column = 1)
        
        CB_Sunrise = Checkbutton(Frame_CheckBox, 
                                 text = "Sunrise", 
                                 variable = self.State_Sunrise, 
                                 onvalue = 1, 
                                 offvalue = 0, 
                                 height = 1, 
                                 width = 20, 
                                 anchor = 'w')
        CB_Sunrise.grid(row = 2, column = 1)
        
        CB_Sunset = Checkbutton(Frame_CheckBox, 
                                text = "Sunset", 
                                variable = self.State_Sunset, 
                                onvalue = 1, 
                                offvalue = 0, 
                                height = 1, 
                                width = 20, 
                                anchor = 'w')
        CB_Sunset.grid(row = 3, column = 1)
        
        CB_Condition = Checkbutton(Frame_CheckBox, 
                                   text = "Condition", 
                                   variable = self.State_Condition, 
                                   onvalue = 1, 
                                   offvalue = 0, 
                                   height = 1, 
                                   width = 20, 
                                   anchor = 'w')
        CB_Condition.grid(row = 4, column = 1)

        # Checkboxes for daily informations 
        self.State_TemperatureByHour = IntVar(value=1)
        self.State_WindSpeedByHour = IntVar(value=1)
        self.State_HumidityByHour = IntVar(value=1)

        Label(Frame_CheckBox, 
              text="Daily Data:", 
              padx = 5, 
              pady = 5, 
              height = 1, 
              width = 25, 
              anchor = 'w').grid(row = 0, column = 2)
        
        CB_TemperaturByHour = Checkbutton(Frame_CheckBox, 
                                          text = "Temperature", 
                                          variable = self.State_TemperatureByHour, 
                                          onvalue = 1, 
                                          offvalue = 0, 
                                          height = 1, 
                                          width = 20, 
                                          anchor = 'w')
        CB_TemperaturByHour.grid(row = 1, column = 2)
        
        CB_WindSpeedByHour = Checkbutton(Frame_CheckBox, 
                                         text = "Wind Speed", 
                                         variable = self.State_WindSpeedByHour, 
                                         onvalue = 1, 
                                         offvalue = 0, 
                                         height = 1, 
                                         width = 20, 
                                         anchor = 'w')
        CB_WindSpeedByHour.grid(row = 2, column = 2)
        
        CB_HumidityByHour = Checkbutton(Frame_CheckBox, 
                                        text = "Humidity", 
                                        variable = self.State_HumidityByHour, 
                                        onvalue = 1, 
                                        offvalue = 0, 
                                        height = 1, 
                                        width = 20, 
                                        anchor = 'w')
        CB_HumidityByHour.grid(row = 3, column = 2)
        
        # Checkboxes for output formats
        self.State_OutputConsole = IntVar(value=1)
        self.State_OutputHTML = IntVar(value=1)
        self.State_OutputEmail = IntVar(value=0)

        Label(Frame_CheckBox, 
              text="Output Formats:", 
              padx = 5, 
              pady = 5, 
              height = 1, 
              width = 25, 
              anchor = 'w').grid(row = 0, column = 3)
        
        CB_OutputConsole = Checkbutton(Frame_CheckBox, 
                                       text = "Console", 
                                       variable = self.State_OutputConsole, 
                                       onvalue = 1, 
                                       offvalue = 0, 
                                       height = 1, 
                                       width = 20, 
                                       anchor = 'w')
        CB_OutputConsole.grid(row = 1, column = 3)
        
        CB_OutputHTML = Checkbutton(Frame_CheckBox, 
                                    text = "HTML", 
                                    variable = self.State_OutputHTML, 
                                    onvalue = 1, 
                                    offvalue = 0, 
                                    height = 1, 
                                    width = 20, 
                                    anchor = 'w')
        CB_OutputHTML.grid(row = 2, column = 3)
        
        CB_OutputEmail = Checkbutton(Frame_CheckBox, 
                                     text = "Email", 
                                     variable = self.State_OutputEmail, 
                                     onvalue = 1, 
                                     offvalue = 0, 
                                     height = 1, 
                                     width = 20, 
                                     anchor = 'w')
        CB_OutputEmail.grid(row = 3, column = 3)

        # Add Buttons
        # Reset all checkboxes
        Button(Frame_Button, text = "Reset", command = self.ClearInput).grid(row = 0, column = 0, padx = 10, pady = 10)
        # Show biweekly weather prediction
        Button(Frame_Button, text = "Show", command = self.ShowBiweeklyPlot).grid(row = 0, column = 1, padx = 10, pady = 10)
        # Close GUI
        Button(Frame_Button, text = "Done", command = self.Quit).grid(row = 0, column = 2, padx = 10, pady = 10)
        
        # Download weather data from API
        WeatherAPI.GetWeatherData(self.Input_CityName.get())
        self.Saved_CityName = self.Input_CityName.get()

        self.Obj_API_Data = ProcessDataFromAPI.API_Data(self.Input_CityName.get(), 
                                                        self.SelectedBiweeklyInfo,
                                                        self.SelectedDailyInfo,
                                                        self.SelectedOutputFormat)        

        self.Root.mainloop()

        self.GetCheckBoxStates()

        return self.SelectedBiweeklyInfo, self.SelectedDailyInfo, self.SelectedOutputFormat, self.Email.get()
    
    def GetCheckBoxStates(self):
        # Collect index of selected Biweekly weather informations
        self.SelectedBiweeklyInfo = [self.State_TempMax.get(),
                                    self.State_TempMin.get(),
                                    self.State_WindSpeed.get(),
                                    self.State_PrecipProb.get(),                             
                                    self.State_Humidity.get(),
                                    self.State_Sunrise.get(),
                                    self.State_Sunset.get(),
                                    self.State_Condition.get()]
        
        # Collect index of selected Daily weather informations
        self.SelectedDailyInfo =  [self.State_TemperatureByHour.get(),
                                   self.State_WindSpeedByHour.get(),
                                   self.State_HumidityByHour.get()]
        
        # Collect index of selected output formats
        self.SelectedOutputFormat = [self.State_OutputConsole.get(),
                                     self.State_OutputHTML.get(),
                                     self.State_OutputEmail.get()]
        
        

    def Quit(self):
        self.Root.quit()
    
    def ClearInput(self):
        # Basic Biweekly Informations
        self.State_TempMax.set(0)
        self.State_TempMin.set(0)
        self.State_WindSpeed.set(0)
        self.State_PrecipProb.set(0)

        # Extended Biweekly Informations
        self.State_Humidity.set(0)
        self.State_Sunrise.set(0)
        self.State_Sunset.set(0)
        self.State_Condition.set(0)

        # Daily Informations
        self.State_TemperatureByHour.set(0)
        self.State_WindSpeedByHour.set(0)
        self.State_HumidityByHour.set(0)

        #Output Formats
        self.State_OutputConsole.set(0)
        self.State_OutputHTML.set(0)
        self.State_OutputEmail.set(0)

        self.RefreshFrameFigure()


    def ShowBiweeklyPlot(self):

        self.RefreshFrameFigure()
        self.GetCheckBoxStates()
        self.RefreshCityName()
        
        if sum(self.SelectedBiweeklyInfo) > 0:
            UI_Figure = self.Obj_API_Data.ProcessDataFromAPI_BiweeklyProgression(Target = "UI_Figure")

            # Append figure to GUI
            self.Frame_Figure = FigureCanvasTkAgg(UI_Figure, self.Root)
            self.Frame_Figure.get_tk_widget().pack()
            self.UI_FigureIsPresent = True

        self.Frame_FigureButton = Frame(self.Root)
        #Button(self.Frame_FigureButton, text = "Biweekly", command = self.ClearInput).grid(row = 0, column = 0, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 1", command = self.ShowDailyPlot_Day1).grid(row = 0, column = 0, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 2", command = self.ShowDailyPlot_Day2).grid(row = 0, column = 1, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 3", command = self.ShowDailyPlot_Day3).grid(row = 0, column = 2, padx = 10, pady = 10)
        self.Frame_FigureButton.pack()
        
    
    def ShowDailyPlot_Day1(self):

        self.RefreshFrameFigure()
        self.GetCheckBoxStates()
        self.CreateDailyPlot(Day = 1)

        self.Frame_FigureButton = Frame(self.Root)
        Button(self.Frame_FigureButton, text = "Biweekly", command = self.ShowBiweeklyPlot).grid(row = 0, column = 0, padx = 10, pady = 10)
        #Button(self.Frame_FigureButton, text = "Daily: Day 1", command = self.ShowDailyPlot_Day1).grid(row = 0, column = 1, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 2", command = self.ShowDailyPlot_Day2).grid(row = 0, column = 1, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 3", command = self.ShowDailyPlot_Day3).grid(row = 0, column = 2, padx = 10, pady = 10)
        self.Frame_FigureButton.pack()

    
    def ShowDailyPlot_Day2(self):

        self.RefreshFrameFigure()
        self.GetCheckBoxStates()
        self.CreateDailyPlot(Day = 2)

        self.Frame_FigureButton = Frame(self.Root)
        Button(self.Frame_FigureButton, text = "Biweekly", command = self.ShowBiweeklyPlot).grid(row = 0, column = 0, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 1", command = self.ShowDailyPlot_Day1).grid(row = 0, column = 1, padx = 10, pady = 10)
        #Button(self.Frame_FigureButton, text = "Daily: Day 2", command = self.ShowDailyPlot_Day2).grid(row = 0, column = 1, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 3", command = self.ShowDailyPlot_Day3).grid(row = 0, column = 2, padx = 10, pady = 10)
        self.Frame_FigureButton.pack()

    
    def ShowDailyPlot_Day3(self):

        self.RefreshFrameFigure()
        self.GetCheckBoxStates()
        self.CreateDailyPlot(Day = 3)

        self.Frame_FigureButton = Frame(self.Root)
        Button(self.Frame_FigureButton, text = "Biweekly", command = self.ShowBiweeklyPlot).grid(row = 0, column = 0, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 1", command = self.ShowDailyPlot_Day1).grid(row = 0, column = 1, padx = 10, pady = 10)
        Button(self.Frame_FigureButton, text = "Daily: Day 2", command = self.ShowDailyPlot_Day2).grid(row = 0, column = 2, padx = 10, pady = 10)
        #Button(self.Frame_FigureButton, text = "Daily: Day 3", command = self.ShowDailyPlot_Day3).grid(row = 0, column = 1, padx = 10, pady = 10)
        self.Frame_FigureButton.pack()


    def CreateDailyPlot(self, Day):
        self.RefreshCityName()
        
        if sum(self.SelectedDailyInfo) > 0:
            UI_Figure = self.Obj_API_Data.ProcessDataFromAPI_DailyProgression(Target = "UI")

            # Append figure to GUI
            self.Frame_Figure = FigureCanvasTkAgg(UI_Figure[Day - 1], self.Root)
            self.Frame_Figure.get_tk_widget().pack()
            self.UI_FigureIsPresent = True
        

    def RefreshFrameFigure(self):
        if self.UI_FigureIsPresent == True:
            self.Frame_Figure.get_tk_widget().pack_forget()
            self.Frame_FigureButton.pack_forget()
            self.UI_FigureIsPresent == False


    def RefreshCityName(self):
        # If a new city name is given, download new weather data from API
        if self.Input_CityName.get() != self.Saved_CityName:
            WeatherAPI.GetWeatherData(self.Input_CityName.get())
            self.Saved_CityName = self.Input_CityName.get()

        self.Obj_API_Data = ProcessDataFromAPI.API_Data(self.Input_CityName.get(), 
                                                   self.SelectedBiweeklyInfo,
                                                   self.SelectedDailyInfo,
                                                   self.SelectedOutputFormat)

        





    




