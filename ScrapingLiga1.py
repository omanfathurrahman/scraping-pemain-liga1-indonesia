# Importing package
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
import IPython, time

"""
Scraping wikipedia Liga 1 Indonesia
"""

class ScrapeWeb:
    def __init__(self, link = 'https://id.wikipedia.org/wiki/Liga_1_(Indonesia)#Sponsor'):
        self.soup = bs(requests.get(link).content, 'html.parser')
        teams_table = self.soup.find_all('table', class_ = 'wikitable sortable')[0]
        teams_asal = [team.string for team in teams_table.select('tbody td a') if team.string != "Liga 1 2020"]
        self.teams = teams_asal[::2]
        self.asal = teams_asal[1::2]
        self.link_team = ['https://id.wikipedia.org'+team['href'] for team in teams_table.select('tbody td a') if team.string != 'Liga 1 2020'][::2]
        

        
    def showEntireWeb(self):
        print(self.soup.prettify())
    
    def daftarTim(self):
        for num, nama, asal, link in zip(range(len(self.teams)),self.teams, self.asal, self.link_team):
            print('[',num,']',sep='')
            print("Nama tim:",nama,"\nDaerah:",asal,"\nLink tim:",link,end='\n\n')
        
    def pemain(self, team):
        print('Berikut daftar pemain dari tim',self.teams[team],"menurut Wikipedia")
        # Mengambil website team
        team = bs(requests.get(self.link_team[team]).content, 'html.parser')
        
        # Mengambil data pemain
        players = [i.find('span', class_='fn') for i in \
                team.find('tr', class_='vcard agent').parent.parent.parent\
                .parent.find_all('tr', class_='vcard agent')]
        player_names = [i.string for i in players] # Mengumpulkan nama pemain
        
        # Mengumpulkan alamat website pemain
        link_players = []
        for i in players:
            if i.find('a'):
                if '/w/' not in i.a['href']:
                    link_players.append('https://id.wikipedia.org'+i.a['href'])
                else:
                    link_players.append('belum ada web')
            else: link_players.append('belum ada web')
        
        pilihPemain = dict()
        for i,nama in enumerate(link_players):
            pilihPemain[i] = nama
        self.currentPilihPemain = pilihPemain
        
        [print(i,'. ',j,sep='') for i,j in enumerate(player_names)]
        
        
        
    def dataPemain(self, player):
    
        # Jika player belum memiliki website wiki
        if player == 'belum ada web':
            print('Pemain tersebut belum memiliki artikel di Wikipedia')
            return

        # Player-player yang memiliki website yang bermasalah
        if 'Hariono' in player or \
        'Safrudin_Tahar' in player or \
        'Muhammad_Ridwan' in player or \
        'https://id.wikipedia.org/wiki/-' in player or\
        'Reza_Irfana' in player:
            print('Pemain tersebut memiliki website wiki yang bermasalah')
            return

        # Membuat object player
        player = bs(requests.get(player).content, 'html.parser')

        # Mengambil tabel box dari website wiki player
        playerbox = player.find('table', class_ = 'infobox').tbody

        data_player={} # Untuk menyimpan data player

        # Pengulangan tabel row pada tabel box player
        for i in playerbox.select('tr'):
            th = i.find('th')
            td = i.find('td')
            if td != None and th != None:
                if th.string == 'Nama lengkap':
                    if i.find('sup'):
                        sup = i.sup.extract()
                    data_player[th.string] =td.string[1:]
                if th.string == 'Tanggal lahir':
                    if td.find('span'):
                        umur = i.span.extract()
                    if td.string is None:
                        data_player[th.string] = list(td.strings)[0][1:]
                    else:
                        data_player[th.string] = td.string[1:]

                if th.string == 'Tempat lahir':
                    if i.find('span'):
                        bendera = i.span.extract()
                    if len([i.string for i in td.select('a')])>1:
                        data_player[th.string] = ', '.join([i.string for i in td.select('a')])
                    else:
                        if td.find('a'):
                            data_player[th.string] = [i.string for i in td.select('a')][0]
                        else:
                            data_player[th.string] = td.string.strip()

                if th.string == 'Tinggi':
                    if i.find('style'):
                        stl = i.style.extract()
                    if i.find('sup'):
                        sup = i.sup.extract()
                    if i.find('span'):
                        span = i.span.extract()
                    if td.string is None:

                        if '[' in list(td.strings)[1]:
                            data_player[th.string] = int(list(td.strings)[0].strip()[:3])
                        else:
                            if ',' in list(td.strings)[1]:
                                data_player[th.string] = int(list(td.strings)[1][0]+list(td.strings)[1][2:5])
                            else:
                                data_player[th.string] = int(list(td.strings)[1][0]+list(td.strings)[1][1:3])
                    elif len(td.string.strip())<4:
                        data_player[th.string] = int(td.string.strip())
                    else:
                        if 'kaki' in td.string:
                            data_player[th.string]= int(td.string[11:14])
                        elif len(list(td.strings))>1:
                            if ',' in list(td.strings)[1]:
                                data_player[th.string] = int(list(td.strings)[1][0]+list(td.strings)[1][2:5])
                        elif ',' in td.string:
                            if td.string[3]=='f':
                                 data_player[th.string] = td.string[12]+td.string[14:16]
                            else:
                                data_player[th.string] = int(td.string[1]+td.string[3:5])
                        else:
                            data_player[th.string] = int(td.string[1:4])

                if th.string == 'Posisi bermain':
                    if i.find('sup'):
                        sup = i.sup.extract()
                    if len([i.string for i in td.select('a')])==1:
                        data_player[th.string] = [i.string for i in td.select('a')][0]
                    else:
                        if td.find('a'):
                            data_player[th.string] = [i.string for i in td.select('a')]
                        else:
                            data_player[th.string] = td.string.strip()

                # if th.string == 'Klub saat ini':
                #     if td.find('a'):
                #         data_player[th.string] = td.find('a').string
                #     else:
                #         data_player[th.string] = td.string.strip()

                if th.string == 'Nomor':
                    if td.find('a'):
                        data_player[th.string] = td.find('a').string
                    elif td.find('p'):
                        data_player[th.string] = i.td.p.string.strip()
                    else:
                        data_player[th.string] = td.string.strip()
        data_player['umur'] = int(umur.string[-3:-1])
        
        for key,value in data_player.items():
            print(key.ljust(15),':',value)

# liga1 = ScrapeWeb()

# liga1.daftarTim()
# liga1.pemain()

def mulai():
    
    print("Daftar Tim:")
    liga1 = ScrapeWeb()
    def menuUtama():
        
        global pilihTim
        liga1.daftarTim()
        pilihTim = int(input('Pilih tim untuk melihat daftar pemain: '))
        detailPemain()
    
    def detailPemain():
        liga1.pemain(pilihTim)
        pilihPemain = int(input('Pilih pemain untuk melihat data dari pemain tersebut: '))
        liga1.dataPemain(liga1.currentPilihPemain[pilihPemain])
        x = input("[0] Lihat data pemain {} yang lain\n[1] Menu Utama\n[2] Selesai\nPilihan: ".format(liga1.teams[pilihTim]))
        if x == '0':
            detailPemain()
        elif x == '1':
            menuUtama()
        else:
            return
            
    menuUtama()

mulai()

