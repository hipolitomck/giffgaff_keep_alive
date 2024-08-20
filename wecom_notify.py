# wecom_notify.py

import sys
import requests
import json
from corp_init import Corpid, Agentid, Corpsecret, Touser, Media_id

class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        values = {"corpid": self.CORPID, "corpsecret": self.CORPSECRET}
        req = requests.post(url, params=values)
        return req.json()["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.get_access_token()}"
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": message},
            "safe": "0",
        }
        return requests.post(send_url, json=send_values).json()["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.get_access_token()}"
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [{
                    "title": title,
                    "thumb_media_id": media_id,
                    "content": message.replace("\n", "<br/>"),
                    "digest": message,
                }]
            }
        }
        return requests.post(send_url, json=send_values).json()["errmsg"]

def wecom_app(title: str, content: str):
    wx = WeCom(Corpid, Corpsecret, Agentid)
    response = wx.send_mpnews(title, content, Media_id, Touser) if Media_id else wx.send_text(f"{title}\n{content}", Touser)
    if response != "ok":
        print(f"推送失败: {response}")
    else:
        print("推送成功!")

if __name__ == "__main__":
    title, content = sys.argv[1], sys.argv[2]
    wecom_app(title, content)
