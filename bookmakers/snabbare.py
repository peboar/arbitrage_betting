import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from helpers import *
from selenium.webdriver.common.keys import Keys


def snabbare(sport='football'):
    games = []
    odds = []

    web = "https://www.snabbare.com/sv/sportsbook"
    firefox_path = "/usr/local/bin/"
    path = '/home/per/Desktop/pythonProject/arbitrage_betting/' + sport + '/'
    filename = path + 'snabbare' + '_' + sport

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_path, options=options)
    driver.get(web)

    # Cookie
    cookie_cn = "btn.btn--ghost"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, cookie_cn)))
    cookie = driver.find_element(By.CLASS_NAME, cookie_cn)
    driver.execute_script("arguments[0].click();", cookie)

    # Switch frame to find matches
    iframe_tn = "iframe"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, iframe_tn)))
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, iframe_tn))

    # Select sport
    sport_labels_cn = "sports-list-item-text-name"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, sport_labels_cn)))
    sport_labels = driver.find_elements(By.CLASS_NAME, sport_labels_cn)
    for sport_label in sport_labels:
        if eng_to_swe(sport) == sport_label.text.strip().lower(): # Only match start of string
            driver.execute_script("arguments[0].click();", sport_label)
            break

    # Loop to get both live and coming games
    buttons_cn = "tab-switch-btn"
    buttons = []
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, buttons_cn)))
    counter = 0
    buttons = driver.find_elements(By.CLASS_NAME, buttons_cn)
    buttons_text = [button.text.lower() for button in buttons]

    # Makes sure live button
    while "matchkalender" not in buttons_text and counter < 1e2:
        counter += 1
        buttons = driver.find_elements(By.CLASS_NAME, buttons_cn)
        buttons_text = [button.text.lower() for button in buttons]

    # Collapsible strings
    collapsibles_cn = "rj-instant-collapsible"
    click_collapsibles_cn = "rj-instant-collapsible__trigger" # Clickable to collapse
    view_more_cn = "rj-ev-list__view-more-btn"

    # Scroll to top html
    html_tag = "html"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, html_tag)))
    html_element = driver.find_element(By.TAG_NAME, html_tag)

    # Date strings for calender
    date_cn = "rj-carousel-item"

    # Events, names, and odds strings
    events_cn = "rj-ev-list__ev-card__buttons-holder.rj-ev-list__ev-card__buttons-holder--regular"
    names_cs_cn = "rj-ev-list__bet-btn__content.rj-ev-list__bet-btn__text"
    odds_event_cn = "rj-ev-list__bet-btn__content.rj-ev-list__bet-btn__odd"
    n_odds_cn = "rj-ev-list__bet-btn__inner"
    for button in buttons:
        if button.text.lower() == "live nu" or button.text.lower() == "matchkalender":
            driver.execute_script("arguments[0].click();", button)

            # Date tabs only exist for matchkalender
            if button.text.lower() == "live nu":
                tabs = [None]
            elif button.text.lower() == "matchkalender":
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, date_cn)))
                    tabs = driver.find_elements(By.CLASS_NAME, date_cn)
                except selenium.common.exceptions.TimeoutException:
                    tabs = [None]
                    print("tab tab not found")

            # Loop over all tabs
            for tab in tabs:

                html_element.send_keys(Keys.HOME)  # Must scroll back to top to load dynamic elements

                # Change date
                if tab:
                    driver.execute_script("arguments[0].click();", tab)

                # Collapse hidden bets,
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, collapsibles_cn)))

                #  Wait for staleness
                if button.text.lower() == "matchkalender":
                    try:
                        stale_check = driver.find_elements(By.CLASS_NAME, collapsibles_cn)
                        if stale_check:
                            WebDriverWait(driver, 5).until(EC.staleness_of(stale_check[0]))
                    except selenium.common.exceptions.TimeoutException:
                        pass

                # Have to scroll to load all collapsibles
                collapsibles = driver.find_elements(By.CLASS_NAME, collapsibles_cn)
                while collapsibles:
                    collapsible = collapsibles.pop(0)

                    is_not_collapsed = collapsible.get_attribute("data-collapsed")
                    click_collapsible = collapsible.find_element(By.CLASS_NAME, click_collapsibles_cn)
                    driver.execute_script("arguments[0].scrollIntoView(true);", collapsible)  # Scroll to find all
                    if is_not_collapsed == "true":
                        driver.execute_script("arguments[0].click();", click_collapsible)

                    if not collapsibles:  # When only last element remains
                        time.sleep(2)  # Sleep to make sure new elements are loaded
                        # Press view more button
                        try:
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, view_more_cn)))
                            view_more = driver.find_element(By.CLASS_NAME, view_more_cn)
                            driver.execute_script("arguments[0].click();", view_more)
                            time.sleep(2)
                        except selenium.common.exceptions.TimeoutException:
                            pass

                    # Finds the new collapsibles after scrolling
                    collapsibles = driver.find_elements(By.CLASS_NAME, collapsibles_cn)  # Find new dynamic elements
                    if collapsible in collapsibles:
                        slice_index = collapsibles.index(collapsible)
                        collapsibles = collapsibles[slice_index + 1:]  # Slicing to prevent duplicates

                    # Scraping odds
                    counter = 0
                    max_counter = 100
                    events = []
                    # While loop to make sure all games are loaded
                    while not events and counter < max_counter:
                        events = collapsible.find_elements(By.CLASS_NAME, events_cn)
                        counter += 1
                        for event in events:
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, names_cs_cn)))
                            names_el = event.find_elements(By.CLASS_NAME, names_cs_cn)
                            n_names = len(names_el)
                            names = [None] * n_names
                            for i in range(n_names):
                                names[i] = names_el[i].text

                            odds_event_el = event.find_elements(By.CLASS_NAME, odds_event_cn)
                            n_odds = len(event.find_elements(By.CLASS_NAME, n_odds_cn))
                            n_found_odds = len(odds_event_el)
                            odds_event = [None] * n_odds  # Have to use n_odds for check if odds are missing
                            for i in range(n_found_odds):
                                odds_event[i] = odds_event_el[i].text

                            if all(odds_event) and odds_event:
                                games.append(game_string(*names))
                                odds.append(game_odds(*odds_event))

    driver.close()
    save_frame(filename, web, games, odds)
#









