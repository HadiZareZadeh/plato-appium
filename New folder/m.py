from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions
from appium import webdriver
from appium.options.android import UiAutomator2Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

appPackage = 'com.plato.android'

options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:deviceName": "Poco M4 pro",
    "appium:automationName": "UiAutomator2",
    "appium:noReset": True,
    "appium:fullReset": False,
    "appium:newCommandTimeout": 300,
    "appium:uiautomator2ServerInstallTimeout": 60000,
    "appium:ensureWebviewsHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:connectHardwareKeyboard": True
})

d = webdriver.Remote("http://127.0.0.1:4723", options=options)
if d.is_locked():
    d.execute_script('mobile: shell', {
        'command': 'input',
        'args': ['text', '7852'],
        'includeStderr': True,
        'timeout': 5000
    })
    d.execute_script('mobile: shell', {
        'command': 'input',
        'args': ['keyevent', '66'],
        'includeStderr': True,
        'timeout': 5000
    })

d.terminate_app(appPackage)
d.activate_app(appPackage)

game_tab = WebDriverWait(d, 10).until(EC.visibility_of_element_located(
    (By.ID, 'com.plato.android:id/plato_image_games')))
game_tab.click()

game_button = WebDriverWait(d, 10).until(EC.visibility_of_element_located(
    (By.ID, 'com.plato.android:id/game_list_item_ripple')))

games_button = d.find_elements(
    'id', "com.plato.android:id/game_list_item_ripple")


for game in games_button:
    print(game.find_element(By.ID, 'com.plato.android:id/game_list_item_title').text)
    # game.click()
    # sleep(2)
    # d.back()

sleep(2)

d.quit()
input('enter')
