import undetected_chromedriver as uc
from time import sleep
#import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from random import randint
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv('config.env')
style_conf = {
    'Condominium' : os.getenv('Condominium'),
    'Co_op' : os.getenv('Co_op'),
    'Duplex' : os.getenv('Duplex'),
    'Farm_and_Ranch' : os.getenv('Farm_and_Ranch'),
    'House' : os.getenv('House'),
    'Lots_and_Land' : os.getenv('Lots_and_Land'),
    'Mobile_Manufactured_Modular_House' : os.getenv('Mobile_Manufactured_Modular_House'),
    'Multi_Family' : os.getenv('Multi_Family'),
    'Recreational_Cabin_Timeshare_etc' : os.getenv('Recreational_Cabin_Timeshare_etc'),
    'Single_Family' : os.getenv('Single_Family'),
    'Townhouse' : os.getenv('Townhouse'),
    'Triplex' : os.getenv('Triplex'),
    'Apartment' : os.getenv('Apartment'),
}


def init_UC():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-setuid-sandbox')
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"108.0.5359.125"',
    'sec-ch-ua-full-version-list': '"Not?A_Brand";v="8.0.0.0", "Chromium";v="108.0.5359.125", "Google Chrome";v="108.0.5359.125"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"8.0.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-chrome-id-consistency-request': 'version=1,client_id=77185425430.apps.googleusercontent.com,device_id=91c169ab-71ab-4040-933c-d2bca9ab8f98,signin_mode=all_accounts,signout_mode=show_confirmation',
    'x-client-data': 'CLL5ygE=',
}
    driver = uc.Chrome(executable_path=os.path.join(os.getcwd(),'chromedriver'),options = chrome_options)
    return driver




data  = {
     'image' : '/user1-128x128.jpg',
     'address' : '27 Newton Dr',
     'city' : 'Toronto',
     'zip_code' : 'M2M 2M6',
     'price' : '$3,000,000',
     'sales_type' : 'Sale',
     'style_string' : 'DetachedLink:N2-StoreyIrreg:Front On:SAcre:40 x 122 Feet',
     'storey' : '2',
     'exterior' : 'Brick',
     'heat' : 'Forced Air / Gas',
     'ac' : 'Central Air',
     'sqft' : '',
     'g_stalls' : '2',
     'amenties' : '',
     'remarks' : '***No Door Knock Or Visit Land Permited***Prohibited Transpassing Without Consent***',
     'extra' : '',
     'bedrooms' : '2',
     'bathrooms' : '2'
     }

def run_post(username, password , results):

    driver = init_UC()
    print('3')
    #login
    driver.get('https://www.point2homes.com/CA')

    actions = ActionChains(driver)

    sleep(randint(1,2))

    try:
        driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
        sleep(randint(2,3))
    except:
        pass
    driver.find_element(By.XPATH , '//*[@id="login"]').click()

    sleep(randint(1,2))

    while(True):
        try:
            driver.find_element(By.ID ,'Username').click()
            sleep(randint(1,2))
            break
        except:
            sleep(randint(3,5))
    driver.find_element(By.ID , 'Username').send_keys(username)
    sleep(randint(1,2))
    driver.find_element(By.ID ,'Password').click()
    sleep(randint(1,2))
    driver.find_element(By.ID , 'Password').send_keys(password)
    sleep(randint(1,2))

    driver.find_element(By.XPATH , '//*[@id="login_form"]/div/fieldset/div[1]/p/button').click()
    sleep(randint(20,30))
    i=0
    for data in results:
        try:
            while(True):
                try:
                    driver.get('https://www.point2homes.com/Account/AddAListing')
                    break
                except:
                    sleep(randint(3,5))

            driver.find_element(By.XPATH , '//button[@data-id="citySelector"]').click()

            sleep(randint(1,2))

            search_input= driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[3]/div/div/div/input')
            sleep(.5)

            while(True):
                try:
                    search_input.send_keys(data['city'])
                    break
                except:
                    sleep(randint(2,3))
                    continue

            sleep(randint(1,2))

            while(True):
                try:
                    city_lists = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[3]/div/div/ul')
                    cities = city_lists.find_elements(By.TAG_NAME , 'li')
                    break
                except:
                    sleep(randint(2,3))
                    continue
            for city in cities:
                if(city.get_attribute('class') != 'hidden' and city.text.strip().upper() == data['city'].upper()):
                    city.click()
                    break

            sleep(.5)
            while(True):
                try:
                    driver.find_element(By.ID,'Address').click()
                    sleep(.5)
                    driver.find_element(By.ID,'Address').send_keys(data['address'])
                    sleep(randint(1,2))
                    break
                except:
                    sleep(randint(1,2))
                    continue

            while(True):
                try:
                    actions.move_to_element(driver.find_element(By.ID,'ZipCode')).perform()
                    driver.find_element(By.ID,'ZipCode').click()
                    sleep(.5)
                    driver.find_element(By.ID,'ZipCode').send_keys(data['zip_code'])
                    sleep(randint(1,2))
                    break
                except:
                    sleep(randint(1,2))
                    continue

            while(True):
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH , '//input[@value="sale"]'))
                    
                    if(data['sales_type'].upper() == 'SALE'):
                        driver.find_element(By.XPATH , '//input[@value="sale"]').click()
                    else:
                        driver.find_element(By.XPATH , '//input[@value="sale_pending"]').click()
                    break
                except:
                    sleep(randint(1,2))
                    continue
            
            sleep(.5)

            #price
            while(True):
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.ID,'Price'))
                    # driver.find_element(By.ID,'Price').click()
                    sleep(.5)
                    driver.find_element(By.ID,'Price').send_keys(data['price'])
                    sleep(randint(1,2))
                    break
                except:
                    sleep(randint(1,2))
                    continue

            #photo
            try:
                driver.find_element(By.XPATH , '//*[@id="fileupload"]/div[2]/div/span/input').send_keys(data['image'])
                sleep(randint(2,3))
            except Exception as e:
                print(e)

            while(True):
                try:
                    driver.find_element(By.ID,'AddPhotoBtn').click()
                    sleep(randint(2,3))
                    driver.find_element(By.XPATH , '//*[@id="fileupload"]/div[2]/div/button').click()
                    sleep(randint(2,3))
                    break
                except:
                    sleep(randint(1,2))
                    continue

            #description
            # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"Description_ifr")))
            while(True):
                try:
                    iframe = driver.find_element(By.ID,'Description_ifr')
                    driver.switch_to.frame(iframe)
                    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tinymce"))).click()
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.ID ,'tinymce'))
                    
                    driver.find_element(By.ID ,'tinymce').click()

                    driver.find_element(By.ID ,'tinymce').send_keys(data['remarks'] + '\n' + 'Extras : ' + data['extra'])
                    break
                except:
                    sleep(randint(1,2))
                    continue

            # desc_iframe = driver.find_element(By.ID , 'Description_ifr')
            # desc_body = desc_ifsrame.find_element(By.ID,'tinymce')
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='tinymce']"))).send_keys(data['remarks'] + '\n' + 'Extras : ' + data['extra'])
            # desc_body.find_element(By.TAG_NAME , '').click()
            # desc_body.find_element(By.TAG_NAME , '').send_keys(data['remarks'] + '\n' + 'Extras : ' + data['extra'])
            sleep(randint(1,2))
            #building type
            driver.switch_to.default_content()

            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.ID , 'BuildingDetails_Type'))

            driver.find_element(By.ID , 'BuildingDetails_Type').click()
            sleep(.5)
            driver.find_element(By.ID , 'BuildingDetails_Type').find_elements(By.TAG_NAME,'option')[1].click()
            sleep(randint(1,2))

            #building style
            style_selector = driver.find_element(By.ID , 'residentialSubTypes')
            style_selector.click()
            sleep(.5)
            items = style_selector.find_elements(By.TAG_NAME,'option')
            selected = False
            for i in range(1,len(items) - 1):
                item = items[i]
                key = item.text.strip().replace('-','_').replace(' ','_').replace(',','').replace('(','').replace(')','')
                if(style_conf[key] != '' and style_conf[key] in data['style_string']):
                    item.click()
                    selected = True
                    break
            if(not selected):
                items[len(items)-1].click()#click other
            sleep(randint(1,2))
            #building type
            while(True):
                try:
                    type_selector = driver.find_element(By.ID , 'BuildingDetails_BuildingUnitType')
                    type_selector.click()
                    break
                except:
                    sleep(randint(1,2))
                    continue
            sleep(.5)
            items = type_selector.find_elements(By.TAG_NAME,'option')
            selected = False
            for i in range(1,len(items)):
                item = items[i]
                if(item.text in data['style_string']):
                    item.click()
                    selected = True
                    break
            if(not selected):
                items[0].click()#click not specified
            sleep(randint(1,2))
            #stories
            while(True):
                try:
                    stories_selector = driver.find_element(By.ID,'BuildingDetails_Stories')
                    stories_selector.click()
                    break
                except:
                    sleep(randint(1,2))
                    continue
            sleep(.5)
            items = stories_selector.find_elements(By.TAG_NAME,'option')
            selected = False
            for i in range(1,len(items)):
                item = items[i]
                if(item.text.strip() in data['storey']):
                    item.click()
                    selected = True
                    break
            if(not selected):
                items[0].click()#click not specified
            sleep(randint(1,2))
            #bedrooms
            while(True):
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.ID , 'BuildingDetails_Bedrooms'))
                    driver.find_element(By.ID , 'BuildingDetails_Bedrooms').click()
                    sleep(.5) 
                    driver.find_element(By.ID , 'BuildingDetails_Bedrooms').send_keys(data['bedrooms'])
                    sleep(randint(1,2))
                    break
                except:
                    sleep(randint(1,2))
                    continue
            #bathrooms

            while(True):
                try:
                    driver.find_element(By.ID , 'BuildingDetails_Bathrooms').click()
                    sleep(.5) 
                    driver.find_element(By.ID , 'BuildingDetails_Bathrooms').send_keys(data['bathrooms'])
                    sleep(randint(1,2))
                    break
                except:
                    sleep(randint(1,2))
                    continue 
            #garage stalls
            while(True):
                try:
                    driver.find_element(By.ID , 'BuildingDetails_GarageStalls').click()
                    sleep(.5) 
                    driver.find_element(By.ID , 'BuildingDetails_GarageStalls').send_keys(data['g_stalls'])
                    sleep(randint(1,2))
                    break
                except:
                    sleep(randint(1,2))
                    continue
            #interior
            while(True):
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[1]'))
                    interior_panel = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[1]')
                    for checkbox in interior_panel.find_elements(By.CLASS_NAME,'features-checkbox'):
                        text = checkbox.text.strip()
                        if(text.upper() in data['amenties'].upper()):
                            checkbox.click()
                            sleep(1)

                    break
                except:
                    sleep(randint(1,2))
                    continue
            #exterior
            while(True):
                try:            
                    exterior_panel = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[2]')
                    for checkbox in exterior_panel.find_elements(By.CLASS_NAME,'features-checkbox'):
                        text = checkbox.text.strip()
                        if(text.upper() in data['exterior'].upper()):
                            checkbox.click()
                            sleep(1)
                    break
                except:
                    sleep(randint(1,2))
                    break
            #lot
            while(True):
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[3]'))
                    lot_panel = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[3]')
                    for checkbox in lot_panel.find_elements(By.CLASS_NAME,'features-checkbox'):
                        text = checkbox.text.strip()
                        if(text.upper() in data['amenties'].upper()):
                            checkbox.click()
                            sleep(1)
                    break
                except:
                    sleep(randint(1,2))
                    continue
            
            #appliances
            while(True):
                try:
                    appliances_panel = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[4]')
                    for checkbox in appliances_panel.find_elements(By.CLASS_NAME,'features-checkbox'):
                        text = checkbox.text.strip()
                        if(text.upper() in data['extra'].upper()):
                            checkbox.click()
                            sleep(1)
                    break
                except:
                    sleep(randint(1,2))
                    continue

            #view
            while(True):
                try:
                    view_panel = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[5]')
                    for checkbox in view_panel.find_elements(By.CLASS_NAME,'features-checkbox'):
                        text = checkbox.text.strip()
                        if(text.upper() in data['remarks'].upper()):
                            checkbox.click()
                            sleep(1)
                    break
                except:
                    sleep(randint(1,2))
                    continue

            #heating
            while(True):
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[6]'))

                    heating_panel = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[6]')
                    for checkbox in heating_panel.find_elements(By.CLASS_NAME,'features-checkbox'):
                        text = checkbox.text.strip()
                        if(text.upper() in data['heat'].upper()):
                            checkbox.click()
                            sleep(1)
                    break
                except:
                    sleep(randint(1,2))
                    continue

            #cooling
            while(True):
                try:
                    cooling_panel = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[7]')
                    for checkbox in cooling_panel.find_elements(By.CLASS_NAME,'features-checkbox'):
                        text = checkbox.text.strip()
                        if(text.upper() in data['ac'].upper()):
                            checkbox.click()
                            sleep(1)
                    break
                except:
                    sleep(randint(1,2))
                    continue

            #extra
            while(True):
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[6]'))
                    
                    extra_panel = driver.find_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[6]/fieldset/div[10]')
                    for checkbox in extra_panel.find_elements(By.CLASS_NAME,'features-checkbox'):
                        text = checkbox.text.strip()
                        if(text.upper() in data['amenties'].upper()):
                            checkbox.click()
                            sleep(1)
                    break
                except:
                    sleep(randint(1,2))
                    continue

            #save button
            sleep(randint(2,3))
            driver.find_element(By.XPATH , '//*[@id="manuallyInsertedListingForm"]/div[7]/button').click()
            i +=1
            #activate
            while(True):
                try:
                    driver.find_elements(By.CLASS_NAME,'item-cnt')[0].find_element(By.CLASS_NAME,'btn-primary').click()
                    sleep(1.5)
                    driver.find_element(By.ID,'btnYes').click()
                    sleep(randint(2,3))
                    break
                except:
                    sleep(randint(1,2))
            print('success : ' + data['address'])
        except:
            print('fail')
        sleep(randint(5,10))
    success_count = i
    fail_count = len(results) - success_count
    return success_count, fail_count





    


