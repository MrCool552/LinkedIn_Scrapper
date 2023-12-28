import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import csv

def setup_driver():
    '''Setting up chrome Driver'''
    return webdriver.Chrome()

def login(driver, username, password):
    '''LinkedIn login USERNAME/PASSWORD to succesful scrape profile details
    '''
    driver.get('https://www.linkedin.com/login')
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button').click()
    print("Login Successfully")

def visit_profile(driver, profile_url):
    '''Parsing Profile as an response'''
    driver.get(profile_url)
    return driver.page_source

def parse_profile(html):
    '''Using HTML parser to parse the response targeted tag'''
    soup = BeautifulSoup(html, 'html.parser')

    # Extract the name, headline, location, and summary
    name = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text.strip()
    title = soup.find('div', {'class': 'text-body-medium break-words'}).text.strip()
    location = soup.find('span', {'class': 'text-body-small inline t-black--light break-words'}).text.strip()

    text_span = soup.find("span", class_="t-14 t-normal")
    experience = text_span.find("span").get_text(strip=True) if text_span else None

    return {
        'Name': name,
        'Headline': title,
        'Location': location,
        'Experience': experience
    }

def close_driver(driver):
    driver.quit()

def save_to_csv(data_list, csv_filename='linkedin_profiles.csv'):
    '''Saving the Data as per desired data format '''

    header = ['Name', 'Headline', 'Location', 'Experience']

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data_list)

if __name__ == "__main__":

    driver = setup_driver()

    #please enter the your valid Linked Creadentials for login USE .Env file to save the password.
    linkedin_username = 'PLEASE ENTER YOUR LINKEDIN EMAIL ADDRESS HERE'
    linkedin_password = os.getenv('pswrd') # set your password in .env file

    # Login in to LinkedIn
    login(driver, linkedin_username, linkedin_password)

    # List of well-known LinkedIn profiles in Technology
    profiles = [
        'https://www.linkedin.com/in/williamhgates/',
        'https://www.linkedin.com/in/satyanadella/',
        'https://www.linkedin.com/in/garyvaynerchuk/',
        'https://www.linkedin.com/in/kunalshah1/',
        'https://www.linkedin.com/in/arvindkrishna/'
    ]

    # List to store scraped data
    data_list = []

    for profile_url in profiles:
        page_source = visit_profile(driver, profile_url)
        driver.implicitly_wait(10)
        # extract information from the profile
        profile_data = parse_profile(page_source)
        data_list.append(profile_data)

    # Saving data to CSV
    save_to_csv(data_list)

    # Close the browser
    close_driver(driver)
