import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from email_sender import EmailSender
from logger import Logger

# Configure logging for this module
logger = Logger.get_logger()

class WebDriverManager:
    """Handles all WebDriver-related functionality."""

    def __init__(self, url):
        self.url = url
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        try:
            logger.info("Initializing WebDriver...")
            driver = webdriver.Chrome()
            driver.get(self.url)
            logger.info("WebDriver initialized and URL loaded.")
            return driver
        except WebDriverException as e:
            logger.error(f"Error initializing WebDriver: {e}")
            raise

    def quit(self):
        """Close the WebDriver instance."""
        if self.driver:
            logger.info("Closing WebDriver...")
            self.driver.quit()

    def refresh(self):
        """Refresh the browser page."""
        logger.info("Refreshing the page...")
        self.driver.refresh()


class PriceChecker:
    """Handles the logic to check prices and sort options."""

    def __init__(self, driver_manager, threshold=599):
        self.driver_manager = driver_manager
        self.threshold = threshold
        self.wait = WebDriverWait(self.driver_manager.driver, 20)

    def sort_by_price(self):
        """Clicks on the sorting option to sort by price (low to high)."""
        try:
            logger.info("Attempting to sort by price...")
            sort_by = self.wait.until(ec.presence_of_element_located(
                (By.CLASS_NAME, "filterBar-dropDown-title-sort-by")
            ))
            sort_by.click()

            sort_option = self.wait.until(ec.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'מחיר נמוך לגבוה')]")
            ))
            sort_option.click()
            logger.info("Sorting by price successful.")
            time.sleep(3)  # Wait for the results to update
        except TimeoutException as e:
            logger.error(f"Timeout while trying to sort by price: {e}")
            raise

    def get_lowest_price(self):
        """Fetches the lowest price on the page."""
        try:
            price_element = self.wait.until(ec.presence_of_element_located((By.ID, "lastPriceDisp")))
            price_text = price_element.text
            price_value = int(price_text.replace("₪", "").replace(",", "").strip())
            logger.info(f"Found price: {price_value} ILS")
            return price_value
        except TimeoutException as e:
            logger.error(f"Timeout while waiting for price element: {e}")
            raise
        except ValueError as e:
            logger.error(f"Error converting price to an integer: {e}")
            raise

    def is_price_below_threshold(self, price):
        """Checks if the price is below the defined threshold."""
        return price < self.threshold


class NotificationService:
    """Handles notifications when a condition is met."""

    def __init__(self, email_service):
        self.email_sender = email_service

    def send_price_alert(self, price):
        """Sends a price alert email."""
        logger.info(f"Sending price alert for {price} ILS")
        self.email_sender.send_email(price)

    def send_error_alert(self):
        """Sends an error notification in case of failure."""
        logger.error("Sending error notification.")
        self.email_sender.send_email(0, True)  # Assuming you use `True` flag for error



class PriceMonitor:
    """Main class to orchestrate price checking and notifications."""

    def __init__(self, url, email_service, refresh_min=50, refresh_max=70):
        self.url = url
        self.refresh_min = refresh_min
        self.refresh_max = refresh_max
        self.driver_manager = WebDriverManager(self.url)
        self.price_checker = PriceChecker(self.driver_manager)
        self.notification_service = NotificationService(email_service)

    def run(self):
        """Main loop to run the price monitor."""
        try:
            logger.info("Starting price monitoring...")
            while True:
                self._print_current_time()

                # Step 1: Sort by price
                self.price_checker.sort_by_price()

                # Step 2: Get the lowest price
                price = self.price_checker.get_lowest_price()

                # Step 3: Check if price is below threshold
                if self.price_checker.is_price_below_threshold(price):
                    logger.info(f"Price below threshold found: {price} ILS")
                    self.notification_service.send_price_alert(price)
                    break  # Exit loop after sending alert
                else:
                    logger.info(f"No deals below threshold. Current lowest price: {price} ILS")

                # Step 4: Refresh with random delay
                refresh_time = random.randint(self.refresh_min, self.refresh_max)
                logger.info(f"Refreshing in {refresh_time} seconds...")
                time.sleep(refresh_time)
                self.driver_manager.refresh()

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            self.notification_service.send_error_alert()

        finally:
            self.driver_manager.quit()

    @staticmethod
    def _print_current_time():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Current Time: {current_time}")


# Usage
if __name__ == "__main__":
    URL = "https://www.fattal-alazman.co.il/"
    email_sender = EmailSender()
    monitor = PriceMonitor(URL, email_sender)
    monitor.run()
