"""
测试从豆瓣电影页面提取信息
"""
import requests
from bs4 import BeautifulSoup
import json
import re


def extract_info_from_html(html_content):
    """
    从豆瓣HTML页面提取信息
    
    Args:
        html_content: HTML内容
        
    Returns:
        提取的信息字典
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    info = {}
    
    # 1. 提取标题
    title_tag = soup.find('span', property='v:itemreviewed')
    info['title'] = title_tag.get_text().strip() if title_tag else ''
    
    # 2. 提取年份
    year_tag = soup.find('span', class_='year')
    if year_tag:
        year_text = year_tag.get_text().strip()
        # 从 "(2012)" 中提取 "2012"
        year_match = re.search(r'(\d{4})', year_text)
        info['year'] = year_match.group(1) if year_match else ''
    else:
        info['year'] = ''
    
    # 3. 提取评分
    rating_tag = soup.find('strong', class_='ll rating_num', property='v:average')
    info['rating'] = float(rating_tag.get_text().strip()) if rating_tag else 0.0
    
    # 4. 提取评分人数
    votes_tag = soup.find('span', property='v:votes')
    info['votes'] = int(votes_tag.get_text().strip()) if votes_tag else 0
    
    # 5. 提取详细信息（从 #info div）
    info_div = soup.find('div', id='info')
    if info_div:
        # 导演
        director_link = info_div.find('a', rel='v:directedBy')
        info['director'] = director_link.get_text().strip() if director_link else ''
        
        # 编剧
        writer_span = info_div.find('span', class_='pl', string=lambda text: text and '编剧' in text)
        if writer_span:
            writer_links = writer_span.parent.find_all('a', class_=lambda x: x and 'attrs' in x)
            if not writer_links:
                # 尝试另一种方式：查找 attrs span 下的 a 标签
                attrs_span = writer_span.find_next_sibling('span', class_='attrs')
                if attrs_span:
                    writer_links = attrs_span.find_all('a')
            
            if writer_links:
                writers = [w.get_text().strip() for w in writer_links]
                info['writers'] = ','.join(writers)
            else:
                info['writers'] = ''
        else:
            info['writers'] = ''
        
        # 主演（可选）
        starring_links = info_div.find_all('a', rel='v:starring')
        if starring_links:
            stars = [s.get_text().strip() for s in starring_links[:10]]  # 只取前10个
            info['casts'] = ','.join(stars)
        else:
            info['casts'] = ''
        
        # 类型
        genre_tags = info_div.find_all('span', property='v:genre')
        if genre_tags:
            genres = [g.get_text().strip() for g in genre_tags]
            info['genres'] = ','.join(genres)
        else:
            info['genres'] = ''
        
        # 制片国家/地区
        country_span = info_div.find('span', class_='pl', string=lambda text: text and '制片国家' in text)
        if country_span:
            # 获取后面的文本节点
            next_text = country_span.next_sibling
            if next_text:
                info['country'] = next_text.strip()
            else:
                info['country'] = ''
        else:
            info['country'] = ''
        
        # 语言
        language_span = info_div.find('span', class_='pl', string=lambda text: text and '语言' in text)
        if language_span:
            next_text = language_span.next_sibling
            if next_text:
                info['language'] = next_text.strip()
            else:
                info['language'] = ''
        else:
            info['language'] = ''
        
        # 首播/上映时间
        release_span = info_div.find('span', property='v:initialReleaseDate')
        if release_span:
            info['release_date'] = release_span.get_text().strip()
        else:
            # 尝试查找 "上映日期"
            release_span = info_div.find('span', class_='pl', string=lambda text: text and ('上映' in text or '首播' in text))
            if release_span:
                date_tag = release_span.find_next_sibling('span')
                if date_tag:
                    info['release_date'] = date_tag.get_text().strip()
                else:
                    info['release_date'] = ''
            else:
                info['release_date'] = ''
        
        # 季数
        season_span = info_div.find('span', class_='pl', string=lambda text: text and '季数' in text)
        if season_span:
            next_text = season_span.next_sibling
            if next_text:
                season_match = re.search(r'(\d+)', next_text.strip())
                info['seasons'] = int(season_match.group(1)) if season_match else 0
            else:
                info['seasons'] = 0
        else:
            info['seasons'] = 0
        
        # 集数
        episode_span = info_div.find('span', class_='pl', string=lambda text: text and '集数' in text)
        if episode_span:
            next_text = episode_span.next_sibling
            if next_text:
                episode_match = re.search(r'(\d+)', next_text.strip())
                info['episodes'] = int(episode_match.group(1)) if episode_match else 0
            else:
                info['episodes'] = 0
        else:
            info['episodes'] = 0
        
        # 单集片长
        duration_span = info_div.find('span', class_='pl', string=lambda text: text and '单集片长' in text)
        if duration_span:
            next_text = duration_span.next_sibling
            if next_text:
                duration_text = next_text.strip()
                # 从 "45分钟" 中提取数字
                duration_match = re.search(r'(\d+)', duration_text)
                info['duration'] = int(duration_match.group(1)) * 60 if duration_match else 0  # 转换为秒
            else:
                info['duration'] = 0
        else:
            info['duration'] = 0
        
        # 别名/又名
        aka_span = info_div.find('span', class_='pl', string=lambda text: text and ('又名' in text or '别名' in text))
        if aka_span:
            next_text = aka_span.next_sibling
            if next_text:
                info['aka'] = next_text.strip()
            else:
                info['aka'] = ''
        else:
            info['aka'] = ''
        
        # IMDb ID
        imdb_span = info_div.find('span', class_='pl', string=lambda text: text and 'IMDb' in text)
        if imdb_span:
            next_text = imdb_span.next_sibling
            if next_text:
                imdb_text = next_text.strip()
                # 从 "tt6622786" 中提取
                imdb_match = re.search(r'(tt\d+)', imdb_text)
                info['imdb_id'] = imdb_match.group(1) if imdb_match else ''
            else:
                info['imdb_id'] = ''
        else:
            info['imdb_id'] = ''
    
    # 6. 提取简介
    summary_tag = soup.find('span', property='v:summary')
    if summary_tag:
        summary = summary_tag.get_text().strip()
        # 清理多余空格和换行
        summary = ' '.join(summary.split())
        info['summary'] = summary
    else:
        info['summary'] = ''
    
    return info


def test_douban_page_extraction():
    """测试从豆瓣电影页面提取信息"""
    
    # 测试URL
    test_urls = [
        'https://movie.douban.com/subject/6312211/',  # 爱情公寓3
        'https://movie.douban.com/subject/3926132/',  # 爱情公寓1
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    for url in test_urls:
        print(f"\n{'='*70}")
        print(f"测试URL: {url}")
        print('='*70)
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text[:200]}")
                continue
            
            # 检查是否是验证页面
            if 'sec' in response.text and 'tok' in response.text:
                print("⚠️  检测到豆瓣反爬虫验证，无法直接获取页面内容")
                print("需要手动通过浏览器访问或使用Selenium等工具")
                # 保存HTML用于分析
                douban_id = url.split('/')[-2]
                with open(f'douban_page_{douban_id}_blocked.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✓ HTML已保存到: douban_page_{douban_id}_blocked.html")
                continue
            
            # 提取信息
            info = extract_info_from_html(response.text)
            
            # 打印结果
            print(f"\n提取结果:")
            print(f"  标题: {info.get('title', 'N/A')}")
            print(f"  年份: {info.get('year', 'N/A')}")
            print(f"  评分: {info.get('rating', 'N/A')}")
            print(f"  评分人数: {info.get('votes', 'N/A')}")
            print(f"  导演: {info.get('director', 'N/A')}")
            print(f"  编剧: {info.get('writers', 'N/A')}")
            print(f"  主演: {info.get('casts', 'N/A')[:50]}..." if info.get('casts') else "  主演: N/A")
            print(f"  类型: {info.get('genres', 'N/A')}")
            print(f"  国家: {info.get('country', 'N/A')}")
            print(f"  语言: {info.get('language', 'N/A')}")
            print(f"  首播: {info.get('release_date', 'N/A')}")
            print(f"  季数: {info.get('seasons', 'N/A')}")
            print(f"  集数: {info.get('episodes', 'N/A')}")
            print(f"  单集片长: {info.get('duration', 'N/A')}秒")
            print(f"  别名: {info.get('aka', 'N/A')}")
            print(f"  IMDb ID: {info.get('imdb_id', 'N/A')}")
            print(f"\n  简介 (前100字符): {info.get('summary', 'N/A')[:100]}...")
            
            # 保存结果到JSON
            douban_id = url.split('/')[-2]
            with open(f'douban_extracted_{douban_id}.json', 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
            print(f"\n✓ 提取结果已保存到: douban_extracted_{douban_id}.json")
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    test_douban_page_extraction()
