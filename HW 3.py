# Homework: Python and Web Scraper
# Name: Emily Murphy
# Computing ID: ekm4xz


# =============================================================================
# Additional Sources:
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://vimeo.com/209499033
https://stackoverflow.com/questions/2363731/append-new-row-to-old-csv-file-python
https://stackoverflow.com/questions/43316608/remove-timestamp-from-date-string-in-python/43316706
https://www.geeksforgeeks.org/split-a-text-column-into-two-columns-in-pandas-dataframe/?ref=rp
https://stackoverflow.com/questions/38309729/count-unique-values-with-pandas-per-groups
# =============================================================================


# The first step is to confirm make sure I am in the correct working directory.
# I used os.mkdir('Homework 3') to create a new folder where the output would be stored and confirmed the directory.
import os
os.getcwd()
os.chdir('c:\\Users\\emkmu\\OneDrive\\Documents\\SDS\\CS 5010\\')
os.mkdir('Homework 3')
os.chdir('c:\\Users\\emkmu\\OneDrive\\Documents\\SDS\\CS 5010\\Homework 3')
os.getcwd()


# I used the following code to install the various modules I would need.
# Lines 29-32 are necessary to perform the web scrapping. Numpy and pandas is used to analyze the data afterwards.
pip install beautifulsoup4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from numpy import *
import pandas as pd


# Created a variable with the url.
my_url2 = 'https://tracker.flightview.com/FVAccess2/tools/fids/fidsDefault.asp?accCustId=FVWebFids&fidsId=20001&fidsInit=arrivals&fidsApt=ORD&fidsFilterAl=&fidsFilterDepap='

# Opening up connection, grabbing the page
uClient2 = uReq(my_url2)

# Turns the client into a variable
page_html2 = uClient2.read()
# Closes the client, so the link to the url is not open.
uClient2.close()
# Reads the html code from the url using the format "html.parser"
page_soup2 = soup(page_html2, "html.parser")

# I reviewed the html code to identify the patterns in the html.
# I also used 'Invesigate' in the web browser to see how the individual lines of data were entered.
page_soup2

# I determined each row of data started with the class 'odd' or 'even', and it alternated between these two.
# I started with the class 'odd' and found all the instances where this class was listed.
odd = page_soup2.findAll("tr", {"class":"odd"})

# I created a new variable call 'odd_flight' to review the first value in odd in more detail.
# Based on this code and reviewing the browser, I decided I would search for the variables:
#   airline carrier, flight number, arriving from city, flight status, expected date & time for arrival, and updated date & time for arrival.
odd_flight = odd[0]

# Below is the code I used to find each of the variables. These will be added to the for loop.
# Carrier: I used the appropriate class and .text method to return the string of only the airline name.
carrier = odd_flight.findAll("td",{"class":"ffAlLbl"})
carrier[0].text

# Flight Number: I used the appropriate class and .text method to return the string of only the flight number.
flightnum_odd = odd_flight.findAll("td",{"class":"c2"})
flightnum = flightnum_odd[0].text

# Arrival from city: I used the appropriate class and .text method to return the string of only the city.
fromcity_odd = odd_flight.findAll("td",{"class":"c3"})
fromcity = fromcity_odd[0].text

# Gate: I used the appropriate class and .text method to return the string of only the terminal number and gate.
gate_odd = odd_flight.findAll("td",{"class":"c7"})
gate = gate_odd[0].text

# Status:  I used the appropriate class and .text method to return the string.
# The string had additional spaces and letters, so I used .strip() to return only the status.
status_odd = odd_flight.findAll("td",{"class":"c4"})
status = status_odd[0].text.strip()

# Departure Time: After reviewing the html, I determined there was no class name for the dates and times.
# To reference to the correct line, I used the .next_sibling method to reach the correct string of data.
time1 = odd_flight.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_element
# The string returned was the entire datetime code, which did not work iwt hthe .strptime method. 
# I removed the unnecessary information, which only worked due to the standard naming convention between lines.
time1_string = time1[11:len(time1)-12]
# The datetime function could then be used to turn the string into the correct date and time.
time1_time = datetime.datetime.strptime(time1_string, "%Y-%m-%d,%H:%M:%S")
# I separated the date and time to store separately and converted to string to print later.
sch_date = str(time1_time.date())
sch_time = str(time1_time.time())

# Repeated the same process for updated date and time.
# Added the if loop in case the updated date and time was blank, which may occur in the case of a cancelled flight.
time2 = odd_flight.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_element
    if len(time2) == 1:
        arr_date=""
        arr_time=""
    else:
        time2_string = time2[11:len(time2)-12]
        time2_time = datetime.datetime.strptime(time2_string, "%Y-%m-%d,%H:%M:%S")
        arr_date = str(time2_time.date())
        arr_time = str(time2_time.time())


# AFter finding the variables,  I created a new file named ORD_Flights.csv
filename = "ORD_Flights.csv"
f = open(filename, "w")

# Wrote out the headers with commas to separate into different cells and wrote to the file.
headers = "carrier,flight_number,from city,gate,status,scheduled_date,scheduled_time,updated_date,updated_time\n"
f.write(headers)

# Created a for loop for all lines of data in odd using the code defined above.
for odd_flight in odd:
    carrier_odd = odd_flight.findAll("td",{"class":"ffAlLbl"})
    carrier = carrier_odd[0].text
    
    flightnum_odd = odd_flight.findAll("td",{"class":"c2"})
    flightnum = flightnum_odd[0].text
    
    fromcity_odd = odd_flight.findAll("td",{"class":"c3"})
    fromcity = fromcity_odd[0].text
    
    gate_odd = odd_flight.findAll("td",{"class":"c7"})
    gate = gate_odd[0].text
    
    status_odd = odd_flight.findAll("td",{"class":"c4"})
    status = status_odd[0].text.strip()
    
    time1 = odd_flight.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_element
    time1_string = time1[11:len(time1)-12]
    time1_time = datetime.datetime.strptime(time1_string, "%Y-%m-%d,%H:%M:%S")
    sch_date = str(time1_time.date())
    sch_time = str(time1_time.time())
    
    time2 = odd_flight.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_element
    if len(time2) == 1:
        arr_date=""
        arr_time=""
    else:
        time2_string = time2[11:len(time2)-12]
        time2_time = datetime.datetime.strptime(time2_string, "%Y-%m-%d,%H:%M:%S")
        arr_date = str(time2_time.date())
        arr_time = str(time2_time.time())
        
    # I printed all the variables to confirm there were no errors
    print(carrier)
    print(flightnum)
    print(fromcity)
    print(gate)
    print(status)
    print(sch_date)
    print(sch_time)
    print(arr_date)
    print(arr_time)
    
    # I wrote all the code to the file and separated each cell with "," and each line with "\n"
    # I added .replace, so the City, State would not be put in different cells.
    # International cities do not have a state listed, so this will prevent the columns from being inconsistent
    f.write(carrier + "," + flightnum + "," + fromcity.replace(",", "|") + "," + gate + "," 
            + status + "," + sch_date + "," + sch_time + "," + arr_date + "," + arr_time  +"\n")

# Closed the file. 
f.close()

# I repeated the entire process for the 'even' class.
even = page_soup2.findAll("tr", {"class":"even"})

even_flight = even[0]
even_flight

# The only difference is instead of writing to a file, I am appending these values onto ORD_Flights.csv
filename = "ORD_Flights.csv"
f_a = open(filename, "a")

for even_flight in even:
    carrier_even = even_flight.findAll("td",{"class":"ffAlLbl"})
    carrier = carrier_even[0].text
    
    flightnum_even = even_flight.findAll("td",{"class":"c2"})
    flightnum = flightnum_even[0].text
    
    fromcity_even = even_flight.findAll("td",{"class":"c3"})
    fromcity = fromcity_even[0].text
    
    gate_even = even_flight.findAll("td",{"class":"c7"})
    gate = gate_even[0].text
    
    status_even = even_flight.findAll("td",{"class":"c4"})
    status = status_even[0].text.strip()
    
    time1 = even_flight.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_element
    time1_string = time1[11:len(time1)-12]
    time1_time = datetime.datetime.strptime(time1_string, "%Y-%m-%d,%H:%M:%S")
    sch_date = str(time1_time.date())
    sch_time = str(time1_time.time())
    
    time2 = even_flight.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_element
    if len(time2) == 1:
        arr_date=""
        arr_time=""
    else:
        time2_string = time2[11:len(time2)-12]
        time2_time = datetime.datetime.strptime(time2_string, "%Y-%m-%d,%H:%M:%S")
        arr_date = str(time2_time.date())
        arr_time = str(time2_time.time())
    
    print(carrier)
    print(flightnum)
    print(fromcity)
    print(gate)
    print(status)
    print(sch_date)
    print(sch_time)
    print(arr_date)
    print(arr_time)
    
    f_a.write(carrier + "," + flightnum + "," + fromcity.replace(",", "|") + "," + gate + "," 
              + status + "," + sch_date + "," + sch_time + "," + arr_date + "," + arr_time  +"\n")
    
f_a.close()

# Now the csv file has all the flight information. I will next use pandas to import and analyze the data.

# I set it so the columns will be displayed fully.
pd.set_option('display.max_columns', None)

# I read ORD_Flights.csv into the data frame df.
df = pd.read_csv("ORD_Flights.csv",header=0,encoding = "ISO-8859-1")

# I used the following code to view df and ensure the data was loaded properly.
df.head()
df.count()

# Changed the | back to a "," in Washington, DC
df['from city'] = df['from city'].replace("Washington| DC", "Washington, DC")

# Split the City, State into two separate columns and added these columns to df.
# Washington, DC and international cities will be blank in the state column.
df[['city','state']] = df['from city'].str.split("|",expand=True)

# Filtered all flights for those that were delayed.
print("\n List of all delayed flights: \n",df[df['status']=='Delayed'])

# Determined the number of flight numbers for each flight status (arrived, in air, landed, delayed, etc)
print("\n Show the number of flight numbers for each status: \n",df[['flight_number','status']].groupby(['status']).count())

# Listed the cities with the most flights to Chicago O'Hare.
# Used the .nunique method with gate to determine the number of flights from each city, 
# because there are multiple flight numbers with each flight from a city.
city = df.groupby('city')['gate'].nunique()
freq_city = city.sort_values(ascending=False).head(10)
print("\n Cities with the Most Arrivals: \n",freq_city)


# Extra Credit

# Created a user defined field for airline name
airline = input("Please provide an airline name to look up: ")

# All the user to view all flights and their status for their selected airline
print("\n List of "+ airline + " flights: \n",df[df['carrier']==airline])

# Used get_dummies to turn each value of the status column into its own column with the value 0 or 1.
df_1 = pd.get_dummies(df, columns=['status'])

# Summed up all the delayed statuses for each airline carrier.
status_by_carrier = df_1.drop(['flight_number','status_Arrived','status_Departed','status_In Air','status_Landed','status_No Recent Info - Call Airline','status_Scheduled'], axis=1).groupby(['carrier']).sum()

# Filtered the data to only show carriers with 1 delayed flight and sorted to show the most delays to the least.
delays = status_by_carrier[status_by_carrier['status_Delayed'] > 0].sort_values('status_Delayed',ascending=False)
print('\n List of Airlines with the Most Delays: \n',delays)

df['scheduled_date'] = pd.to_datetime(df['scheduled_date'])
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])

df['updated_date'] = pd.to_datetime(df['updated_date'])
df['updated_time'] = pd.to_datetime(df['updated_time'])

df['Difference'] = (df['updated_time'] - df['scheduled_time'])

df.head(25)

# =============================================================================
# Code to make sure loops work
# =============================================================================



my_url = 'https://tracker.flightview.com/FVAccess2/tools/fids/fidsDefault.asp?accCustId=FVWebFids&fidsId=20001&fidsInit=arrivals&fidsApt=ORD&fidsFilterAl=&fidsFilterDepap='

# opening up connection, grabbing the page
uClient = uReq(my_url)

# turns the client into a variable
page_html = uClient.read()

# close the client
uClient.close()

page_soup = soup(page_html, "html.parser")

page_soup.title

even = page_soup.findAll("tr", {"class":"even"})

len(odd)


len(odd)
odd[0]

odd_flight = odd[6]

print(odd_flight.prettify)

print(odd_flight.get_text())


time1 = odd_flight.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_element
time1_string = time1[11:len(time1)-12]

time1_time = datetime.datetime.strptime(time1_string, "%Y-%m-%d,%H:%M:%S")

sch_date = str(time1_time.date())
sch_time = str(time1_time.time())

print(sch_date)
print(sch_time)


time2 = odd_flight.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_element

if len(time2) == 1:
    arr_date=""
    arr_time=""
else:
    time2_string = time2[11:len(time2)-12]
    time2_time = datetime.datetime.strptime(time2_string, "%Y-%m-%d,%H:%M:%S")
    arr_date = str(time2_time.date())
    arr_time = str(time2_time.time())

print(arr_date)
print(arr_time)


status_odd = odd_flight.findAll("td",{"class":"c4"})
status_odd[0].text.strip()


carrier = odd_flight.findAll("td",{"class":"ffAlLbl"})
carrier[0].text

flightnum = odd_flight.findAll("td",{"class":"c2"})
flightnum[0].text

tocity = odd_flight.findAll("td",{"class":"c3"})
tocity[0].text

gate = odd_flight.findAll("td",{"class":"c7"})
gate[0].text