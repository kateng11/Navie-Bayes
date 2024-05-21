import joblib
import requests
from database.models import Douyin
from model.TrainModel import tokenize

cookie = 'passport_csrf_token=0e24f80a41ecba8ee033771dfb87f0b3; passport_csrf_token_default=0e24f80a41ecba8ee033771dfb87f0b3; bd_ticket_guard_client_web_domain=2; passport_assist_user=CkFLZ9gDT1KR9ba79rx6bAkJL91H_xRRfdIf9ijbdRiU_gjkkDmkMICA7HjX68k_DCoN6j4Sl-XVqYMTshDa1KBV-xpKCjzQJy_voqpRPjMCVv-b5qviZ9j81VUHC09JFB0V501tF7BCNxuy5k-1NU2K87uCfPPaVVC4coTlY5nphGEQoILLDRiJr9ZUIAEiAQOHdyuT; n_mh=4IKlPjPvnD0kmeI6H_ZzlNDLDGssOtSRnjCOV-lYNLI; sso_uid_tt=ac84ace5a92c85e154a06af1315f42d9; sso_uid_tt_ss=ac84ace5a92c85e154a06af1315f42d9; toutiao_sso_user=958d3fe9c208eb61561f649485f87e5b; toutiao_sso_user_ss=958d3fe9c208eb61561f649485f87e5b; LOGIN_STATUS=1; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=f1d5d01dac480c2e0f4e13816a729e76; __security_server_data_status=1; store-region=cn-ah; store-region-src=uid; sid_ucp_v1=1.0.0-KGE5YTk1Y2FiYzU2MTVlODdiODVjZTZmMzAzZjE4MGM3ZWYwMzk0ZjIKGwj47dDt5PTHBBCCjJWvBhjvMSAMOAZA9AdIBBoCaGwiIGQwZTJhMTdlMTQ1NGYzNGU2NDhhMDBhNTQwZGQwMzdl; ssid_ucp_v1=1.0.0-KGE5YTk1Y2FiYzU2MTVlODdiODVjZTZmMzAzZjE4MGM3ZWYwMzk0ZjIKGwj47dDt5PTHBBCCjJWvBhjvMSAMOAZA9AdIBBoCaGwiIGQwZTJhMTdlMTQ1NGYzNGU2NDhhMDBhNTQwZGQwMzdl; ttwid=1%7CNi_EwgvXLYYLRghCuvy9a9POCunBlaedIbEsJzCNSos%7C1709558725%7C645640280ff55576253c2a0d4bf003ac2c288bbb18587a1cb8b9199f3cf88bfc; dy_swidth=1536; dy_sheight=864; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A1%7D; publish_badge_show_info=%220%2C0%2C0%2C1713348964657%22; sid_ucp_sso_v1=1.0.0-KDlmYTc1MmNjMGJmZmNiYWM2ZTk0MjdjZTVhYzUzNDBkOGFmYWM4NWMKHwj47dDt5PTHBBDlwv6wBhjvMSAMMPW4k_sFOAZA9AcaAmxxIiA5NThkM2ZlOWMyMDhlYjYxNTYxZjY0OTQ4NWY4N2U1Yg; ssid_ucp_sso_v1=1.0.0-KDlmYTc1MmNjMGJmZmNiYWM2ZTk0MjdjZTVhYzUzNDBkOGFmYWM4NWMKHwj47dDt5PTHBBDlwv6wBhjvMSAMMPW4k_sFOAZA9AcaAmxxIiA5NThkM2ZlOWMyMDhlYjYxNTYxZjY0OTQ4NWY4N2U1Yg; sid_guard=958d3fe9c208eb61561f649485f87e5b%7C1713348965%7C5184001%7CSun%2C+16-Jun-2024+10%3A16%3A06+GMT; uid_tt=ac84ace5a92c85e154a06af1315f42d9; uid_tt_ss=ac84ace5a92c85e154a06af1315f42d9; sid_tt=958d3fe9c208eb61561f649485f87e5b; sessionid=958d3fe9c208eb61561f649485f87e5b; sessionid_ss=958d3fe9c208eb61561f649485f87e5b; SEARCH_RESULT_LIST_TYPE=%22single%22; WallpaperGuide=%7B%22showTime%22%3A1713353403930%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A7%2C%22cursor2%22%3A0%7D; download_guide=%222%2F20240417%2F0%22; pwa2=%220%7C0%7C2%7C0%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __ac_signature=_02B4Z6wo00f010y3itwAAIDDut6D-yGvBR9Ml45AALUY7fDF0bRK3WPYxctv6NWIz8Hdav0SjLfmDC5fNso8I5F7pSBR45oZDrqJhf3iENJsY-1SFpur4RAX743ZeCr2NbxXmo1Vx8UWaRzTd4; csrf_session_id=4f903ac33162368d326f178bdf63d452; strategyABtestKey=%221713406257.411%22; _waftokenid=eyJ2Ijp7ImEiOiJHdlVxRzdXc3Z1MitjdVNNakNZbjFmK0JzeHpkQW5qbGxrMUFtRUhDWnNBPSIsImIiOjE3MTM0MTA1MzcsImMiOiJpMHZqVzVCbXVJcmVCYUluMWJJV2VZTHJTem83djBERGtMemlURFFwNWRJPSJ9LCJzIjoibFRxN2lsNHU3RmhoaDZDaFBGZERlbk41YmtqN0w5VUw2cHlaN2lkeGE4WT0ifQ; douyin.com; xg_device_score=6.758185374092299; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAnl0AcxQNM-47NKNKyifgpfb1CmSNmIKOHBKCaAReNGHush33Edat3nPjG5-NXAEt%2F1713456000000%2F0%2F0%2F1713411740045%22; xgplayer_device_id=84736140868; xgplayer_user_id=314980815919; odin_tt=556d51de2a8d0a2473f617f284071bb313597d69393ad704fb5ba937e2aecfdef4858fbf8dbdbfee98dd058e2f2abf117d5c6bc7b935d1db40727dc45e4818ec; msToken=TJa2ZIA5GxUxvEjXr7kAECMHiwyIXil49_WL7gm3OMANdp60P-mxOc4yuM58OK2vVuBKHHum1Yx7IS-0D4hGA2mlcB9cYqnAScEioiN0ThRdFNGgRAuhF4zNI86r; IsDouyinActive=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A6.6%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A300%7D%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS0dDZDRYdUZQQThTYVAyRXFhS1lxZGt6VDN0TGdITVJTaWo2aWp3dFIrZnIwZXJaRGR0SzhINysrQWhrS1ErRWtUSGt4bExEeldwUURLTi91NEl4RFU9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; passport_fe_beating_status=true; home_can_add_dy_2_desktop=%221%22'
root_headers = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    'Cookie': cookie
}
naive_bayes = joblib.load('file/naive_bayes_model.pkl')
tfidf_vectorizer = joblib.load('file/tfidf_vectorizer.pkl')


def get_keypage(keyword,page):
    params = {
        'aid': 6383,
        'channel': 'channel_pc_web',
        'search_channel': 'aweme_video_web',
        'keyword': keyword,
        'offset': 20,
        'publish_time': 0,
        'sort_type': 0,
        'is_filter_search': 0,
        'count': page
    }
    url = 'https://www.douyin.com/aweme/v1/web/search/item/'
    try:
        resp = requests.get(url, headers=root_headers, params=params)
        resp.encoding = 'utf-8'
        items = resp.json()['data']
        for item in items:
            process_item(item,keyword)
    except Exception as e:
        print(f"Failed to fetch or process data: {e}")


def process_item(item,keyword):
    aweme_id = item['aweme_info']['aweme_id']
    vedioname = item['aweme_info']['desc']
    comments_count = item['aweme_info']['statistics']['comment_count']
    url2 = item['aweme_info']['share_info']['share_url']
    get_comments(aweme_id, vedioname, url2, comments_count,keyword)


def get_comments(aweme_id, vedioname, url2, data_count,keyword):
    pages = data_count / 50
    if pages >= 10:
        pages = 10
    i = 0
    while i < pages:
        params = {
            'aid': 6383,
            'cursor': i,
            'aweme_id': aweme_id,
            'count': 50,
        }
        i = i + 1
        url = 'https://www.douyin.com/aweme/v1/web/comment/list'
        try:
            resp = requests.get(url, headers=root_headers, params=params)
            resp.encoding = 'utf-8'
            comments = resp.json()['comments']
            if comments is None:
                print("数据未获取")
            else:
                for comment in comments:
                    username = comment["user"]["nickname"]
                    text = comment["text"]
                    sentiment = predict_sentiment(text)
                    save_comment(username, text, vedioname, url2, sentiment,keyword)
        except Exception as e:
            print(f"Failed to fetch or process comments: {e}")


def save_comment(username, text, vedioname, url2, sentiment_label,keyword):
    try:
        obj = Douyin(
            username=username,
            comment=text,
            vedioname=vedioname,
            url=url2,
            keyword=keyword,
            labels=sentiment_label
        )
        obj.save()
    except Exception as e:
        print(f"Failed to save data: {e}")


def predict_sentiment(text):
    # 分词处理
    tokenized_text = tokenize(text)
    # 转换为TF-IDF向量
    text_tfidf = tfidf_vectorizer.transform([tokenized_text])
    # 进行情感预测
    prediction = naive_bayes.predict(text_tfidf)[0]
    # 将预测结果转换为积极或消极的字符串
    sentiment = "正面情绪" if prediction == 1 else "负面情绪"
    return sentiment
