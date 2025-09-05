# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 23:19:14 2024

@author: 34711
"""

import pandas as pd
import time
import os

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


#Abrimos el navegador
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.maximize_window()
browser.get('https://www.wegow.com/es/')

#Click en el botón de cookies
cookies_button = (WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,
    "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))))
cookies_button.click()

#Hacemos click en festivales añadiendo espera
festivales_button = WebDriverWait(browser, 60).until(
    EC.visibility_of_element_located((By.XPATH, "//div[@class='title-option' and text()='FESTIVALES']")))
festivales_button.click() 

#Definimos la columna de ciudades
cities_column = WebDriverWait(browser, 60).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.w-60.flex.flex-col")))

#Definimos todas las opciones de la columna de ciudades
cities = cities_column.find_elements(By.CSS_SELECTOR, "a.option")

#Creamos un dataframe y listas vacias que rellenaremos
festivales = pd.DataFrame(columns=["city", "event_names", "event_dates","event_prices", "event_followers"])

city_names = []
event_names = []
event_dates = []
event_prices = []
event_followers = []

#Tomamos los datos de cada festival de cada ciudad
for i in range(len(cities)):
    
    city = cities[i]
    name = city.text.split()[-1]
    city.click()
    
    event_container = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.flex-wrap.justify-start")))
    events = WebDriverWait(browser, 60).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.event-card.main-small.m-1")))
    
    for event in events:
        
        event_name = event.find_element(By.CSS_SELECTOR, "h2.font-museo-500.text-left.event-name").text
        
        event_names.append(event_name)

        event_date = event.find_element(By.CSS_SELECTOR, "span.event-date.font-museo-300").text
        
        event_dates.append(event_date)
        
        try:
            event_price = event.find_element(By.CSS_SELECTOR, "span.font-museo-700.align-middle")
            event_price = event_price.text
            
        except NoSuchElementException:
            
            event_price = None
            
        event_prices.append(event_price)

        followers = event.find_element(By.CSS_SELECTOR, "span.followers-container").text
        
        event_followers.append(followers)
        
        city_names.append(name)
        
        
    festivales_button = WebDriverWait(browser, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='title-option' and text()='FESTIVALES']")))
    festivales_button.click()
   
    cities_column = WebDriverWait(browser, 60).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.w-60.flex.flex-col")))
    cities = cities_column.find_elements(By.CSS_SELECTOR, "a.option")
    

#Asignamos a cada columna del dataframe la lista
festivales['city'] = city_names
festivales['event_names'] = event_names
festivales['event_dates'] = event_dates
festivales['event_prices'] = event_prices
festivales['event_followers'] = event_followers


festivales.to_csv("./data/festivalesprueba_city.csv", index=False)

#Vamos a hacer el mismo procedimiento con la columna de los géneros
genre_column = WebDriverWait(browser, 60).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.w-\[16rem\].flex.flex-col")))

festivales_by_genre = pd.DataFrame(columns=["genre", "event_names", "event_dates","event_prices", "event_followers"])

genres = genre_column.find_elements(By.CSS_SELECTOR, "a.option")

genre_names = []
event_names = []
event_dates = []
event_prices = []
event_followers = []

for i in range(len(genres)):
    
    genre = genres[i]
    name = genre.text.split()[-1]
    genre.click()
    
    event_container = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.flex-wrap.justify-start")))
    events = WebDriverWait(browser, 60).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.event-card.main-small.m-1")))
    
    for event in events:
        
        event_name = event.find_element(By.CSS_SELECTOR, "h2.font-museo-500.text-left.event-name").text
    
        event_names.append(event_name)

        event_date = event.find_element(By.CSS_SELECTOR, "span.event-date.font-museo-300").text
        
        event_dates.append(event_date)
        
        try:
            event_price = event.find_element(By.CSS_SELECTOR, "span.font-museo-700.align-middle")
            event_price = event_price.text
            
        except NoSuchElementException:
            
            event_price = None
            
        event_prices.append(event_price)

        followers = event.find_element(By.CSS_SELECTOR, "span.followers-container").text
        
        event_followers.append(followers)
        
        genre_names.append(name)
        
    festivales_button = WebDriverWait(browser, 60).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='title-option' and text()='FESTIVALES']")))
    festivales_button.click()
   
    genre_column = WebDriverWait(browser, 60).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.w-\[16rem\].flex.flex-col")))
    genres = genre_column.find_elements(By.CSS_SELECTOR, "a.option")


festivales_by_genre['genre'] = genre_names
festivales_by_genre['event_names'] = event_names
festivales_by_genre['event_dates'] = event_dates
festivales_by_genre['event_prices'] = event_prices
festivales_by_genre['event_followers'] = event_followers

festivales_by_genre.to_csv("./data/festivalesprueba_genero.csv", index=False)


browser.quit()

