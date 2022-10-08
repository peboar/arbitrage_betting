from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from helpers import *


def unibet(sport='football'):
    games = []
    odds = []

    web = "https://www.unibet.se/betting/sports/home"
    firefox_path = "/usr/local/bin/"
    path = '/home/per/Desktop/pythonProject/arbitrage_betting/' + sport + '/'
    filename = path + 'unibet' + '_' + sport

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_path, options=options)
    driver.get(web)

    # Cookies
    cookie_xp = '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cookie_xp)))
    cookie = driver.find_element(By.XPATH, cookie_xp)
    driver.execute_script("arguments[0].click();", cookie)

    sport_labels_cn = '_3dfd9'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, sport_labels_cn)))
    sport_labels = driver.find_elements(By.CLASS_NAME, sport_labels_cn)
    for sport_label in sport_labels:
        if eng_to_swe(sport.lower()) == sport_label.text.strip().lower():
            driver.execute_script('arguments[0].click();', sport_label)
            break

    # Collapse uncollapsed competitions
    collapsibles_cn = "_5f930 "
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, collapsibles_cn)))
    collapsibles = driver.find_elements(By.CLASS_NAME, collapsibles_cn)
    for collapsible in collapsibles:
        is_collapsed = collapsible.find_elements(By.CLASS_NAME, collapsibles_cn)
        click_collapse = collapsible.find_elements(By.CLASS_NAME, '_488fa._16e3c._0175e.fd7df')  # Cannot click _5f930
        if not is_collapsed and click_collapse:
            driver.execute_script("arguments[0].click();", click_collapse[0])

    # Collapse inner
    sub_collapsibles_cn = '_488fa.d7975.fd7df'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, sub_collapsibles_cn)))
    sub_collapsibles = driver.find_elements(By.CLASS_NAME, sub_collapsibles_cn)
    for sub_collapsible in sub_collapsibles:
        is_not_collapsed = sub_collapsible.find_elements(By.ID, 'expand')
        if is_not_collapsed:
            driver.execute_script("arguments[0].click();", sub_collapsible)

    # X coordinate to only get match odds
    match_odds_coordinate_css = "div[class^='_63e0b d54d4']"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, match_odds_coordinate_css)))
    match_odds_coordinate = driver.find_element(By.CSS_SELECTOR, match_odds_coordinate_css).location["x"]

    events_cn = 'c21a2'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, events_cn)))
    events = driver.find_elements(By.CLASS_NAME, events_cn)
    # Scraping odds
    for event in events:
        names_cn = 'ca197.isExpandedView'
        names_el = event.find_elements(By.CLASS_NAME, names_cn)
        n_names = len(names_el)
        names = [None]*n_names
        for i in range(n_names):
            names[i] = names_el[i].text

        odds_event_cards_css = "div[class^='bb419']"
        odds_event_cards = event.find_elements(By.CSS_SELECTOR, odds_event_cards_css)

        for odds_event_card in odds_event_cards:
            x_coordinate = odds_event_card.location["x"]
            print(x_coordinate, match_odds_coordinate)
            if x_coordinate < match_odds_coordinate: # Coordinate of match odds
                odds_event_cn = '_278bc'
                odds_event_el = odds_event_card.find_elements(By.CLASS_NAME, odds_event_cn)
                n_odds = len(odds_event_el)
                odds_event = [None] * n_odds

                for i in range(n_odds):
                    odds_event[i] = odds_event_el[i].text

                if all(odds_event) and odds_event:
                    games.append(game_string(*names))
                    odds.append(game_odds(*odds_event))

    # driver.close()
    save_frame(filename, games, odds)


