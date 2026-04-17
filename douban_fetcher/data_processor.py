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
    def normalize_name(name: str) -> str:
        """
        标准化视频名称：去除所有空格和特殊字符
        
        Args:
            name: 原始视频名称
            
        Returns:
            标准化后的名称
        """
        if not name:
            return ''
        # 去除所有空格、制表符、换行符等空白字符
        import re
        normalized = re.sub(r'\s+', '', name.strip())
        return normalized
    
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
            
            # 检查名称是否精确匹配（去除所有空格后比较）
            normalized_target = DataProcessor.normalize_name(target_name)
            normalized_result = DataProcessor.normalize_name(result_name)
            name_match = normalized_target == normalized_result
            
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
    def calculate_similarity(str1: str, str2: str) -> float:
        """
        计算两个字符串的相似度（基于编辑距离）
        
        Args:
            str1: 第一个字符串
            str2: 第二个字符串
            
        Returns:
            相似度分数 (0-1)，1表示完全相同
        """
        if not str1 or not str2:
            return 0.0
        
        # 转换为小写并标准化
        str1 = str1.lower()
        str2 = str2.lower()
        
        # 如果完全相同
        if str1 == str2:
            return 1.0
        
        # 计算编辑距离
        len1, len2 = len(str1), len(str2)
        
        # 创建距离矩阵
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        # 初始化边界
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j
        
        # 填充矩阵
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if str1[i-1] == str2[j-1]:
                    cost = 0
                else:
                    cost = 1
                
                dp[i][j] = min(
                    dp[i-1][j] + 1,      # 删除
                    dp[i][j-1] + 1,      # 插入
                    dp[i-1][j-1] + cost  # 替换
                )
        
        # 计算相似度
        max_len = max(len1, len2)
        similarity = 1 - (dp[len1][len2] / max_len)
        
        return similarity
    
    @staticmethod
    def check_name_containment(name1: str, name2: str) -> bool:
        """
        检查两个名称是否存在包含关系
        
        Args:
            name1: 第一个名称
            name2: 第二个名称
            
        Returns:
            是否存在包含关系
        """
        if not name1 or not name2:
            return False
        
        # 标准化名称
        norm1 = DataProcessor.normalize_name(name1)
        norm2 = DataProcessor.normalize_name(name2)
        
        # 检查包含关系
        if norm1 in norm2 or norm2 in norm1:
            return True
        
        # 检查核心词匹配（处理“伟大的觉醒”vs“大觉醒”这种情况）
        # 如果较短的字符串长度>=2，且其所有字符都在较长字符串中出现
        if len(norm1) >= 2 and len(norm2) >= 2:
            shorter = norm1 if len(norm1) < len(norm2) else norm2
            longer = norm2 if len(norm1) < len(norm2) else norm1
            
            # 移除数字后再比较（避免“蜘蛛侠3”和“蜘蛛侠：英雄无归”误匹配）
            import re
            shorter_no_num = re.sub(r'\d', '', shorter)
            longer_no_num = re.sub(r'\d', '', longer)
            
            # 如果去除数字后较短字符串仍然>=2个字符
            if len(shorter_no_num) >= 2:
                # 计算较短字符串中有多少字符在较长字符串中出现
                common_chars = sum(1 for char in shorter_no_num if char in longer_no_num)
                match_ratio = common_chars / len(shorter_no_num)
                
                # 更严格的条件：
                # 1. 超过80%的字符都匹配
                # 2. 或者较短字符串至少有4个字符且70%匹配
                if (match_ratio >= 0.8) or (len(shorter_no_num) >= 4 and match_ratio >= 0.7):
                    return True
        
        return False
    
    @staticmethod
    def match_douban_search_results(search_results: List[Dict], target_name: str, target_year: str, target_area: str = '', target_director: str = '') -> Optional[Dict]:
        """
        从豆瓣搜索结果中匹配目标视频（增强版：分级匹配策略）
        
        匹配策略：
        1. 第一级（严格）：名称精确匹配 + 年份 + 地区 + 导演，如果只有1个结果就返回
        2. 第二级（宽松）：如果第一级结果为0，则使用名称相似度/包含关系，年份和导演必须非空且匹配，地区可选
        
        Args:
            search_results: 豆瓣搜索结果列表
            target_name: 目标视频名称
            target_year: 目标视频年份
            target_area: 目标视频地区（可选）
            target_director: 目标视频导演（可选）
            
        Returns:
            匹配的搜索结果，None表示未匹配
        """
        import re
        
        if not search_results:
            return None
        
        # ========== 第一级匹配：严格模式（名称精确匹配 + 年份 + 地区 + 导演）==========
        strict_matched = []
        
        for result in search_results:
            result_name = result.get('title', '')
            result_year = str(result.get('year', ''))
            
            if not result_name:
                continue
            
            # 严格模式：只检查精确匹配（去除所有空格后比较）
            normalized_target = DataProcessor.normalize_name(target_name)
            normalized_result = DataProcessor.normalize_name(result_name)
            exact_match = normalized_target == normalized_result
            
            # 检查年份是否匹配
            year_match = DataProcessor._check_year_match(target_year, result_year)
            
            # 检查地区是否匹配（如果提供了地区信息）- 使用包含关系
            area_match = DataProcessor._check_area_match(target_area, result)
            
            # 检查导演是否匹配（如果提供了导演信息）
            director_match = DataProcessor._check_director_match(target_director, result)
            
            # 第一级：名称精确匹配 + 其他字段匹配
            if exact_match and year_match and area_match and director_match:
                strict_matched.append(result)
        
        # 如果严格匹配只有1个结果，直接返回
        if len(strict_matched) == 1:
            return strict_matched[0]
        elif len(strict_matched) > 1:
            return 'multiple'
        
        # ========== 第二级匹配：宽松模式（名称相似度/包含关系 + 年份/地区/导演必须非空且匹配）==========
        # 只有当严格匹配结果为0时，才进入宽松模式
        if len(strict_matched) == 0:
            loose_matched = []
            
            for result in search_results:
                result_name = result.get('title', '')
                result_year = str(result.get('year', ''))
                
                if not result_name:
                    continue
                
                # 宽松模式：名称使用包含关系或相似度
                containment_match = DataProcessor.check_name_containment(target_name, result_name)
                similarity = DataProcessor.calculate_similarity(target_name, result_name)
                similarity_match = similarity >= 0.7  # 提高阈值到0.7
                
                # 名称匹配：包含关系 OR 相似度达标
                loose_name_match = containment_match or similarity_match
                
                # 关键：年份、导演必须非空且匹配，地区可选
                # 检查年份是否非空且匹配
                if not target_year or not target_year.strip():
                    continue  # 年份为空，跳过
                year_match = DataProcessor._check_year_match(target_year, result_year)
                if not year_match:
                    continue
                
                # 检查地区是否匹配（如果提供了地区信息）- 地区可以为空
                area_match = DataProcessor._check_area_match(target_area, result)
                if not area_match:
                    continue
                
                # 检查导演是否非空且匹配
                if not target_director or not target_director.strip():
                    continue  # 导演为空，跳过
                director_match = DataProcessor._check_director_match(target_director, result)
                if not director_match:
                    continue
                
                # 第二级：名称可以宽松，但年份、地区、导演必须非空且匹配
                if loose_name_match:
                    loose_matched.append(result)
            
            # 处理宽松匹配结果
            if len(loose_matched) == 1:
                return loose_matched[0]
            elif len(loose_matched) > 1:
                return 'multiple'  # 多个结果返回'multiple'
        
        return None
    
    @staticmethod
    def _check_year_match(target_year: str, result_year: str) -> bool:
        """
        检查年份是否匹配
        
        Args:
            target_year: 目标年份
            result_year: 结果年份
            
        Returns:
            是否匹配
        """
        import re
        
        if not target_year or not target_year.strip():
            return True  # 没有年份信息，跳过匹配
        
        # 提取纯数字年份
        target_years = re.findall(r'\d{4}', target_year.strip())
        result_years = re.findall(r'\d{4}', result_year.strip())
        
        if target_years and result_years:
            if len(target_years) == 1:
                return target_years[0] in result_years
            else:
                return bool(set(target_years) & set(result_years))
        else:
            return target_year.strip() == result_year.strip()
    
    @staticmethod
    def _check_area_match(target_area: str, result: Dict) -> bool:
        """
        检查地区是否匹配
        
        Args:
            target_area: 目标地区
            result: 搜索结果
            
        Returns:
            是否匹配
        """
        if not target_area or not target_area.strip():
            return True  # 没有地区信息，跳过匹配
        
        # 从结果中提取地区信息
        result_area = result.get('country', '') or result.get('area', '')
        if result_area:
            # 使用包含关系匹配
            return target_area.strip() in result_area or result_area in target_area.strip()
        else:
            return True  # 结果中没有地区信息，跳过匹配
    
    @staticmethod
    def _check_director_match(target_director: str, result: Dict) -> bool:
        """
        检查导演是否匹配
        
        Args:
            target_director: 目标导演
            result: 搜索结果
            
        Returns:
            是否匹配
        """
        if not target_director or not target_director.strip():
            return True  # 没有导演信息，跳过匹配
        
        # 从结果中提取导演信息
        result_directors = []
        if 'directors' in result and isinstance(result['directors'], list):
            result_directors = [d.get('name', '') for d in result['directors'] if d.get('name')]
        
        if result_directors:
            # 使用包含关系匹配
            return any(target_director.strip() in director or director in target_director.strip() 
                       for director in result_directors)
        else:
            return True  # 结果中没有导演信息，跳过匹配
    
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
