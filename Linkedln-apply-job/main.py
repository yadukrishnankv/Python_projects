from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

def close_window():
    close_btn = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_btn.click()

    discard_btn = driver.find_element(By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")
    discard_btn.click()

linkedin_url = "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(linkedin_url)

time.sleep(1)
sign_in = driver.find_element(By.XPATH, value='//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')
sign_in.click()

time.sleep(1)
username = driver.find_element(By.XPATH, value='//*[@id="base-sign-in-modal_session_key"]')
username.send_keys("ADD YOUR MAIL", Keys.TAB, "ADD YOUR PASSWORD", Keys.ENTER)

input("Press enter after solving the captcha: ")

time.sleep(2)
all_jobs = driver.find_elements(By.CLASS_NAME, value="job-card-list__title--link")
for job in all_jobs:
    job.click()
    time.sleep(1)

    try:
        easy_apply = driver.find_element(By.CSS_SELECTOR, value='.jobs-apply-button--top-card button')
        easy_apply.click()

        phone_num = driver.find_element(By.CLASS_NAME, value=" artdeco-text-input--input")
        if phone_num == "":
            phone_num.send_keys("1234567890")
        time.sleep(1)

        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
        print(submit_button.text)
        if submit_button.text == "Next":
            close_window()
            print("Complex application, skipped.")
            continue
        else:
            # Click Submit Button
            print("Submitting job application")
            submit_button.click()

    except NoSuchElementException:
        print("Next job.")
        close_window()
        continue

