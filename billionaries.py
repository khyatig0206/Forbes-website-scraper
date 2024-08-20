from playwright.sync_api import sync_playwright
import requests

def get_cookie():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.forbes.com/billionaires/")
        datadome_cookie = context.cookies()[0]['value']
        vwo = context.cookies()[1]['value']
        browser.close()
    return datadome_cookie, vwo

def req(datadome_cookie, vwo):
    url = "https://www.forbes.com/forbesapi/person/billionaires/2024/position/true.json"
    querystring = {"filter": "uri,finalWorth,age,country,source,qas,rank,category,person,personName,industries,organization,gender,firstName,lastName,squareImage,bios"}
    payload = ""
    
    headers = {
        'Cookie': f'datadome={datadome_cookie}; VWO={vwo};',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Referer': 'https://www.forbes.com/billionaires/'
    }
    
    r = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    # Check the status code
    print(f"Status Code: {r.status_code}")
    
    # Print the raw response content
    # print(f"Response Content: {r.text}")

    # Attempt to return JSON if the response was successful
    if r.status_code == 200:
        return r.json()
    else:
        return None
    
def extract_data(person_data):
    return {
        'personName': person_data.get('personName'),
        'age': person_data.get('age'),
        'country': person_data.get('country'),
        'city': person_data.get('city'),
        'organization': person_data.get('organization'),
        'position': person_data.get('position')
    }


if __name__ == "__main__":
    datadome, vwo = get_cookie()
    data = req(datadome, vwo)
    if data:
        
        persons = data['personList']['personsLists'][:10]
        for person in persons: 
            extracted_info = extract_data(person)
            print(extracted_info)
            
    else:
        print("Failed to retrieve data.")
