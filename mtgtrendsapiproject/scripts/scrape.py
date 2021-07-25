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
    # if not datetime.date.today().weekday() % 7 == 0:
    #     return
    scrape_obj = Scrape()
    scrape_obj.save()
    scrape_id = scrape_obj.id
    x = (scrape_id - 1) % 4
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
                    if 'price' in dic:
                        price_diff_prev = price - dic['price_' + str(prev_x)]
                        kwargs['price_diff_prev'] = price_diff_prev
                    for y in range(4):
                        prev_scrape_obj = Scrape.objects.filter(id = kwargs['scrape_' + str(y) + '_id']).first()
                        kwargs['scrape_' + str(y)] = prev_scrape_obj
                        kwargs.pop('scrape_' + str(y) + '_id')
                    kwargs['scrape_' + str(x)] = scrape_obj
                    Item.objects.filter(product_id=product_id).delete()
                    obj = Item(**kwargs)
                else:
                    kwargs = {'product_id': product_id, 'name': name, 'scrape_' + str(x): scrape_obj, 'price_' + str(x): price}
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
            if i % 40 == 0:
                time.sleep(3600)

        except urllib.error.HTTPError as err:
            print("{} ErrorOccured:{}".format(err.code, err.reason))
            existPage = False
        except urllib.error.URLError as err:
            print("{} ErrorOccured:{}".format(err.code, err.reason))
            existPage = False
        except:
            print(sys.exc_info())
            existPage = False
            
    else:
        scrape_obj.is_finished = True
        scrape_obj.finished_at = datetime.datetime.now()
        scrape_obj.save()
