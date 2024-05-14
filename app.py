from seleniumbase import Driver
import pandas as pd
import csv
import os

#Driver tanımlaması gerçekleşir
driver = Driver(uc=True)

#openPage fonksiyonu oluşturulur
def openPage(driver):
    url = "https://sahibinden.com"
    driver.uc_open_with_reconnect(url, 3)

#clickVerify fonksiyonu oluşturulur
def clickVerify(driver):
    driver.switch_to_frame("iframe")


openPage(driver)
openPage(driver)
clickVerify(driver)
#Çerezler red edilir
# driver.uc_click("#onetrust-reject-all-handler")
pageOffset = -20
for page in range(1,51):
    pageOffset += 20
    driver.get(f"https://www.sahibinden.com/satilik/istanbul/sahibinden?pagingOffset={pageOffset}")
    for i in range(1, 22):
        try:
            #Burada sayfadki ilana tıkladığı zaman hata alıp almadığı kontrol edilir
            driver.uc_click(f"#searchResultsTable > tbody > tr:nth-child({i}) > td.searchResultsTitleValue > a")
            print(f"Liste {i} elemanına tıkladım")

            # Verilen XPath ifadesi altındaki tüm <li> elementlerini bul
            li_elements = driver.find_elements("#classifiedDetail > div > div.classifiedDetailContent > div.classifiedInfo > ul > li")
            num_li_elements = len(li_elements)

            # Dataset sütun isimleri
            columns = ["İlan No", "İlan Tarihi", "Emlak Tipi", "m² (Brüt)", "m² (Net)", "Oda Sayısı", "Bina Yaşı",
                       "Bulunduğu Kat", "Kat Sayısı", "Isıtma", "Banyo Sayısı", "Balkon", "Asansör", "Otopark", "Eşyalı",
                       "Kullanım Durumu", "Site İçerisinde", "Site Adı", "Aidat (TL)", "Krediye Uygun", "Tapu Durumu",
                       "Takas", "İlçe", "Fiyat"]

            # İlan özelliklerini tutacak dictionary oluştur
            newData = ",,,,,,,,,,,,,,,,,,,,,,,"
            price = driver.get_text(f"//*[@id=\"classifiedDetail\"]/div/div[2]/div[2]/h3")
            ilçe = driver.get_text(f"#classifiedDetail > div > div.classifiedDetailContent > div.classifiedInfo > h2 > a:nth-child(3)")
            print(price)
            print(ilçe)
            
            for column in range(1, num_li_elements+1):
                strong = driver.get_text(f"#classifiedDetail > div > div.classifiedDetailContent > div.classifiedInfo > ul > li:nth-child({column}) > strong")
                span = driver.get_text(f"#classifiedDetail > div > div.classifiedDetailContent > div.classifiedInfo > ul > li:nth-child({column}) > span")
                print("-----------------------------")
                print(f"{strong} : {span}")
                try:
                    # strong değerini columns listesi içinde arayıp indeksini bul
                    index = columns.index(strong)
                    print(index)
                    # Kaçıncı , den önce yazmam gerektiğini alıyorum
                    index += 1
                    print(index)

                    

                    comma_index = newData.find(',', 0)
                    for i in range(index):
                        comma_index = newData.find(',', comma_index + 1)

                    comma_index -= 1
                    print(f"{index}. virgülün indeksi (find ile):", comma_index)


                    newData = newData[:comma_index] + span + newData[comma_index:]


                except Exception as e:
                    continue
            
            #İlçe ekleniyor
            newData = newData[:23] + ilçe + newData[23:]

            #Fiyat ekleniyor
            newData += price

            # Yeni veriyi CSV dosyasına ekle
            with open('dataset.csv', 'a', newline='', encoding='utf-8') as f:
                # Eğer dosya boşsa sütun isimlerini yaz
                if os.stat('dataset.csv').st_size == 0:
                    writer = csv.writer(f)
                    writer.writerow(columns)
                # Yeni veriyi dosyaya ekle
                writer = csv.writer(f)
                writer.writerow(newData.split(','))


            driver.get(f"https://www.sahibinden.com/satilik/istanbul/sahibinden?pagingOffset={pageOffset}")
        except Exception as e:
            print(f"Hata: {e}. Bir sonraki iterasyona geçiliyor.")
            i -= 1
            continue



#toplam 50 sayfa var
#her sayfada 1 tanesi reklam üzere 21 adet liste elemanı var

#Benim bu ilanın kaç özelliği olduğunu öğrenebilmem gerekli o sayıyı elde etmem lazım
#elimde bir adet dataset.csv dosyası olacak. ve "fiyat" isimli sütun her zaman olacak
#

#bu for döngüsünün altında önce 
#classifiedDetail > div > div.classifiedDetailContent > div.classifiedInfo > ul > li:nth-child(1) > strong
#classifiedId
#classifiedId
#classifiedDetail > div > div.classifiedDetailContent > div.classifiedInfo > ul > li:nth-child(2) > strong
#classifiedDetail > div > div.classifiedDetailContent > div.classifiedInfo > ul > li:nth-child(2) > span


#ilk önce csv dosyasının ilk satırını bir liste olara tutacağım en başta boş olacak
#ilanın özelliklerini strong ve span olarak iki listede tutacağaım
#döngü bittikten sonra csv dosyasını güncelleme sırası başlayacak
