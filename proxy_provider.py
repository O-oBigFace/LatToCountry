p = {
    "proxyHost": "proxy.crawlera.com",
    "proxyPort": "8010",
    "proxyAuth": "4181f1829ce5445eb9ce3fdf1ffe507a:"
}

proxy_auth = p['proxyHost']
proxy_host = p['proxyHost']
proxy_port = p['proxyPort']


def get_proxy():
    return {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
            "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
    # return {'http': 'socks5://127.0.0.1', 'https': 'socks5://127.0.0.1'}