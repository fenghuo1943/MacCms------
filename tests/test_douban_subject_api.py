"""
测试豆瓣Subject API返回的完整数据结构
"""
import requests
import json


def test_douban_subject_api():
    """测试豆瓣Subject API"""
    
    api_key = '0ab215a8b1977939201640fa14c66bab'
    
    # 测试几个不同的豆瓣ID
    test_ids = [
        '6312211',   # 爱情公寓
        '36995126',  # The Drama
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    for douban_id in test_ids:
        print(f"\n{'='*70}")
        print(f"测试豆瓣ID: {douban_id}")
        print('='*70)
        
        url = f'https://api.douban.com/v2/movie/subject/{douban_id}'
        
        try:
            # 使用POST方法
            data = {'apikey': api_key}
            response = requests.post(url, data=data, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"响应: {response.text[:200]}")
                continue
            
            result = response.json()
            
            # 打印完整的JSON结构（格式化）
            print("\n完整JSON数据:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 保存到一个文件方便分析
            with open(f'douban_subject_{douban_id}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n✓ JSON已保存到: douban_subject_{douban_id}.json")
            
        except Exception as e:
            print(f"发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    test_douban_subject_api()
