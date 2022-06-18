# import requests
# from bs4 import BeautifulSoup
# import json
# import os

# links = []
# episode_m3u8_links = []
# failed_links = []

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     MIDDLELINE = '\033[9m'
#     OKGRAY = '\033[2m'
#     ITALIC = '\033[3m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'
    
# class M3U8Scrapper:
#     def __init__(self, url):
#         self.url = url # url of the m3u8 file    
#         self.list = list
        
#     def getEpisodes(self,url):
#         """Verilen url'deki dizileri listelemek için kullanılır.
        
#         Parametreler: 
#         • url(str): dizilerin listelenmesi istenen url
        
#         Örnek Kullanım:
        
#         scrapper = M3U8Scrapper()
#         scrapper.getMovies("https://www.trtizle.com/diziler/leyla-ile-mecnun")
#         """
        
#         viewsource = requests.get(url)
#         soup = BeautifulSoup(viewsource.text, 'html.parser')
#         episodes = soup.find_all("a", {"data-gtm":"gtm:Episode Search (show-blade)"}) # for series
#         for episode in episodes:
#             links.append("https://www.trtizle.com"+episode.get("href"))
            
#         return links

#     def getMovies(self, url):
#         """Verilen url'deki filmleri listelemek için kullanılır.
        
#         Parametreler: 
#         • url(str): filmlerin listelenmesi istenen url
        
#         Örnek Kullanım:
        
#         scrapper = M3U8Scrapper()
#         scrapper.getMovies("https://www.trtizle.com/filmler")
#         """
        
#         viewsource = requests.get(url)
#         soup = BeautifulSoup(viewsource.text, 'html.parser')
#         episodes = soup.find_all("a", {"class":"card-go-video"}) # for movies
#         for episode in episodes:
#             links.append("https://www.trtizle.com"+episode.get("href"))
            
#         return links
            
#     def getM3U8Links(self, list):
#         """Verilen liste içerisindeki linkleri kullanarak m3u8 linklerini listeler.
        
#         Parametreler:
#         • list(list): dizi veya film linklerini barındıran liste
        
#         Örnek Kullanım:
        
#         episodes_list = [...]
        
#         scrapper = M3U8Scrapper()
        
#         scrapper.getM3U8Links(episode_list)
#         """      
#         os.remove("Links/"+ filename + ".txt")
#         for episode in episode_links:   
#             source = requests.get(episode)
#             code = BeautifulSoup(source.text, "html.parser") 
#             last = code.find_all("script",{"type":"application/ld+json"})
#             try:
#                 listt = json.loads(last[0].text)
#             except:
#                 print(bcolors.FAIL + "Hatalı Bölüm: " + bcolors.ENDC + episode)
#                 failed_links.append(episode)
                
#             episode_link = listt["contentUrl"].replace("master","master720p")
#             episode_name = listt["name"]

#             with open("Links/" + filename + ".txt", "a") as f:
#                 f.write(episode_name + "|" + episode_link + "\n")
#             episode_m3u8_links.append(episode_link)
#             print(f"{bcolors.ITALIC}{bcolors.WARNING}Çekilen Bölüm:{bcolors.ENDC} {episode_name}")
            
#         os.system("cls")
#         if not failed_links:
#             print(f"{bcolors.OKGREEN}İşlem tamamlandı.\nÇekilen Dizi: {bcolors.ENDC}{filename}\n{bcolors.OKGREEN}Bölüm sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}\n{bcolors.WARNING}Hatalı Link(ler):{bcolors.ENDC} Yok") 
#         else:    
#             print(f"{bcolors.OKGREEN}İşlem tamamlandı.\nÇekilen Dizi:{bcolors.ENDC} {filename}\n{bcolors.OKGREEN}Bölüm sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}\n{bcolors.WARNING}Hatalı Link(ler):{bcolors.ENDC} {failed_links}") 
#         return episode_m3u8_links

# if __name__ == "__main__":
#     os.mkdir("Links")
#     filename = input(bcolors.OKGREEN + "Dizi veya İçerik Adı: " + bcolors.ENDC)
#     linkofseries = input(f"{bcolors.OKBLUE}Linki giriniz: {bcolors.ENDC}")   
#     choose = input(f"{bcolors.OKBLUE}İçerik tipi(dizi/film): {bcolors.ENDC}")
#     scrapper = M3U8Scrapper(linkofseries)
    
#     if choose == "dizi":
#         episode_links = scrapper.getEpisodes(linkofseries) 
#         links = scrapper.getM3U8Links(episode_links)
#     elif choose == "film":
#         episode_links = scrapper.getMovies(linkofseries)
#         links = scrapper.getM3U8Links(episode_links)
#     else:
#         print(bcolors.FAIL + "Hatalı İçerik Tipi" + bcolors.ENDC)

import requests
from bs4 import BeautifulSoup
import json
import os
import subprocess

links = []
episode_m3u8_links = []
failed_links = []
episode_names = []

class bcolors: #If it is not working, please remove bcolors and variables
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
    
class M3U8Scrapper:
    def __init__(self,url):
        self.url = url # url of the m3u8 file    

    def getEpisodes(self,url):
        """Verilen url'deki dizileri listelemek için kullanılır.
        
        Parametreler: 
        • url(str): dizilerin listelenmesi istenen url
        
        Örnek Kullanım:
        
        scrapper = M3U8Scrapper()
        scrapper.getMovies("https://www.trtizle.com/diziler/leyla-ile-mecnun")
        """
        viewsource = requests.get(url)
        soup = BeautifulSoup(viewsource.text, 'html.parser')
        episodes = soup.find_all("a", {"data-gtm":"gtm:Episode Search (show-blade)"}) # for series
        for episode in episodes:
            links.append("https://www.trtizle.com"+episode.get("href"))
            
        return links

    def getMovies(self, url):
        """Verilen url'deki filmleri listelemek için kullanılır.
        
        Parametreler: 
        • url(str): filmlerin listelenmesi istenen url
        
        Örnek Kullanım:
        
        scrapper = M3U8Scrapper()
        scrapper.getMovies("https://www.trtizle.com/filmler")
        """
        viewsource = requests.get(url)
        soup = BeautifulSoup(viewsource.text, 'html.parser')
        episodes = soup.find_all("a", {"class":"card-go-video"}) # for movies
        for episode in episodes:
            links.append("https://www.trtizle.com"+episode.get("href"))
            
        return links
            
    def getM3U8Links(self, list):
        """Verilen liste içerisindeki linkleri kullanarak m3u8 linklerini listeler.
        
        Parametreler:
        • list(list): dizi veya film linklerini barındıran liste
        
        Örnek Kullanım:
        
        episodes_list = [...]
        
        scrapper = M3U8Scrapper()
        
        scrapper.getM3U8Links(episode_list)
        """      
        for episode in episode_links:   
            source = requests.get(episode)
            code = BeautifulSoup(source.text, "html.parser") 
            last = code.find_all("script",{"type":"application/ld+json"})
            try:
                listt = json.loads(last[0].text)
            except:
                print(bcolors.FAIL + "Hatalı Bölüm: " + bcolors.ENDC + episode)
                failed_links.append(episode)
                
            episode_link = listt["contentUrl"].replace("master","master720p")
            episode_name = listt["name"]

            with open("Links/" + filename + ".txt", "a", encoding="utf-8") as f:
                f.write(episode_name + "|" + episode_link + "\n")
            episode_m3u8_links.append(episode_link)
            print(f"{bcolors.ITALIC}{bcolors.WARNING}Çekilen Bölüm:{bcolors.ENDC} {episode_name}")
            
        os.system("cls")
        if not failed_links:
            print(f"{bcolors.OKGREEN}İşlem tamamlandı.\nÇekilen Dizi: {bcolors.ENDC}{filename}\n{bcolors.OKGREEN}Bölüm sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}\n{bcolors.WARNING}Hatalı Link(ler):{bcolors.ENDC} Yok")
        else:
            print(f"{bcolors.OKGREEN}İşlem tamamlandı.\nÇekilen Dizi:{bcolors.ENDC} {filename}\n{bcolors.OKGREEN}Bölüm sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}\n{bcolors.WARNING}Hatalı Link(ler):{bcolors.ENDC} {failed_links}") 
        return episode_m3u8_links

    def getVideos(self, series_name): 
        with open("Links/" + series_name + ".txt", "r", encoding="utf-8") as f:
            links = f.readlines()

        for link in links:
            episode_link = link.split("|")[1].replace("\n","")
            episode_name = link.split("|")[0].replace(" ","_")
            with open("Episode Names.txt","a",encoding="utf-8") as f:
              f.write(episode_name + "\n")
            output = f"{folder_name}{episode_name}.mp4"
            subprocess.run(['yt-dlp',episode_link,'-o',output])



if __name__ == "__main__":
    
    selection = int(input("1. Filmleri çek\n2. Dizi bölümlerini çek\n3. Dizi/Filmi indir\n\nSeçiminiz: "))
    if selection == 1: #Film  
        filename = input(bcolors.OKGREEN + "Dosya Adı: " + bcolors.ENDC)
        linkofseries = input(f"{bcolors.OKBLUE}Linki giriniz: {bcolors.ENDC}")
        try:
            folder_name = os.mkdir(f"{filename}/")
        except FileExistsError:
            folder_name = f"{filename}/"
        scrapper = M3U8Scrapper(linkofseries)
        episode_links = scrapper.getEpisodes(linkofseries)
        links = scrapper.getM3U8Links(episode_links)

    if selection == 2: #Dizi
        filename = input(bcolors.OKGREEN + "Dosya Adı: " + bcolors.ENDC)
        linkofseries = input(f"{bcolors.OKBLUE}Linki giriniz: {bcolors.ENDC}")
        try:
            folder_name = os.mkdir(f"{filename}/")
        except FileExistsError:
            folder_name = f"{filename}/"
        scrapper = M3U8Scrapper(linkofseries)
        episode_links = scrapper.getEpisodes(linkofseries)
        links = scrapper.getM3U8Links(episode_links)
        
    if selection == 3: #Dizi/Film indirme
        try:
            folder_name = os.mkdir(f"{filename}/")
        except FileExistsError:
            folder_name = f"{filename}/"
        scrapper = M3U8Scrapper(None)
        serie_name = input("İndirmek İstediğiniz İçeriğin Adını Girin: ")
        scrapper.getVideos(serie_name)
        print(f"{bcolors.OKGREEN}İndirme işlemi tamamlandı.{bcolors.ENDC}")
    else:
        print(bcolors.FAIL + "Hatalı Seçim" + bcolors.ENDC)