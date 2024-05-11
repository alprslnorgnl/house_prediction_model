from seleniumbase import Driver


driver = Driver(uc=True)
url = "https://sahibinden.com"
driver.uc_open_with_reconnect(url, 3)
driver.switch_to_frame("iframe")
driver.uc_click("span.mark")

#success-text

#Çerezler red edilir
driver.uc_click("#onetrust-reject-all-handler")

pageOffset = -20

for page in range(1,51):
    pageOffset += 20
    driver.get(f"https://www.sahibinden.com/satilik/istanbul/sahibinden?pagingOffset={pageOffset}")
    for i in range(1, 22):
        try:
            #Burada sayfadki ilana tıkladığı zaman hata alıp almadığı kontrol edilir
            driver.uc_click(f"#searchResultsTable > tbody > tr:nth-child({i}) > td.searchResultsTitleValue > a")
            print("Liste {i} elemanına tıkladım")
            driver.get(f"https://www.sahibinden.com/satilik/istanbul/sahibinden?pagingOffset={pageOffset}")
        except Exception as e:
            print(f"Hata: {e}. Bir sonraki iterasyona geçiliyor.")
            continue



#toplam 50 sayfa var
#her sayfada 1 tanesi reklam üzere 21 adet liste elemanı var
#her ilanın özellik sayısı ise değişiyor bunu benim bulmam gerekli