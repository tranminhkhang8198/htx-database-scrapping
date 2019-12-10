from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.error import HTTPError
import json

document = []

for i in range(1, 567):
    trang = str(i)

    print("Start scrapping phan bon with page = ", trang)

    my_url = (
        "http://www.cpp.community/danh-muc/phan-bon/search?ten=&thanh_phan=_all_&doanh_nghiep=_all_&loai=&sxnk=&to_chuc_quy_chuan=&bo=&trang="
        + trang
    )

    # opening up connection, grapping the page
    try:
        uClient = uReq(my_url)
    except HTTPError as e:
        content = e.read()

    page_html = uClient.read()

    uClient.close()

    page_soup = soup(page_html, "html.parser")

    # grabs the content
    container = page_soup.find("div", {"id": "content"})

    for tr in container.tbody.findAll("tr"):
        phan_bon = {}

        tds = tr.findAll("td")

        phan_bon["Bộ"] = tds[0].text.strip()
        phan_bon["Tên tỉnh"] = tds[1].text.strip()
        phan_bon["Tên doanh nghiệp"] = tds[2].text.strip()
        phan_bon["Loại phân bón, cách bón"] = tds[3].text.strip()
        phan_bon["Tên phân bón"] = tds[4].text.strip()
        phan_bon["Thành phần, hàm lượng chất dinh dưỡng"] = tds[5].text.strip()
        phan_bon["Căn cứ, tiêu chuẩn, quy định"] = tds[6].text.strip()
        phan_bon["Tổ chức chứng nhận hợp quy"] = tds[7].text.strip()
        phan_bon["Sản xuất, nhập khẩu"] = tds[8].text.strip()

        for i in document:
            if i["Tên phân bón"] == phan_bon["Tên phân bón"]:
                continue
        document.append(phan_bon)

# save json to file
with open("data_phan_bon.json", "w", encoding="utf-8") as f:
    json.dump(document, f, ensure_ascii=False, indent=4)
