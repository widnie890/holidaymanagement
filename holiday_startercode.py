import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

importloc = "holidays.json"

holidayswebsite = "https://www.timeanddate.com/holidays/us/"
# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:

    """Holiday class"""
      
    def __init__(self,name, date):
        #print('Initializing name and date')
        self.__name = name
        self.__date = date
    
    def __str__ (self):
        return f"{self.__name} {self.__date}"
        # String output
        # Holiday output when printed.
    
    @property
    def name(self):
        return self.__name
    
    @property
    def date(self):
        return self.__date
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name
    
    @date.setter
    def date(self, new_date_str,date_format):
        self.__date = datetime.strptime(new_date_str,date_format)
    
    @name.deleter
    def name(self):
        del self.__name
    
    @date.deleter
    def date(self):
        del self.__date
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    """Holiday list"""

    def __init__(self):
       self.__innerHolidays = []
    
    def addHoliday(self):
        print("Add a holiday")
        print("===================")

        _holiday = str(input("Holiday name: "))
        _holidaydate = input("When is the holiday? Input in yyyy-mm-dd: ")
        date = datetime.datetime.strptime(_holidaydate,"%Y-%m-%d").date()
        holidayObj = Holiday(_holiday,date)

        if (type(holidayObj)== Holiday):
            self.__innerHolidays.append(holidayObj)
            #print(f"Holiday : {_holiday}")
            #print("Date: " + date.strftime('%Y-%m-%d'))  
            print(f'Success: \n {_holiday} ({date}) has been added to the holiday list')
        else:
            print("Error:\n Please try again.")
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(self,HolidayName, HolidayDate):
        for holiday in self.__innerHolidays:
            if holiday.name == HolidayName and holiday.date == HolidayDate:
                return holiday
            else:
                #print(f'{HolidayName} not found.')
                return False 
        # Find Holiday in innerHolidays
        # Return Holiday
    
    def removeHoliday(self):
        print("Remove a holiday")
        print("=====================")

        HolidayName = str(input("What holiday would you like to remove?: "))
        HolidayDate = input("When is the holiday? Input in yyyy-mm-dd: ")
        date = datetime.datetime.strptime(HolidayDate,"%Y-%m-%d").date()

        h = self.findHoliday(HolidayName,date)
        
        if h == False:
            print(f"Error:\n {HolidayName} could not be found.")
        else:
            self.__innerHolidays.remove(h)
            print(f"Success:\n {HolidayName} has been removed from the holiday list")
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self,filelocation):
        with open(filelocation, "r") as f:
            holidays = json.load(f)
            for i in holidays["holidays"]:
                date = datetime.datetime.strptime(i["date"],"%Y-%m-%d")
                if self.findHoliday(i["name"], date) != False:
                    newHoliday = Holiday(i["name"], date)
                    self.__innerHolidays.append(newHoliday)
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self, filelocation):
        with open(filelocation, "w") as f:
            tempholidays = []
            for i in self.__innerHolidays:
                holiday = {"Name": i.name, "Date": i.date.strftime("%Y/%m/%d")}
                tempholidays.append(holiday)
            json.dump(tempholidays,f)
        # Write out json file to selected file.
    
    
    def scrapeHolidays(self):
        for i in range(2020,2025):
            url = (f"https://www.timeanddate.com/holidays/us/{i}?hol=33554809")
            url = url.format(i)
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            holidaytable = soup.find('table', attrs ={'id':'holidays-table'})

            for row in holidaytable.find_all_next('tr',class_ = 'showrow'):
                cells = row.find_all_next('td')
                mmdd = row.find('th',class_ = 'nw').text
                yyyy = f"{i} {mmdd}"
                rmmdd = datetime.datetime.strptime(yyyy,"%Y %b %d").date()
                hname = cells[1].text
                
                h = self.findHoliday(hname, rmmdd)
                if h == False:
                    newHoliday = Holiday(hname, rmmdd)
                    self.__innerHolidays.append(newHoliday)
            # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     
    def numHolidays(self):
        return(len(self.__innerHolidays))
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(self, year, week_number):
        holidays = list(filter(lambda holiday: holiday.date.isocalendar()[1] == week_number
            and holiday.date.year == year, self.__innerholidays))

        return holidays
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self, HolidayList):
        hWeek = self.filter_holidays_by_week(HolidayList[0], HolidayList[1])

        for h in hWeek:
            print(h)
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    #def getWeather(self, currentweek):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        year = datetime.now().year
        week = datetime.now().isocalendar()[1]
        currentweek = [week, year]

        return currentweek
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
def start():
    holist = HolidayList()
    holist.read_json(importloc)
    holist.scrapeHolidays()
    return holist

def main():
    HolidayList = start()
    print("Welcome to Holiday Management System")
    print("=============================================")
    print(f"There are {HolidayList.numHolidays()} holidays stored in the system")
    input("Press E to enter the main menu: ")
    usercontinue = True
    saved = True

    while True:
        print("Holiday Menu")
        print("=============================================")
        print("1. Add a holiday")
        print("2. Remove a holiday")
        print("3. Save holiday list")
        print("4. View holidays")
        print("5. Exit")
        choice = int(input("Enter a menu number to navigate: "))
        if choice not in range (1,6):
            print("That is not an option.")
        elif choice == 1:
            HolidayList.addHoliday()
        elif choice == 2:
            HolidayList.removeHoliday()
        elif choice == 3:
            print("Saving Holiday List")
            print("========================")
            while saved: 
                save = str(input("Are you sure you want to save your changes? [y/n]: "))
            
            if save == 'y':
                print("Success:\n Your changes have been saved.")
                HolidayList.save_to_json(importloc)
                saved = False
            elif save == 'n':
                print("Canceled:\n Holiday list file save canceled.")
                saved = False
            else:
                print("Invalid entry!")
        elif choice == 4:
            yearCheck = False
            while yearCheck == False:
                try:
                    yr = int(input("Which Year?: "))
                    yearCheck = True
                except:
                    print("Error:\n Please enter an integer for year")
            weekCheck = False
            while weekCheck == False:
                wk = input("Which Week?: #[1-52, Leave blank for the current week]: ")
                if wk == int(wk):
                    wk = HolidayList.viewCurrentWeek()
                    weekCheck = True
                else:
                    print("\nError: please enter an integer for week!\n")
            
            x = HolidayList.filter_holidays_by_week(yr, wk)
            if len(x) == 0:
                print(f"\nThere are no Holidays for {yr} Week #{wk}.")
            else:
                print(f"\nThese are the Holidays for {yr} Week #{wk}:")
                HolidayList.displayHolidaysInWeek(x)
        elif choice == 5:
            print("Exit")
            print("=======")
            exit = str(input("Are you sure you want to exit? [y/n]: ")).lower()
            
            if exit == "y":
                print("Goodbye!")
                usercontinue = False
                saved = False
            elif exit == 'n':
                print("Returning to the main menu")
            elif saved == True:
                doubleexit = str(input("Are you sure you want to exit?\nYour changes will be lost.\n[y/n]:"))
            if doubleexit == 'y':
                print("Goodbye!")
                usercontinue = False
            elif doubleexit == 'n':
                print("Returning to the main menu")
            else:
                print("Error:\n That is not a valid choice.")








    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





