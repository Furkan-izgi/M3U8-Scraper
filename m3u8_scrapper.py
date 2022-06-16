from cgi import print_arguments
from fileinput import filename
import requests as req
from bs4 import BeautifulSoup
import json
import os
from pyrogram import Client

links = []
episode_m3u8_links = []
failed_links = []

# api_id = 18009375 
# api_hash = "1c6b8b0a259aa35affee58377c634eeb"
# bot_token = "5331589042:AAHMXBoJiXSTHG-AJylj2iE1KHDA9mXot9E"
# chatID = -750324776

# app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
# app.start()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    MIDDLELINE = '\033[9m'
    OKGRAY = '\033[2m'
    ITALIC = '\033[3m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def getEpisodes(url):
    viewsource = req.get(url)
    soup = BeautifulSoup(viewsource.text, 'html.parser')
    episodes = soup.find_all("a", {"data-gtm":"gtm:Episode Search (show-blade)"})
    for episode in episodes:
        links.append("https://www.trtizle.com"+episode.get("href"))
    return links

        
def getM3U8Links(list):        
    for episode in episode_links:   
        source = req.get(episode)
        code = BeautifulSoup(source.text, "html.parser") 
        last = code.find("script",{"type":"application/ld+json"})
        try:
            listt = json.loads(last.text)
        except:
            print(bcolors.FAIL + "Hatalı Bölüm: " + bcolors.ENDC + episode)
            failed_links.append(episode)
            
        episode_link = listt["contentUrl"].replace("master","master720p")
        episode_name = listt["name"]
        with open("Links/" + filename + ".txt", "a") as f:
            f.write(episode_name + ": " + episode_link + "\n")
        episode_m3u8_links.append(episode_link)
        print(f"{bcolors.ITALIC}{bcolors.WARNING}Çekilen link sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}")
        
    os.system("cls")
    if failed_links == []:
        print(f"{bcolors.OKGREEN}İşlem tamamlandı.\nÇekilen link sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}\n{bcolors.WARNING}Hatalı Link(ler):{bcolors.ENDC} Yok") 
    else:    
        print(f"{bcolors.OKGREEN}İşlem tamamlandı.\nÇekilen link sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}\n{bcolors.WARNING}Hatalı Link(ler):{bcolors.ENDC} {failed_links}") 
    return episode_m3u8_links


filename = input(bcolors.OKGREEN + "Dizi veya İçerik Adı: " + bcolors.ENDC)
linkofseries = input(f"{bcolors.OKCYAN}Linki giriniz: {bcolors.ENDC}")   
episode_links = getEpisodes(linkofseries) 
links = getM3U8Links(episode_links)
