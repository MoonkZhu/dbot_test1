import pyotp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_totp(two_fa_token):
    totp = pyotp.TOTP(two_fa_token)
    code = totp.now()
    print(f"Generated TOTP code: {code}")  # Debug info
    return code

def change_password(email, current_password, new_password, two_fa_token):
    # Initialize ChromeDriver (update the path to your downloaded chromedriver)
    service = Service(executable_path='path\\to\\chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    try:
        # Open Discord login page
        driver.get('https://discord.com/login')

        # Wait for the login page to load
        time.sleep(5)

        # Find the email input field and enter the email
        email_field = driver.find_element(By.NAME, 'email')
        email_field.send_keys(email)

        # Find the password input field and enter the current password
        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(current_password)

        # Press Enter to login
        password_field.send_keys(Keys.RETURN)

        # Wait for the login to process
        time.sleep(5)

        # Handle captcha if present
        try:
            # Check if the captcha is present
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="captcha"]'))
            )
            input("Please complete the captcha manually and press Enter to continue...")
        except:
            pass

        # Wait for the 2FA prompt to appear
        print("Waiting for 2FA prompt...")

        # Use a longer wait time and a more specific selector if necessary
        try:
            two_fa_field = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="6位数字身份验证码"]'))
            )
            print("2FA input field located.")
        except:
            print("Timeout waiting for 2FA input field.")
            return

        # Get the TOTP code
        totp_code = get_totp(two_fa_token)
        print(f"TOTP Code: {totp_code}")

        # Enter the TOTP code
        two_fa_field.send_keys(totp_code)
        two_fa_field.send_keys(Keys.RETURN)
        print("2FA Code entered.")

        # Wait for the main page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="containerDefault-"]'))
        )
        print("Logged in successfully.")

        # Navigate to User Settings
        user_settings_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="User Settings"]'))
        )
        user_settings_button.click()

        # Wait for the settings page to load
        time.sleep(5)

        # Navigate to Change Password section
        change_password_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[text()="Change Password"]'))
        )
        change_password_button.click()

        # Wait for the change password section to appear
        time.sleep(2)

        # Enter current password
        current_password_field = driver.find_element(By.NAME, 'current_password')
        current_password_field.send_keys(current_password)

        # Enter new password
        new_password_field = driver.find_element(By.NAME, 'new_password')
        new_password_field.send_keys(new_password)

        # Confirm new password
        confirm_password_field = driver.find_element(By.NAME, 'confirm_new_password')
        confirm_password_field.send_keys(new_password)

        # Submit the password change
        confirm_password_field.send_keys(Keys.RETURN)

        # Wait for a few seconds to ensure the password change is processed
        time.sleep(5)
    finally:
        # Close the browser
        driver.quit()

# Test account information
email = 'X'
current_password = 'X'
new_password = 'X'  # Replace with the new password you want to set
two_fa_token = 'X'

change_password(email, current_password, new_password, two_fa_token)
