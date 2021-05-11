from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(executable_path='../drivers/chromedriver.exe')
driver.maximize_window()
driver.implicitly_wait(10)
output = {}

# Step 1: Launch the website ixigo
driver.get('https://www.ixigo.com/')

# Step 2: Validate the page is opened
assert driver.find_element_by_id('ixiLogoImg').is_displayed()
print(driver.title)
assert driver.title == 'ixigo - Flights, IRCTC Train Booking, Bus Booking, Air Tickets & Hotels'

# Step 3: Enter From – Delhi , To – Bangalore , Departure – 27 April 2020 , Return – 24 June 2020 , Travelers - 2

# Enter From Location
from_text_filed = driver.find_element_by_xpath("//div[.='From']//input[@placeholder='Enter city or airport']")
from_text_filed.clear()
from_text_filed.send_keys('DEL')
time.sleep(2)
from_text_filed.send_keys(Keys.ENTER)

# Enter To location
to_text_field = driver.find_element_by_xpath("//div[.='To']//input[@placeholder='Enter city or airport']")
to_text_field.clear()
to_text_field.send_keys('BLR')
time.sleep(2)
to_text_field.send_keys(Keys.ENTER)


# Select Departure Date
driver.find_element_by_xpath("//input[@placeholder='Depart']").click()

try:
    if driver.find_element_by_xpath("//div[@class='rd-month-label']").text != 'June 2021':
        driver.find_element_by_xpath("//button[@class='ixi-icon-arrow rd-next']").click()
        driver.find_element_by_xpath("//td[@data-date='27062021']").click()
    else:
        driver.find_element_by_xpath("//td[@data-date='27062021']").click()
except NoSuchElementException:
    print('Calendar Not found')
time.sleep(5)

# Select Return Date
driver.find_element_by_xpath("//input[@placeholder='Return']").click()
calendar_move_next_buttons = driver.find_elements_by_xpath("//button[@class='ixi-icon-arrow rd-next']")
try:
    if driver.find_element_by_xpath("//div[@class='rd-month-label']").text != 'August 2021':
        calendar_move_next_buttons[1].click()
        driver.find_element_by_xpath("//td[@data-date='24082021']").click()
    else:
        driver.find_element_by_xpath("//td[@data-date='24082021']").click()
except NoSuchElementException:
    print('Calendar Not found')

# Enter number of passengers
driver.find_element_by_xpath("//div[.='Travellers | Class']//input").click()
driver.find_element_by_xpath("//div[.='Adult']/parent::div/parent::div//span[.='2']").click()

# Selecting Business class
driver.find_element_by_xpath("//div[@data-radioindex='1']//span[@class='radio-button u-pos-rel u-ib u-v-align-top']")\
    .click()

# Step 4: CLick an search and validate the results
driver.find_element_by_xpath("//button[.='Search']").click()

# Validate the search operation and results
print('Search page title', driver.title)
# assert driver.title == 'New Delhi - Bengaluru, Business Flights, roundtrip, 27 Jun - 24 Aug'
assert driver.find_element_by_link_text('FLIGHTS').is_displayed()

time.sleep(10)
# Step 5: Validate filter option and select Non Stop option in filters
assert driver.find_element_by_xpath("//div[@class='fltr-col-1 u-ib']").is_displayed()
driver.find_element_by_xpath("//div[@class='stops']//div[@data-checkboxindex='0']//span").click()

# Step 6: Print the results
results = driver.find_elements_by_xpath("//div[@class='result-col outr']//div[@class='summary-section']")
depature_time = driver.find_elements_by_xpath("//div[@class='result-col outr']//div[@class='time-group']/div[1]")
airine_text = driver.find_elements_by_xpath("//div[@class='result-col outr']//div[@class='airline-text']//div")
price =  driver.find_elements_by_xpath("//div[@class='result-col outr']//div[@class='price']//span[2]")

print(len(results))
print(len(depature_time))
print(len(airine_text))
print(len(price))

for result in range(0, len(results)+1):
    if int(price[result].text) < 25000:
        air_line_details = airine_text[result].text
        airline_number = air_line_details[-5:]
        print('Airline Number: ', airline_number, 'Departure Time: ',
              depature_time[result].text, 'Price: ', price[result].text)



