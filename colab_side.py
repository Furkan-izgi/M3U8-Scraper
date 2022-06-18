import requests
from bs4 import BeautifulSoup
import json
import os
import telebot
import subprocess
from yt_dlp import YoutubeDL

links = []
episode_m3u8_links = []
failed_links = []
episode_names = []

# api_hash = "1c6b8b0a259aa35affee58377c634eeb"
# api_id = 18009375
bot_token = "5331589042:AAHMXBoJiXSTHG-AJylj2iE1KHDA9mXot9E" 
chat_ID = -750324776

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
    
class M3U8Scrapper:
    def __init__(self,url,bot_token):
        self.url = url # url of the m3u8 file    
        self.bot_token = bot_token

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

            with open("/content/drive/Shareddrives/Edu-Test Drive/Links/" + filename + ".txt", "a", encoding="utf-8") as f:
                f.write(episode_name + "|" + episode_link + "\n")
            episode_m3u8_links.append(episode_link)
            print(f"{bcolors.ITALIC}{bcolors.WARNING}Çekilen Bölüm:{bcolors.ENDC} {episode_name}")
            
        os.system("cls")
        if not failed_links:
            print(f"{bcolors.OKGREEN}İşlem tamamlandı.\nÇekilen Dizi: {bcolors.ENDC}{filename}\n{bcolors.OKGREEN}Bölüm sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}\n{bcolors.WARNING}Hatalı Link(ler):{bcolors.ENDC} Yok") 
            app.send_message(chat_ID,f"İşlem tamamlandı.\nÇekilen Dizi: {filename}\nBölüm sayısı: {len(episode_m3u8_links)}\nHatalı Link(ler): Yok") 
        else:
            print(f"{bcolors.OKGREEN}İşlem tamamlandı.\nÇekilen Dizi:{bcolors.ENDC} {filename}\n{bcolors.OKGREEN}Bölüm sayısı:{bcolors.ENDC} {len(episode_m3u8_links)}\n{bcolors.WARNING}Hatalı Link(ler):{bcolors.ENDC} {failed_links}") 
            app.send_message(chat_ID,f"İşlem tamamlandı.\nÇekilen Dizi: {filename}\nBölüm sayısı: {len(episode_m3u8_links)}\nHatalı Link(ler): {failed_links}") 
        return episode_m3u8_links

    def getVideos(self, series_name): 
        app.send_message(chat_ID, "İndirmeye Başlıyorum.")
        with open("/content/drive/Shareddrives/Edu-Test Drive/Links/"+series_name+".txt","r",encoding="utf-8") as f:
            links = f.readlines()

        for link in links:
            episode_link = link.split("|")[1].replace("\n","")
            episode_name = link.split("|")[0].replace(" ","_")
            with open("/content/drive/Shareddrives/Edu-Test Drive/Episode Names.txt","a",encoding="utf-8") as f:
              f.write(episode_name+"\n")

            output = f"{folder_name}{episode_name}.mp4"
            # subprocess.run(['ffmpeg', '-i', episode_link, '/content/Videos/'+ episode_name + '.mp4'])
            subprocess.run(['yt-dlp',episode_link,'-o',output])
            # with YoutubeDL() as ydl:
            #     ydl.download(episode_link)
    def uploadVideos(self, episodes):
        app.send_message(chat_ID, "Yükleniyor.")
        for episode in episodes:
            filename = episode + ".mp4"
            app.send_video(chat_ID, filename,caption=episode)
            os.remove(f"{folder_name}{filename}")
            os.remove("/content/drive/Shareddrives/Edu-Test Drive/Episode Names.txt")

        app.send_message(chat_ID, "Yükleme işlemi tamamlandı.")


if __name__ == "__main__":
    app = telebot.TeleBot(bot_token)
    app.send_message(chat_ID,"Scrapper'a Hoşgeldin!")
    selection = int(input("1. Filmleri çek\n2. Dizi bölümlerini çek\n3. Dizi/Filmi indir/yükle\n\nSeçiminiz: "))

    if selection == 1: #Film  
        filename = input(bcolors.OKGREEN + "Dosya Adı: " + bcolors.ENDC)
        linkofseries = input(f"{bcolors.OKBLUE}Linki giriniz: {bcolors.ENDC}")
        try:
            folder_name = os.mkdir(f"/content/drive/Shareddrives/Edu-Test Drive/{filename}/")
        except FileExistsError:
            folder_name = f"/content/drive/Shareddrives/Edu-Test Drive/{filename}/"
        scrapper = M3U8Scrapper(linkofseries, bot_token)
        episode_links = scrapper.getEpisodes(linkofseries)
        links = scrapper.getM3U8Links(episode_links)

    if selection == 2: #Dizi
        filename = input(bcolors.OKGREEN + "Dosya Adı: " + bcolors.ENDC)
        linkofseries = input(f"{bcolors.OKBLUE}Linki giriniz: {bcolors.ENDC}")
        try:
            folder_name = os.mkdir(f"/content/drive/Shareddrives/Edu-Test Drive/{filename}/")
        except FileExistsError:
            folder_name = f"/content/drive/Shareddrives/Edu-Test Drive/{filename}/"
        scrapper = M3U8Scrapper(linkofseries, bot_token)
        episode_links = scrapper.getEpisodes(linkofseries)
        links = scrapper.getM3U8Links(episode_links)
        
    if selection == 3: #Dizi/Film indirme
        try:
            folder_name = os.mkdir(f"/content/drive/Shareddrives/Edu-Test Drive/{filename}/")
        except FileExistsError:
            folder_name = f"/content/drive/Shareddrives/Edu-Test Drive/{filename}/"
        scrapper = M3U8Scrapper("boş", bot_token)
        serie_name = input("İndirmek İstediğiniz İçeriğin Adını Girin: ")
        scrapper.getVideos(serie_name)
        select = input("Yükleme yapılsın mı?(e/h)\n\nSeçiminiz: ")
        if select == "e":
            scrapper.uploadVideos(episode_names)
        else:
            app.send_message(chat_ID, "İşlem tamamlandı.")
            os.makedir()
    else:
        print(bcolors.FAIL + "Hatalı Seçim" + bcolors.ENDC)