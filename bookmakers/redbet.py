import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bookmakers.helpers import *


def redbet(sport='tennis'):
    games = []
    odds = []

    web = "https://www.redbet.com/int/sports/home"
    firefox_path = "/usr/local/bin/"
    path = '/home/per/Desktop/pythonProject/arbitrage_betting/' + sport + '/'
    filename = path + 'redbet' + '_' + sport

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_path, options=options)
    driver.get(web)

    # Cookie 1
    cookie_cn = "btn.btn--flash__accept.btn--button"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, cookie_cn)))
    cookie1 = driver.find_element(By.CLASS_NAME, cookie_cn)
    driver.execute_script("arguments[0].click();", cookie1)

    # Cookie 2
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, cookie_cn)))
    cookie2 = driver.find_element(By.CLASS_NAME, cookie_cn)
    driver.execute_script("arguments[0].click();", cookie2)

    sport_labels_cn = "KambiBC-navigation-menu__label-wrapper"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, sport_labels_cn)))
    sport_labels_cn = driver.find_elements(By.CLASS_NAME, sport_labels_cn)

    for sport_label in sport_labels_cn:
        if sport == sport_label.text.strip().lower():
            driver.execute_script("arguments[0].click();", sport_label)
            break

    # Collapse uncollapsed competitions
    collapsibles_css = "div[class^='CollapsibleContainer__CollapsibleWrapper-sc-'][class$='mod-event-group-container']"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, collapsibles_css)))
    collapsibles = driver.find_elements(By.CSS_SELECTOR, collapsibles_css)
    click_collapse_css = "header[class^='CollapsibleContainer__HeaderWrapper']"
    while collapsibles:
        for collapsible in collapsibles:
            click_collapse = collapsible.find_element(By.CSS_SELECTOR, click_collapse_css)  # Cannot click collapsibles
            driver.execute_script("arguments[0].click();", click_collapse)
        collapsibles = driver.find_elements(By.CSS_SELECTOR, collapsibles_css)

    # Collapse inner
    sub_collapsibles_cn = "CollapsibleContainer__HeaderWrapper-sc-1bmcohu-1.fntBWx"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, sub_collapsibles_cn)))
    sub_collapsibles = driver.find_elements(By.CLASS_NAME, sub_collapsibles_cn)
    while sub_collapsibles:
        for sub_collapsible in sub_collapsibles:
            driver.execute_script("arguments[0].click();", sub_collapsible)
        sub_collapsibles = driver.find_elements(By.CLASS_NAME, sub_collapsibles_cn)

    # Scraping odds
    events_cn = "KambiBC-event-item__event-wrapper"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, events_cn)))
    events = driver.find_elements(By.CLASS_NAME, events_cn)

    for event in events:
        names_cn = "KambiBC-event-participants__name"
        names_el = event.find_elements(By.CLASS_NAME, names_cn)  #
        n_names = len(names_el)
        names = [None]*n_names
        for i in range(n_names):
            names[i] = names_el[i].text

        outcome_cn = "KambiBC-bet-offer__outcomes"  # Only scrapes outcomes

        try:
            outcome = event.find_element(By.CLASS_NAME, outcome_cn)
            odds_event_css = "div[class^='OutcomeButton__Odds-sc']"
            odds_event_el = outcome.find_elements(By.CSS_SELECTOR, odds_event_css)
            n_odds = len(odds_event_el)
            odds_event = [None] * n_names  # Have to use n_names for check if odds are missing

            for i in range(n_odds):
                odds_event[i] = odds_event_el[i].text

        except selenium.common.exceptions.NoSuchElementException:
            if all(names):
                print("Failed to retrieve match odds for {}".format(game_string(*names)))

        if all(odds_event) and odds_event:
            games.append(game_string(*names))
            odds.append(game_odds(*odds_event))

    driver.close()
    save_frame(filename, games, odds)



