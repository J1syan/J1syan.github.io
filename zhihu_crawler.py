#!/usr/bin/env python3
"""
知乎用户文章爬虫
功能：爬取指定知乎用户的全部文章，保存为 Markdown 格式，图片下载到本地
使用网页抓取方式获取完整内容
"""

import os
import re
import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime

# 禁用代理，避免 SOCKS 依赖问题
for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(var, None)


# ================= 配置区 =================

# 知乎 Cookie
ZHIHU_COOKIE = "__snaker__id=ZJRV8UMlnPK0QteD; SESSIONID=YUQjrhFGAT8S3OKmoX1c3kz4R1OKd6B4tXFrKrSmGSb; JOID=UFkXBEM0crWB9CzEMi9MYalsfDopUxTD-6t5gGV7JcHAtUmBdXJvTO39LMI4Dz4LTKZIiR9LfFeggbEVQTjL28Q=; osd=UFsWAkI0cLSH9SzGMylNYattejspURXF-qt7gWN6JcPBs0iBd3NpTe3_LcQ5DzwKSqdIix5NfVeigLcUQTrK3cU=; _xsrf=82vOGPGys4OVGAcVtLvRJ9Kjte8EjV3i; _zap=8c098428-a6c5-430a-a11b-abacf5eaa9f4; d_c0=_ERUJi2m8RuPTvxnwcMaSnyce2N7Jq3ocK4=|1772853266; gdxidpyhxdE=n6h%2B1mAz88Rfsy%2Fz4fD9DVw4dzt74An%5CX11OCE1%2FVwGCdv1yShtJLn7fu1UmvDJ14VQUBI%2B%5CG6cPuVdN%2Fm1i32VgxzK1vQcwLfDL%2BrlWHTZaUiyV4s1CSrXmnEVU5pngSUizWj2OjKu0b%2FMWuQzijXy9WciVjv0UN1G4CpwokODRZxfI%3A1775902699022; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1776684670,1776847003,1777081734,1777538902; HMACCOUNT=CA6B83D4B6239E56; capsion_ticket=2|1:0|10:1777538943|14:capsion_ticket|44:MzE3OGFlZjc3NTVmNGUxOGExNzgzNGI2OTFlZWNmYmI=|e2100a05d639d9c33cc9b13c92199aae590e4889fa553afbaca182736f011162; __zse_ck=005_Xy6NPGK1S0KFdcrbTKhcPx/lEBoV6y2DVhhcjam3AMDN4W=rsZhqQY/z3m6d40T/Vew5v4GN=ZTYkZTnNehzjRVedv4CSkvyt9tGjUaZXeM0H4UNtl4qEU8c0W01xfbQ-eh6VkshIDamFJTls8MGOFvOBSlTl0TWdjwel5H6/fRDBPg9XTMpAEKwYCqnXkH8F63LywaBYtLng90lXpOubG+Y7p+L2ijFr7djuOESM7h4zz5Xz65lFHYFz0/RICpCO; captcha_session_v2=2|1:0|10:1777538982|18:captcha_session_v2|88:U1d3RW9CK1d2U053UHRFQmxHcC9EdmZQbXpwQjI1ZHVxOFlMdk93YlpkQ2g1b3B3WEozWTJtZ2tXV0JRcy82Wg==|dc5d1f3b068e98a7b3c306957ab4f939764b17120386a075743f7e9e6d95b738; z_c0=2|1:0|10:1777539007|4:z_c0|92:Mi4xMkppS0JRQUFBQUQ4UkZRbUxhYnhHeVlBQUFCZ0FsVk5zbVhnYWdBdktIX0V5SnBFdjh2OVl3SGUtTFhxYzhYbXRR|982621088cd8c015489a26a5eaea30d2c088fd57dc59f525987b9952e2a4dee5; SESSIONID=desuUVGRETwDNoFD0VimWvmQKFR5PfPMNFAodIjk2o7; JOID=UFARCkp-nlSf4x6ZaWughrB0QGd0EPcq4rVC0jY4wC_WpXLVIbiIov3qGJhsRLSn8MUnaO8s0SesCMdRqzeSNrk=; osd=VVAQAE17nlWV5BuZaGGng7B1SmBxEPYg5bBC0zw_xS_Xr3XQIbmCpfjqGZJrQbSm-sIiaO4m1iKsCc1WrjeTPL4=; BEC=7aabe613cb4d97a48eb82ad02e0db63f; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1777539910"

# 知乎用户名
ZHIHU_USERNAME = "samge-ge-43"

# 保存路径
BASE_DIR = Path("/home/j1syan/Documents") / ZHIHU_USERNAME

# 图片保存目录
IMAGES_DIR = BASE_DIR / "images"

# 请求延迟（秒）
REQUEST_DELAY = 15  # 文章之间的延迟

# 最小内容长度
MIN_CONTENT_LENGTH = 800

# 最大重试次数
MAX_RETRIES = 5

# 重试延迟（秒）- 逐步递增
RETRY_DELAYS = [30, 60, 90, 120, 180]

# ================= 工具函数 =================

def get_headers(referer=None):
    """获取请求头"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Cookie": ZHIHU_COOKIE,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    if referer:
        headers["Referer"] = referer
    return headers


def get_api_headers(referer=None):
    """获取 API 请求头"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Cookie": ZHIHU_COOKIE,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    if referer:
        headers["Referer"] = referer
    return headers


session = requests.Session()


def fetch_article_ids(url_token):
    """分页获取用户文章 ID 列表"""
    articles = []
    offset = 0

    while True:
        url = f"https://www.zhihu.com/api/v4/members/{url_token}/articles"
        params = {
            "include": "data[*].comment_count,suggest_is_edit,follower_count",
            "offset": offset,
            "limit": 20,
        }

        print(f"正在获取文章列表，偏移量: {offset}...")
        resp = session.get(url, headers=get_api_headers(), params=params)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("data", [])
        if not items:
            break

        for item in items:
            articles.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "url": item.get("url"),
            })

        print(f"已获取 {len(items)} 篇文章 ID，总计 {len(articles)} 篇")

        paging = data.get("paging", {})
        if not paging.get("is_end", False):
            offset += 20
            time.sleep(REQUEST_DELAY)
        else:
            break

        if len(articles) >= 500:
            print("已达到单次最大获取数量 500 篇")
            break

    return articles


def fetch_article_content(article_id, retries=MAX_RETRIES):
    """通过网页获取文章完整内容，带重试机制"""
    url = f"https://zhuanlan.zhihu.com/p/{article_id}"
    
    for attempt in range(retries):
        try:
            print(f"  正在获取文章详情 (尝试 {attempt + 1}/{retries})")
            
            # 每次重试创建新的 Session
            current_session = requests.Session()
            
            resp = current_session.get(url, headers=get_headers(referer=url), timeout=30)
            resp.raise_for_status()

            match = re.search(r'<script id="js-initialData"[^>]*>(.*?)</script>', resp.text, re.DOTALL)
            if not match:
                print(f"  警告: 未找到 initialData")
                if attempt < retries - 1:
                    wait_time = RETRY_DELAYS[attempt] if attempt < len(RETRY_DELAYS) else 180
                    print(f"  等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                return None

            data = json.loads(match.group(1))
            
            entities = data.get('initialState', {}).get('entities', {}).get('articles', {})
            if not entities:
                print(f"  警告: 未找到 articles 实体")
                if attempt < retries - 1:
                    wait_time = RETRY_DELAYS[attempt] if attempt < len(RETRY_DELAYS) else 180
                    print(f"  等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                return None

            article_key = list(entities.keys())[0]
            article_data = entities[article_key]

            content = article_data.get("content", "")
            
            # 检查内容完整性
            is_complete, reason = check_content_completeness(content)
            if not is_complete:
                print(f"  警告: {reason}")
                if attempt < retries - 1:
                    wait_time = RETRY_DELAYS[attempt] if attempt < len(RETRY_DELAYS) else 180
                    print(f"  等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue

            return {
                "title": article_data.get("title", ""),
                "content": content,
                "created": article_data.get("created", 0),
                "excerpt": article_data.get("excerpt", ""),
            }
        except Exception as e:
            print(f"  获取文章详情失败: {e}")
            if attempt < retries - 1:
                wait_time = RETRY_DELAYS[attempt] if attempt < len(RETRY_DELAYS) else 180
                print(f"  等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                continue
            return None
    
    return None


def check_content_completeness(content):
    """检查文章内容是否完整"""
    if not content:
        return False, "内容为空"
    
    if len(content) < MIN_CONTENT_LENGTH:
        return False, f"内容过短 ({len(content)} < {MIN_CONTENT_LENGTH})"
    
    # 检查末尾是否有完整的 HTML 结构
    last_200 = content[-200:]
    
    # 应该有 HTML 闭合标签
    has_closing_tag = any(tag in last_200 for tag in ['</p>', '</blockquote>', '</li>', '</h2>', '</h3>', '</code>', '</pre>', '</ul>', '</ol>'])
    
    # 或者以中文标点结尾（句号等）
    has_sentence_end = any(p in last_200 for p in ['。</p>', '。</blockquote>', '！</p>', '？</p>'])
    
    # 或者以代码块闭合标签结尾
    has_code_end = '</code>' in last_200 or '</pre>' in last_200
    
    if not (has_closing_tag or has_sentence_end or has_code_end):
        # 检查未闭合的 HTML 标签数量
        open_tags = len(re.findall(r'<(?!/)[a-z]+[^>]*>', content, re.IGNORECASE))
        close_tags = len(re.findall(r'</[a-z]+>', content, re.IGNORECASE))
        if open_tags - close_tags > 3:  # 超过 3 个标签未闭合
            return False, f"HTML 标签未闭合 ({open_tags - close_tags} 个)"
    
    return True, "内容完整"


def download_image(url, article_title, idx):
    """下载单张图片"""
    try:
        safe_title = re.sub(r'[\\/*?:"<>|]', "", article_title)[:50]
        safe_title = re.sub(r'\s+', '_', safe_title)
        
        ext = ".jpg"
        url_path = url.split("?")[0]
        if "." in url_path:
            ext = "." + url_path.split(".")[-1].lower()
            if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"):
                ext = ".jpg"

        filename = f"{safe_title}_{idx}{ext}"
        filepath = IMAGES_DIR / filename

        if filepath.exists():
            return f"images/{filename}"

        img_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.zhihu.com/",
        }
        
        resp = session.get(url, headers=img_headers, timeout=30)
        resp.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(resp.content)

        return f"images/{filename}"
    except Exception as e:
        print(f"    下载图片失败: {e}")
        return url


def html_to_markdown(html_content, article_title):
    """将知乎的 HTML 内容转换为 Markdown"""
    if not html_content:
        return ""

    md_parts = []
    image_idx = 0

    for match in re.finditer(r'<h2[^>]*>(.*?)</h2>', html_content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text:
            md_parts.append(f"## {text}")

    for match in re.finditer(r'<h3[^>]*>(.*?)</h3>', html_content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text:
            md_parts.append(f"### {text}")

    img_pattern = r'<img[^>]+data-original="([^"]+)"[^>]*>'
    for match in re.finditer(img_pattern, html_content):
        img_url = match.group(1)
        # 尝试获取图片描述
        alt_match = re.search(r'data-caption="([^"]*)"', match.group(0))
        if not alt_match:
            alt_match = re.search(r'alt="([^"]*)"', match.group(0))
        alt = alt_match.group(1) if alt_match else ""
        
        local_path = download_image(img_url, article_title, image_idx)
        if alt:
            md_parts.append(f"![{alt}]({local_path})")
        else:
            md_parts.append(f"![]({local_path})")
        image_idx += 1
    
    # 如果没找到图片，尝试备用模式
    if image_idx == 0:
        img_pattern2 = r'<img[^>]+src="([^"]+)"[^>]*>'
        for match in re.finditer(img_pattern2, html_content):
            img_url = match.group(1)
            # 跳过小图标
            if '_1440w.jpg' in img_url or '_r.jpg' in img_url:
                alt_match = re.search(r'data-caption="([^"]*)"', match.group(0))
                if not alt_match:
                    alt_match = re.search(r'alt="([^"]*)"', match.group(0))
                alt = alt_match.group(1) if alt_match else ""
                
                local_path = download_image(img_url, article_title, image_idx)
                if alt:
                    md_parts.append(f"![{alt}]({local_path})")
                else:
                    md_parts.append(f"![]({local_path})")
                image_idx += 1

    blockquote_pattern = r'<blockquote[^>]*>(.*?)</blockquote>'
    for match in re.finditer(blockquote_pattern, html_content, re.DOTALL):
        content = match.group(1)
        text = re.sub(r'<[^>]+>', '', content).strip()
        if text:
            for line in text.split("\n"):
                md_parts.append(f"> {line.strip()}")
            md_parts.append("")

    p_pattern = r'<p[^>]*>(.*?)</p>'
    for match in re.finditer(p_pattern, html_content, re.DOTALL):
        content = match.group(1)
        
        if re.match(r'^\s*<img', content.strip()):
            continue
        
        content = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
        content = re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', r'**\1**', content)
        content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content)
        text = re.sub(r'<[^>]+>', '', content).strip()
        
        if text:
            md_parts.append(text)
            md_parts.append("")

    li_pattern = r'<li[^>]*>(.*?)</li>'
    for match in re.finditer(li_pattern, html_content, re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text:
            md_parts.append(f"- {text}")

    if len(md_parts) < 2:
        clean_text = re.sub(r'<[^>]+>', '', html_content).strip()
        if clean_text:
            md_parts.append(clean_text)

    return "\n".join(md_parts)


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.strip()
    name = re.sub(r'\s+', '_', name)
    if len(name) > 100:
        name = name[:100]
    return name


def save_article(article_id, article_info):
    """获取并保存单篇文章"""
    title = article_info.get("title", "无标题")
    print(f"\n正在处理: {title}")

    detail = fetch_article_content(article_id)
    if not detail:
        print(f"  跳过: 无法获取完整内容")
        return False

    content = detail.get("content", "")
    created_time = detail.get("created", 0)
    excerpt = detail.get("excerpt", "")
    title = detail.get("title", title)

    pub_date = datetime.fromtimestamp(created_time).strftime("%Y-%m-%d") if created_time else "unknown"

    md_content = html_to_markdown(content, title)

    md_header = f"""---
title: "{title}"
date: {pub_date}
tags: []
category: "知乎"
source: "https://www.zhihu.com/p/{article_id}"
excerpt: "{excerpt}"
---

"""

    full_md = md_header + md_content

    filename = sanitize_filename(f"{pub_date}_{title}")
    if not filename.endswith(".md"):
        filename += ".md"

    filepath = BASE_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_md)

    print(f"  已保存: {filepath}")
    print(f"  原始 HTML 长度: {len(content)} 字符")
    print(f"  Markdown 长度: {len(md_content)} 字符")
    
    time.sleep(REQUEST_DELAY)
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("知乎文章爬虫")
    print("=" * 60)

    BASE_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"保存路径: {BASE_DIR}")
    print(f"图片路径: {IMAGES_DIR}")
    print()

    print("正在获取用户信息...")
    try:
        url = f"https://www.zhihu.com/api/v4/members/{ZHIHU_USERNAME}"
        resp = session.get(url, headers=get_api_headers())
        resp.raise_for_status()
        user_data = resp.json()
        user_name = user_data.get("name", ZHIHU_USERNAME)
        print(f"用户名: {user_name}")
        print(f"URL Token: {ZHIHU_USERNAME}")
    except Exception as e:
        print(f"获取用户信息失败: {e}")
        sys.exit(1)

    print()

    print("开始获取文章列表...")
    try:
        articles = fetch_article_ids(ZHIHU_USERNAME)
    except Exception as e:
        print(f"获取文章列表失败: {e}")
        sys.exit(1)

    print(f"\n共找到 {len(articles)} 篇文章")
    print()

    if not articles:
        print("没有找到任何文章，退出")
        return

    print("开始保存文章...")
    success_count = 0
    fail_count = 0

    for i, article in enumerate(articles, 1):
        try:
            print(f"\n[{i}/{len(articles)}]")
            if save_article(article["id"], article):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"保存文章失败: {article.get('title', '未知')} - {e}")
            fail_count += 1
            time.sleep(REQUEST_DELAY)

    print("\n" + "=" * 60)
    print("爬取完成!")
    print(f"成功: {success_count} 篇")
    print(f"失败: {fail_count} 篇")
    print(f"保存路径: {BASE_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
