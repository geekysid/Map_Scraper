#!/usr/bin/env python3


# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#   Name: Siddhant Shah                             #
#   Date: 08/04/2021                                #
#   Desc: Instragram Accounts that Liked Post       #
#   Email: siddhant.shah.1986@gmail.com             #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #


# ## PROJECT REQUIREMENTS:
# ## Go to 'http://www.housinginnovationalliance.com/whats-new/off-site-heat-map/ 
# ## and extract important data points for all places in map


# >> IMPORTANT IMPORTS
import requests, json, pyfiglet
import random, logging, time
from bs4 import BeautifulSoup
from termcolor import cprint
from colorama import init
import pandas as pd


# >> GLOBAL VARIABLE 
logger = None


# >> IMPORTANT HEADER FOR API CALL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': '*/*',
    'Accept-Language': 'en-GB,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'http://www.zeemaps.com/pub?group=3839111&legend=1&search=1&simpleadd=1&track=UA-41067143-4&x=-100.193057&y=43.712520&z=13',
}


# ------------------------------- # 
# ------ GENERAL FUNCTIONS ------ # 
# ------------------------------- # 


# >> just for decoration
def intro_deco():
    print('\n\n')
    print(pyfiglet.figlet_format(" GeekySid"))
    print()
    print('  # # # # # # # # # # # # #  # # # # # # # #')
    print('  #                                        #')
    print('  #         SCRAPER DATA FROM MAPS         #')
    print('  #           By: SIDDHANT SHAH            #')
    print('  #             Dt: 08-04-2021             #')
    print('  #      siddhant.shah.1986@gmail.com      #')
    print('  #    **Just for Educational Purpose**    #')
    print('  #                                        #')
    print('  # # # # # # # # # # # # #  # # # # # # # #')
    print()


# >> SEETING UP LOGGER
def logger_setup():
    global logger

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('logger.log')
    formatter = logging.Formatter('%(asctime)s - %(process)d - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.info(f' >>>>>>>>>>>>>>>>>>>> START >>>>>>>>>>>>>>>>>>>> ')


# >> RANDOM TIME IN SECONDS FOR WHICH SCRIPT WILL SLEEP
def sleep():
    sleep_time = random.randint(10, 20)/10
    cprint(f'      [~~] Waiting for {sleep_time} secs', 'white')
    time.sleep(sleep_time)


# >> FUNCTION TO OUTPUT TOTAL TME TAKEN BY THE SCRIPT
def timer(start_time):    
    end_time = time.time()

    execution_time = end_time - start_time
    hrs = str(int(execution_time//3600))
    mins = str(int((execution_time%3600)//60))
    secs = str(int((execution_time%3600)%60))
    execution_time_str = f"  Total Time of Execution: {hrs}hrs {mins}mins {secs}secs  "
    deco_str = "="*len(execution_time_str)
    logger.info(f'  [+] {deco_str}')
    logger.info(f'  [+] {execution_time_str}')
    logger.info(f'  [+] {deco_str}\n')
    

    print("\n")
    cprint("="*len(execution_time_str), "blue", attrs=["bold"])
    cprint(f"[*] {execution_time_str}", "blue", attrs=["bold"])
    cprint("="*len(execution_time_str), "blue", attrs=["bold"])
    print("\n")


# >> EXTRACTING REQUIRED DATA FROM THE HTML STRING
def get_html_data(_text):
    soup = BeautifulSoup(_text, 'html.parser')
    try:
        website = soup.find('a')['href']
    except:
        website = ''
        
    try:
        phone = soup.find('span', class_='phone').text.strip()
    except:
        phone = ''
        
    try:
        description = soup.find('span', class_='bold').next_sibling.strip()
    except:
        description = ''

    return {
        'website': website,
        'phone': phone,
        'description': description
    }


# >> SAVING DATA TO THE CSV FILE
def save_to_csv(data):
    try:
        pd.DataFrame(data).to_csv('data.csv', index=False)
        logger.info('  [+] Saved data to the CSV File')
    except Exception as e:
        logger.exception('  [X] Exception while saving data to the CSV file')
    

# ---------------------- # 
# ------ API CALL ------ # 
# ---------------------- # 


# >> GETTING ALL LEGENDS FROM API
def get_legends():
    logger.info(f'  [+] Making API call to fetch Legends')
    cprint(f'\n  [+] Making API call to fetch Legends', 'yellow', attrs=['bold'])

    params = (('g', '3839111'),)
    response = requests.get('http://www.zeemaps.com/legends/getall', headers=headers, params=params, )

    if response.status_code == 200:
        result = response.json()
        logger.info(f'  [+] Total Legends Fetched: {len(result)}')
        cprint(f'      [>>] Total Legends Fetched: {len(result)}', 'green', attrs=['bold'])
        return result
    else:
        logger.error(f'  [x] Got {response.status_code} response')
        cprint(f'      [xx] Got {response.status_code} response', 'red', attrs=['bold'])
        return {
            "error": f"Got Status Error: {response.status_code}"
        }


# >> GETTING MAP DATA FROM API
def get_map_data():
    logger.info(f'  [+] Making API call to fetch Map Data')
    cprint(f'\n  [+] Making API call to fetch Map Data', 'yellow', attrs=['bold'])

    params = (('g', '3839111'), ('k', 'REGULAR'), ('e', 'true'), ('_dc', '0.6220957961214806'), )
    response = requests.get('http://www.zeemaps.com/emarkers', headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        logger.info(f'  [+] Total Legends Fetched: {len(result)}')
        cprint(f'      [>>] Total Legends Fetched: {len(result)}', 'green', attrs=['bold'])
        return result
    else:
        logger.error(f'  [x] Got {response.status_code} response')
        cprint(f'      [xx] Got {response.status_code} response', 'red', attrs=['bold'])
        return {
            "error": f"Got Status Error: {response.status_code}"
        }


# >> GETTING DATA FOR DIFFERENT LEGENEDS GOT FROM get_map_data()
def get_legend_data(_id):
    logger.info(f'  [+] Making API call to fetch Data of Item with ID - {_id}')
    cprint(f'\n  [+] Making API call to fetch Data of Item with ID - {_id}', 'cyan', attrs=['bold'])
    params = ( ('g', ['3839111', '3839111']), ('j', '1'), ('sh', ''), ('_dc', '0.48580308055575416'), ('eids', f'[{_id}]'), ('emb', '1'),)

    response = requests.get('http://www.zeemaps.com/etext', params=params, verify=False)

    if response.status_code == 200:
        result = response.json()
        logger.info(f'  [+] Data Fetched')
        cprint(f'      [>>] Data Fetched', 'green', attrs=['bold'])
        return result
    else:
        logger.error(f'  [x] Got {response.status_code} response')
        cprint(f'      [xx] Got {response.status_code} response', 'red', attrs=['bold'])
        return {
            "error": f"Got Status Error: {response.status_code}"
        }


# --------------------------- # 
# ------ MAIN FUNCTION ------ # 
# --------------------------- # 


# >> MAIN FUNCTION
def main():
    legends = get_legends()         # API call to get legends
    map_data = get_map_data()       # API call to get locations
    legend_data_list = []
    html_data_list = []
    final_data = []

    # calling API to fetch data for every location
    for item in map_data:
        _id = item['id']
        legend_data = get_legend_data(_id)
        html_data_list.append(get_html_data(legend_data['t']))
        legend_data_list.append(legend_data)
        sleep()

    print()
    
    # cleaning data
    for legend_data, html_data in zip(legend_data_list, html_data_list):
        data = {**legend_data, **html_data}
        f_data = {**data, **data['ad']}
        del f_data['ad']
        del f_data['t']
        final_data.append(f_data)
        
        # saving data to the CSV file fter fetching evert 10th data
        if len(final_data) % 10 == 0:
            save_to_csv(final_data)

    save_to_csv(final_data)     # saving data to the CSV file


# >> EXECUTES ONLY IF SCRIPT IS NOT IMPORTED
if __name__ == "__main__":
    try:
        init()
        start_time = time.time()
        intro_deco()
        logger_setup()
        cprint('\n  [+] STARTING TO FETCH DATA ', 'white','on_magenta', attrs=['bold'])
        main()
    except Exception as e:
        cprint(f'  [!!] Exception: {str(e)}', "red", attrs=["bold"])
        logger.exception('  [!!] Exception Occured ')
    timer(start_time)
