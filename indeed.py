from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# 1. Настройка маскировки
options = webdriver.ChromeOptions()
# Добавляем реальный User-Agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

data = []

try:
    print("Открываю Indeed...")
    driver.get("https://www.indeed.com/jobs?q=truck+driver")
    time.sleep(5) 

    # 2. Собираем ссылки
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

    print(f"Нашел {len(job_links)} ссылок. Начинаю сбор данных...")

    # 3. Глубокий сбор
    for job in job_links:
        current_name = job['name']
        current_url = job['url']
        try:
            driver.get(current_url)
            time.sleep(3) 

            try:
                # Ищем зарплату
                salary_elem = driver.find_element("css selector", "#salaryInfoAndJobType, .jobsearch-JobMetadataHeader-item")
                salary_val = salary_elem.text.strip()
            except:
                salary_val = "Не указана"

            print(f"Собрал: {current_name} | Зарплата: {salary_val}")

            data.append({
                "Title": current_name,
                "Salary": salary_val,
                "URL": current_url,
                "Source": "Indeed"
            })
            
        except Exception as e:
            print(f"Ошибка на вакансии {current_name}: {e}")
            continue

    # 4. Сохранение
    if data:
        df = pd.DataFrame(data)
        df.to_csv("indeed_vacancies.csv", index=False, encoding='utf-8-sig')
        print(f"\nУспех! Сохранено {len(data)} вакансий.")
    else:
        print("\nДанные не собраны.")

except Exception as e:
    print(f"Критическая ошибка: {e}")

finally:
    driver.quit()
