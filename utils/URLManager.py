class UrlManager():
    def __init__(self):
        self.new_urls = set()  # 存储新的url
        self.old_urls = set()  # 存储旧的url

    def add_new_url(self, url):
        if url is None or len(url) == 0:  # 合法性检查，如果url为空则返回
            return
        if url in self.new_urls or url in self.old_urls:  # 如果该url已经在new_urls或者在old_urls中也返回
            return
        self.new_urls.add(url)  # 向set中添加url

    def add_new_urls(self, urls):
        if len(urls) == 0 or urls is None:
            return
        for url in urls:
            self.add_new_url(url)

    def get_url(self):
        if self.has_new_url():  # 如果检测到new_urls中有元素
            url = self.new_urls.pop()  # 将其从new_urls中移除
            self.old_urls.add(url)  # 添加到old_urls中
            return url
        else:
            return None  # 如果new_urls中没有元素，则直接返回

    def has_new_url(self):
        return len(self.new_urls) > 0  # 如果大于0表示还有url


if __name__ == "__main__":
    url_manager = UrlManager()
    urls = ['url1', 'url2']
    url_manager.add_new_url('url1')
    url_manager.add_new_urls(urls)
    print(url_manager.new_urls, url_manager.old_urls)

    print("#" * 30)
    new_url = url_manager.get_url()
    print(url_manager.new_urls, url_manager.old_urls)

    print("#" * 30)
    new_url = url_manager.get_url()
    print(url_manager.new_urls, url_manager.old_urls)

    print("#" * 30)
    print(url_manager.has_new_url())

