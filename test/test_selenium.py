
import selenium
from selenium import webdriver

URL="https://www.naver.com"



driver = webdriver.Chrome(executable_path='chromedriver85')
driver.get(url=URL)