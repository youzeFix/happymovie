import requests

def get_proxy():
    response = requests.get("http://106.55.169.250:5010/get/").json()
    return response.get("proxy")

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Referer": "https://movie.douban.com/top250",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
}

if __name__ == "__main__":
    url = "https://movie.douban.com/top250?start=25&filter="
    # url = "https://www.baidu.com"
    proxy = get_proxy()
    print("proxy:", proxy)
    # proxy = "125.87.95.242:3256"
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    print(proxies)
    res = requests.get(url, headers=headers, proxies=proxies)

    print(res.status_code)
    print(res.text)

