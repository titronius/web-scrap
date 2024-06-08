from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import json


if __name__ == "__main__":
    chrome_path = ChromeDriverManager().install()
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('log-level=3')
    browser_service = Service(executable_path=chrome_path)
    browser = Chrome(service=browser_service, options=options)

    def wait_element(browser, delay_seconds = 1, by = By.CLASS_NAME, value = None):
        try:
            return WebDriverWait(browser, delay_seconds).until(
                expected_conditions.presence_of_element_located((by, value))
            )
        except:
            return False

    def create_json():
        json_data = []
        with open('vacancies.json', 'w', encoding='utf8') as file:
            file.write(json.dumps(json_data, indent=2, ensure_ascii=False))

    def add_to_json(json_data):
        data = json.load(open("vacancies.json"))
        data.append(json_data)
        with open("vacancies.json", "w", encoding='utf8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            
    browser.get("https://spb.hh.ru/vacancy?text=python&area=1&area=2")

    vacancy_list_tag = wait_element(browser, by = By.ID, value = "a11y-main-content")
    vacancy_tags = vacancy_list_tag.find_elements(By.CSS_SELECTOR, 'div.serp-item.serp-item_simple.serp-item_link')

    links = []

    for vacancy in vacancy_tags:
        a_tag = wait_element(vacancy, by = By.CLASS_NAME, value = "bloko-link")
        if a_tag:
            link = a_tag.get_attribute("href")
            links.append(link)
            
    create_json()

    for link in links:
        browser.get(link)
        
        vacancy_description_tag = wait_element(browser, by = By.CSS_SELECTOR, value = "[data-qa=vacancy-description]")
        desc_text = vacancy_description_tag.text.lower()
        
        if "django" in desc_text and "flask" in desc_text:
            salary_tag = wait_element(browser, by = By.CSS_SELECTOR, value = "[data-qa=vacancy-salary-compensation-type-net]")
            if salary_tag:
                salary = salary_tag.text
            else:
                salary = "ЗП не указана"

            company_name = wait_element(browser, by = By.CSS_SELECTOR, value = "[data-qa=vacancy-company-name]").text

            company_location_tag = wait_element(browser, by = By.CSS_SELECTOR, value = "[data-qa=vacancy-view-location]")
            if company_location_tag:
                company_location = company_location_tag.text
            else:
                company_location_tag = wait_element(browser, by = By.CSS_SELECTOR, value = "[data-qa=vacancy-view-link-location-text]")
                if company_location_tag:
                    company_location = company_location_tag.text
                else:
                    company_location = "Не указана локация"
            
            json_data = {
                'link': link,
                'salary': salary,
                'company_name': company_name,
                'company_location': company_location,  
            }

            add_to_json(json_data)
        