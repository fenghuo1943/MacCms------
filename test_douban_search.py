"""
测试豆瓣API搜索功能的正确参数格式
"""
import requests
import json


def test_douban_search_api():
    """测试豆瓣API搜索功能的不同参数格式"""
    
    # 豆瓣API配置
    api_key = '0ab215a8b1977939201640fa14c66bab'
    base_url = 'https://api.douban.com/v2/movie/search'
    
    # 测试用例
    test_cases = [
        {
            'name': '直接中文',
            'params': {'q': '爱情公寓', 'apikey': api_key}
        },
        {
            'name': 'URL编码中文',
            'params': {'q': '%E7%88%B1%E6%83%85%E5%85%AC%E5%AF%93', 'apikey': api_key}
        },
        {
            'name': 'Unicode转义',
            'params': {'q': '\\u7231\\u60c5\\u516c\\u5bd3', 'apikey': api_key}
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    for case in test_cases:
        print(f"\n{'='*50}")
        print(f"测试: {case['name']}")
        print(f"参数: {case['params']}")
        
        try:
            response = requests.get(
                base_url,
                params=case['params'],
                headers=headers,
                timeout=10
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"返回标题: {data.get('title', 'N/A')}")
                
                # 显示前几个结果
                subjects = data.get('subjects', [])
                if subjects:
                    print(f"找到 {len(subjects)} 个结果:")
                    for i, subject in enumerate(subjects[:3]):  # 只显示前3个
                        title = subject.get('title', 'N/A')
                        year = subject.get('year', 'N/A')
                        rating = subject.get('rating', {}).get('average', 'N/A')
                        print(f"  {i+1}. {title} ({year}) - 评分: {rating}")
                else:
                    print("未找到相关结果")
                    
            else:
                print(f"请求失败: {response.text[:200]}")
                
        except Exception as e:
            print(f"发生错误: {str(e)}")


if __name__ == '__main__':
    test_douban_search_api()