import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from helpers import *


def comeon(sport='tennis'):
    web = 'https://www.comeon.com/sv/sportsbook'
    firefox_path = '/usr/local/bin/'

    games = []
    odds = []
    path = '/home/per/Desktop/pythonProject/arbitrage_betting/' + sport + '/'
    filename = path + 'comeon' + '_' + sport

    # Open browser
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_path, options=options)
    driver.get(web)

    # Cookies
    cookie_cs = 'btn.btn--ghost'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, cookie_cs)))
    cookie = driver.find_element_by_class_name(cookie_cs)
    driver.execute_script('arguments[0].click();', cookie)

    # Switch frame
    driver.switch_to.frame(0)

    # Choose sport
    href = '//a[@href="/sports/' + eng_to_swe(sport) + '/"]'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, href)))
    label = driver.find_element_by_xpath(href)
    driver.execute_script("arguments[0].click();", label)

    # Date carousels
    carousels_cs = 'rj-carousel-item'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, carousels_cs)))
    carousels = driver.find_elements_by_class_name(carousels_cs)

    for carousel in carousels:
        driver.execute_script('arguments[0].click();', carousel)
        time.sleep(1)

        collapsibles_cs = 'rj-instant-collapsible'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, collapsibles_cs)))
        collapsibles = driver.find_elements_by_class_name(collapsibles_cs)

        # Collapse hidden competitions
        for collapsible in collapsibles:
            if collapsible.get_attribute('data-collapsed') == 'true':
                trigger = collapsible.find_element_by_class_name('rj-instant-collapsible__trigger')
                driver.execute_script("arguments[0].click();", trigger)
                driver.execute_script("arguments[0].scrollIntoView(true);", collapsible)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, collapsibles_cs)))
        collapsibles = driver.find_elements_by_class_name(collapsibles_cs)
        time.sleep(1)

        # Collapse hidden events
        for collapsible in collapsibles:
            events_cs = 'rj-ev-list__ev-card__buttons-holder.rj-ev-list__ev-card__buttons-holder--regular'
            driver.execute_script("arguments[0].scrollIntoView(true);", collapsible)
            events = collapsible.find_elements_by_class_name(events_cs)
            counter = 0
            while not events and counter < 1e2:
                events = collapsible.find_elements_by_class_name(events_cs)
                counter += 1

            # Scraping odds
            for event in events:
                data_cs = 'rj-ev-list__bet-btn__row'
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, data_cs)))
                data = event.find_elements_by_class_name(data_cs)
                names = [d.text for d in data[::2]]
                odds_event = [d.text for d in data[1::2]]

                if all(odds_event):
                    games.append(game_string(*names))
                    odds.append(game_odds(*odds_event))

    driver.close()
    save_frame(filename, games, odds)
