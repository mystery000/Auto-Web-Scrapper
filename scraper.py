import requests
# from requests_html import HTMLSession
import re
from bs4 import BeautifulSoup
from autopost import run_post
import urllib.request
import os
from time import sleep
from random import randint
from datetime import datetime
base_dir = os.getcwd()

def scrape_url(url):
    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Content-type':'application/json', 
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection' : 'keep-alive',
        'Host' : 'v3.torontomls.net',
        'Accept-Encoding':'gzip, deflate',
        'Upgrade-Insecure-Requests' : '1',
        'Cache-Control' : 'max-age=0'
        }
    
    

    # parsed_html_content = html.fromstring(html_content)

    r = requests.get(url,headers=headers)
    html = r.text
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    report_panel = soup.find('div',attrs={'class' : 'reports'})
    items = report_panel.find_all('div',attrs={'class' : 'link-item'})
    
    # r.html.render()
    i=0
    links = []
    for item in items:
        if(item.get('data-deferred-load')):
            links.append(item.get('data-deferred-load'))
        else:
            links.append(item.get('data-deferred-loaded'))

    results = []
    i = 0
    for link in links:
        try:
            r = requests.get(link,headers=headers)
            html = r.text
            soup = BeautifulSoup(html, features="html.parser")

            for script in soup(["script", "style"]):
                script.extract()    # rip it out
        

            result = {}
            report_container = soup.find('div',attrs={'class' : 'report-container'})
            tabulars = report_container.find_all('div',attrs={'class' : 'tabular'})
            image = tabulars[0].find('div',attrs={'class' : 'imageset_container'})

            horizontals = tabulars[0].find_all('div',attrs={'class' : 'horizontal'})

            address_panel = horizontals[1].find('div' ,attrs={'class' : 'horizontal'}).find('div',attrs={'class':'vertical'})

            price_panel = horizontals[1].find('div' ,attrs={'class' : 'horizontal'}).find_all('div',attrs={'class':'vertical'},recursive=False)[1]
            #get address info
            address = address_panel.find('div',attrs={'class' : 'horizontal'}).get_text().strip()
            if('unit' in address):
                address = address[:address.index('unit')]
            result['address'] = address
            image_url = image.find('img')['src']
            extension = image_url[-4:]
            if('.' not in extension):
                extension = '.' + extension
            if('jpg' not in extension and extension != '.png'):
                extension = '.jpg'
            #if(not os.path.exists('/Users/jackhunter/Downloads/auto/listings')):
            os.makedirs('/Users/jackhunter/Downloads/auto/listings',exist_ok=True)
            dir_name = '/Users/jackhunter/Downloads/auto/listings/' + result['address']
            #if(not os.path.exists(dir_name)):
            os.makedirs(dir_name,exist_ok=True)
            image_file_name = str(int(datetime.now().timestamp())) + extension
            image_file_path = os.path.join(dir_name + '/' + image_file_name)
            response = requests.get(image_url,timeout=300)
            with open(image_file_path , 'wb') as f:
                f.write(response.content)
            # urllib.request.urlretrieve(image_url, image_file_path)

            result['image'] = image_file_path
            

            

            values = address_panel.find_all('div',attrs={'class' : 'horizontal'},recursive=False)[1].find_all('span',attrs={'class' : 'value'})

            country = values[0].get_text().strip()

            city = values[1].get_text().strip()

            zip_code = values[2].get_text().strip()

            result['city'] = country
            result['state'] = city
            result['zip_code'] = zip_code
            #get price info
            values = price_panel.find_all('div',attrs={'class' : 'horizontal'})[0].find_all('span',attrs={'class' : 'value'})

            price = values[0].get_text().strip()

            sales_type = values[1].get_text().strip()

            result['price'] = price
            result['sales_type'] = sales_type

            #remarks 
            legacyBorder = report_container.find('div',attrs={'class' : 'legacyBorder'})

            remarks = legacyBorder.find_all('span',recursive=False)[0]
            remarks_string = remarks.find('span',attrs={'class':'value'}).get_text().strip()
            #extra
            extra = legacyBorder.find_all('span',recursive=False)[1]
            extra_string = extra.find('span',attrs={'class':'value'}).get_text().strip()
            #
            rooms_panel = tabulars[0].find('div',attrs={'class':'horizontal'}).find_all('div',attrs={'class':'vertical'},recursive=False)[1].find_all('div',recursive=False)[4]

            room_detail_panel = rooms_panel.find_all('div',recursive=False)[1]

            result['remarks'] = remarks_string
            result['extra'] = extra_string
            #style
            style_panel = tabulars[0].find('div').find_all('div',recursive=False)[1].find_all('div',recursive=False)[4].find('div')

            # values = style_panel.find_all('span',attrs={'class':'value'})

            # building_type = values[0].get_text().strip()
            # stories = values[2].get_text().strip()

            # result['building_type'] = building_type
            # result['story'] = stories   
            style_string = style_panel.get_text().strip()
            try:
                span_storey = style_panel.find(string=re.compile('Storey')).parent
                storey = span_storey.get_text().strip()
                if('-' in storey):
                    storey = storey.replace('-Storey','')
                else:
                    storey = storey.replace('Storey','').replace(' 1/2 ','.5')
            except:
                storey = ''
            result['style_string'] = style_string
            result['storey'] = storey


            #rooms
            values = room_detail_panel.find_all('span',attrs={'class':'value'})
            bedrooms = values[1].get_text().strip()
            if('+' in bedrooms):
                bedrooms = bedrooms[:bedrooms.index('+')-1]
            bathrooms = values[2].get_text().strip()
            if('+' in bathrooms):
                bathrooms = bathrooms[:bathrooms.index('+')]

            result['bedrooms'] = bedrooms
            result['bathrooms'] = bathrooms

            #sqft
            sqft_field = tabulars[1].find(string=re.compile('Apx Sqft')).parent.parent
            sqft = sqft_field.find('span',attrs={'class':'value'}).get_text().strip()
            if('-' in sqft):
                sqft = sqft[sqft.index('-'):].strip()
            result['sqft'] = sqft
            #garage_stalls
            spaces = 0
            garage_field = tabulars[1].find(string=re.compile('Tot Pk Spcs')).parent.parent
            g_stalls = garage_field.find('span',attrs={'class':'value'}).get_text().strip()
            if('None' in g_stalls):
                g_stalls = 0
            else:
                try:
                    spaces = int(float(g_stalls))
                except:
                    pass
            # garage_field = tabulars[1].find(string=re.compile('Gar/Gar Pk Spcs')).parent.parent
            # g_stalls = garage_field.find('span',attrs={'class':'value'}).get_text().strip()
            # if('None' in g_stalls):
            #     g_stalls = 0
            # else:
            #     g_stalls = int(g_stalls)
            #     if(spaces < g_stalls):
            #         spaces = g_stalls
            try:
                garage_field = tabulars[1].find(string=re.compile('Drive Pk Spcs')).parent.parent
                g_stalls = garage_field.find('span',attrs={'class':'value'}).get_text().strip()
                if('None' in g_stalls):
                    g_stalls = 0
                else:
                    g_stalls = int(float(g_stalls))
                    if(spaces < g_stalls):
                        spaces = g_stalls
            except:
                pass

            result['g_stalls'] = str(spaces)

            #exterior
            exterior_field = tabulars[1].find(string=re.compile('Exterior')).parent.parent
            exterior = exterior_field.find('span',attrs={'class':'value'}).get_text().strip()
            result['exterior'] = exterior
            #heat
            heat_field = tabulars[1].find(string=re.compile('Heat')).parent.parent
            heat = heat_field.find('span',attrs={'class':'value'}).get_text().strip()
            result['heat'] = heat
            #a/c
            AC_field = tabulars[1].find(string=re.compile('A/C')).parent.parent
            ac = AC_field.find('span',attrs={'class':'value'}).get_text().strip()
            result['ac'] = ac
            #amenties
            try:
                amenties_field = tabulars[1].find(string=re.compile('Bldg Amen')).parent.parent
                amenties = amenties_field.find('span',attrs={'class':'value'}).get_text().strip()
            except:
                amenties = ''
            result['amenties'] = amenties
            results.append(result)
            print('success : ' + result['address'])
            i +=1
        except Exception as e:
            print('fail')
            print(e)
        sleep(randint(3,5))
        
    
    return results , i , len(results) - i







    
