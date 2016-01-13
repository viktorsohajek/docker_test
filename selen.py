import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os 
import datetime
from datetime import date, timedelta
import csv
from pyvirtualdisplay import Display

datum= str(time.strftime("%Y-%m-%d"))

display = Display(visible=0, size=(1024, 768))
display.start()

### LIST SHOPU ###
yesterday = date.today() - timedelta(1)
date = yesterday.strftime('%Y-%m-%d')

dict={}
dict['Heureka.cz'] = {}
dict['Zbozi.cz'] = {}
dict['Heureka.cz']['Login_1'] = {'Login': 'valiska@sportmall.cz',
                     'Password': 'heurech15',
                     'Url_login': 'https://login.heureka.cz/login',
                     'Shop': ['Sporty.cz','Snowboards.cz','Kolonial.cz','Prodeti.cz'],
                     'Url_stats': ['http://sluzby.heureka.cz/obchody/statistiky/?shop=5709&from='+date+'&to='+date+'&cat=-4','http://sluzby.heureka.cz/obchody/statistiky/?shop=1786&from='+date+'&to='+date+'&cat=-4','http://sluzby.heureka.cz/obchody/statistiky/?shop=53090&from='+date+'&to='+date+'&cat=-4','http://sluzby.heureka.cz/obchody/statistiky/?shop=45555&from='+date+'&to='+date+'&cat=-4'] }

dict['Heureka.cz']['Login_2'] = {'Login': 'heureka@bigbrands.cz',
                     'Password': 'ecommerceheureka',
                     'Url_login': 'https://login.heureka.cz/login',
                     'Shop': ['BigBrands.cz'],
                     'Url_stats': ['http://sluzby.heureka.cz/obchody/statistiky/?from='+date+'&to='+date+'&shop=42893&cat=-4'] }

dict['Heureka.cz']['Login_3'] = {'Login': 'info@limal.cz',
                     'Password': 'heureka123456',
                     'Url_login': 'https://login.heureka.cz/login',
                     'Shop': ['Rozbaleno.cz'],
                     'Url_stats': ['http://sluzby.heureka.cz/obchody/statistiky/?from='+date+'&to='+date+'&shop=6590&cat=-4'] }

dict['Zbozi.cz']['Login_1'] = {'Login': 'it@snowboards.cz',
                     'Password': 'wsappcsk25',
                     'Url_login': '',
                     'Shop': ['Sporty.cz','Snowboards.cz','Prodeti.cz'],
                     'Shop_shortcut': ['sm','snb','pd'],
                     'Shop_id': ['15801','9072','109963'],
                     'Url_stats': [''] }


dict['Zbozi.cz']['Login_2'] = {'Login': 'jc@limal.cz',
                     'Password': '0EF78C6C',
                     'Url_login': '',
                     'Shop': 'Rozbaleno.cz',
                     'Shop_shortcut': 'ro',
                     'Shop_id': '90738',
                     'Url_stats': [''] }

dict['Zbozi.cz']['Login_3'] = {'Login': 'ppc.bigbrands.cz@gmail.com',
                     'Password': '253CD1C7',
                     'Url_login': '',
                     'Shop': 'BigBrands.cz',
                     'Shop_shortcut': 'bb',
                     'Shop_id': '105672',
                     'Url_stats': [''] }                     


### /LIST SHOPU ###


### DEFINICE ###
#user input - cesta k souboru, kam se maji statistiky ukladat
save_path="/"
#set current date as "today - delta"
delta=2
current_date = '{d.day}.{d.month}.{d.year}'.format(d=datetime.datetime.now()-timedelta(delta))
#set stats dates
date_from = current_date
date_to = current_date

#account info
username = "it@snowboards.cz"
password = "wsappcsk25"

### /DEFINICE ###


#zmeni working directory na slozku, kam se ukladaji statistiky
os.chdir(save_path)


# To prevent download dialog
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', save_path) # custom location path
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')


#inicializace virtual browseru
def init_driver():
    driver = webdriver.Firefox(profile)
    driver.wait = WebDriverWait(driver, 5)
    return driver
 
#logovaci funkce 
def lookup(driver, query1,query2):
    driver.get("https://admin.zbozi.cz/loginScreen?url=%2F")
    try:
        box_username = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "username")))
        box_password = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "password")))   
        box_username.send_keys(query1)
        box_password.send_keys(query2)
        driver.find_element_by_xpath("//input[@type='submit']").click()
    except TimeoutException:
        print("Box or Button not found in google.com")




### BROWSER START FCN ###


def scrape(driver,web_id,shop_name):
    if os.path.isfile("out_zbozi_stats_"+shop_name+".csv"):
        os.rename("out_zbozi_stats_"+shop_name+".csv","zbozi_stats_"+shop_name+"_"+datetime.datetime.now().isoformat()+".csv")

    #definice linku pro stahnuti
    link_web_stats = 'https://admin.zbozi.cz/premiseStatistics?premiseId='+web_id+'&dateFrom='+date_from+'&dateTo='+date_to

    #zavola link na stranku statistik
    driver.get(link_web_stats)
    time.sleep(5)

    #zaskrtne radio pole "po kategoriich"
    driver.find_element_by_xpath("//input[@id='sg']").click()
    #stickne button na vygenerovani reportu
    driver.find_element_by_xpath("//input[@id='createNewReport']").click()

    #pocka 20 sec nez se vygeneruje .csv
    time.sleep(20)

    #znovu nacte stranku kvuli objeveni odkazu na ztazeni .csv v html
    driver.get(link_web_stats)

    #najde link na ztazeni .csv statistik
    for a in driver.find_elements_by_xpath("//table[@id='statisticsContainer']//tr[3]//td[5]/a"):
	   link_stats=a.get_attribute('href')

    #proklikne link_stats na stazeni .csv se statistikama
    driver.get(link_stats)

    #w8
    time.sleep(10)


    #prejmenuje .csv soubor poslednich statistik na jednotny nazev, ktery pak pujde do KBC
    for filename in os.listdir(save_path):
        if filename.startswith("statistics"):
            os.rename(filename,"zbozi_stats_"+shop_name+".csv")



#inicializuje browser
driver=init_driver()
time.sleep(5)

# zaloguje usera
lookup(driver,dict['Zbozi.cz']['Login_1']['Login'], dict['Zbozi.cz']['Login_1']['Password'])
time.sleep(5)

#zavola scraping
for index in range(0,3):
    shop_id = dict['Zbozi.cz']['Login_1']['Shop_id'][index]
    shop_shortcut = dict['Zbozi.cz']['Login_1']['Shop_shortcut'][index]
    
    scrape(driver,shop_id,shop_shortcut)


# zaloguje usera 2
lookup(driver,dict['Zbozi.cz']['Login_2']['Login'], dict['Zbozi.cz']['Login_2']['Password'])
time.sleep(5)
shop_id = dict['Zbozi.cz']['Login_2']['Shop_id']
shop_shortcut = dict['Zbozi.cz']['Login_2']['Shop_shortcut']
    
scrape(driver,shop_id,shop_shortcut)


# zaloguje usera 3
lookup(driver,dict['Zbozi.cz']['Login_3']['Login'], dict['Zbozi.cz']['Login_3']['Password'])
time.sleep(5)
shop_id = dict['Zbozi.cz']['Login_3']['Shop_id']
shop_shortcut = dict['Zbozi.cz']['Login_3']['Shop_shortcut']
    
scrape(driver,shop_id,shop_shortcut)


#zavre browser
driver.close()
display.stop()

time.sleep(5)

os.chdir(save_path)

for filename in os.listdir(save_path):
    if filename.endswith(".csv"):
        with open(save_path+filename,'r') as csvinput:
            with open(save_path+'out_'+filename, 'w') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n',delimiter=";")
                reader = csv.reader(csvinput,delimiter=";")

                all = []
                row = next(reader)
                row.append('Date')
                all.append(row)

                for row in reader:
                    row.append(datum)
                    all.append(row)

                writer.writerows(all)


for filename in os.listdir(save_path):
    if not filename.startswith("out_"):
        os.remove(filename)
