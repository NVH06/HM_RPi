import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def get_rate():
    options = Options()
    options.headless = True

    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get("https://www.immothekerfinotheker.be/nl/rentebarometer/")

    cookie = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')))
    cookie.click()

    dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div[2]/section/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]')))
    dropdown.click()

    actions = ActionChains(driver)
    for _ in range(2):
        actions.send_keys(Keys.DOWN).perform()
        time.sleep(1)

    actions.send_keys(Keys.ENTER).perform()

    rate_str = driver.find_element_by_xpath('//*[@id="gatsby-focus-wrapper"]/div[2]/section/div/div[2]/div/div[2]/div[2]').text
    rate = float(rate_str[:-1])

    driver.close()

    return rate

# print(get_rate())

