import requests
from bs4 import BeautifulSoup
import re

def get_wikipedia_urls(start_url,url_save_path='temp.txt', max_url_num=100):
    """
    使用循环获取维基百科页面的所有 URL
    """
    count = 0 
    # 存储所有已访问过的 URL
    visited_urls = set()

    # 存储待访问的 URL 队列
    queue = [start_url]

    # 存储所有页面的 URL
    all_urls = []

    # 循环直到队列为空
    while queue:
        # 从队列中取出一个 URL
        url = queue.pop(0)

        # 如果 URL 已经访问过，则跳过
        if url in visited_urls:
            continue

        # 发送 HTTP 请求获取页面内容
        try:
            response = requests.get(url)
        except:
            import time
            time.sleep(0.2)
            continue 
        if response.status_code != 200:
            print(f'Failed to fetch URL: {url}')
            continue

        # 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到页面中的所有链接
        links = soup.find_all('a', href=True)

        # 提取维基百科页面的链接
        wiki_links = [link['href'] for link in links if link['href'].startswith('/wiki/')]

        # 添加当前页面到已访问集合中
        visited_urls.add(url)

        # 写入文件
        with open(url_save_path, 'a', encoding="utf-8") as f:
            f.write(f"{url}\n")
                    
        # 添加当前页面的 URL 到结果列表中
        all_urls.append(url)
        if len(all_urls) > max_url_num:
            break
        print(count, url)
        count += 1
                
        # 将新发现的链接添加到队列中
        for link in wiki_links:
            full_link = f'https://zh.wikipedia.org{link}'
            if full_link not in visited_urls and full_link not in queue:
                queue.append(full_link)

    return all_urls

if __name__ == '__main__':
    # 维基百科主页的 URL
    # start_url = 'https://zh.wikipedia.org/wiki/Main_Page'

    # start_url = 'https://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95'
    start_url = 'https://zh.wikipedia.org/wiki/%E6%8B%94%E7%BD%90'
    
    max_url_num = 10000
    url_save_path = f'all_url_{max_url_num}.txt'

    # 获取所有页面的 URL
    all_urls = get_wikipedia_urls(start_url, url_save_path, max_url_num=max_url_num)

    # 可以删除写入，因为已经一遍爬虫一遍写入
    with open("all_url_10000.txt", "w", encoding="utf-8") as file:
        for item in all_urls:
            file.write(f"{item}\n")

    # # 打印所有获取到的 URL
    # for url in all_urls:
    #     print(url)
