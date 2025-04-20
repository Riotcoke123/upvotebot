from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
import logging

# Setup logging
logging.basicConfig(filename='likebot-error.log', level=logging.ERROR)

# Credentials
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'

# Define already upvoted posts set
already_upvoted = set()

# Chrome Options for header configuration
options = Options()
options.add_argument("--start-maximized")  # Open Chrome maximized
options.add_argument("--disable-extensions")
options.add_argument("--headless")  # Comment this out if you want to see the browser
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36')

# Suppress WebGL warning by disabling software rasterizer
options.add_argument("--disable-software-rasterizer")

# Set custom headers using Chrome DevTools Protocol
def set_custom_headers(driver):
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    })
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
        "headers": {
            "referer": "https://communities.win/c/IP2Always/new",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-api-key": "x-api-key",
            "x-api-platform": "Scored-Desktop",
            "x-api-secret": "x-api-secret",
            "x-xsrf-token": "x-xsrf-token"
        }
    })

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Apply custom headers to the driver
set_custom_headers(driver)

# Function to log errors
def log_error(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    logging.error(f"[{timestamp}] {msg}")

# Open the target website
driver.get("https://communities.win/c/IP2Always/new")

# Wait for the page to load
time.sleep(3)

# Log in
try:
    login_button = driver.find_element(By.CSS_SELECTOR, '#app > header > div.sc-1tg9jte-32.gcGDRG.navbar > div.sc-1tg9jte-1.fsVFHt.desktop > div.sc-1tg9jte-31.iuSply > div > div.sc-1tg9jte-5.dGvpnF')
    login_button.click()
    time.sleep(2)

    # Enter credentials
    username_field = driver.find_element(By.ID, 'field-9')
    password_field = driver.find_element(By.ID, 'field-10')
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    
    # Click the login button
    login_submit_button = driver.find_element(By.CSS_SELECTOR, '#chakra-modal-8 > footer > button.chakra-button.css-za4or7')
    login_submit_button.click()
    time.sleep(5)

    print("✅ Logged in successfully")
except Exception as e:
    log_error(f"Login failed: {str(e)}")

# Function to upvote posts
def upvote_post():
    try:
        # Get upvote buttons
        upvote_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.sc-1tigerj-0.sc-1tigerj-1.fQDdlK.fQWcKY.up.vote-delta')
        
        for button in upvote_buttons:
            aria_label = button.get_attribute('aria-label') or button.text

            if aria_label not in already_upvoted:
                disabled = button.get_attribute('disabled')

                # If the button isn't disabled, click it
                if not disabled:
                    button.click()
                    already_upvoted.add(aria_label)
                    print(f"✅ Upvoted: {aria_label}")
                    time.sleep(random.uniform(1.5, 2.5))  # Random delay
                else:
                    print(f"Skipped disabled post: {aria_label}")
            else:
                print(f"Skipped already upvoted post: {aria_label}")

    except Exception as e:
        log_error(f"Error upvoting posts: {str(e)}")

# Auto-scroll and upvote loop
scroll_count = 0
while True:
    try:
        # Upvote posts on the current page
        upvote_post()

        # Scroll to the bottom to load more posts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4 + random.uniform(0, 2))  # Randomize delay to simulate human scrolling
        scroll_count += 1
        print(f"🔁 Scrolled {scroll_count} times")

    except Exception as e:
        log_error(f"Error in upvoting loop: {str(e)}")
        break

# Optionally close the browser
# driver.quit()
