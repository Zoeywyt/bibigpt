import aiohttp
import asyncio
import os
import re

def sanitize_filename(filename):
    """清理文件名中的非法字符"""
    return re.sub(r'[\\/*?:"<>|]', '', filename)

class SubtitleDownload:
    def __init__(self, headers, bvid):
        self.headers = headers
        self.bvid = bvid

    async def fetch_pagelist(self):
        async with aiohttp.ClientSession() as session:
            pagelist_api = f"https://api.bilibili.com/x/player/pagelist?bvid={self.bvid}"
            async with session.get(pagelist_api, headers=self.headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data['data']

    async def fetch_subtitle_list(self, cid):
        async with aiohttp.ClientSession() as session:
            subtitle_api = "https://api.bilibili.com/x/player/v2"
            params = {'bvid': self.bvid, 'cid': cid}
            async with session.get(subtitle_api, params=params, headers=self.headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data['data']['subtitle']['subtitles']

    async def download_subtitle(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data['body']

async def save_subtitle(content, filename):
    """保存字幕到文件"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join([item['content'] for item in content]))

async def main():
    headers = {
       'authority': 'api.bilibili.com',
       'accept': 'application/json, text/plain, */*',
'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'origin': 'https://www.bilibili.com',
'referer': 'https://www.bilibili.com/',
'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
 'AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/119.0.0.0 Safari/537.36'),
'cookie': "buvid3=766C0764-31D4-714C-461F-2E0CD45687E331382infoc; b_nut=1709811031; CURRENT_FNVAL=4048; _uuid=981456EC-89108-821E-B857-CDCF4C51D59B31618infoc; buvid4=086D5D47-E1FB-A9C0-6031-B39AB24660EC32226-024030711-yrJl6DDziHwZ0SdVgQAQ1Q%3D%3D; buvid_fp=395526f27bb7ca8e1d7d53a2892fb4c3; rpdid=|(um~u)~Ju||0J'u~|m)uu|JJ; DedeUserID=3546619685374821; DedeUserID__ckMd5=0ba71023014508ad; b_lsid=2F35E6410_18E6D4C16DF; bsource=search_bing; enable_web_push=DISABLE; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=5; browser_resolution=1638-873; SESSDATA=63ed3dd9%2C1726782691%2Cd9c8c%2A31CjB4EaZxJXWeaIJNz8EDdWfenHz6O67mWIu1F8EePqmEFY1rGxj-5bP9aPtoYZELQDISVnhfSG5pR3c1YWN2a1czZ1NjRmJ6M0JNZFZPaU9mMEpEUEJjVDkwcFg4ZEU2Y29qY2h4MGxuMndoQV9SWWZ5ZVV4cHFkMjczMWxfMTBSR01FVlhSVFVBIIEC; bili_jct=0745cd51ac3c2f9529deeffa45020e7e; sid=7zt594o6; bp_video_offset_3546619685374821=912081170546556935", # ... (same as before)
    }
    print("请输入 Bilibili 视频的 BV 号码：")
    bvid = input().strip()
    subtitle_downloader = SubtitleDownload(headers, bvid)

    try:
        pagelist = await subtitle_downloader.fetch_pagelist()
        for item in pagelist:
            print(f"正在下载《{item['part']}》的字幕...")
            cid = item['cid']
            subtitles_list = await subtitle_downloader.fetch_subtitle_list(cid)
            for subtitle in subtitles_list:
                if subtitle['lan'] == 'zh-Hans':  # 假设中文的lan字段是这个
                    subtitle_url = f"https:{subtitle['subtitle_url']}"
                    subtitle_content = await subtitle_downloader.download_subtitle(subtitle_url)
                    filename = f"database/subtitles/{sanitize_filename(item['part'])}.txt"
                    await save_subtitle(subtitle_content, filename)
                    print(f"已保存：{filename}")
                    break  # 找到中文字幕后停止该集的字幕搜索

    except Exception as e:
        print(f"发生错误：{e}")

asyncio.run(main())

