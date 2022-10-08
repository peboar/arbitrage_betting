from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bets import Odds
from unidecode import unidecode
from selenium.webdriver.firefox.options import Options


def betfair(matches, sport='tennis'):
    web = 'https://www.betfair.se/'
    path = '/usr/local/bin/'
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(path, options=options)
    # driver = webdriver.Firefox(path)
    driver.get(web)

    # Cookies
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
    cookie = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
    driver.execute_script("arguments[0].click();", cookie)



# /html/body/div[1]/div[2]/div/div/div/div[1]/div[2]/ul/li[5]/a

    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "/sport/tennis")))

    sport_label = driver.find_element_by_xpath("//a[@href ='/sport/" + sport + "']")
    driver.execute_script("arguments[0].click();", sport_label)


    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/span")))
    full_list = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/span')
    driver.execute_script("arguments[0].click();", full_list)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "src-CompetitionMarketGroup")))
    competitions = driver.find_elements_by_class_name("src-CompetitionMarketGroup")

    for i in range(len(competitions)):

        names = competitions[i].find_elements_by_class_name("rcl-ParticipantFixtureDetailsTeam")
        odds = competitions[i].find_elements_by_class_name("sgl-ParticipantOddsOnly80_Odds")
        n = len(odds)//2
        odds1 = odds[:n]
        odds2 = odds[n:]

        #Has to wait to get all matches for some reason
        if i == 0:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "rcl-ParticipantFixtureDetailsTeam")))

        for j in range(n):
            if odds[j].text.strip():
                if "/" in names[2*j].text and "/" in names[2*j+1].text:
                    n1 = names[2*j].text.strip().lower()
                    n2 = names[2*j+1].text.strip().lower()
                else:
                    n1 = names[2*j].text.strip().lower().split()[0] + " " + names[2*j].text.strip().lower().split()[-1]
                    n2 = names[2*j+1].text.strip().lower().split()[0] + " " + names[2*j+1].text.strip().lower().split()[-1]
                match = n1 + ' vs ' + n2
                match = match.replace("-", " ")
                o1 = float(odds1[j].text.strip())
                o2 = float(odds2[j].text.strip())
                matches.append(unidecode(match), Odds([o1, o2], web))







