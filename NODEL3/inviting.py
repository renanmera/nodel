#imports here
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
  
#code by pythonjar, MariyaSha, ansokolov, not me

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome('C:/Users/renanmera/chromedriver.exe', options=chrome_options)

#open the webpage
driver.get("https://www.facebook.com/")

#target credentials
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

#enter username and password
username.clear()
username.send_keys("@gmail.com")
password.clear()
password.send_keys("pass")

#target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#We are logged in!

time.sleep(2)
driver.get("https://www.facebook.com/permalink.php?story_fbid=404502267619027&id=121067232629200")

#engagement
engagement_div = driver.find_element_by_css_selector("a[href*='/ufi/reaction']")
driver.execute_script("arguments[0].click();", engagement_div)

# switch to all engagement - not working
engagement_all = driver.find_element_by_css_selector("a[tabindex*='-1']")
driver.execute_script("arguments[0].click();", engagement_div)

# click see more until there no such option
while True:
    try:
        viewMoreButton = driver.find_element_by_css_selector("a[href*='/ufi/reaction/profile/browser/fetch']")
        driver.execute_script("arguments[0].click();", viewMoreButton)
        time.sleep(4)
    except Exception as e:
        break

# invite users
users = driver.find_elements_by_css_selector("a[ajaxify*='/pages/post_like_invite/send/']")
invitedUsers = 0

for user in users:
    #user = driver.find_element_by_css_selector("a[ajaxify*='/pages/post_like_invite/send/']")
    driver.execute_script("arguments[0].click();", user)
    invitedUsers = invitedUsers + 1
    time.sleep(3)

driver.quit()