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
    
    # 1. Находим карточки
    cards = driver.find_elements("css selector", "div.job_seen_beacon")
    job_links = []
    for card in cards:
        try:
            t_elem = card.find_element("css selector", "h2.jobTitle a")
            job_links.append({
                "name": t_elem.text.strip(),
                "url": t_elem.get_attribute("href")
            })
        except:
            continue

    data = []
    print(f"Начинаю глубокий сбор для {len(job_links)} вакансий...")

    for job in job_links:
        try:
            driver.get(job['url'])
            time.sleep(3) 

            try:
                salary_elem = driver.find_element("css selector", "#salaryInfoAndJobType, .jobsearch-JobMetadataHeader-item")
                salary_val = salary_elem.text.strip()
            except:
                salary_val = "Не указана"

            print(f"Проверено: {job['name']} | Зарплата: {salary_val}")

            data.append({
                "Title": job['name'],
                "Salary": salary_val,
                "URL": job['url'],
                "Source": "Indeed"
            })
            
        except Exception as e:
            print(f"Ошибка на вакансии {job['name']}: {e}")
            # ССЫЛКА (важно!)
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

    #Сохраняем 
    df = pd.DataFrame(data)
    df.to_csv("indeed_vacancies.csv", index=False, encoding='utf-8-sig')
    print(f"\nУспех! Сохранено {len(data)} вакансий в indeed_vacancies.csv")
except Exception as e:
    print(f"Ошибка: {e}")

finally:
    driver.quit()   
