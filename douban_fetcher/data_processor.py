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
            info['duration'] = int(info['duration']) if info['duration'] else 0
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
    def extract_douban_subject_info(douban_data: Dict) -> Dict:
        """
        从豆瓣Subject API返回数据中提取详细信息
        
        Args:
            douban_data: 豆瓣Subject API返回的数据
            
        Returns:
            提取的详细信息字典
        """
        info = {}
        
        # 基本信息
        info['doubanId'] = douban_data.get('id', '')
        info['title'] = douban_data.get('title', '')
        info['originalTitle'] = douban_data.get('original_title', '')
        info['year'] = douban_data.get('year', '')
        
        # 评分信息
        if 'rating' in douban_data and isinstance(douban_data['rating'], dict):
            rating = douban_data['rating']
            avg = rating.get('average', 0.0)
            info['doubanRating'] = float(avg) if avg else 0.0
            
            # 评分人数
            num_raters = douban_data.get('ratings_count', 0)
            info['doubanVotes'] = int(num_raters) if num_raters else 0
        
        # 简介
        info['description'] = douban_data.get('summary', '')
        
        # 导演
        if 'directors' in douban_data and isinstance(douban_data['directors'], list):
            directors = [d.get('name', '') for d in douban_data['directors'] if d.get('name')]
            info['directors'] = ','.join(directors)
        
        # 演员（可用于后续扩展）
        if 'casts' in douban_data and isinstance(douban_data['casts'], list):
            casts = [c.get('name', '') for c in douban_data['casts'] if c.get('name')]
            info['casts'] = ','.join(casts[:10])  # 只取前10个
        
        # 类型/标签
        if 'genres' in douban_data and isinstance(douban_data['genres'], list):
            info['tags'] = ','.join(douban_data['genres'])
        
        # 别名
        if 'aka' in douban_data and isinstance(douban_data['aka'], list):
            info['alias'] = ','.join(douban_data['aka'])
        
        # 季数和集数（电视剧）
        info['seasons_count'] = douban_data.get('seasons_count')
        info['current_season'] = douban_data.get('current_season')
        info['episodes_count'] = douban_data.get('episodes_count')
        
        # 国家
        if 'countries' in douban_data and isinstance(douban_data['countries'], list):
            info['country'] = ','.join(douban_data['countries'])
        
        # 子类型（movie/tv）
        info['subtype'] = douban_data.get('subtype', '')
        
        return info
    
    @staticmethod
    def match_douban_search_results(search_results: List[Dict], target_name: str, target_year: str) -> Optional[Dict]:
        """
        从豆瓣搜索结果中匹配目标视频
        
        Args:
            search_results: 豆瓣搜索结果列表
            target_name: 目标视频名称
            target_year: 目标视频年份
            
        Returns:
            匹配的搜索结果，None表示未匹配
        """
        import re
        
        if not search_results:
            return None
        
        matched_videos = []
        
        for result in search_results:
            result_name = result.get('title', '')
            result_year = str(result.get('year', ''))
            
            if not result_name:
                continue
            
            # 检查名称是否精确匹配
            name_match = target_name.strip() == result_name.strip()
            
            # 检查年份是否匹配
            year_match = False
            if target_year and target_year.strip():
                # 提取纯数字年份
                target_years = re.findall(r'\d{4}', target_year.strip())
                result_years = re.findall(r'\d{4}', result_year.strip())
                
                if target_years and result_years:
                    if len(target_years) == 1:
                        year_match = target_years[0] in result_years
                    else:
                        year_match = bool(set(target_years) & set(result_years))
                else:
                    year_match = target_year.strip() == result_year.strip()
            else:
                # 如果没有年份信息，只匹配名称
                year_match = True
            
            if name_match and year_match:
                matched_videos.append(result)
        
        if len(matched_videos) == 1:
            return matched_videos[0]
        elif len(matched_videos) > 1:
            return 'multiple'
        else:
            return None
    
    @staticmethod
    def prepare_db_info_from_douban(douban_info: Dict) -> Dict:
        """
        准备用于数据库更新的信息（仅使用豆瓣API）
        
        Args:
            douban_info: 从豆瓣Subject API提取的信息
            
        Returns:
            符合数据库要求的信息字典
        """
        # 创建符合数据库要求的信息结构
        info = {
            'doubanId': douban_info.get('doubanId', ''),
            'doubanRating': douban_info.get('doubanRating', 0.0),
            'doubanVotes': douban_info.get('doubanVotes', 0),
            'imdbId': None,  # 豆瓣API不提供，使用NULL
            'imdbRating': None,  # 豆瓣API不提供，使用NULL
            'imdbVotes': 0,  # 豆瓣API不提供
            'writers': '',  # 豆瓣API不提供
            'description': douban_info.get('description', ''),
            'episodes': int(douban_info.get('episodes_count', 0) or 0),
            'duration': 0,  # 豆瓣API不直接提供单集片长
            'dateReleased': douban_info.get('year', ''),  # 使用年份作为上映时间
            'alias': douban_info.get('alias', ''),
            'tags': douban_info.get('tags', ''),
        }
        
        return info
