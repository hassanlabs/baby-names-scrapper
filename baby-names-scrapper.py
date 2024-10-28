from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Path to your browser driver (e.g., ChromeDriver)
driver_path = "C:/1/chromedriver.exe"

# Initialize Selenium WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open the URL
url = "https://parenting.firstcry.com/baby-names/boy/religion/hindu/"
driver.get(url)

# Wait for the initial content to load
time.sleep(5)

# Initialize lists to store names and descriptions
names = []
descriptions = []

# Define the function to scrape the data
def scrape_data(container):
    try:
        # Find all name elements within the specific section using the 'data-name' attribute
        name_elements = container.find_elements(By.CSS_SELECTOR, 'div[data-name]')
        # Find all description elements within the specific section using 'span[data-name]' inside 'div.names'
        desc_elements = container.find_elements(By.CSS_SELECTOR, 'div.names span[data-name]')

        # Extract the 'data-name' attribute from each element and add to the lists
        for name, desc in zip(name_elements, desc_elements):
            names.append(name.get_attribute('data-name'))
            descriptions.append(desc.text)
            print(name.get_attribute('data-name'), '--------', desc.text)
    except Exception as e:
        print(f"Error during scraping data: {e}")

# Find the specific scrollable section by its class or ID (update the selector accordingly)
try:
    container = driver.find_element(By.CSS_SELECTOR, 'ul.names-list')  # Update selector if necessary
except Exception as e:
    print(f"Error finding the container: {e}")
    driver.quit()

# Scroll within this container and scrape the data
last_height = driver.execute_script("return arguments[0].scrollHeight", container)
while True:
    print('Scrolling...')
    # Scroll down inside the container
    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)

    # Wait for the new content to load within the container
    time.sleep(5)

    # Scrape data within the container
    scrape_data(container)

    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return arguments[0].scrollHeight", container)
    
    # If new height is the same as the last height, it means no new content is loaded
    if new_height == last_height:
        break

    last_height = new_height

# Store the scraped data in a DataFrame
data = pd.DataFrame({
    'Name': names,
    'Description': descriptions
})

# Remove duplicates in case any names/descriptions were captured multiple times during scrolling
data = data.drop_duplicates()

# Save the data to a CSV file
data.to_csv('baby_names_dynamic_scroll.csv', index=False)

print(f"Scraping completed, {len(data)} names saved to 'baby_names_dynamic_scroll.csv'.")

# Close the browser
driver.quit()
