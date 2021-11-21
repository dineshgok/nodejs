import requests
from bs4 import BeautifulSoup


def main_scrape_func(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }

    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.content, 'lxml')

    services = []
    for option in soup.find('select', {'title':'Filter by Services'}).find_all('option'):
        if option.get('value'):
            services.append((option.get('value'), option.text))

    full_datas = []

    for service_id, service_name in services[1:6]:
        service_url = url + f"?Services={service_id}"
        res = requests.get(url=service_url, headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')

        for option in soup.find('select', {'title':'Filter by Offices'}).find_all('option')[1:]:
            if option.text:
                office_id = option.get('value')
                # print('Service Name :', service_name, 'Service ID :', service_id, 'Office Name :', option.text, 'Office ID :', office_id)
                
                api_key = "{" + "8BEE2997-A9B1-4874-A4C3-7EBA04C493EC" + "}"
                for page_num in range(5):
                    full_url = f"https://www.ballardspahr.com/sitecore/api/people/search?lang=en&sc_apikey={api_key}&page={page_num}&Services={service_id}&Offices={office_id}"
                    res = requests.get(full_url, headers=headers)
                    
                    if res.ok:
                        for i in res.json()['Results']:
                            person_url = i['url']
                            final_url = f"https://www.ballardspahr.com/sitecore/api/layout/render/jss?lang=en&sc_apikey={api_key}&item={person_url}"
                            res = requests.get(url=final_url, headers=headers)
                          
                            json_object = res.json()['sitecore']['route']
                            
                            datas = {
                                'Page': page_num,
                                'URL': final_url,
                                'Service Name': service_name,
                                "Name": json_object['name'],
                                'Offices': option.text,
                                "Role": json_object['placeholders']['content'][0]['placeholders']['aside'][0]['fields']['Title']['fields']['Name']['value'],
                                "Email": json_object['placeholders']['content'][0]['placeholders']['aside'][0]['fields']['Email']['value'],
                                "Tele-Phone": json_object['placeholders']['content'][0]['placeholders']['aside'][1]['placeholders']['related-offices'][0]['fields']['OfficeNumber']['value'],
                                "Fax-Number": json_object['placeholders']['content'][0]['placeholders']['aside'][1]['placeholders']['related-offices'][0]['fields']['FaxNumber']['value'],
                            }
                            print(datas)
                            full_datas.append(datas)
                
                break
    return full_datas

if __name__ == "__main__":
    url = "https://www.ballardspahr.com/People"
    for i in main_scrape_func(url):
        print(i)