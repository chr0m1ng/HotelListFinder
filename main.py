from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome import service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#Return if exists an element in the actual page by passing his class
def check_exists_by_class_name(element_class):
    try:
        driver.find_element_by_class_name(element_class)
    except NoSuchElementException:
        return False
    return True

#Check if the city of the Hotel match with the Searched City
def check_city(city):
    address = driver.find_element_by_class_name("address").text
    if city.lower() in address.lower():
        return True
    else:
        return False

#Reads the file with City in the First Line and the others are the Hotel List
lines = [line.rstrip('\n') for line in open('hoteis.txt')]
#Pop the First Line, it's the city
searchCity = lines.pop(0)

#Write The List of Hotels with the desired information
arquivoSaida = open('notas.txt', 'w')

#Location of Opera Driver
webdriver_service = service.Service('.\\operadriver_win64\\operadriver.exe')
webdriver_service.start()

#Location of Opera Browser
capabilities = {
    'operaOptions': {
        'binary': 'C:\\Program Files\\Opera\\launcher.exe'
    }
}
driver = webdriver.Remote(webdriver_service.service_url, capabilities)

for l in lines:
    driver.get('http://booking.com')
    #Clean and Write the Hotel Name on the Search Box
    driver.find_element_by_id("ss").clear()
    driver.find_element_by_id("ss").send_keys(l)
    
    #Click Outside the Search Box to remove the autocomplete List and then click in the Search Button
    driver.find_element_by_class_name("sb-searchbox__title-text").click()
    driver.find_element_by_class_name("sb-searchbox__button").click()

    #Check if the Hotel Exists
    if(check_exists_by_class_name("sr-hotel__name")):
        #Check if it's in the same city
        if(check_city(searchCity)):
            #Write the Name, the address and the Score of the Hotel to the Output File
            arquivoSaida.write(driver.find_element_by_class_name("sr-hotel__name").text + " - ")
            arquivoSaida.write(driver.find_element_by_class_name("address").text.split(',')[0] + " ")
            arquivoSaida.write(driver.find_element_by_class_name("review-score-badge").text + "\n")
        #If the Hotel isn't in the same city then Write to the Output that we couldn't found the hotel
        else:
            arquivoSaida.write(l + " NÃO ENCONTRADO NO Booking.com\n")    
    #If the Hotel isn't in the Booking.com then Write to the Output that we couldn't found the hotel
    else:
        arquivoSaida.write(l + " NÃO ENCONTRADO NO Booking.com\n")