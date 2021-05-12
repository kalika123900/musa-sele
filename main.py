from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from definitions import ROOT_DIR
import getpass


# Global variables
delay = 3
bus_website = 'https://www.business.gov.om/portal/searchEstablishments'
user_data_dir = "./user-data"

def check_cr(cr):

    # cr='114425'

    # open website
    driver.get(bus_website)

    # locate the text box
    try:
        search_box = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'commercial_no')))
    except TimeoutException:
        # TODO: Handle errors in the fully functional webapp
        print("Loading search box took too much time!")


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

    #     TODO: return from this function and ustalize the variables by adding them into a database or sending them back to the front end page using flask/django

    except TimeoutException:
        pass

    # search for the 'results not found error'
    try:
        results_not_found = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "// div[ @ class = 'alert alert-warning']")))
        print('CR search results section displayed | CR not found')

    #     TODO: send an error message to the front end saying that CR number not found in bus website

    except TimeoutException:
        # TODO: Handle errors in the fully functional webapp
        print("Loading 'results' table OR 'results not found' section took too much time!")



    # return the results

    return

def instagram_check(user_name, cr_no):

    driver.get('https://www.instagram.com/{0}/'.format(user_name))

    # Load the entire source code of the page in a variable
    src = driver.page_source

    # Check if the CR number exists the page
    if cr_no in src:
        # cr no found in the page
        check_cr(cr_no[3:])

    else:
        print('cr not found')
    # cr no not found in the page


    # TODO: Respond with a message
    print('CR number verified from bus')

    return

# verify CR in website
def website_cr_verification(cr_page, cr_no):

    # TODO: get the cr_page and cr_no from the business owner submitted form
    # Manually using hard coded cr_page and cr_number for testing only
    # cr_page = 'https://muscatmobiles.com/terms-and-conditions/'
    # cr_no = 'CR:1144252'

    # Open business web page which has the CR number
    driver.get(cr_page)

    # Load the entire source code of the page in a variable
    src = driver.page_source

    # Check if the CR number exists the page
    if cr_no in src:
        # cr no found in the page

        check_cr(cr_no[3:])

    else:
        print('cr not found')
    # cr no not found in the page

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    # options.add_argument(r"--user-data-dir=C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
    driver = webdriver.Chrome(options=options, executable_path=r'F:\python\ali\chromedriver.exe')


    # Website verification
    website_cr_verification(cr_page='https://muscatmobiles.com/terms-and-conditions/', cr_no='CR:1144252')

    # Instagram verification
    instagram_check(user_name='muscatmobiles', cr_no='CR:1144252')


