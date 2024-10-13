import colorama
import requests
import time
from bs4 import BeautifulSoup
from colorama import Fore
from urllib.parse import urljoin

colorama.init(autoreset=True)

banner = """




_________                 ________                          
__  ____/_____ _______ ______  __ \_________  ______________
_  /    _  __ `/_  __ `__ \_  / / /  __ \_  |/_/  _ \_  ___/
/ /___  / /_/ /_  / / / / /  /_/ // /_/ /_>  < /  __/  /    
\____/  \__,_/ /_/ /_/ /_//_____/ \____//_/|_| \___//_/     Version 1.2 
                                                            By Mr. BILRED
                                                            (Even More Powerful Than Before)
                                                                     

CamDoxer: A tool designed for discovering publicly accessible IP camera streams across various countries. 
Perfect for cybersecurity enthusiasts and researchers seeking to understand network vulnerabilities and improve 
device security.

Crafted with precision by:
Mr. Bilred aka Bilal Ahmad Khan

Github: https://github.com/BilalAhmadKhanKhattak
Visit For New Updates(if any)
"""
print(Fore.LIGHTCYAN_EX + banner)

insecam_countries_dict = {
    'US': "United States", 'JP': "Japan", 'IT': "Italy", 'DE': "Germany",
    'TW': "Taiwan, Province Of", 'RU': "Russian Federation", 'KR': "Korea, Republic Of",
    'FR': "France", 'AT': "Austria", 'CZ': "Czech Republic", 'CH': "Switzerland",
    'NO': "Norway", 'PL': "Poland", 'GB': "United Kingdom", 'RO': "Romania", 'CA': "Canada",
    'NL': "Netherlands", 'ES': "Spain", 'SE': "Sweden", 'BG': "Bulgaria", 'DK': "Denmark",
    'VN': "Viet Nam", 'BR': "Brazil", 'BE': "Belgium", 'IR': "Iran, Islamic Republic",
    'RS': "Serbia", 'IN': "India", 'TR': "Turkey", 'UA': "Ukraine", 'HU': "Hungary",
    'ZA': "South Africa", 'FI': "Finland", 'ID': "Indonesia", 'IE': "Ireland", 'CL': "Chile",
    'SK': "Slovakia", 'TH': "Thailand", 'MX': "Mexico", 'GR': "Greece",
    'BA': "Bosnia And Herzegovina", 'LV': "Latvia", 'AR': "Argentina", 'AU': "Australia",
    'MY': "Malaysia", 'LT': "Lithuania", 'SY': "Syria", 'EE': "Estonia", 'IL': "Israel",
    'MD': "Moldova, Republic Of", 'SI': "Slovenia", 'NZ': "New Zealand", 'HK': "Hong Kong",
    'EC': "Ecuador", 'BD': "Bangladesh", 'CN': "China", 'AM': "Armenia", 'KZ': "Kazakhstan",
    'TZ': "Tanzania", 'HR': "Croatia", 'NI': "Nicaragua", 'PE': "Peru", 'TN': "Tunisia",
    'BY': "Belarus", 'CO': "Colombia", 'IS': "Iceland", 'FO': "Faroe Islands",
    'ME': "Montenegro", 'NC': "New Caledonia", 'PK': "Pakistan", 'TT': "Trinidad And Tobago",
    'LA': "Laos", 'GU': "Guam", 'KY': "Cayman Islands", 'PT': "Portugal", 'LU': "Luxembourg",
    'GG': "Guernsey", 'CI': "Ivory Coast", 'AO': "Angola", 'PA': "Panama", 'HN': "Honduras",
    'GE': "Georgia"}  # Don't Freak out, I copied the above thing, to make things easier for users

skyline_countries_dict = {
    "AR": "argentina", "BB": "barbados", "BR": "brazil", "CA": "canada", "CW": "caribbean-netherlands",
    "CL": "chile", "CR": "costa-rica", "DO": "dominican-republic", "EC": "ecuador", "SV": "el-salvador",
    "GD": "grenada", "HN": "honduras", "MX": "mexico", "PA": "panama", "PE": "peru", "US": "united-states",
    "VI": "us-virgin-islands", "VE": "venezuela", "AL": "albania", "AT": "austria", "BE": "belgium",
    "HR": "croatia", "CY": "cyprus", "FO": "faroe-islands", "FR": "france", "DE": "germany", "GR": "greece",
    "HU": "hungary", "IS": "iceland", "IE": "ireland", "IT": "italy", "MT": "malta", "NL": "netherlands",
    "NO": "norway", "PL": "poland", "PT": "portugal", "SM": "republic-of-san-marino", "RO": "romania",
    "SI": "slovenia", "ES": "spain", "CH": "switzerland", "GB": "united-kingdom", "EG": "egypt", "KE": "kenya",
    "MU": "mauritius", "SC": "seychelles", "ZA": "south-africa", "TZ": "zanzibar", "CN": "china", "IL": "israel",
    "JO": "jordan", "MV": "maldives", "PH": "philippines", "LK": "sri-lanka", "TH": "thailand", "TR": "turkey",
    "AE": "united-arab-emirates", "VN": "vietnam", "AU": "australia"
}

def disclaimer():
    disclaimer_text = """
        ***********************************************************************
        *                          IMPORTANT NOTICE                           *
        ***********************************************************************
        This tool is intended solely for educational purposes and ethical use 
        by cybersecurity professionals and researchers. It is designed to raise 
        awareness about the importance of securing Internet-connected devices 
        such as IP cameras.

        Unauthorized access to computer systems, networks, or devices without 
        explicit permission is illegal and punishable by law. Misuse of this 
        tool to access, monitor, or control devices without the owner's consent 
        is a violation of privacy rights and may lead to severe legal 
        consequences.

        By using this tool, you agree to use it responsibly, ethically, and 
        in compliance with all applicable laws and regulations. The author 
        of this tool assumes no liability for any misuse or damage caused by 
        improper use.

        If you do not agree with these terms, you should not use this tool.

        ***********************************************************************
        """
    print(Fore.LIGHTCYAN_EX + disclaimer_text)


def user_agreement():
    ask = input(
        Fore.LIGHTMAGENTA_EX + "Do You Agree To Use This Tool Ethically And Responsibly? (yes/no) ").strip().lower()
    if ask != "yes":
        print(Fore.LIGHTRED_EX + "You Must Agree To The Terms To Use This Tool. Exiting...")
        exit()


def fetch_pages(url, headers, retries=5, delay=0.2):
    for attempt in range(retries):
        try:
            respOnse = requests.get(url, headers=headers)
            if respOnse.status_code == 200:
                return respOnse.content
            else:
                print(f" {attempt + 1} Error Occurred: {respOnse.status_code}")

        except Exception as e:
            print(f" {attempt + 1} An Error Occurred: {e}")

        time.sleep(delay)

    print(Fore.LIGHTYELLOW_EX + "Max retries reached. Failed To Retrieve Page")
    return None


def parse_insecam_html(html):
    soup = BeautifulSoup(html, "html.parser")  # Converts the html to BeautifulSoup Object
    links = soup.find_all("a", href=True)  # Find The links with anchor tag "a" where href is true
    base_url = "http://www.insecam.org"
    full_urls = [urljoin(base_url, link['href']) for link in links if '/view/' in link['href']]

    """ The Above Thing is called list comprehension, if u dont know how it works, see below:
     [expression for item in iterable if condition]

     expression: value, which will be returned in new list
     item: a variable representing each element in iterable
     iterable: a collection or sequence(like a list) you wanna iterate over
     condition: optional filter that determines if the item should be included in new list or not """

    return full_urls
# Don't remove this, will help study the problems and solutions
# def parse_skyline_html(html):
#     soup = BeautifulSoup(html, "html.parser")
#     links = soup.find_all("a", href=True)
#     full_urls = [urljoin(f"https://www.skylinewebcams.com", link['href']) for link in links if '/webcam/' in link['href']]
#     return full_urls


def parse_skyline_html(html, country, skyline_countries_dict):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a", href=True)

    # This is to retrieve the country value(identifier) from the skyline_countries_dict
    country_value = skyline_countries_dict.get(country, "").lower()

    # Filters URLs that contain both /webcam/ and country value
    full_urls = [
        urljoin("https://www.skylinewebcams.com", link['href'])
        for link in links
        if '/webcam/' and country_value in link['href'].lower()
    ]
    return full_urls
def main():
    disclaimer()
    user_agreement()



    while True:
        country = input(
            Fore.LIGHTMAGENTA_EX + "Enter The Country Code(US, JP, FR) or type 'LIST' to list all the country "
                                   "codes: ").upper().strip()
        if country == "LIST":
            print(Fore.LIGHTGREEN_EX + "Insecam Available Country Codes: ")
            for code, name in insecam_countries_dict.items():
                print(Fore.LIGHTCYAN_EX + f"{code}: {name}")
            print(Fore.LIGHTGREEN_EX + "Skyline Available Country Codes: ")
            for code, name in skyline_countries_dict.items():
                print(Fore.LIGHTCYAN_EX + f"{code}: {name}")
            continue  # After printing all the country codes, this 'continue' skips the rest of the loop and prompts
            # the user to try again

        if country in insecam_countries_dict or country in skyline_countries_dict:
            break
        else:
            print(Fore.LIGHTRED_EX + "Bruh, Enter A Two letter country code")

    try:
        num_pages = int(input(Fore.LIGHTMAGENTA_EX + "Enter The Number Of Pages You Wanna Scrape: "))

    except ValueError:
        print("Value Must Be An Integer")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }

    # Loop Through pages and scrape urls
    all_camera_urls = []

    if country in insecam_countries_dict:
        print(Fore.LIGHTCYAN_EX + f"Fetching Insecam Results For {insecam_countries_dict[country]}...")
        insecam_base_url = f"http://www.insecam.org/en/bycountry/{country}/?page="
        for page_num in range(1, num_pages + 1):
            full_url = insecam_base_url + str(page_num) #  This Part Helps in changing the page number
            print(Fore.LIGHTGREEN_EX + f"Scraping Insecam URL: {full_url}")
            html_content = fetch_pages(full_url, headers)

            # This logic prints the total number of cameras found on a page
            if html_content:  # If html content is successfully retrieved then below snippet will work
                camera_urls = parse_insecam_html(html_content)
                all_camera_urls.extend(camera_urls)  # Adds the found camera URLs to the all_camera_urls list.
                print(Fore.LIGHTGREEN_EX + f"Found {len(camera_urls)} cameras on page {page_num}.")
            else:
                print(Fore.LIGHTRED_EX + "Failed to retrieve data from the page")

    # This Had the problem, please dont remove this, this will help future programmer to understand the problems and solutions

    # if country in skyline_countries_dict:
    #     print(Fore.LIGHTCYAN_EX + f"Fetching Skyline Results For {skyline_countries_dict[country]}...")
    #     skyline_base_url = f"https://www.skylinewebcams.com/en/webcam/{skyline_countries_dict[country]}.html"
    #     print(Fore.LIGHTGREEN_EX + f"Scraping Skyline URL: {skyline_base_url}")
    #     html_content = fetch_pages(skyline_base_url, headers)
    #     if html_content:
    #         camera_urls = parse_skyline_html(html_content)
    #         all_camera_urls.extend(camera_urls)
    #         print(Fore.LIGHTGREEN_EX + f"Found {len(camera_urls)} cameras on Skyline.")
    #     else:
    #         print(Fore.LIGHTRED_EX + "Failed To Retrieve Data From Skyline")

    # This is the solution(this is also the same thing down below)
    # if country in skyline_countries_dict:
    #     print(Fore.LIGHTCYAN_EX + f"Fetching Skyline Results For {skyline_countries_dict[country]}...")
    #     skyline_base_url = f"https://www.skylinewebcams.com/en/webcam/{skyline_countries_dict[country]}.html"
    #     print(Fore.LIGHTGREEN_EX + f"Scraping Skyline URL: {skyline_base_url}")
    #     html_content = fetch_pages(skyline_base_url, headers)
    #     if html_content:
    #         camera_urls = parse_skyline_html(html_content, country, skyline_countries_dict)  # Pass the country and dict
    #         all_camera_urls.extend(camera_urls)
    #         print(Fore.LIGHTGREEN_EX + f"Found {len(camera_urls)} cameras on Skyline.")
    #     else:
    #         print(Fore.LIGHTRED_EX + "Failed To Retrieve Data From Skyline")

    if country in skyline_countries_dict:
        print(Fore.LIGHTCYAN_EX + f"Fetching Skyline Results For {skyline_countries_dict[country]}...")
        skyline_base_url = f"https://www.skylinewebcams.com/en/webcam/{skyline_countries_dict[country]}.html"
        print(Fore.LIGHTGREEN_EX + f"Scraping Skyline URL: {skyline_base_url}")
        html_content = fetch_pages(skyline_base_url, headers)

        try:
            if html_content:
                camera_urls = parse_skyline_html(html_content, country, skyline_countries_dict)
                all_camera_urls.extend(camera_urls)
                print(Fore.LIGHTGREEN_EX + f"Found {len(camera_urls)} cameras on Skyline.")
            else:
                print(Fore.LIGHTRED_EX + "Failed To Retrieve Data From Skyline")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")

        except Exception as e:
            print(f"An Error Occurred: {e}")

    #  Displaying the results
    if all_camera_urls:
        print(Fore.LIGHTGREEN_EX + "\nList Of Camera URLS Retrieved:")
        for i, url in enumerate(all_camera_urls, start=1):
            print(f"{i}.{url}")
    else:
        print(Fore.LIGHTRED_EX + "No cameras found or an error occurred")


if __name__ == "__main__":
    main()
