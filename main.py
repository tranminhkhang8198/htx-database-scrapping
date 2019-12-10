from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# config for csv
filename = "thuoc-bvtv.csv"
f = open(filename, "w")

headers = "Tên thuốc, Hoạt chất, Hàm lượng, Nhóm thuốc, Nhóm độc, Phạm vi sử dụng, Liều lượng, Cách dùng, Đơn vị đăng kí, Địa chỉ, Nhà sản xuất, Địa chỉ sản xuất\n"

f.write(headers)

for i in range(10):
    thuoc_id = 6000 + i
    my_url = "http://113.190.254.147/EcoFarm/en/thuoc/viewthuocmobile?thuocid=" + str(
        thuoc_id
    )

    # opening up connection, grapping the page
    uClient = uReq(my_url)

    page_html = uClient.read()

    uClient.close()

    page_soup = soup(page_html, "html.parser")

    # grabs the content
    container = page_soup.find("div", {"class": "body-content"})

    # get ten thuoc
    ten_thuoc = container.h3.text

    # get all table
    tables = page_soup.findAll("table")

    final_content = ""

    final_content += ten_thuoc + ","

    # ##########################################################################################
    # # get info from first table
    # table1_content = ""
    # i = 1
    # for tr in tables[0].findAll("tr"):
    #     if i == 4:
    #         nhom_docs = ""
    #         for nhom_doc in tr.findAll("td")[1].findAll("p"):
    #             ten = nhom_doc.text.strip()
    #             so = nhom_doc.span.img["src"].split("/")[-1].split(".")[0][-1].strip()

    #             nhom_docs += ten + ":" + so + "|"
    #         nhom_docs = nhom_docs[:-1]
    #         table1_content += nhom_docs + ","
    #         break

    #     content = tr.findAll("td")[1].text.strip()
    #     table1_content += content + ","
    #     i += 1

    # final_content += table1_content

    # ##########################################################################################
    # # get info from second table
    # table2_content = ""

    # for tr in tables[1].findAll("tr"):

    #     content_2 = ""
    #     for pham_vi in tr.findAll("td"):
    #         content_2 += pham_vi.text.strip().replace(",", "") + "|"

    #     content_2 = content_2[:-1]
    #     table2_content += content_2 + ","

    # final_content += table2_content

    ##########################################################################################
    # get info from third table
    table3_content = ""
    for tr in tables[2].findAll("tr"):
        content_3 = ""
        for thong_tin in tr.findAll("td")[1]:

            content_3 += str(thong_tin).strip().replace(",", " -")
            print(content_3)

        table3_content += content_3 + ","

    table3_content = table3_content[:-1]

    final_content += table3_content

    f.write(final_content + "\n")
