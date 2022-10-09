from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options = options)

driver.get("https://masteringruneterra.com/meta-tier-list/")
table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "meta-archetypes-content")))
soup = BeautifulSoup(table.get_attribute("innerHTML"), 'html.parser')
driver.close()

exceptions = ["Lee", "Sin", "Tahm", "Kench", "Aurelion", "Sol", "Jarvan", "IV", "Master", "Yi", "Miss", "Fortune", "Twisted", "Fate"]


def write_to_csv(soup):

    decks = soup.find_all('div', {"class": "deck-title wp-dark-mode-ignore"})
    match = soup.find_all('div', {"class": "deck-detail matches-played wp-dark-mode-ignore"})
    play_rate = soup.find_all('div', {"class": "deck-detail play-rate wp-dark-mode-ignore"})
    win_rate = soup.find_all('div', {"class": "deck-detail win-rate wp-dark-mode-ignore"})

    for place in range(1, 101):
        champs = decks[place-1].text.split()
        heroes = []
        single = True
        for i in range(len(champs)):
            if champs[i] not in heroes:
                if champs[i] not in exceptions:
                    heroes.append(champs[i])
                    single = True
                elif (champs[i] in exceptions) and single:
                    two_word_champ = champs[i] + " " + champs[i + 1]
                    heroes.append(two_word_champ)
                    single = False

        mat = match[place-1].text.split()[1]
        win = win_rate[place-1].text.split()[2][:-1]
        play = play_rate[place-1].text.split()[2][:-1]
        while len(heroes) < 3:
            heroes.append(None)
        list_input = [place, heroes[0], heroes[1], heroes[2], mat, win, play]

        with open("allDecks.csv", "a") as file:  # Open the csv file.
            csv_writer = csv.writer(file)
            csv_writer.writerow(list_input)


write_to_csv(soup)