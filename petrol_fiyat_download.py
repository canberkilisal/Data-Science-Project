from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

EXECUTABLE_PATH = "C:/Users/Casper/Desktop/chrome_driver/chromedriver.exe"
LOCATIONS = ["İSTANBUL (AVRUPA)", "İSTANBUL (ANADOLU)"]
FUEL_TYPE = ["Kurşunsuz Benzin 95 Oktan", "Motorin"]

# Configure the Selenium webdriver with Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Create a Service object with the path to the Chrome web driver
SERVICE = Service(executable_path=EXECUTABLE_PATH)

# Start the service
SERVICE.start()

# Pass the Service object to the webdriver
driver = webdriver.Chrome(service=SERVICE, options=options)

start_date = datetime.strptime("01.01.2020", "%d.%m.%Y")
finish_date = datetime.strptime("01.03.2020", "%d.%m.%Y")
stop_date = datetime.strptime("01.01.2023", "%d.%m.%Y")

while start_date < stop_date:

    # Load the webpage
    driver.get('https://bildirim.epdk.gov.tr/bildirim-portal/faces/pages/tarife/petrol/illereGorePetrolAkaryakitFiyatSorgula.xhtml')

    # Start Time
    start_time = driver.find_element(By.ID, 'akarYakitFiyatlariKriterleriForm:j_idt29_input')
    start_time.clear()
    start_date_string = start_date.strftime("%d.%m.%Y")
    start_time.send_keys(start_date_string)

    # Finish Time
    finish_time = driver.find_element(By.ID, 'akarYakitFiyatlariKriterleriForm:j_idt36_input')
    finish_time.clear()
    finish_date_string = finish_date.strftime("%d.%m.%Y")
    finish_time.send_keys(finish_date_string)


    # Brand
    Select(driver.find_element(By.ID, "akarYakitFiyatlariKriterleriForm:j_idt32_input"))\
        .select_by_value("BP")

    for location in LOCATIONS:
        # Location
        Select(driver.find_element(By.ID, "akarYakitFiyatlariKriterleriForm:j_idt39_input"))\
            .select_by_value(location)

        for fuel_type in FUEL_TYPE:
            # Fuel Type
            Select(driver.find_element(By.ID, "akarYakitFiyatlariKriterleriForm:j_idt46_input"))\
                .select_by_value(fuel_type)

            # 'Sorgula' button
            button = driver.find_element(By.ID, 'akarYakitFiyatlariKriterleriForm:j_idt49')
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)

            # Download Results
            button = driver.find_element(By.ID, 'akarYakitFiyatlariKriterleriForm:j_idt51')
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)

    finish_date = finish_date + relativedelta(months=2)
    start_date = start_date + relativedelta(months=2)

driver.quit()
SERVICE.stop()
