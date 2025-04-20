from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # Import TimeoutException
import time
import random
import logging

# Setup logging
# Added format to include timestamp
logging.basicConfig(filename='likebot-debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Credentials
USERNAME = 'username'
PASSWORD = 'password'

# Define already processed buttons set using aria-label (Note: This might not be a perfectly reliable unique identifier for posts. Finding a post ID is better if possible)
# We will use this set to avoid re-processing buttons already clicked or identified as already upvoted in this session.
already_processed_buttons_identifier = set()

# --- UPDATED STABLE UPVOTE BUTTON SELECTOR ---
# Based on the HTML snippet: <button type="button" class="...">
# Targets a button with type="button" and the classes "up" and "vote-delta"
# Confirm this selector in your browser's developer tools!
UPVOTE_BUTTON_SELECTOR = 'button[type="button"].up.vote-delta'
# --------------------------------------------


# Chrome Options
options = Options()
options.add_argument("--start-maximized")  # Open Chrome maximized
options.add_argument("--disable-extensions")
# options.add_argument("--headless")  # Uncomment this if you don't want to see the browser
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
options.add_argument("--no-sandbox")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/555.0.0 Safari/555.0.0 Chrome/135.0.0.0') # Slightly modified UA
options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer

# Set custom headers using Chrome DevTools Protocol
# Note: These headers are typically for API requests and might not be necessary
# for simulating clicks on page elements. Kept from original code but commented out sensitive parts.
def set_custom_headers(driver):
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/555.0.0 Safari/555.0.0 Chrome/135.0.0.0" # Match options UA
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
            "x-api-key": "key", 
            "x-api-platform": "Scored-Desktop", 
            "x-api-secret": "secret",
            "x-xsrf-token": "token" ,
        }
    })

# Initialize the Chrome WebDriver
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    logging.info("WebDriver initialized successfully.")
    # Apply custom headers to the driver (optional, see note above)
    set_custom_headers(driver)
    logging.info("Custom headers applied (optional).")
except Exception as e:
    logging.error(f"Failed to initialize WebDriver or apply headers: {str(e)}")
    exit() # Exit if driver fails to initialize


# Open the target website
try:
    driver.get("https://communities.win/c/IP2Always/new")
    logging.info("Opened target website.")
    # Wait for a basic element to indicate the page has loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    logging.info("Page loaded.")
except Exception as e:
    logging.error(f"Failed to open website: {str(e)}")
    driver.quit()
    exit()


# Log in
# Note: Login selectors might be dynamic. Inspect the page for stable selectors if login fails.
try:
    # Wait for and click the login button
    login_button_selector = '#app > header > div.sc-1tg9jte-32.gcGDRG.navbar > div.sc-1tg9jte-1.fsVFHt.desktop > div.sc-1tg9jte-31.iuSply > div > div.sc-1tg9jte-5.dGvpnF'
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, login_button_selector))
    )
    logging.info("Login button found.")
    login_button.click()
    logging.info("Clicked login button.")

    # Wait for login modal to appear and enter credentials
    username_field_selector = 'field-9' # Using ID
    password_field_selector = 'field-10' # Using ID
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, username_field_selector)))
    password_field = driver.find_element(By.ID, password_field_selector)
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    logging.info(f"Entered username.") # Avoid logging password

    # Wait for and click the login submit button
    login_submit_button_selector = 'button.chakra-button.css-za4or7' # This might also be dynamic
    login_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, login_submit_button_selector))
    )
    logging.info("Login submit button found.")
    login_submit_button.click()
    logging.info("Clicked login submit button.")

    # Wait for login to complete (e.g., wait for an element that appears post-login or the login button to disappear)
    time.sleep(7) # Increased sleep as a fallback, replace with EC if possible
    logging.info("Login sequence completed. Assuming logged in.")

except Exception as e:
    logging.error(f"Login failed: {str(e)}")
    # Decide whether to continue if login fails - script will currently try to upvote.
    # If login is mandatory for upvoting, add 'driver.quit()' here.


# Function to find and upvote visible buttons using the stable selector
def upvote_visible_buttons():
    try:
        # Find all upvote buttons on the current page view
        # Use WebDriverWait to wait for at least one button matching the selector
        upvote_buttons = WebDriverWait(driver, 15).until(
             EC.presence_of_all_elements_located((By.CSS_SELECTOR, UPVOTE_BUTTON_SELECTOR))
        )
        logging.info(f"Found {len(upvote_buttons)} potential upvote buttons on the current view.")

        clicked_count = 0
        for button in upvote_buttons:
            # Use aria-label, text, or element string as a temporary identifier for tracking within this run
            button_identifier = button.get_attribute('aria-label') or button.text or str(button)

            # Check if this button identifier has already been processed in this run
            if button_identifier in already_processed_buttons_identifier:
                logging.debug(f"Skipped already processed button identifier: {button_identifier}")
                continue # Skip if already processed

            try:
                # --- START: CHECK FOR ALREADY UPVOTED STATE ---
                # YOU MUST REPLACE THE LOGIC BELOW based on your inspection of an already-upvoted button's HTML
                # Look for a specific class, attribute, or attribute value that indicates it's active/upvoted.

                is_already_upvoted_state = False # Default to False

                # Example Check 1: Check for a specific class on the button when it's upvoted
                # Replace 'upvoted-active-class' with the actual class name
                # button_classes = button.get_attribute('class', '')
                # if 'upvoted-active-class' in button_classes:
                #     is_already_upvoted_state = True
                #     logging.debug(f"Button {button_identifier} appears already upvoted based on class.")

                # Example Check 2: Check for a specific data attribute value when it's upvoted
                # Replace 'data-state' and 'active' with the actual attribute name and value
                # button_data_state = button.get_attribute('data-state')
                # if button_data_state == 'active':
                #      is_already_upvoted_state = True
                #      logging.debug(f"Button {button_identifier} appears already upvoted based on data-state.")

                # Example Check 3: Check for aria-pressed="true" if used for state
                # aria_pressed_state = button.get_attribute('aria-pressed')
                # if aria_pressed_state == 'true':
                #      is_already_upvoted_state = True
                #      logging.debug(f"Button {button_identifier} appears already upvoted based on aria-pressed.")

                # If you cannot find a reliable indicator, you may have to skip this check,
                # but be aware of the risk of undoing upvotes.

                # --- END: CHECK FOR ALREADY UPVOTED STATE ---

                if is_already_upvoted_state:
                    logging.info(f"Skipped button {button_identifier} as it appears already upvoted.")
                    already_processed_buttons_identifier.add(button_identifier) # Add to processed set to skip it on future checks within this scroll/loop
                    continue # Move to the next button

                # Original checks for enabled and visible before attempting to click
                if button.is_enabled() and button.is_displayed():
                     # Use JavaScript click as a fallback if direct click fails (uncomment if needed)
                     # driver.execute_script("arguments[0].click();", button)
                     button.click() # Attempt direct click

                     clicked_count += 1
                     already_processed_buttons_identifier.add(button_identifier) # Add identifier to the set after attempting click
                     logging.info(f"✅ Clicked upvote button: {button_identifier}")

                     # Human-like random delay after clicking
                     time.sleep(random.uniform(1, 2.5)) # Shorter delay after successful click

                else:
                     logging.debug(f"Skipped disabled or non-visible button: {button_identifier}")
                     # Optionally add disabled/invisible buttons to the processed set to avoid re-checking them repeatedly
                     # already_processed_buttons_identifier.add(button_identifier)

            except Exception as button_error:
                # Log errors related to processing a single button but continue
                logging.debug(f"Error clicking or processing button {button_identifier}: {str(button_error)}")
                # Consider adding the identifier to already_processed_buttons_identifier here too if an error occurs,
                # to avoid retrying the same problematic button repeatedly.
                # already_processed_buttons_identifier.add(button_identifier)


        logging.info(f"Attempted to process and click {clicked_count} upvote buttons on this scroll.")

    except TimeoutException:
         # This happens if no elements matching the selector are found within the wait time
         logging.info(f"No upvote buttons found on the current view within the timeout.")
    except Exception as e:
        logging.error(f"Error finding or iterating through upvote buttons: {str(e)}")


# Auto-scroll and upvote loop
scroll_count = 0
# Clear the set periodically to manage memory. Note: This means buttons from earlier scrolls might be re-attempted IF they reappear in the DOM AND are not marked as already upvoted.
BUTTONS_PROCESSED_BEFORE_CLEAR = 150 # Clear the set after attempting this many buttons

while True:
    try:
        # Find and upvote buttons on the current page view
        upvote_visible_buttons()

        # Scroll to the bottom to load more content
        logging.info("Scrolling down...")
        # Get current height
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load by checking scroll height or just a fixed delay
        # Increased and randomized delay to simulate human scrolling and allow content to load
        wait_time = 7 + random.uniform(0, 3)
        logging.info(f"Waiting for {wait_time:.2f} seconds for content to load.")
        time.sleep(wait_time)

        new_height = driver.execute_script("return document.body.scrollHeight")

        # Break loop if no new content loaded after scroll and wait (or if height stops increasing)
        if new_height == last_height:
            logging.info("End of page reached or no new content loaded after scrolling.")
            # Optional: Try one more scroll or wait longer if needed, but breaking is common here.
            break # Exit the loop if no new content

        scroll_count += 1
        logging.info(f"🔁 Scrolled {scroll_count} times. New page height: {new_height}")

        # Clear already_processed_buttons_identifier set periodically to avoid excessive memory usage
        # This set tracks buttons processed in the *current* session (clicked or skipped).
        if len(already_processed_buttons_identifier) >= BUTTONS_PROCESSED_BEFORE_CLEAR:
            logging.info(f"Clearing processed buttons list ({len(already_processed_buttons_identifier)} cleared).")
            already_processed_buttons_identifier.clear()

        # Optional: Add a condition to stop after a certain number of scrolls or time
        # if scroll_count > 30: # Example: stop after 30 scrolls
        #    logging.info("Stopping after 30 scrolls.")
        #    break

    except Exception as e:
        logging.error(f"Error in auto-scroll loop: {str(e)}")
        break # Exit the loop on error

# Optionally close the browser when the loop finishes or breaks
# driver.quit()
logging.info("Script finished.")
