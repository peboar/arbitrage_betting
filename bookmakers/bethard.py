from pathlib import Path
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from helpers import *

def bethard(sport='football', leagues=[]):
    web = "https://www.bethard.com/sv/sports"

    # firefox_path = "/usr/local/bin/"
    path = Path(__file__).parent.parent / sport


    firefox_path = r"C:\Users\ogy572\AppData\Local\Mozilla Firefox\firefox.exe"

    games = []
    odds = []
    name = "bethard" + "_" + sport + ".pickle"
    filename = path / name
    # Open browser
    options = Options()
    options.binary_location = FirefoxBinary(firefox_path)
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(web)

    # Cookies
    cookie_cn = "icon.icon-times"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, cookie_cn)))
    cookie = driver.find_element(By.CLASS_NAME, cookie_cn)
    driver.execute_script("arguments[0].click();", cookie)

    # Switch frame to find matches
    iframe_tn = "iframe"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, iframe_tn)))
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, iframe_tn))

    # Select sport
    sport_labels_cn = "sports-list-item.sports-list-item-live "
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, sport_labels_cn)))
    sport_labels = driver.find_elements(By.CLASS_NAME, sport_labels_cn)
    for sport_label in sport_labels:
        if eng_to_swe(sport) == sport_label.text.strip().lower():  # Only match start of string
            driver.execute_script("arguments[0].click();", sport_label)
            break

    tabs_cn = "tab-switch-btn"
    "tabs-Center_TabSwitchResponsiveBlock_17974"
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, tabs_cn)))
    tabs = driver.find_elements(By.CLASS_NAME, tabs_cn)
    tabs_text = [tab.text for tab in tabs]
    counter = 0

    # Makes sure all league button is present
    while "Alla ligor" not in tabs_text and counter < 1e2:  # Not working right now
        counter += 1
        print(counter, tabs_text)
        tabs = driver.find_elements(By.CLASS_NAME, tabs_cn)
        tabs_text = [tab.text for tab in tabs]

    # Switch to find all competitions
    for tab in tabs:
        if tab.text.lower() == "alla ligor":
            driver.execute_script("arguments[0].click();", tab)

    # Show all competitions button
    show_all_btn_cn = "rj-league-list__show-all-btn"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, show_all_btn_cn)))
    show_all_btn_cn = driver.find_element(By.CLASS_NAME, show_all_btn_cn)
    driver.execute_script("arguments[0].click();", show_all_btn_cn)

    # Store hrefs of competitions
    hrefs = set()  # Store links to scrape data
    competitions_cn = "rj-league-list__item-link"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, competitions_cn)))
    competitions = driver.find_elements(By.CLASS_NAME, competitions_cn)

    for competition in competitions:
        if not leagues:
            hrefs.add(competition.get_attribute("href"))
        else:
            ct = competition.text

            if len(ct.split("-")) > 1:
                if any(l.lower() in ct.lower() and eng_to_swe(c.lower()) in ct.lower() for c, l in leagues):
                    hrefs.add(competition.get_attribute("href"))
            else:
                if any(l.lower() in ct.lower() for c, l in leagues):
                    hrefs.add(competition.get_attribute("href"))

    events_css = "div[class^='rj-ev-list__ev-card rj-ev-list__ev-card--regular rj-ev-list__ev-card']"
    names_cn = "rj-ev-list__bet-btn__content.rj-ev-list__bet-btn__text"
    odds_event_cn = "rj-ev-list__bet-btn__content.rj-ev-list__bet-btn__odd"

    for href in hrefs:
        driver.get(href) # Open link to scrape
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, events_css)))
            events = driver.find_elements(By.CSS_SELECTOR, events_css)
        except selenium.common.exceptions.TimeoutException:
            print("No events found")
            continue

        while events:
            event = events.pop(0)
            driver.execute_script("arguments[0].scrollIntoView(true);", event)  # Scroll to find all

            events = driver.find_elements(By.CSS_SELECTOR, events_css) # Find new dynamic elements
            if event in events:
                slice_index = events.index(event)
                events = events[slice_index + 1:]  # Slicing to prevent duplicates

            names_el = event.find_elements(By.CLASS_NAME, names_cn)
            n_names = len(names_el)
            names = [None] * n_names
            for i in range(n_names):
                names[i] = names_el[i].text

            odds_event_el = event.find_elements(By.CLASS_NAME, odds_event_cn)
            n_odds = len(odds_event_el)
            odds_event = [None] * n_odds  # Have to use n_odds for check if odds are missing
            for i in range(n_odds):
                odds_event[i] = odds_event_el[i].text

            # Need to check if empty odds need extra caring
            if all(odds_event) and odds_event:
                games.append(game_string(*names))
                odds.append(game_odds(*odds_event))

    driver.close()
    save_frame(filename, games, odds, web)