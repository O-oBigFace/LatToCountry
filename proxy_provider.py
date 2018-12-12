p = {
    "proxyHost": "proxy.crawlera.com",
    "proxyPort": "8010",
    "proxyAuth": "a6f8ba24bb164642994d21d647a6d866:"
}

proxy_auth = p['proxyHost']
proxy_host = p['proxyHost']
proxy_port = p['proxyPort']


def get_proxy():
    # return {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
    #         "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
    return {'http': 'socks5://127.0.0.1', 'https': 'socks5://127.0.0.1'}