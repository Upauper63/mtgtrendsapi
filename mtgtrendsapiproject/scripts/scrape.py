from bs4 import BeautifulSoup
import datetime
import urllib.request
import time
import re

import sys
sys.path.append('../')
from mtgtrendsapi.models import Item, Scrape

def run():
    # HerokuSchedulerで1週間沖にJobが動くための条件
    if not datetime.date.today().weekday() % 7 == 0:
        return
    scrape_obj = Scrape()
    scrape_obj.save()
    scrape_id = scrape_obj.id
    x = (scrape_id - 1) % 4

    Item.objects.all().update(current_price=None)
    # 英語 ノーマル 値段高い順にソート
    ori_url = "https://www.hareruyamtg.com/ja/products/search?foilFlg%5B0%5D=0&language%5B0%5D=2&sort=price&order=DESC&page="
    items_class = ".itemList"
    name_class = '.itemName'
    price_class = '.itemDetail__price'
    url_class = '.itemData > a'
    existPage = True
    i = 1
    while existPage == True:
        try:
            url = ori_url + str(i)
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
            }
            request = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(request)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select(items_class)
            # 終了判定
            if len(items) == 0:
                existPage = False
                continue
            for item in items:
                name = item.select(name_class)[0].text.strip()
                price = item.select(price_class)[0].text.strip()
                url = item.select(url_class)[0].get('href')
                seg = 'detail/'
                product_id = int(url[url.find(seg)+len(seg):url.find('?')])
                # 値段の成形
                price = int(re.sub(r"\D",'', price))

                obj = ""
                obj = Item.objects.filter(product_id = product_id, name = name).first()
                if obj and obj.name:
                    prev_x = (x - 1) % 4
                    dic = obj.__dict__
                    dic.pop('_state')
                    kwargs = dic
                    kwargs['price_' + str(x)] = price
                    kwargs['current_price'] = price
                    if dic['price_' + str(prev_x)]:
                        diff_price_prev = price - dic['price_' + str(prev_x)]
                        kwargs['diff_price_prev'] = diff_price_prev
                    for y in range(4):
                        prev_scrape_obj = Scrape.objects.filter(id = kwargs['scrape_' + str(y) + '_id']).first()
                        kwargs['scrape_' + str(y)] = prev_scrape_obj
                        kwargs.pop('scrape_' + str(y) + '_id')
                    kwargs['scrape_' + str(x)] = scrape_obj
                    Item.objects.filter(product_id=product_id, name = name).delete()
                    obj = Item(**kwargs)
                else:
                    kwargs = {'product_id': product_id, 'name': name, 'scrape_' + str(x): scrape_obj, 'price_' + str(x): price, 'current_price': price}
                    obj = Item(**kwargs)
                if obj:
                    # レコード数に制限があるため、対象データに制限
                    if price < 300:
                        existPage = False
                    elif price <= 100000:
                        obj.save()
                else:
                    existPage = False

            i += 1
            time.sleep(10)
            if i % 20 == 0:
                # herokuがスリープに入らないように分割して間隔時間をとる
                for _ in range(10):
                    url = "https://upauper63-mtgtrendsapi.herokuapp.com/api/"
                    request = urllib.request.Request(url=url, headers=headers)
                    urllib.request.urlopen(request)
                    time.sleep(360)

        except urllib.error.HTTPError as err:
            print("{} ErrorOccured:{}".format(err.code, err.reason))
            scrape_obj.is_finished = True
            scrape_obj.finished_at = datetime.datetime.now()
            scrape_obj.status = 2
            scrape_obj.status_info = str(err.code) + ':' + str(err.reason)
            scrape_obj.save()
            existPage = False
            Item.objects.filter(current_price=None).delete()
        except urllib.error.URLError as err:
            print("{} ErrorOccured:{}".format(err.code, err.reason))
            scrape_obj.is_finished = True
            scrape_obj.finished_at = datetime.datetime.now()
            scrape_obj.status = 3
            scrape_obj.status_info = str(err.code) + ':' + str(err.reason)
            scrape_obj.save()
            existPage = False
            Item.objects.filter(current_price=None).delete()
        except:
            print(sys.exc_info())
            scrape_obj.is_finished = True
            scrape_obj.finished_at = datetime.datetime.now()
            scrape_obj.status = 4
            scrape_obj.status_info = str(sys.exc_info())
            existPage = False
            Item.objects.filter(current_price=None).delete()
            
    else:
        scrape_obj.is_finished = True
        scrape_obj.finished_at = datetime.datetime.now()
        scrape_obj.status = 1
        scrape_obj.save()
        Item.objects.filter(current_price=None).delete()