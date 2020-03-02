################################################## ALBUM SALES ##########################################################################

################################################## RETRIEVING DATA ###########################################################################
from bs4 import BeautifulSoup
import requests
import pandas as pd
url = 'https://hitsdailydouble.com/sales_plus_streaming'  ## CREDIT TO hitsdailydouble FOR ALL DATA
response = requests.get(url, timeout = 5)
content = BeautifulSoup(response.content, 'html.parser')
################################################## TOP50CALCULATION + OBJECT CREATION #############################################################
AlbumObject = content.findAll('tr', attrs = {"class": "hits_album_chart_header_full_alt2"})  ##Have to stitch together all album headers as they use alternate tags
AlbumObject2 =content.findAll('tr', attrs = {"class": "hits_album_chart_header_full_alt1"})
AlbumsObject = []
i = 0
j = 0
while i<25 and j <25:
    AlbumsObject.append(AlbumObject[i])
    AlbumsObject.append(AlbumObject2[j])
    i +=1
    j+=1

################################################### ALBUM OBJECT CREATION#################################################################################

#Artist = Artist name (Or Movie if soundtrack)
#name = Album name
#sales = Total Album Sales
#pureSales = Pure Album Sales "Physical, Itunes purchase"
#change = % change in #sales since last week
#sea = Streaming equivalent albums (1500 streams = 1 album sale)
#tea = Track equivalent albums
class LP:
    def __init__(self, artist, name, sales, pureSales, change, tea, sea ):
        self.artist = artist
        self.name = name
        self.sales = sales
        self.pureSales = pureSales
        self.change = change
        self.sea = sea
        self.tea = tea
    def __repr__(self):
        return (self.artist +" "+ self.name+" " +self.sales+" " + self.pureSales+" "+self.change+" " + self.tea+" " + self.sea)


List = [LP("","","","","","","") for i in range(50)] ## List containing 50 album objects
j = 0
for i in List:
    i.sales = AlbumsObject[j].find('td', attrs={"class": "hits_album_chart_item_top_details_full_sales chart_tweak col_sales"}).text
    nA = AlbumsObject[j].find('span', attrs={"class": "hits_album_chart_item_details_full_artist"}).text
    nA = nA.split("|")
    i.artist = nA[0]
    i.name = nA[1]
    i.change = AlbumsObject[j].find('td', attrs={"class": "hits_album_chart_item_top_details_full_change chart_tweak col_change"}).text
    i.pureSales = AlbumsObject[j].find('td', attrs={"class": "hits_album_chart_item_top_details_full_sales_albums chart_tweak col_albums"}).text
    i.tea = AlbumsObject[j].find('td', attrs={"class":"hits_album_chart_item_top_details_full_sales_tea chart_tweak col_tea"}).text
    i.sea = AlbumsObject[j].find('td', attrs={"class":"hits_album_chart_item_top_details_full_sales_sea chart_tweak col_sea"}).text
    j+=1


df = pd.DataFrame([t.__dict__ for t in List])
print(df.head(5))
############################################################################# Create your List #############################################################################
file_name = input("write your filename")
df.to_excel(file_name)
print("Check to see if file has been written.")



#######################################STREAMING CHARTS##########################################################
##Spotify Music charts
## You can already download the csv for any spotify chart you would like at https://spotifycharts.com/regional/global/daily/latest . This program would be useful if you would like
#to measure album bombs or how
## many songs an artist keeps in the top 200.
## W I P ###
