import requests
import lxml.html
from youtube_dl import YoutubeDL

session = requests.session()


def get_client_id():
    page = session.get("https://soundcloud.com")
    tree = lxml.html.fromstring(page.content)
    src_js = tree.xpath('//*/script')

    for i in src_js:
        src = i.get('src')
        if src and 'a-v2.sndcdn.com/assets/app' in src:
            src_js = session.get(src)
            return src_js.text.split('client_id:"')[1].split('",')[0]
    return None


CLIENT_ID = get_client_id()


class SoundCloudCL:
    API_HOST = 'https://api-v2.soundcloud.com'
    API_SEARCH = '%s/search' % API_HOST

    @classmethod
    def search(cls, q, limit=20, offset=0):
        API_SEARCH_QUERY = '%s?linked_partitioning=1&app_locale=en&' \
                           'q=%s&client_id=%s&limit=%s&offset=%s' % (cls.API_SEARCH, q, CLIENT_ID, limit, offset)
        r = session.get(API_SEARCH_QUERY)
        return r.json()

    @classmethod
    def top_50(cls, limit=20, offset=0):
        API_TOP_50 = '{0}/charts?kind=top&genre=soundcloud%3Agenres%3Aall-music&high_tier_only=false&' \
                     'client_id={1}&limit={2}&offset={3}&linked_partitioning=1&app_locale=en'.format(cls.API_HOST,
                                                                                                     CLIENT_ID,
                                                                                                     limit, offset)
        return session.get(API_TOP_50).json()

    @classmethod
    def song(cls, permalink_url):
        y = YoutubeDL({
            'format': 'best',
        })
        return y.extract_info(permalink_url, download=False)
