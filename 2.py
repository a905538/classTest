# coding: utf-8
import requests
import pandas as pd
import datetime as dt
import json

url = "https://api.cnyes.com/media/api/v1/newslist/category/headline"  # 新聞連結
data = []

payload = {
    "page": 1,
    "limit": 100,
    "isCategoryHeadline": 1,
    "startAt": int((dt.datetime.today() - dt.timedelta(days=10)).timestamp()),
    "endAt": int(dt.datetime.today().timestamp()),
}

# 抓取第1頁
res = requests.get(url, params=payload)
jd = json.loads(res.text)
data.append(pd.DataFrame(jd["items"]["data"]))

# 抓取第2頁以後
for i in range(2, jd["items"]["last_page"] + 1):
    payload["page"] = i  # 修正這行
    res = requests.get(url, params=payload)
    jd = json.loads(res.text)
    data.append(pd.DataFrame(jd["items"]["data"]))

# 合併所有頁面
df = pd.concat(data, ignore_index=True)
df = df[["newsId", "title", "summary"]]  # 取出特定欄位
df["link"] = df["newsId"].apply(lambda x: "https://m.cnyes.com/news/id/" + str(x))  # 建立連結
print(df)
