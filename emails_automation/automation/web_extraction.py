from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os

def web_scrapy(url):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)  

    # Find all links
    elements = driver.find_elements(By.TAG_NAME, "a")
    file_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.docx', '.xlsx', '.zip']

    # Collect file links
    file_links = []
    for elem in elements:
        href = elem.get_attribute('href')
        if href and any(href.lower().endswith(ext) for ext in file_extensions):
            file_links.append(href)
            
    output_folder = "downloads"
    os.makedirs(output_folder, exist_ok=True)

    for i, file_link in enumerate(file_links, start=1):
        file_response = requests.get(file_link)
        file_extension = os.path.splitext(file_link)[1]
        file_filename = os.path.join(output_folder, f"file_{i}{file_extension}")

        with open(file_filename, "wb") as file:
            file.write(file_response.content)

        print(f"Downloaded: {file_filename}")

    driver.quit()


# if __name__ == "__main__":
#     # url = "https://tcpdf.org/examples/example_041/"
#     url = "https://www.princexml.com/samples/"
    
#     web_scrapy(url)