import requests,time,pandas,datetime,json
from bs4 import BeautifulSoup
import sys


'''
變數與常數
'''
from dotenv import load_dotenv
import os
load_dotenv()

# 目標網址
BASE_URL = 'https://www.ptt.cc/bbs/'

# 目標頁面
TARGET_PAGE = '/index'


# 目標頁面的頁面的附屬檔名
HTML_EXT = '.html'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

'''
執行參數
'''

# 目標看板
target_board = 'Stock'

# 目標頁面的頁數
page_num = ''

# 合併完整路徑
target = BASE_URL + target_board + TARGET_PAGE + page_num + HTML_EXT


def download_html(target, headers=HEADERS):
 
    data = requests.get(target, headers=headers)
    return data


def get_article_url(html_code):
    url_list = []
    html_parser = BeautifulSoup(html_code.content)
    div_list = html_parser.find_all('div', class_="title")

    for div_ in div_list:
      try:
        a_tag = div_.find('a').attrs['href']
        url_list.append(a_tag)
        print(a_tag)
      except:
        print(None)
    return url_list


# 讀取各文章資料
def parser_article_content(url_list):
    article_base_url = BASE_URL.replace('/bbs/', '')
    ptt_data = []


    for url_ in url_list:
        if url_ != None:
            article_url = article_base_url + url_
            page_data = download_html(article_url)
            page_html_code = BeautifulSoup(page_data.content)
            meta_info = page_html_code.find_all('span', class_='article-meta-value')
            author = meta_info[0].contents[0]
            title = meta_info[2].contents[0]
            date = meta_info[3].contents[0]
            article = page_html_code.find('div', id = 'main-content').contents[4]


            # 建立字典型態
            article_row = {
                'url': article_url,
                'title': title,
                'author': author,
                'date': date,
                'content': article
            }


            # 加入 list 內
            ptt_data.append(article_row)
            # 暫停
            time.sleep(0.5)
    return ptt_data



# 儲存為 json 或 csv
def save_result(data, format = 'csv'):
    data_df = pandas.DataFrame(data)
    if format == 'json':
        data_df.to_json('data-{}.json'.format(get_datetime_str()))
    elif format == 'csv':
        data_df.to_csv('data-{}.csv'.format(get_datetime_str()))
    elif format == 'excel':
        data_df.to_excel('data-{}.xlsx'.format(get_datetime_str()))
    else:
        data_df.to_json('data-{}.json'.format(get_datetime_str()))
    return True


def get_datetime_str():
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    return now.strftime('%Y%m%d-%H%M%S')

'''
Test
'''

def send_line_notify(msg = "傳送訊息"):
    line_notify_url = "https://notify-api.line.me/api/notify"
    line_notify_token = os.getenv("Token")

    #Line Auth Header
    line_notify_header = {
        'Authorization': 'Bearer {}'.format(line_notify_token)
    }


    # Line Message
    line_notify_body = {
        'message': msg
    }


    res = requests.post(line_notify_url, headers= line_notify_header, data = line_notify_body)
    res_msg = json.loads(res.text)


    return res_msg['status']

'''
Test
'''
# x = download_html(target)
# y = get_article_url(x)
# z = parser_article_content(y)
# save_result(z,'excel')
# # print(z)
send_line_notify("Test")


# 爬蟲主程式
def main():
    if len(sys.argv) < 2:
        print("缺少參數: 爬蟲目標看板")
        sys.exit()
    elif len(sys.argv) == 2:
        print("未指定看版目標頁數，因此爬取最新資訊")
        page_num = ""
    else:
        page_num = sys.argv[2]

    target_board = sys.argv[1]
    # 合併完整路徑
    target = BASE_URL + target_board + TARGET_PAGE + page_num + HTML_EXT
    board_info = download_html(target)
    article_url_list = get_article_url(board_info)
    article_data = parser_article_content(article_url_list)
    save_result(article_data,'excel')
    send_line_notify("{}: 看板 {} 完成爬蟲".format(get_datetime_str(), target_board))
    print("爬蟲完成")
    return True

# 加入 __main__ 執行區段
if __name__ == '__main__':
    main()