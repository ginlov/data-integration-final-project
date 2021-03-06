def crawlDiDongViet():
    import time
    import csv
    import pandas as pd

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.common.by import By
    from pymongo import MongoClient
    from datetime import date

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path='D:/workspace/drivers/chromedriver.exe', chrome_options=options)

    LOGIN_URL = 'https://didongviet.vn/dien-thoai'

    ignored_exceptions=(NoSuchElementException, StaleElementReferenceException,)
    time.sleep(5)

    product_links = []

    def get_more_product(driver):
        for i in range(50):
            time.sleep(1)
            try:
                driver.find_elements(By.CLASS_NAME,'more_product')[0].click()
            except:
                print('can not get more product')


    def get_product_link(driver):
        number = len(driver.find_elements(By.CLASS_NAME, 'item.product.product-item'))
        print('NUMBER: ', number)
        for i in range(number):
            product_link = (driver.find_elements(By.CLASS_NAME, 'item.product.product-item')[i]).find_element(By.TAG_NAME,'a').get_attribute('href')
            # print(product_link)
            product_links.append(product_link)
        return product_links

    driver.get(LOGIN_URL)
    get_more_product(driver)
    product_links = get_product_link(driver)


    for link in product_links:
        try:
            driver.get(str(link))
            time.sleep(1)

            name =''
            price = ''

            bluetooth = ''
            thuong_hieu=''
            xuat_xu=''
            ho_tro_the_nho_ngoai=''
            chip_set=''
            toc_do_cpu=''
            kich_thuoc=''
            cong_nghe_man_hinh=''
            jack_tai_nghe=''
            loai_pin=''
            loai_sim=''
            trong_luong=''
            ram=''
            do_phan_giai=''
            rom=''
            kich_thuoc_man_hinh=''

            name_CN = 'heading-title'

            try:
                name = driver.find_element(By.CLASS_NAME, name_CN).text
            except:
                print('NO NAME')
            try:
                price = driver.find_element(By.CLASS_NAME, 'price-wrapper ').text
                print(price)
            except:
                print('NO PRICE')
            table = driver.find_element(By.CLASS_NAME,'data.table.additional-attributes')
            rows = table.find_elements(By.TAG_NAME,'li')
            for row in rows:
                th = row.find_element(By.TAG_NAME,'p').text
                td = row.find_element(By.TAG_NAME,'span').text
                # print(td,th)
                try:
                    if th == 'Bluetooth':
                        bluetooth = td
                    if th == 'Th????ng hi???u':
                        thuong_hieu = td
                    if th == 'Xu???t x??? th????ng hi???u':
                        xuat_xu = td
                    if th == 'H??? tr??? th??? nh??? ngo??i':
                        ho_tro_the_nho_ngoai = td
                    if th == 'Chipset (h??ng SX CPU)':
                        chip_set = td
                    if th == 'T???c ????? CPU':
                        toc_do_cpu = td
                    if th == 'M??n h??nh r???ng':
                        kich_thuoc = td
                    if th == 'C??ng ngh??? m??n h??nh':
                        cong_nghe_man_hinh = td
                    if th == 'Jack tai nghe':
                        jack_tai_nghe = td
                    if th == 'Dung l?????ng pin':
                        loai_pin = td
                    if th == 'SIM':
                        loai_sim = td
                    if th == 'Tr???ng l?????ng':
                        trong_luong = td
                    if th == 'RAM':
                        ram = td
                    if th == '????? ph??n gi???i':
                        do_phan_giai = td
                    if th == 'B??? nh??? trong':
                        rom = td
                    if th == 'K??ch th?????c m??n h??nh':
                        kich_thuoc_man_hinh = td
                except:
                    print('cant get tr')
            with open('didongviet.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([name, price, bluetooth, thuong_hieu, xuat_xu, ho_tro_the_nho_ngoai, chip_set,
                                 toc_do_cpu, kich_thuoc, cong_nghe_man_hinh, loai_pin, loai_sim, trong_luong, ram,
                                 do_phan_giai, rom])
        except:
            print('can not get link')

        data = pd.read_csv("didongviet.csv", header=None)
        data["date"] = [str(date.today())]*data.shape[0]
        data.reset_index(inplace=True)
        data_dict = data.to_dict('records')

        client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
        db = client["data-integration2"]

        collec = db["didongviet"]

        collec.insert_many(data_dict)
