from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Настройка браузера
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("Открываю Indeed...")
    driver.get("https://www.indeed.com/jobs?q=truck+driver")
    time.sleep(5)

    titles = driver.find_elements("css selector", "h2.jobTitle span")
    
    # Находим карточки
    job_cards = driver.find_elements("css selector", "div.job_seen_beacon")
    data = [] 

    for card in job_cards:
        try:
            title_elem = card.find_element("css selector", "h2.jobTitle")
            driver.execute_script("arguments[0].click();", title_elem)
            time.sleep(7) 

            name = title_elem.text.strip()
            
            try:
                salary_val = driver.find_element("css selector", "#salaryInfoAndJobType").text.strip()
            except:
                salary_val = "Не указана"

            # ССЫЛКА 
            link = card.find_element("css selector", "h2.jobTitle a").get_attribute("href")

            print(f"Собрал: {name} | Зарплата: {salary_val}")

            if name: 
                data.append({
                    "Title": name,
                    "Salary": salary_val,
                    "URL": link,
                    "Source": "Indeed"
                })

        except Exception as e:
            continue

    df = pd.DataFrame(data)
    df.to_csv("indeed_vacancies.csv", index=False, encoding='utf-8-sig')
    print(f"\nУспех! Сохранено {len(data)} вакансий в indeed_vacancies.csv")
except Exception as e:
    print(f"Ошибка: {e}")

finally:

    driver.quit()   
