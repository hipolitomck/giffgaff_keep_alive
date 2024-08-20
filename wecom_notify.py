# wecom_notify.py

import sys
import requests

# 企业微信配置
class WeComConfig:
    CORPID = "your_corpid"  # 替换为你的企业ID
    AGENTID = "your_agentid"  # 替换为你的企业应用ID
    CORPSECRET = "your_corpsecret"  # 替换为你的企业应用凭证密钥
    TOUSER = "@all"  # 默认@all发送给所有成员，你也可以指定具体用户
    MEDIA_ID = ""  # 可选：媒体文件ID，不填则发送文本消息

class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin"

    def get_access_token(self):
        """获取访问令牌"""
        url = f"{self.base_url}/gettoken"
        params = {"corpid": self.corpid, "corpsecret": self.corpsecret}
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("errcode") != 0:
            raise Exception(f"获取 access_token 失败: {data.get('errmsg')}")
        return data["access_token"]

    def send_message(self, message, touser=WeComConfig.TOUSER, msgtype="text"):
        """发送消息（文本或图文）"""
        url = f"{self.base_url}/message/send?access_token={self.get_access_token()}"
        data = {
            "touser": touser,
            "msgtype": msgtype,
            "agentid": self.agentid,
        }

        if msgtype == "text":
            data["text"] = {"content": message}
        elif msgtype == "mpnews":
            title, content = message
            data["mpnews"] = {
                "articles": [{
                    "title": title,
                    "thumb_media_id": WeComConfig.MEDIA_ID,
                    "content": content.replace("\n", "<br/>"),
                    "digest": content,
                }]
            }

        response = requests.post(url, json=data)
        result = response.json()
        if result.get("errcode") != 0:
            raise Exception(f"发送消息失败: {result.get('errmsg')}")
        return "ok"

def wecom_app(title: str, content: str):
    """主函数：发送企业微信消息"""
    wx = WeCom(WeComConfig.CORPID, WeComConfig.CORPSECRET, WeComConfig.AGENTID)
    message = (title, content) if WeComConfig.MEDIA_ID else f"{title}\n{content}"
    msgtype = "mpnews" if WeComConfig.MEDIA_ID else "text"
    
    try:
        wx.send_message(message, WeComConfig.TOUSER, msgtype)
        print("推送成功!")
    except Exception as e:
        print(f"推送失败: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wecom_notify.py <title> <content>")
        sys.exit(1)
    
    title, content = sys.argv[1], sys.argv[2]
    wecom_app(title, content)
