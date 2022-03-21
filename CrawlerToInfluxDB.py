from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from influxdb_client import InfluxDBClient, Point, WriteOptions
import time
from bs4 import BeautifulSoup
import csv
import datetime
from datetime import date, timedelta
from influxdb_client.client.util import date_utils
from dateutil.tz import tzlocal

org = 'Codecentric'
bucket = 'Energiedata'
token = '5I6c26WUqkJ87rBVVsypqp34DzObPRovzgR5eUEUUdQGYX-71Lv6gQOz05XBo9YGNO_bhTRYIWex4PccyeJoBw=='

#connection
client = InfluxDBClient(url="http://localhost:8086", token = token , org = org)

##instantiate the WriteAPI and QueryAPI
write_api = client.write_api()  #parameter (write_options = SYNCHRONOUS/ASYNCHRONOUS) möglich (vorher importieren)
#query_api = client.query_api()

#Frühester Beginn der Aufzeichnung 2015 Dezember nach erstem Skim, sinnvoll vielleicht nur die letzten 2-3 Jahre?
a = datetime.datetime.today()

numdays = 40
dateList = []
for x in range (0, numdays):
    dateList.append(a - datetime.timedelta(days = x))

adjDateList = []
for x in range (0, numdays):
    adjDateList.append(dateList[x].strftime('%d').lstrip('0') + '.' + dateList[x].strftime('%m').strip('0') + '.' + dateList[x].strftime('%y'))
b = adjDateList[1]



immobilien = ["buergerhaus-kinderhaus", "stadthaus-2", "stadthaus-3", "stadtkasse-kaemmerei", "rathaus-stadtweinhaus", "standesamt", "gesundheits-und-veterinaeramt", "stadtbuecherei","buergerhaus-bennohaus", "aegidii-ludgeri-schule" , "albert-schweitzer-schule", "annette-von-droste-huelshoff-grundschule", "annette-von-droste-huelshoff-grundschule-nienberge", "astrid-lindgren-schule", "bodelschwinghschule", "davertschule", "dietrich-bonhoeffer-schule", "dreifaltigkeitsschule", "eichendorffschule-angelmodde", "gottfried-von-cappenberg-schule", "hermannschule", "idaschule", "idaschule2","johannisschule", "kardinal-von-galen-schule", "kinderhaus-west", "kreuzschule", "loevelingloh", "ludgerusschule-albachten","ludgerusschule-hiltrup","margaretenschule", "marienschule-hiltrup", "martin-luther-schule","martinischule", "matthias-claudius-schule","mauritzschule","melanchthonschule","michaelschule","mosaik-schule","norbertschule","overbergschule", "paul-gerhardt-schule", "paul-schneider-schule", "peter-wust-schule","pleisterschule","poetterhoekschule","primus-schule","grundschule-sprakel","theresienschule","thomas-morus-schule","wartburg-grundschule","adolph-kolping-berufskolleg","adolph-kolping-berufskolleg-2","adolph-kolping-berufskolleg-3","anne-frank-berufskolleg","annette-von-droste-huelshoff-gymnasium","augustin-wibbelt-schule","erna-de-vries-realschule","freiherr-vom-stein-gymnasium","friedensreich-hundertwasser-schule","geistschule","gesamtschule-muenster-mitte" , "geschwister-scholl-gymnasium", "paulinum","gymnasium-wolbeck","hans-boeckler-berufskolleg","hauptschule-coerde","johann-conrad-schlaun-gymnasium","ludwig-erhard-berufskolleg","mathilde-anneke-gesamtschule","pascal-gymnasium","ratsgymnasium","realschule-im-kreuzviertel","beckstrasse","richard-von-weizsaecker-schule","schillergymnasium","uppenbergschule","waldschule-kinderhaus","wilhelm-emmanuel-von-ketteler-berufskolleg","wilhelm-hittorf-gymnasium","kita-albachten","kita-am-edelbach","kita-inselbogen","kita-wolbeck","kita-berg-fidel","kita-brueningheide","kita-burgwall","kita-handorf","kinderhaus-west-1","kita-emmerbachtal","kita-gievenbeck","kita-in-der-alten-schule","kita-kinderhaus","kita-legdenweg","kita-loddengrund","kita-mecklenbeck","kita-normannenweg","kita-drostenhof","kita-am-gievenbach","kita-hiltrup-west","kita-im-moorhock","kita-killingstrasse","kita-rumphorst","kita-sonnentau","kita-wielerort","kita-wilkinghege","dreifachsportanlage","grosssporthalle-berg-fidel","sportanlage-hiltrup-sued","sportanlage-sentruper-hoehe","sporthalle-mosaik-schule","sporthalle-ost"]
#immobilien = ["hansa-berufskolleg"] ERROR, weil Daten lückenhaft geupdated werden
#immobilien = ["stadthaus-2"]
service = Service('/Users/Real/chromedriver')
url_base = 'https://www.stadt-muenster.de/immobilien/umwelt-und-energie/lastganganalyse/smartoptimo-standorte/'
urls = [url_base + i for i in immobilien]



#hierarchy: id > name > class
def get_plain_text(url, energie):
    driver = webdriver.Chrome(service=service)
    #Vorbereitungen: Pointer im quellcode ausfindig machen

    if energie == 'Wärme':
        value1 = "//a[@title='Wärmezähler auswählen']"
        value2 = "//a[@title='Wasserverbrauch als Tabelle darstellen']"
    elif energie == 'Strom':
        value1 = "//a[@title='Stromzähler auswählen']"
        value2 = "//a[@title='Stromverbrauch als Tabelle darstellen']"
    elif energie == 'Wasser':
        value1 = "//a[@title='Wasserzähler auswählen']"
        value2 = "//a[@title='Wasserverbrauch als Tabelle darstellen']"

    #get to main page
    driver.get(url)

    #get to frame quellcode
    frames = driver.find_element(by=By.TAG_NAME, value= "iFrame")
    src = frames.get_attribute("src")
    driver.get(src)

    #get desired dataset (Strom, Wärme, Wasser) + Tag
    try:
        energy = driver.find_element(by=By.XPATH, value= value1)
        href = energy.get_attribute('href')
        driver.get(href)
    except:

        #thewriter.writerow({'Immobilie': immobilien[counter], 'Datum': 'x', 'Energietyp': energie, 'Verbrauch' : 'No Data'})
        return

    # get Tabelle
    element = driver.find_element(by=By.XPATH, value=value2)
    hrefbase = element.get_attribute('href')
    for date in adjDateList[1:]:  #iterieren durch tage
        href = hrefbase.replace('t' + str(b), 't' + date) #gewünschten Tag auswählen
        driver.get(href)

        #speichere quellcode
        plain_text = driver.page_source
        main_spider(plain_text, energie)
    driver.quit()

hour_list = ['00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08','08-09','09-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23','23-00']
hour_list_updated = ['00:00:00','01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00','21:00:00','22:00:00','23:00:00']
def main_spider(plain_text, energie):
    soup = BeautifulSoup(plain_text, "lxml")
    Datum = []
    time_counter = 0
    #DateTime Objects erstellen
    for entry in soup.findAll('td', class_='first'):
        if entry.text != 'Summe' and entry.text != 'Datum/Uhrzeit' and entry.text != '* Ersatzwert':
            date_time_str = entry.text.replace('.','/').replace(hour_list[time_counter],hour_list_updated[time_counter])
            date_time_obj = datetime.datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
            Datum.append(date_time_obj.astimezone(tzlocal()))
            time_counter += 1

    #Verbrauch in Liste
    Verbrauch = []
    entry_list = list(filter(lambda x: x.text != ' ' and x.text != '*', soup.findAll('td', align = 'right')))
    for index, entry in zip(range(24), entry_list):

        Verbrauch.append(entry.text.replace(',','.'))

    #Write to DB
    x = zip(Datum, Verbrauch)
    for i, j in x:
        # create and write the point
        print(i,j)
        p = Point("Energieverbrauch").tag("Immobilie", immobilien[counter]).field(energie, float(j)).time(i)
        write_api.write(bucket=bucket, org=org, record=p)  # write the point to DB


#Initialize Function
Energietyp = ['Wärme', 'Strom', 'Wasser']
counter = 0

for url in urls:
    for energie in Energietyp:
        get_plain_text(url,energie)
    counter += 1


#Probleme:
#1. 23-0 Uhr Wert wird geskipped