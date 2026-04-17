"""
豆瓣网页数据提取器模块
"""
import re
from typing import Dict, Optional
from bs4 import BeautifulSoup

from .config import logger


class DoubanPageExtractor:
    """豆瓣页面信息提取器"""
    
    @staticmethod
    def extract_search_results(html_content: str) -> list:
        """
        从豆瓣搜索页面提取搜索结果
        
        Args:
            html_content: HTML内容
            
        Returns:
            搜索结果列表，每个结果包含: id, title, year, type, url
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # 查找所有搜索结果项
        result_items = soup.find_all('div', class_='result')
        
        for item in result_items:
            try:
                # 提取标题和链接
                title_tag = item.find('a', class_='nbg')
                if not title_tag:
                    continue
                
                title = title_tag.get('title', '')
                url = title_tag.get('href', '')
                
                # 从URL中提取豆瓣ID
                douban_id = ''
                if '/subject/' in url:
                    match = re.search(r'/subject/(\d+)/', url)
                    if match:
                        douban_id = match.group(1)
                
                # 提取年份和类型
                subject_info = item.find('span', class_='subject-cast')
                year = ''
                content_type = ''
                
                if subject_info:
                    info_text = subject_info.get_text()
                    # 提取年份
                    year_match = re.search(r'(\d{4})', info_text)
                    if year_match:
                        year = year_match.group(1)
                    
                    # 提取类型（电影/电视剧）
                    if '电影' in info_text:
                        content_type = 'movie'
                    elif '电视剧' in info_text:
                        content_type = 'tv'
                
                if douban_id and title:
                    results.append({
                        'id': douban_id,
                        'title': title,
                        'year': year,
                        'type': content_type,
                        'url': url
                    })
                    
            except Exception as e:
                logger.warning(f"提取搜索结果项时出错: {str(e)}")
                continue
        
        logger.info(f"从搜索页面提取到 {len(results)} 个结果")
        return results
    
    @staticmethod
    def extract_movie_info(html_content: str) -> Dict:
        """
        从豆瓣电影详情页提取完整信息
        
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
            writer_span = info_div.find('span', class_='pl', 
                                       string=lambda text: text and '编剧' in text)
            if writer_span:
                writer_links = writer_span.parent.find_all('a', 
                                                          class_=lambda x: x and 'attrs' in x)
                if not writer_links:
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
            
            # 主演
            starring_links = info_div.find_all('a', rel='v:starring')
            if starring_links:
                stars = [s.get_text().strip() for s in starring_links[:10]]
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
            country_span = info_div.find('span', class_='pl', 
                                        string=lambda text: text and '制片国家' in text)
            if country_span:
                next_text = country_span.next_sibling
                info['country'] = next_text.strip() if next_text else ''
            else:
                info['country'] = ''
            
            # 语言
            language_span = info_div.find('span', class_='pl', 
                                         string=lambda text: text and '语言' in text)
            if language_span:
                next_text = language_span.next_sibling
                info['language'] = next_text.strip() if next_text else ''
            else:
                info['language'] = ''
            
            # 首播/上映时间
            release_span = info_div.find('span', property='v:initialReleaseDate')
            if release_span:
                info['release_date'] = release_span.get_text().strip()
            else:
                release_span = info_div.find('span', class_='pl', 
                                            string=lambda text: text and ('上映' in text or '首播' in text))
                if release_span:
                    date_tag = release_span.find_next_sibling('span')
                    info['release_date'] = date_tag.get_text().strip() if date_tag else ''
                else:
                    info['release_date'] = ''
            
            # 季数
            season_span = info_div.find('span', class_='pl', 
                                       string=lambda text: text and '季数' in text)
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
            episode_span = info_div.find('span', class_='pl', 
                                        string=lambda text: text and '集数' in text)
            if episode_span:
                next_text = episode_span.next_sibling
                if next_text:
                    episode_match = re.search(r'(\d+)', next_text.strip())
                    info['episodes'] = int(episode_match.group(1)) if episode_match else 0
                else:
                    info['episodes'] = 0
            else:
                info['episodes'] = 0
            
            # IMDb ID
            imdb_span = info_div.find('span', class_='pl', 
                                     string=lambda text: text and 'IMDb' in text)
            if imdb_span:
                next_text = imdb_span.next_sibling
                if next_text:
                    imdb_text = next_text.strip()
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
            summary = ' '.join(summary.split())
            info['summary'] = summary
        else:
            info['summary'] = ''
        
        logger.info(f"成功提取电影信息: {info.get('title', 'Unknown')}")
        return info
