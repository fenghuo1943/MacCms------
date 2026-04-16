"""
数据处理模块 - 匹配、提取、计算
"""
import json
from typing import Dict, List, Tuple, Optional
from .models import VideoInfo


class DataProcessor:
    """数据处理器"""
    
    @staticmethod
    def extract_list_names(data_list: List[Dict]) -> str:
        """
        从嵌套列表中提取名称并用逗号连接
        
        Args:
            data_list: 嵌套列表数据
            
        Returns:
            用逗号分隔的名称字符串
        """
        names = []
        for item in data_list:
            if isinstance(item, dict) and 'data' in item:
                for sub_item in item['data']:
                    if isinstance(sub_item, dict) and 'name' in sub_item:
                        names.append(sub_item['name'])
        return ','.join(names[:10]) if names else ''  # 只取前10个
    
    @staticmethod
    def match_video(search_results: List[Dict], target_name: str, target_year: str):
        """
        从搜索结果中匹配目标视频
        
        Args:
            search_results: 搜索结果列表
            target_name: 目标视频名称
            target_year: 目标视频年份
            
        Returns:
            匹配的视频信息，'multiple'表示多个结果，None表示未匹配
        """
        import re
        
        if not search_results:
            return None
        
        matched_videos = []
        
        for result in search_results:
            result_name = ''
            if 'data' in result and isinstance(result['data'], list) and len(result['data']) > 0:
                first_data = result['data'][0]
                if isinstance(first_data, dict) and 'name' in first_data:
                    result_name = first_data['name']
            
            # 如果从 data 中没获取到名称，则使用原来的字段
            if not result_name:
                result_name = result.get('originalName', '') or result.get('title', '') or result.get('name', '')
            
            # 获取年份，优先从 year 字段，如果没有则从 dateReleased 中提取
            result_year = str(result.get('year', ''))
            if not result_year or not re.search(r'\d{4}', result_year):
                # 从 dateReleased 中提取年份（格式如 "2025-12-23"）
                date_released = result.get('dateReleased', '')
                if date_released:
                    year_match_obj = re.search(r'(\d{4})', str(date_released))
                    if year_match_obj:
                        result_year = year_match_obj.group(1)
            
            if not result_name:
                continue
            
            # 检查名称是否精确匹配
            name_match = target_name.strip() == result_name.strip()
            
            # 检查年份是否匹配
            year_match = False
            if target_year and target_year.strip():
                # 提取纯数字年份（处理 "2025–"、"2025-"、"2025-2026" 等格式）
                target_years = re.findall(r'\d{4}', target_year.strip())
                result_years = re.findall(r'\d{4}', result_year.strip())
                
                if target_years and result_years:
                    # 如果目标年份只有一个，检查结果年份中是否包含该年份
                    if len(target_years) == 1:
                        year_match = target_years[0] in result_years
                    else:
                        # 如果目标年份有多个，检查是否有交集
                        year_match = bool(set(target_years) & set(result_years))
                else:
                    # 如果无法提取4位数字，则使用原始比较
                    year_match = target_year.strip() == result_year.strip()
            else:
                # 如果没有年份信息，只匹配名称
                year_match = True
            
            if name_match and year_match:
                matched_videos.append(result)
        
        # 只有精确匹配一个时才返回
        if len(matched_videos) == 1:
            return matched_videos[0]
        elif len(matched_videos) > 1:
            return 'multiple'
        else:
            return None
    
    @staticmethod
    def extract_video_info(video_data: Dict) -> Dict:
        """
        从API返回数据中提取需要的信息
        
        Args:
            video_data: API返回的视频数据
            
        Returns:
            提取的信息字典
        """
        info = VideoInfo.create_empty()
        
        # 基础评分信息
        info.update({
            'imdbId': video_data.get('imdbId', ''),
            'imdbVotes': video_data.get('imdbVotes', 0),
            'imdbRating': video_data.get('imdbRating', 0.0),
            'doubanId': video_data.get('doubanId', 0),
            'doubanRating': video_data.get('doubanRating', 0.0),
            'doubanVotes': video_data.get('doubanVotes', 0),
            'year': str(video_data.get('year', '')),
            'type': video_data.get('type', ''),
            'alias': video_data.get('alias', ''),
            'episodes': video_data.get('episodes', 0),
            'duration': video_data.get('duration', 0),
            'dateReleased': video_data.get('dateReleased', ''),
        })
        
        # 转换数据类型
        try:
            info['imdbVotes'] = int(info['imdbVotes']) if info['imdbVotes'] else 0
            info['imdbRating'] = float(info['imdbRating']) if info['imdbRating'] else 0.0
            info['doubanId'] = int(info['doubanId']) if info['doubanId'] else 0
            info['doubanRating'] = float(info['doubanRating']) if info['doubanRating'] else 0.0
            info['doubanVotes'] = int(info['doubanVotes']) if info['doubanVotes'] else 0
            info['episodes'] = int(info['episodes']) if info['episodes'] else 0
            # 将秒转换为分钟，并添加"分钟"字样
            duration_seconds = int(info['duration']) if info['duration'] else 0
            info['duration'] = f"{duration_seconds // 60}分钟" if duration_seconds > 0 else "0分钟"
        except (ValueError, TypeError):
            pass
        
        # 提取演员、导演、编剧
        if 'actor' in video_data:
            info['actors'] = DataProcessor.extract_list_names(video_data['actor'])
        
        if 'director' in video_data:
            info['directors'] = DataProcessor.extract_list_names(video_data['director'])
        
        if 'writer' in video_data:
            info['writers'] = DataProcessor.extract_list_names(video_data['writer'])
        
        # 提取详细信息
        if 'data' in video_data and isinstance(video_data['data'], list) and len(video_data['data']) > 0:
            first_data = video_data['data'][0]
            if isinstance(first_data, dict):
                info['genre'] = first_data.get('genre', '')
                info['country'] = first_data.get('country', '')
                info['language'] = first_data.get('language', '')
                info['poster'] = first_data.get('poster', '')
                info['description'] = first_data.get('description', '')
        
        return info
    
    @staticmethod
    def calculate_combined_score(imdb_rating: float, douban_rating: float, 
                                  imdb_votes: int, douban_votes: int) -> Tuple[float, int]:
        """
        计算综合评分和评分人数（加权平均）
        
        Args:
            imdb_rating: IMDB评分
            douban_rating: 豆瓣评分
            imdb_votes: IMDB投票人数
            douban_votes: 豆瓣投票人数
            
        Returns:
            (综合评分, 综合评分人数)
        """
        total_votes = imdb_votes + douban_votes
        
        if total_votes == 0:
            return 0.0, 0
        
        # 按投票人数加权平均
        combined_score = (imdb_rating * imdb_votes + douban_rating * douban_votes) / total_votes
        
        # 保留一位小数
        combined_score = round(combined_score, 1)
        
        return combined_score, total_votes
    
    @staticmethod
    def decode_unicode_string(text: str) -> str:
        """
        将Unicode编码的字符串转换为中文
        
        Args:
            text: 可能包含Unicode编码的字符串
            
        Returns:
            解码后的字符串
        """
        if not text:
            return text
        try:
            # 尝试解码Unicode转义序列
            if '\\u' in text:
                return text.encode('utf-8').decode('unicode_escape')
            return text
        except:
            return text
    
    @staticmethod
    def extract_douban_info(douban_data: Dict) -> Dict:
        """
        从豆瓣API返回数据中提取需要的信息
        支持两种API返回格式：
        1. IMDB API: /v2/movie/imdb/{imdbId}
        2. Subject API: /v2/movie/subject/{doubanId}
        
        Args:
            douban_data: 豆瓣API返回的数据
            
        Returns:
            提取的信息字典
        """
        info = {}
        
        # 提取评分信息
        if 'rating' in douban_data and isinstance(douban_data['rating'], dict):
            rating = douban_data['rating']
            # average可能是字符串或数字
            avg = rating.get('average', 0.0)
            info['doubanRating'] = float(avg) if avg else 0.0
            
            # numRaters可能在rating中，也可能在根级别（ratings_count）
            num_raters = rating.get('numRaters') or douban_data.get('ratings_count', 0)
            info['doubanVotes'] = int(num_raters) if num_raters else 0
        
        # 提取标签
        if 'tags' in douban_data and isinstance(douban_data['tags'], list):
            tags = []
            for tag in douban_data['tags']:
                if isinstance(tag, dict) and 'name' in tag:
                    tag_name = DataProcessor.decode_unicode_string(tag['name'])
                    tags.append(tag_name)
            info['tags'] = ','.join(tags[:10])  # 只取前10个标签
        
        return info
    
    @staticmethod
    def merge_video_info(wmdb_info: Dict, douban_info: Dict) -> Dict:
        """
        合并WMDB和豆瓣API的信息
        
        Args:
            wmdb_info: 从WMDB API提取的信息
            douban_info: 从豆瓣API提取的信息
            
        Returns:
            合并后的信息字典
        """
        merged = wmdb_info.copy()
        
        # 用豆瓣API的评分覆盖WMDB的评分（如果豆瓣API有数据）
        if douban_info.get('doubanRating', 0.0) > 0:
            merged['doubanRating'] = douban_info['doubanRating']
        
        if douban_info.get('doubanVotes', 0) > 0:
            merged['doubanVotes'] = douban_info['doubanVotes']
        
        # 添加标签
        if douban_info.get('tags'):
            merged['tags'] = douban_info['tags']
        
        return merged
