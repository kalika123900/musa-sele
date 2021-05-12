from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from definitions import ROOT_DIR

import os

# Global variables
delay = 3
bus_website = 'https://www.business.gov.om/portal/searchEstablishments'
user_data_dir = "./user-data"
# apply the chrome options to avoid logging in again
# options = webdriver.ChromeOptions()

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
# options.add_argument('headless')
# options.add_argument('window-size=0x0')
# options.add_argument('--disable-gpu')
# chrome_driver_path = ROOT_DIR + "/chromedriver.exe"

# driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
# driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_argument(r"--user-data-dir=C:\Users\{}\AppData\Local\Google\Chrome\User Data")
driver = webdriver.Chrome(options=options, executable_path=r'F:\python\ali\chromedriver.exe')

def check_cr(cr):

    # cr='114425'

    # open website
    driver.get(bus_website)

    # locate the text box
    search_box = ''
    try:
        search_box = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'commercial_no')))
    except TimeoutException:
        # TODO: Handle errors in the fully functional webapp
        print("Loading search box took too much time!")
        return 0

    # paste the cr
    search_box.send_keys(cr)

    # locate the search button
    try:
        search_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, "_eventId__search")))

    # click on search button
        search_button.click()
    except TimeoutException:
        # TODO: Handle errors in the fully functional webapp
        print("Loading search button took too much time!")
        return 0


    # wait for results table
    try:
        results_table = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

        rows = results_table.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
        row = rows[1] # Get the first row with data
        col = row.find_elements(By.TAG_NAME, "td")  # Get the columns (all the columns)


        # check contents of the results table
        cr_from_bus = col[0].text
        ar_name_bus = col[1].text
        en_name_bus = col[2].text
        status_bus = col[5].text

        print(cr_from_bus, ar_name_bus, en_name_bus, status_bus, sep='\n')
        return 1;
    #     TODO: return from this function and ustalize the variables by adding them into a database or sending them back to the front end page using flask/django

    except TimeoutException:
        pass

    # search for the 'results not found error'
    try:
        results_not_found = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "// div[ @ class = 'alert alert-warning']")))
        print('CR search results section displayed | CR not found')
        return 0
    #     TODO: send an error message to the front end saying that CR number not found in bus website

    except TimeoutException:
        # TODO: Handle errors in the fully functional webapp
        print("Loading 'results' table OR 'results not found' section took too much time!")
        return 0


    # return the results

    return 1

def instagram_check(user_name, cr_no):

    driver.get('https://www.instagram.com/{0}/'.format(user_name))

    # Load the entire source code of the page in a variable
    src = driver.page_source

    # Check if the CR number exists the page
    if cr_no in src:
        # cr no found in the page
      res =  check_cr(cr_no[3:])
      if res == 0:
        return 0
      else:
        return 1
    else:
        print('cr not found')
        return 0
    # cr no not found in the page


    # TODO: Respond with a message
    print('CR number verified from bus')
    return 1

    return

# verify CR in website
def website_cr_verification(cr_page, cr_no):

    # TODO: get the cr_page and cr_no from the business owner submitted form
    # Manually using hard coded cr_page and cr_number for testing only
    # cr_page = 'https://muscatmobiles.com/terms-and-conditions/'
    # cr_no = 'CR:1144252'
    print(cr_page)
    print(cr_no)
   

    # Open business web page which has the CR number
    driver.get(cr_page)

    # Load the entire source code of the page in a variable
    src = driver.page_source

    # Check if the CR number exists the page
    if cr_no in src:
        # cr no found in the page
       print(cr_no)

       res = check_cr(cr_no[3:])
       if res == 0:
        return 0
       else:
           return 1

    else:
        print('cr not found')
        return 0
    return 1