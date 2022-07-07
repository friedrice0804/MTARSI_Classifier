from attr import attr
import wikipedia
import pandas as pd
from bs4 import BeautifulSoup
import json

from PIL import Image
from pandas.io.html import read_html


class retrieveDetails:
    def __init__(self):
        self.aircraft = None
        self.full_page = None

    def __call__(self, function, aircraft):    
        self.aircraft = aircraft
        self.full_page = wikipedia.page(self.aircraft).html()    

        if function == 'infobox':
            return self.getInfoBox()
        elif function == 'img':
            return self.getImage()

    def getInfoBox(self):
        infobox = read_html(self.full_page, index_col=0, attrs={"class":"infobox"})

        # for infobox[0]
        col_left = infobox[0].index[2:][0:]
        col_right = infobox[0].values[2:]

        col_left_titles = ['info',]
        col_right_details = ['detail',]

        for title, details in zip(col_left, col_right):

            details = str(details)
            details = details.replace("['", '')
            details = details.replace("']", '')

            col_left_titles.append(title)
            col_right_details.append(details)
        
        col_left_titles = pd.DataFrame(col_left_titles)
        col_left_titles.columns = col_left_titles.iloc[0]
        col_left_titles = col_left_titles[1:]

        col_right_details = pd.DataFrame(col_right_details)
        col_right_details.columns = col_right_details.iloc[0]
        col_right_details = col_right_details[1:]
        
        aircraft_details = pd.concat([col_left_titles, col_right_details], axis = 1)
        aircraft_details = aircraft_details.reset_index().to_json(orient ='records') 

        data = []
        data = json.loads(aircraft_details) 
        
        return data

    def getImage(self):
        imglist = []
        soup = BeautifulSoup(self.full_page, 'html.parser')
        images = soup.find_all('img')

        for img in images:
            if img.has_attr('src'):
                imglist.append(img['src'])
        
        imglist[0] = imglist[0].replace('//', 'https://')
                    
        # Implement resizing function

        return imglist[0]