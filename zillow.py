# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 14:40:38 2021

@author: PriyankRao
"""


import pandas as pd
import requests
from bs4 import BeautifulSoup 
import json
import time
import csv
import os 
import re
import datetime

os.chdir(r"C:\Users\PriyankRao\OneDrive - E2\Documents\Project\webscrapping")


class ZillowScrapper():
    result = []
    houseInfo = []
    headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding':'gzip, deflate, br',
           'accept-language': 'en-US,en;q=0.9',
           'cookie':'zguid=23|$a75cb4dd-916f-442a-abc4-411ad78e1603; zgsession=1|077d9b2c-3c77-494b-a68f-3b7fe1771104; zjs_user_id=null; _ga=GA1.2.1832947534.1629924385; _gid=GA1.2.1032777464.1629924385; zjs_anonymous_id="a75cb4dd-916f-442a-abc4-411ad78e1603"; _pxvid=82d6167d-05e5-11ec-9ca6-7773757a4141; _gcl_au=1.1.991067248.1629924385; KruxPixel=true; DoubleClickSession=true; __pdst=5a0d2d5ec48b4f3380af5503db54c2fe; _fbp=fb.1.1629924385459.1255009242; _pin_unauth=dWlkPU1qWXpOekE1WWpRdE9HWmhNQzAwWTJVMkxUaG1Nek10TnprNE1XSTBaRGt4T0dabQ; KruxAddition=true; _gac_UA-21174015-56=1.1629924441.CjwKCAjw1JeJBhB9EiwAV612y25MshJRDX6EtKadZP_OfG00eeyZAAzKCo94xQ19HXSto98iQWzaihoCWPYQAvD_BwE; _gcl_aw=GCL.1629924444.CjwKCAjw1JeJBhB9EiwAV612y25MshJRDX6EtKadZP_OfG00eeyZAAzKCo94xQ19HXSto98iQWzaihoCWPYQAvD_BwE; __gads=ID=531788161cdd8435-229cb03d02ca0093:T=1629924443:S=ALNI_MZVLEVWffT6M-9A9ZWl2K-zo4X2ug; gclid=CjwKCAjw1JeJBhB9EiwAV612y25MshJRDX6EtKadZP_OfG00eeyZAAzKCo94xQ19HXSto98iQWzaihoCWPYQAvD_BwE; utag_main=v_id:017b7f1146ee00188c0d1ea6ebf90307300f106b00bd0$_sn:1$_se:1$_ss:1$_st:1629926243887$ses_id:1629924443887;exp-session$_pn:1;exp-session$dcsyncran:1;exp-session$tdsyncran:1;exp-session$dc_visit:1$dc_event:1;exp-session$dc_region:us-east-1;exp-session; JSESSIONID=9AD91CFD26ADC1284E42DF67158FA407; _uetsid=83779cc005e511eca6a111ec6d6b1444; _uetvid=8377d8f005e511ec972057bb5d50fc48; _gat=1; _px3=411177930c94fd31e8dae9434affcd2a77fc44cf15b14d8bf0d2d1ac1d8b3a6b:7qLfEYmkc3pUvlACFSLrGjs1tj2gLThRd6JUfP6zyoZsObpQrYri4Jl3cy03YvqFf6SiRiX/rAxgrr5WjCx4gQ==:1000:C/YlyKIudoQdB32QIU+zIq+3HZ0BmhpvZT/oUvpPH8qCT7nZ0kGxsPOvVWKZZNZTR2GMlPpZYyaMgxmvVXk/5NJNCgN2bJ96Z41zY5f/7ZjIwEDY8gAZoPQuqPq7QeAMAbmSRbnR5l1wJQ0AdykQZOtkE0cz8lyAU/AHbZXe4o7EXG1E0brTdJ91eSRigfEu9h+xC4CpgjNnPx7nAG5hVA==; AWSALB=6FYklyEJlig54zyV5dnZFuFpDFD8KIvHZK4EPdWbn7UK4QoBzKyYy+r8vMNkoe8UZcCXGP1+hKaT1osNnkKpCj42dnh2OdbNJ9ly2xOqPUnkwuximUTmxwm6ZBGC; AWSALBCORS=6FYklyEJlig54zyV5dnZFuFpDFD8KIvHZK4EPdWbn7UK4QoBzKyYy+r8vMNkoe8UZcCXGP1+hKaT1osNnkKpCj42dnh2OdbNJ9ly2xOqPUnkwuximUTmxwm6ZBGC; search=6|1632548294194|region=los-angeles-ca&rect=35.2%2C-117.49%2C33.2%2C-119.49&disp=map&mdm=auto&fs=1&fr=0&mmm=1&rs=0&ah=0		12447						',
           'sec-fetch-dest':'empty',
           'sec-fetch-mode':'cors',
           'sec-fetch-site':'same-origin',
           'upgrade-insecure-request':'1',
           'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
           }
    
   
    def fetch(self, url, params):
        # response  = requests.get(url, headers = headers, params = params  )
        response  = requests.get(url, headers = self.headers, params = params  )  
        print(response.status_code)
        return response
   
    def parse(self, response):
        content = BeautifulSoup(response, 'lxml')
        deck = content.find('ul',{'class': 'photo-cards photo-cards_wow photo-cards_short'})
        md= content.find('script',{'data-zrr-shared-data-key': 'mobileSearchPageStore'})
        soup = BeautifulSoup(md.string, "html.parser")
        strings = soup.string
        HI = re.findall(r'(?<=listResults).*?(?=resultsHash)', strings)
        
        for matched in re.findall(r'(?<={"zpid").*?(?="relaxed":)', strings):
            try:
                tax = re.findall(r'(?<="taxAssessedValue":).*?(?=,")', matched)[0]
            except IndexError:
                tax = ''
            try:
                address = re.findall(r'(?<="address":").*?(?=")', matched)[0]
            except IndexError:
                address = ''
                
            try:
                url = re.findall(r'(?<="detailUrl":").*?(?=")', matched)[0] 
            except IndexError:
                url = ''
            try:
                price = re.findall(r'(?<="price":").*?(?=")', matched)[0]
            except IndexError:
                price:''
            
            try:
                housetype = re.findall(r'(?<="homeType":").*?(?=")', matched)[0]
            except IndexError:
                housetype = ''
                
            try:
                currency = re.findall(r'(?<="currency":").*?(?=")', matched)[0]
            except IndexError:
                currency = ''
                
            try:
                lotareaunit = re.findall(r'(?<="lotAreaUnit":").*?(?=")', matched)[0]
            except IndexError:
                lotareaunit = ''
            
            try:
                zipcode = re.findall(r'(?<="zipcode":").*?(?=")', matched)[0]
            except:
                zipcode = ''
            
            try:
                latitude = re.findall(r'(?<={"latitude":).*?(?=,")', matched)[0]
            except IndexError:
                latitude = ''
            try:
                longitude = re.findall(r'(?<="longitude":).*?(?=},")', matched)[0]
            except IndexError:
                longitude = ''
            try:
                bath = re.findall(r'(?<="bathrooms":).*?(?=,")', matched)[0]
            except IndexError:
                bath = ''
            try:
                bed = re.findall(r'(?<="bedrooms":).*?(?=,")', matched)[0]
            except IndexError:
                bed = ''
            try:
                living = re.findall(r'(?<="livingArea":).*?(?=,")', matched)[0]
            except IndexError:
                living = ''    
            try:
                lotarea = re.findall(r'(?<="lotAreaValue":).*?(?=,")', matched)[0]
            except IndexError:
                lotarea = '' 
                
            
            self.houseInfo.append(
                {
                    'Address': address,
                    'url' : url,
                    'Zip Code' : zipcode,
                    'Latitude' : latitude,
                    'Longitude': longitude,
                    'House Type' : housetype,
                    'Lot Area': lotarea,
                    'Lot Area Unit' : lotareaunit,
                    'Currency' : currency,
                    'Tax' : tax,
                    'Bath': bath,
                    'Bed': bed,
                    'living Area': living, 
                    'Price' : price
                        
                    }
                )
        if deck:
                deck = content.find('ul',{'class': 'photo-cards photo-cards_wow photo-cards_short'})
        else:
            deck = content.find('ul',{'class': 'photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution'})
        
        for card in deck.contents:
            
            script = card.find('script', {'type': 'application/ld+json'})
            ul = card.find('ul', {'class': 'list-card-details'})
            
            
            if script:
                script_json = json.loads(script.contents[0])
                
                try:              
                    self.result.append(
                        
                        {
                            'latitude': script_json['geo']['latitude'],
                            'longitude': script_json['geo']['longitude'],
                            'Bed': list(list(ul)[0])[0],
                            'Bath': list(list(ul)[1])[0],
                            'Floor Size' : script_json['floorSize']['value'],
                            'url': script_json['url'],
                            'Zipcode': script_json['address']['postalCode'],
                            'Locality': script_json['address']['addressLocality'],
                            'Price': card.find('div', {'class':'list-card-price'}).text
                            })
                    
                except KeyError:
                    self.result.append(       
                        {
                            'latitude': " ",
                            'longitude': " ",
                            'bed': list(list(ul)[0])[0],
                            'bath': list(list(ul)[1])[0],
                            'floor size' : script_json['floorSize']['value'],
                            'url': script_json['url'],
                            'zipcode': script_json['address']['postalCode'],
                            'locality': script_json['address']['addressLocality'],
                            'price': card.find('div', {'class':'list-card-price'}).text
                            })
        
        
                
    def to_csv(self, result):
        with open('zilliow.csv', 'w', newline = '') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames =self.result[0].keys())
            writer.writeheader()
            
            
            for row in self.result:
                writer.writerow(row)    
    def house_info(self, houseInfo):
        with open('houseinfo.csv', 'w', newline = '') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames =self.houseInfo[0].keys())
            writer.writeheader()
            
            
            for row in self.houseInfo:
                writer.writerow(row)    
             
     
    def run(self):
        url = 'https://www.zillow.com/homes/CA_rb'
        
        for page in range(1, 21):
            
            params = {
                'searchQueryState' :'{"pagination":{"currentPage":%s},"usersSearchTerm":"CA","mapBounds":{"west":-127.996833546875,"east":-110.616462453125,"south":26.309097102990197,"north":47.09699523775018},"regionSelection":[{"regionId":9,"regionType":2}],"isMapVisible":true,"filterState":{"sortSelection":{"value":"globalrelevanceex"},"isAllHomes":{"value":true}},"isListVisible":true,"mapZoom":6}' %page
                }
            res = self.fetch(url,params)
            self.parse(res.text)
            time.sleep(4)
            self.to_csv(self.result)
            self.house_info(self.houseInfo)
        
if __name__ == '__main__':
    scrapper = ZillowScrapper()
    scrapper.run()