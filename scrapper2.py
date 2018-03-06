# coding: utf8
import os
import csv #Optionnal (only if you want your file in csv )
import requests
from bs4 import BeautifulSoup

artist = "Eminem/Revival"
url_website = "https://genius.com"
url_repo = "/albums/"
url_artist = url_website + url_repo + artist
print("Wait...")
#Recuperation du site
requete = requests.get(url_artist)#Telechargement de la page
page = requete.content #Recuperation du contenu
soup = BeautifulSoup(page, "html.parser") #Parsing - Contient toutes les données structurer de la page
#print(soup)
#La donnée récupérée est la première occurrence de tag HTML qui soit
#un tag <h1> et qui possède les classes u-display_block.
#On recupere les liens
a = soup.find_all("a", {"class": "u-display_block"})
songs_link = list()
for elt in a:
    songs_link.append(elt['href'])
#Ensuite le titre de chaque son
h3 = soup.find_all("h3", {"class": "chart_row-content-title"})
list_songs = list()
for elt in h3:
    #Extraction titre
    pos1 = str(elt).find('>') + 1
    pos2 = str(elt).find('<', 2)
    #Extraction titre sans feat
    titre = str(elt)[pos1:pos2].strip()
    pos3 = titre.find('(')
    if pos3 != -1:
        titre = titre[0:pos3]
    print(titre.strip('\n'))
    list_songs.append([titre.strip('\n')])

#Recuperation texte de chaque son
list_paroles = list()

for elt in songs_link:
    parole_text = ""
    requete = requests.get(elt)
    page = requete.content  # Recuperation du contenu
    soup = BeautifulSoup(page, "html.parser")  # Parsing - Contient toutes les données structurer de la page
    parole_html = soup.find_all("a", {"class": "referent"})
    for elt1 in parole_html:
        parole_text += elt1.text.strip()
    list_paroles.append(parole_text)

j = len(list_songs)
i = 0
#Stockage dans du csv (Optionnal)
with open("donnees.csv", "w", encoding="utf-8") as fichier:
    writer = csv.writer(fichier, delimiter=';')
    writer.writerow(("Titre", "Paroles"))
    while i < j:
        writer.writerow((list_songs[i], list_paroles[i]))
        i += 1

print("Finish !")