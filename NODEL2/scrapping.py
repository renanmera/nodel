#imports here
from typing import cast
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import time
  
#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome('C:/Users/renanmera/chromedriver.exe')

#open the webpage
driver.get("https://www.instagram.com/")

#target credentials
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

#enter username and password
username.clear()
username.send_keys("user")
password.clear()
password.send_keys("pass")

#target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#We are logged in!

#handle NOT NOW
not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
time.sleep(2)
not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
time.sleep(2)

driver.get("https://www.instagram.com/p/B166OkVBPJR/")

#load all father comments posible

try:
    load_more_comment = driver.find_element_by_class_name('glyphsSpriteCircle_add__outline__24__grey_9')
    while load_more_comment.is_displayed():
        load_more_comment.click()
        time.sleep(5)
        #whitout referencing the class again, it wont work
        load_more_comment = driver.find_element_by_class_name('glyphsSpriteCircle_add__outline__24__grey_9')
except Exception as e:
    pass

#load all child comments posible

childs = driver.find_elements_by_class_name('_61Di1')
for c in childs:
    c.click()

#declare lists for saving data

user_names = []
user_comments = []
user_dates = []
user_likescount = []
user_idFather = []
user_idChilds = []

obj_for_analysis = driver.find_elements_by_class_name('Mr508 ')
for c in obj_for_analysis:
    container = c.find_element_by_class_name('C4VMK')
    content = container.find_elements_by_css_selector('span')
    bar_container = container.find_element_by_class_name('_7UhW9 ')
    bar_content = bar_container.find_elements_by_class_name('FH9sR ')
    user_names.append(content[0].text)
    user_comments.append(content[1].text)
    user_dates.append(bar_content[0].text)
    user_likescount.append(bar_content[1].text)
    user_idFather.append('-1')
    user_idChilds.append('-1')
    try:
        child_obj = c.find_element_by_class_name('TCSYW')
        child_comments = child_obj.find_elements_by_class_name('gElp9 ')
        for j,cc in enumerate(child_comments):
            container2 = cc.find_element_by_class_name('C4VMK')
            content2 = container2.find_elements_by_css_selector('span')
            bar_container2 = container2.find_element_by_class_name('_7UhW9 ')
            bar_content2 = bar_container2.find_elements_by_class_name('FH9sR ')
            user_names.append(content2[0].text)
            user_comments.append(content2[1].text)
            user_dates.append(bar_content2[0].text)
            user_likescount.append(bar_content2[1].text)
            user_idFather.append(str(len(user_comments)-2-j))
            user_idChilds.append(str(j))
    except Exception as e:
        pass


dict = {'Names': user_names, 'Comments': user_comments, 'Dates': user_dates, 'IDFather': user_idFather, 'IDChild': user_idChilds, 'Likes': user_likescount}
df = pd.DataFrame(dict)
df.to_csv('NODEL_RESULT.csv')

driver.quit()