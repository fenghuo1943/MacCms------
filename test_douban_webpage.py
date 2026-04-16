"""
测试从豆瓣电影页面提取信息
"""
import requests
from bs4 import BeautifulSoup
import json


def test_douban_page_extraction():
    """测试从豆瓣电影页面提取信息"""
    
    # 测试URL
    test_urls = [
        'https://movie.douban.com/subject/6312211/',  # 爱情公寓
        'https://movie.douban.com/subject/36995126/',  # The Drama
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
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取标题
            title_tag = soup.find('span', property='v:itemreviewed')
            title = title_tag.get_text().strip() if title_tag else 'N/A'
            print(f"\n标题: {title}")
            
            # 提取年份
            year_tag = soup.find('span', class_='year')
            year = year_tag.get_text().strip('() ') if year_tag else 'N/A'
            print(f"年份: {year}")
            
            # 提取评分
            rating_tag = soup.find('strong', class_='ll rating_num', property='v:average')
            rating = rating_tag.get_text().strip() if rating_tag else 'N/A'
            print(f"评分: {rating}")
            
            # 提取评分人数
            votes_tag = soup.find('span', property='v:votes')
            votes = votes_tag.get_text().strip() if votes_tag else 'N/A'
            print(f"评分人数: {votes}")
            
            # 提取IMDB链接
            imdb_link = soup.find('a', href=lambda href: href and 'imdb.com' in href)
            imdb_id = 'N/A'
            if imdb_link:
                href = imdb_link['href']
                # 从URL中提取IMDB ID
                if 'tt' in href:
                    imdb_id = href.split('/title/')[1].split('/')[0] if '/title/' in href else 'N/A'
            print(f"IMDB ID: {imdb_id}")
            
            # 提取导演和编剧
            director_tag = soup.find('a', rel='v:directedBy')
            director = director_tag.get_text().strip() if director_tag else 'N/A'
            print(f"导演: {director}")
            
            # 提取编剧 - 需要查找"编剧"标签
            info_section = soup.find('div', id='info')
            if info_section:
                # 查找所有span.pl（属性名）
                spans = info_section.find_all('span', class_='pl')
                for span in spans:
                    if '编剧' in span.get_text():
                        # 获取后面的演员链接
                        writer_links = span.parent.find_all('a', class_='attrs')
                        if writer_links:
                            writers = [w.get_text().strip() for w in writer_links]
                            print(f"编剧: {', '.join(writers)}")
                        break
            
            # 提取类型（标签）
            genre_tags = soup.find_all('span', property='v:genre')
            genres = [tag.get_text().strip() for tag in genre_tags]
            print(f"类型: {', '.join(genres)}")
            
            # 提取简介
            summary_tag = soup.find('span', property='v:summary')
            if summary_tag:
                summary = summary_tag.get_text().strip()
                # 清理多余空格和换行
                summary = ' '.join(summary.split())
                print(f"\n简介 (前100字符): {summary[:100]}...")
            
            # 提取其他信息（季数、集数等）
            if info_section:
                print(f"\n详细信息:")
                # 获取所有属性
                all_spans = info_section.find_all('span', class_='pl')
                for span in all_spans:
                    label = span.get_text().strip().rstrip(':')
                    # 获取对应的值
                    next_sibling = span.next_sibling
                    if next_sibling:
                        value = next_sibling.strip() if hasattr(next_sibling, 'strip') else str(next_sibling)
                        if value:
                            print(f"  {label}: {value}")
                    
                    # 也检查是否有链接
                    links = span.parent.find_all('a')
                    if links and len(links) > 0:
                        link_texts = [link.get_text().strip() for link in links]
                        if link_texts:
                            print(f"  {label} (links): {', '.join(link_texts)}")
            
            # 保存HTML用于分析
            with open(f'douban_page_{url.split("/")[-2]}.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"\n✓ HTML已保存到: douban_page_{url.split('/')[-2]}.html")
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    test_douban_page_extraction()
