import requests
from selenium import webdriver
import time


class Info:
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
    headers_simtech = {'Host': 'www.similartech.com',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                       'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'X-Request-Verification-Token': 'zc0bA9fsL8bqSsIfakvv7XY8dKKBnPi_6COrgSNSquc4S2kkLrlIvhwNseUnDuodz89zNLJGRbloUJ7kv3KdD7mt2OKfvZ2xC_Y6XD1CES1NaHIL0',
                       'X-Requested-With': 'XMLHttpRequest',
                       'DNT': '1',
                       'Connection': 'keep-alive',
                       'Referer': 'https://www.similartech.com/dashboard/websites/analysis/url/techrepublic.com'}
    cookies_simtech = {"__hssc": "34316798.3.1574517163585", "__hssrc": "1",
                       "__hstc": "34316798.8cb87d47d08f59ac1974bb5ab6d40c29.1574517163583.1574517163584.1574517163584.1",
                       "__RequestVerificationToken": "9EIWNigGFDxgsv9ilUfmsV7sZEMxfeZF_V3kC4bokhm0xWrujXY0vCTmma8Htuvn_MEzx-gZtMEFVABZx1vj0YnOqpw1",
                       "_fbp": "fb.1.1574517160121.1765027621", "_ga": "GA1.2.197520012.1574517159", "_gat": "1",
                       "_gid": "GA1.2.743509771.1574517159",
                       "_lr_hb_-eiz3eg/similartech": "{\"heartbeat\":1574517264036}",
                       "_lr_tabs_-eiz3eg/similartech": "{\"sessionID\":0,\"recordingID\":\"2-8e3a745c-0462-46a8-915a-1d36d61088cb\",\"lastActivity\":1574517264034}",
                       "_lr_uf_-eiz3eg/similartech": "09cd1452-6296-4ba4-bde3-0e07410133b8",
                       ".SAUTH": "F94A7E37E16EFB839775AEDB18DFA28BFAB992C35EE778CC3642DE1F19EFD20261386D84901FDC4DED2F9E92984685A7308BA7DA82D452B597DCF3190AFE1B9FAE32FDF02E0D873BCB0CEC82EB0CF827D9741782D75643502BDEA85AFAE263DB09C069A8563F5642E33FE6B586BC2210FAF110D4AF4065A70C056734864D0A2F8620A254C7754849B6078C0EA89E7D2C8385B5E6",
                       "cookieconsent_status": "dismiss", "hsfirstvisit": "",
                       "hubspotutk": "8cb87d47d08f59ac1974bb5ab6d40c29", "initialLP": "/account/register",
                       "initialReferrer": "",
                       "intercom-session-v16ho3zr": "Rmw3aXdXK1FHOENCR0E4STlJT0Ird0ZOdHp0aVdjbHN6WURSRVU0Z1oydVdiblhaZE9GOXNwbTc5UFVzc3FCTS0tN0ZlKzhINXRCdkwyTUFUU1FpYUNWdz09--f81446b89213d2dc508a8583c4f808b8743666fc",
                       "sessionLP": "/account/activate?email=mapihor937@exserver.top&token=li5JTzorTvvT_tG8yAvP0cFsHgt8bUoA9vDp6ArF0gQ1&utm_source=membership&utm_medium=email&utm_campaign=welcome&guidance=on",
                       "sessionReferrer": "https://temp-mail.org/ru/", "SGSS": "c481914b-b42a-44f2-bfd7-8f3f1ec472af",
                       "utm_campaign": "welcome", "utm_source": "membership"}

    base_url = 'https://www.similartech.com/api/websites/analysis?site='
    adbrainer_url = 'https://dashboard.adbrainer.com/main/dashboard?token=f0fe34639af4c2587ec33f37346e15ba'
    symbols = (
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w',
        'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    email = ['none']


class Path:
    base_path = 'D:/Vlad/My Project/fabel/src'
    categories_path = base_path + '/base_src/categories.txt'
    sites_path = base_path + '/base_src/sites.txt'
    up_20k_path = base_path + '/trash/sites_more_2000.txt'
    done_path = base_path + '/done/done.txt'
    google_iframe = base_path + '/trash/google_iframe.txt'
    error_click = base_path + '/trash/error_click.txt'
    ads_path = base_path + '/ads/sites_with_ads.txt'
    num_path = base_path + '/buf/num.txt'


class Fake_error(Exception):
    def __init__(self, text):
        self.txt = text


def request(url, headers, cookies):
    session = requests.session()
    response = session.get(url, headers=headers, cookies=cookies)
    return response


def read_list(path):
    list_ = []
    with open(path) as f:
        for line in f:
            list_.append(line.strip().lower())
    return list_


def clear_tabs(driver):
    list_of_tabs = driver.window_handles
    current_tab = driver.current_window_handle
    if len(list_of_tabs) > 1:
        for i in range(1, len(list_of_tabs)):
            driver.switch_to.window(list_of_tabs[i])
            driver.close()
    driver.switch_to.window(current_tab)


def module_similar_tech(site):
    """ This module made for getting data from Similar Tech. Data: monthly visits; google adsense """

    def get_month_visits(response):
        month_visits = response.json()['discover']['info']['monthlyVisits']
        return month_visits

    def get_email(response, email):
        try:
            email = response.json()['discover']['emails']['roleBasedEmails']
        except ValueError and KeyError:
            pass
        return email

    def get_ads(response):
        flag = -1
        try:
            for i in range(len(response.json()['alerts'])):
                count = len(response.json()['alerts'][i]['added'])
                if count > 0:
                    for y in range(count):
                        if response.json()['alerts'][i]['added'][y]['id'] == 237:
                            # print(response.json()['alerts'][i]['date'] + ' added')
                            flag = True
                            raise Fake_error("I found the Adsense in the Added")
                count = len(response.json()['alerts'][i]['removed'])
                if count > 0:
                    for y in range(count):
                        if response.json()['alerts'][i]['removed'][y]['id'] == 237:
                            # print(response.json()['alerts'][i]['date'] + ' removed')
                            flag = False
                            raise Fake_error("I found the Adsense in the Removed")
        except Fake_error as er:
            print(er)
        return flag

    response = request(info.base_url + site, info.headers_simtech, info.cookies_simtech)
    # print(response.content)
    info_site_ads = []
    if response.status_code == 200:
        if int(get_month_visits(response)) > 20000:
            flag = get_ads(response)
            if flag == True:
                email = get_email(response, info.email)
                with open(path.ads_path, 'a') as f:
                    f.write(site)
                    info_site_ads.append(site)
                    for line in range(len(email)):
                        f.write(' ' + email[line])
                        info_site_ads.append(email[line])
                    f.write('\n')
    else:
        print('error response: {}'.format(str(response)))
    return info_site_ads


def module_accepter(driver, site):
    """ This module made for accepting of site in adbrainer database """

    flag = False
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="form_content"]').send_keys(site)
            driver.find_element_by_xpath('//*[@id="form_save"]').click()
            status = driver.find_element_by_xpath('/html/body/div[1]/div/form/div/span').text
            if status == 'Site ' + site + ' is ok!':
                flag = True
                break
            else:
                break
        except:
            driver.get(info.adbrainer_url)
            print('error')
    return flag


def module_iframe_finder(driver, site):
    """ This module made for finding iframe in a site """

    flag = 'no'
    try:
        driver.get('http://' + site)
        time.sleep(4)
        iframes = driver.find_elements_by_tag_name('iframe')
        for i in range(len(iframes)):
            try:
                iframe = iframes[i]
                id = str(iframe.get_attribute('id'))
                if id.find('aswift') != -1 and len(id) > 1:
                    iframe.click()
                    flag = 'aswift'
                    break
                if id.find('google_ads') != -1 and len(id) > 1:
                    iframe.click()
                    flag = 'google_ads'
                    break
            except:
                flag = 'error_click'
    except:
        print('error in module_iframe_finder')
    return flag


def main():
    driver_acceptor = webdriver.Firefox()
    driver_iframe_finder = webdriver.Firefox()
    driver_acceptor.get(info.adbrainer_url)
    sites = read_list(path.sites_path)
    try:
        for i in range(91803, len(sites)):
            print(str(i) + ' ' + info.base_url + sites[i])
            site_ads = module_similar_tech(sites[i])
            if len(site_ads) != 0 and site_ads[1] != 'none':
                flag_accept = module_accepter(driver_acceptor, site_ads[0])
                if flag_accept == True:
                    flag_iframe = module_iframe_finder(driver_iframe_finder, site_ads[0])
                    if flag_iframe == 'aswift':
                        with open(path.done_path, 'a') as f:
                            for y in range(len(site_ads)):
                                f.write(str(site_ads[y]) + ' ')
                            f.write('\n')
                    elif flag_iframe == 'google_ads':
                        with open(path.google_iframe, 'a') as f:
                            for y in range(len(site_ads)):
                                f.write(str(site_ads[y]) + ' ')
                            f.write('\n')
                    elif flag_iframe == 'error_click':
                        with open(path.error_click, 'a') as f:
                            for y in range(len(site_ads)):
                                f.write(str(site_ads[y]) + ' ')
                            f.write('\n')
            if i % 100 == 0:
                clear_tabs(driver_iframe_finder)
                print('')
    except:
        driver_iframe_finder.quit()
        driver_acceptor.quit()


path = Path()
info = Info()

main()
