from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.error import HTTPError

import json
import csv

document = []
for i in range(1, 6980):
    thuoc_id = str(i)

    my_url = (
        "http://113.190.254.147/EcoFarm/en/thuoc/viewthuocmobile?thuocid=" + thuoc_id
    )

    # opening up connection, grapping the page

    try:
        uClient = uReq(my_url)
    except HTTPError as e:
        content = e.read()

    page_html = uClient.read()
    uClient.close()

    print("Start scrapping thuoc info with id = " + thuoc_id)

    page_soup = soup(page_html, "html.parser")

    # grabs the content
    # container = page_soup.find("div", {"class": "body-content"})
    container = page_soup.body

    if container is None:
        continue

    # get ten thuoc
    ten_thuoc = container.h3.text

    # store info
    thuoc_info = {}

    thuoc_info["Tên thuốc"] = ten_thuoc

    # ##########################################################################################
    # # get info from first table
    table_1 = container.findAll("div", {"class": "col-md-12"})[1]
    i = 1
    for tr in table_1.findAll("tr"):
        if i == 4:
            nhom_docs = {}
            for nhom_doc in tr.findAll("td")[1].findAll("p"):
                ten = nhom_doc.text.strip()
                so = nhom_doc.span.img["src"].split("/")[-1].split(".")[0][-1].strip()
                nhom_docs[ten] = so
            thuoc_info["Nhóm độc"] = nhom_docs
            break

        key = tr.findAll("td")[0].text.strip()
        value = tr.findAll("td")[1].text.strip()
        thuoc_info[key] = value
        i += 1

    ##########################################################################################
    # get info from second table
    tables_2 = container.findAll("div", {"class": "col-md-6"})[1].findAll("table")
    pham_vi_su_dungs = []

    for i in range(len(tables_2)):
        index = 0
        pham_vi_su_dung = {}
        for tr in tables_2[i].findAll("tr"):
            if index == 0:
                cay_trong = tr.findAll("td")[0].text.strip()
                dich_hai = tr.findAll("td")[1].text.strip()
                pham_vi_su_dung["Cây trồng"] = cay_trong
                pham_vi_su_dung["Dịch hại"] = dich_hai
                index += 1
                continue

            if index == 1:
                lieu_luong = tr.findAll("td")[0].text.split(":")[-1].strip()
                phi = tr.findAll("td")[1].text.split(":")[-1].strip()
                pham_vi_su_dung["Liều lượng"] = lieu_luong
                pham_vi_su_dung["PHI"] = phi
                index += 1
                continue

            cach_dung = tr.findAll("td")[0].text.split(":")[-1].strip()
            pham_vi_su_dung["Cách dùng"] = cach_dung

            pham_vi_su_dungs.append(pham_vi_su_dung)

    thuoc_info["Phạm vi sử dụng"] = pham_vi_su_dungs

    ##########################################################################################
    # get info from third table
    table_3 = container.findAll("div", {"class": "col-md-6"})[2].findAll("table")[0]
    thong_tin_dang_ky = {}

    for tr in table_3.findAll("tr"):
        key = tr.findAll("td")[0].text.strip()
        value = tr.findAll("td")[1].text.strip()
        thong_tin_dang_ky[key] = value

    thuoc_info["Thông tin đăng ký"] = thong_tin_dang_ky

    document.append(thuoc_info)


# save json to file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(document, f, ensure_ascii=False, indent=4)

