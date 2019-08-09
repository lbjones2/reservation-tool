#Libraries for bot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import  Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

#Libraries for email
import smtplib
from email.message import EmailMessage
import requests
import time

#Global variables for user to input
dateStr = "05/09/2019" #Change date as Needed
#Future updates will have ability to set party size and exact time - Default party size is 2
#partySizeStr = "4"
#primaryTimeStr = '2:00 PM'

#Function to set up email 
def emailFun():
    try:
        #Creating basic message to send over email
        msg = EmailMessage()
        msg.set_content('There is an open dinner reservation at the Lamplight Lounge on '+dateStr+' for 2')
        
        #Establishing SMTP server for emailcommunication
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()

        ###############################################################################
        #Enter user email and password HERE: 'email','password' (must be gmail account)
        ###############################################################################
        server.login('', '')
        
        #Formatting message
        msg['Subject'] = 'Open Reservation'
        #Enter sender email HERE 'email'
        msg['From'] = ''
        #Enter recepitent emails HERE: 'email,email,...'
        msg['To'] = ''
        
        #Sending the message to the email address from dummy email
        server.send_message(msg)
        server.close()
    except:
        print('Something went wrong...')

#Function returning wether or not a reservation is found for the requested date
def botFun():
    #open up the webpage in chrome (enter your own chromedriver executable path)
    browser = webdriver.Chrome(executable_path='/Users/lucas/Documents/Bot/chromedriver')
    browser.get("https://disneyland.disney.go.com/dining/disney-california-adventure/lamplight-lounge/")

    #Timeout interval for webpage to load
    timeout = 10
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='finderDetailsExperienceImage pepde-span-34']")))
    except TimeoutException:
        print("timeout")
        browser.quit()

    #Find date form and send it the user inputted date
    dateInput = browser.find_element_by_id('diningAvailabilityForm-searchDate')
    dateInput.clear()
    dateInput.send_keys(dateStr)

    #Find time form and send it the user inputted time
    #Opens time dropdown menu
    timer = browser.find_element_by_id('searchTime-wrapper')
    timer.click()
    #Selects appropriate time from dropdown
    myTime = browser.find_element_by_xpath("//*[@id='diningAvailabilityForm-searchTime-1']")
    timeActions = ActionChains(browser)
    timeActions.move_to_element(myTime).perform()
    myTime.click()

    #Find party size form and send it the user inputted party size
    #Opens party size dropdown menu
    party = browser.find_element_by_id('partySize-wrapper')
    party.click()
    #Selects appropriate party size from dropdown menu
    myParty = browser.find_element_by_xpath("//*[@id='partySize-1']")
    partyActions = ActionChains(browser)
    partyActions.move_to_element(myParty).perform()
    myParty.click()

    #Click the button to send the data to the form
    button = browser.find_element_by_xpath("//*[@id='dineAvailSearchButton']")
    button.click()

    #Add delay so website can update
    time.sleep(15)

    #Logic to see if a reservation is avaliable
    try:
        browser.find_element_by_class_name('ctaNoAvailableTimesContainer')
        browser.close()
        #If the reservation not avaliable indicator is found
        return False
    except NoSuchElementException: 
        #If notAvaliable element is not found
        browser.close()
        return True

#Main Function
def main():
    #User of the script has not received an email
    noEmail = True

    #While the user has not received an email check for reservations
    while(noEmail == True):
        resAvail = botFun()
        print(resAvail)
        if(resAvail == True):
            emailFun()
            noEmail = False

if (__name__ == '__main__'):
    main()