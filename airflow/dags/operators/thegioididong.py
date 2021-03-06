def crawlTGDD():
    import requests
    from bs4 import BeautifulSoup
    import json
    import pandas as pd
    import pymongo
    from pymongo import MongoClient
    from datetime import date, timedelta

    data_phones = []

    Devices = ["apple-iphone", "samsung", "oppo", "xiaomi", "vivo", "realme", "nokia", "itel", "mobell", "masstel"]
    ID = 1
    for i in range(len(Devices)):
        URL = 'https://www.thegioididong.com/dtdd-' + Devices[i]
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        webpage = requests.get(URL, headers=headers).text
        A = []
        soup = BeautifulSoup(webpage, 'html.parser')
        data = soup.find('ul', {"class": "listproduct"})
        for a in data.find_all('a', href=True):
            try:
                new_str = a['href']
                new_str = new_str.replace("javascript:void(0)", "")
                new_str = new_str.replace("#", "")
                if new_str == "":
                    continue
                if new_str == "/dtdd/poco-c40?src=osp":  # Mẫu điện thoại đang quảng cáo
                    continue
                URL = "https://www.thegioididong.com" + new_str
                headers = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
                webpage = requests.get(URL, headers=headers).text

                soup = BeautifulSoup(webpage, 'html.parser')
                data = json.loads(soup.find('script', id="productld").get_text()).get("additionalProperty")
                name = json.loads(soup.find('script', id="productld").get_text()).get('name')

                data1 = json.loads(soup.find('script', id="productld").text).get("offers").get('price')
                data2 = json.loads(soup.find('script', id="productld").text).get("offers").get('priceValidUntil')
                print('ID = ', ID)
                print(name)
                ID = ID + 1
                print('Price :', data1)
                print('priceValidUntil :', data2)

                item = {}
                item["Thương hiệu"] = Devices[i]
                item['name'] = name
                item['price'] = data1
                item['priceValidUntil'] = data2
                item["url"] = URL

                item["img_url"] = None
                for entry in data:
                    print(entry['name'], ':', entry['value'])
                    item[entry['name']] = entry['value']
                try:
                    color_list = soup.find("div", {"class": "box03 color group desk"}).find_all("a", {"class": "box03__item item"})
                    for each in color_list:
                        item["color"] = each.text
                        data_phones.append(item.copy())
                except:
                    item["color"] = None
                    data_phones.append(item)
            except:
                pass
    df = pd.DataFrame.from_dict(data_phones)
    df.rename(columns={"Bộ nhớ trong": "Bộ nhớ"}, inplace=True)
    df.drop_duplicates(inplace=True)
    client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration2"]
    collec = db["thegioididong"]

    date_save = date.today()
    df["date"] = [str(date_save)] * df.shape[0]
    df.reset_index(drop=True, inplace=True)
    data_dict = df.to_dict("records")
    collec.insert_many(data_dict)
    #df.to_csv("data_phones.csv", encoding="utf-8")


if __name__ == "__main__":
    crawlTGDD()