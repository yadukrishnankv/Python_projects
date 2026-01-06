from selenium import webdriver
from flask import Flask, jsonify, render_template, request

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote 
import time

app = Flask(__name__)

def close_window():
    close_btn = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_btn.click()

    discard_btn = driver.find_element(By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")
    discard_btn.click()

def close_after_submit(driver):
    try:
        done_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button/span[text()='Done']/parent::button")
            )
        )
        done_btn.click()
        time.sleep(2)
    except:
        try:
            driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss").click()
            time.sleep(1)
        except:
            pass

def run_bot(email, password, job_title, location,phone):

    encoded_job = quote(job_title)
    encoded_location = quote(location)

    linkedin_url = (
        f"https://www.linkedin.com/jobs/search/?"
        f"f_LF=f_AL&keywords={encoded_job}&location={encoded_location}"
    )
    

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--start-maximized')

    chrome_options.add_argument('--incognito')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(linkedin_url)

    time.sleep(1)
    sign_in = driver.find_element(By.XPATH, value='//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')
    sign_in.click()

    time.sleep(1)
    username = driver.find_element(By.XPATH, value='//*[@id="base-sign-in-modal_session_key"]')
    username.send_keys(email, Keys.TAB, password, Keys.ENTER)


    time.sleep(2)
    all_jobs = driver.find_elements(By.CLASS_NAME, value="job-card-list__title--link")
    for job in all_jobs:
        job.click()
        time.sleep(5)

        try:
            easy_apply = driver.find_element(By.ID, "jobs-apply-button-id")

            easy_apply.click()

            phone_num = driver.find_element(By.CLASS_NAME, value="artdeco-text-input--input")
            if phone_num.get_attribute("value") == "":
                phone_num.send_keys(phone)
            time.sleep(3)


            wait = WebDriverWait(driver, 10)
            while True:
                try:
                    next_btn = wait.until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "button[data-easy-apply-next-button]")
                        )
                    )
                    print("Clicking Next")
                    next_btn.click()
                    time.sleep(2)

                except:
                    try:
                        review_btn = wait.until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, "button[data-live-test-easy-apply-review-button]")
                            )
                        )
                        print("Clicking Review")

                        try:
                            Select(driver.find_element(By.TAG_NAME, "select")).select_by_visible_text("Yes")
                        except:
                            pass

                        review_btn.click()
                        time.sleep(2)

                    except:
                        try:
                            submit_btn = wait.until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, "button[data-live-test-easy-apply-submit-button]")
                                )
                            )
                            print("Submitting Application")
                            submit_btn.click()
                            time.sleep(3)
                            close_after_submit(driver)
                            print("Application completed, moving to next job")
                            break

                        except:
                            print("Complex application → skipped")
                            close_window()
                            break


        except NoSuchElementException:
            print("Next job.")
            close_window()
            continue

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        run_bot(
            request.form["email"],
            request.form["password"],
            request.form["job_title"],
            request.form["location"],
            request.form["phone"]
        )
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
