import sys
import csv
from bs4 import BeautifulSoup
import urllib2

url = "https://www.magiccardmarket.eu/?mainPage=browseUserProducts&idCategory=1&idUser=14633&editMode=&cardName=%s&idExpansion=&idRarity=&idLanguage=&condition_uneq=&condition=&isFoil=0&isSigned=0&isPlayset=0&isAltered=0&comments=&minPrice=&maxPrice="
page_url = "https://www.magiccardmarket.eu/?mainPage=browseUserProducts&idCategory=1&idUser=14633&editMode=&cardName=%s&idExpansion=&idRarity=&idLanguage=&condition_uneq=&condition=&isFoil=0&isSigned=0&isPlayset=0&isAltered=0&comments=&minPrice=&maxPrice=&resultsPage=%s"
card_file = sys.argv[1]
card_list = [line.rstrip('\n') for line in open(card_file)]


with open('prices.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)


    for card in card_list:
        if card is None or card == "":
            pass
        else:
            price = None
            card_url = url % card.replace(" ", "+")
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]

            page = opener.open(card_url, timeout=20)
            soup = BeautifulSoup(page.read(), 'html.parser')
            page_select = soup.find_all("select", "vAlignMiddle")
            extra_pages = (len(str(page_select).split('value=')) - 1) / 4

            for x in range(0, extra_pages + 1):
                if x is not 0:
                    card_url = page_url % (card.replace(" ", "+"), str(x))
                    page = opener.open(card_url, timeout=20)
                    soup = BeautifulSoup(page.read(), 'html.parser')

                price_cells = soup.find_all(class_="algn-r nowrap")
                name_cells = soup.find_all(class_="vAlignMiddle dualTextDiv")

                listings = zip(price_cells, name_cells)

                for price_cell, name_cell in listings:
                    list_name = name_cell.__str__()
                    list_name = list_name.split('>')[3][:-3]
                    if list_name == card:  # Checking to make sure correct card
                        list_price = price_cell.__str__()             # convert html to string
                        list_price = list_price[26:].split(' ')[0]    # cut off beginning/ending html
                        list_price = list_price.replace(',', '.')     # , to . for floats
                        list_price = float(list_price)                # string to floats
                        if price is None or list_price < price:
                            price = list_price
                    else:
                        pass

            writer.writerow([card, str(price)])
            print card + ' - ' + str(price)
