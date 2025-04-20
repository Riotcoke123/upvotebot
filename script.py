from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import logging

# Credentials & Config
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'
URL = "https://communities.win/c/IP2Always/new"
LOGIN_BUTTON_CSS = "#app > header > div > div.sc-1tg9jte-1.fsVFHt.desktop > div.sc-1tg9jte-31.iuSply > div > div.sc-1tg9jte-5.dGvpnF"
USERNAME_CSS = "#field-9"
PASSWORD_CSS = "#field-10"
SUBMIT_CSS = "#chakra-modal-8 > footer > button.chakra-button.css-za4or7"

UPVOTE_CSS = "div > div > div > div.sc-ct8gzq-1.dzTwau.vote > button.sc-1tigerj-0.sc-1tigerj-1.fQDdlK.fQWcKY.up.vote-delta"
SKIP_CSS = "div > div > div > div.sc-ct8gzq-1.ftfLxN.vote > button.sc-1tigerj-0.sc-1tigerj-1.fQDdlK.fQWcKY.up.vote-delta.active"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# Step 1: Open page
driver.get(URL)

# Step 2: Open login popup
try:
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_BUTTON_CSS)))
    login_button.click()
except Exception as e:
    logging.error("Could not click login popup: " + str(e))
    driver.quit()
    exit()

# Step 3: Fill login form
try:
    username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, USERNAME_CSS)))
    password_input = driver.find_element(By.CSS_SELECTOR, PASSWORD_CSS)

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SUBMIT_CSS)))
    submit.click()
    time.sleep(6)  # Wait for login
except Exception as e:
    logging.error("Login failed: " + str(e))
    driver.quit()
    exit()

# Step 4: Start upvoting loop
already_clicked = set()
scroll_count = 0

while True:
    try:
        # Skip already upvoted
        skipped = driver.find_elements(By.CSS_SELECTOR, SKIP_CSS)
        for btn in skipped:
            already_clicked.add(btn)

        # Find unvoted buttons
        upvote_buttons = driver.find_elements(By.CSS_SELECTOR, UPVOTE_CSS)
        logging.info(f"Found {len(upvote_buttons)} total vote buttons. Skipping {len(already_clicked)} already voted.")

        click_count = 0
        for btn in upvote_buttons:
            if btn in already_clicked:
                continue
            try:
                if btn.is_displayed() and btn.is_enabled():
                    btn.click()
                    already_clicked.add(btn)
                    click_count += 1
                    logging.info("⬆️ Upvoted a post")
                    time.sleep(random.uniform(1, 2.5))
            except Exception as e:
                logging.warning("Could not click a button: " + str(e))

        # Scroll down to load more
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(4, 6))
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            logging.info("Reached end of the page.")
            break

        scroll_count += 1
        logging.info(f"Scrolled {scroll_count} times.")

    except Exception as e:
        logging.error("Error in main loop: " + str(e))
        break

driver.quit()
logging.info("Done.")
