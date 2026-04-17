"""
多设备并发功能测试脚本
用于验证数据库锁定机制是否正常工作
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from douban_fetcher.database import DatabaseManager
from douban_fetcher.config import DB_CONFIG
from douban_fetcher.worker_config import get_worker_id


def test_worker_id_generation():
    """测试设备标识生成"""
    print("=" * 70)
    print("测试1: 设备标识生成")
    print("=" * 70)
    
    worker_id = get_worker_id()
    print(f"生成的设备标识: {worker_id}")
    print(f"长度: {len(worker_id)}")
    print(f"格式正确: {'_' in worker_id}")
    print()
    
    # 生成多个ID，确保唯一性
    ids = [get_worker_id() for _ in range(5)]
    print("生成5个设备标识:")
    for i, wid in enumerate(ids, 1):
        print(f"  {i}. {wid}")
    
    unique_count = len(set(ids))
    print(f"\n唯一标识数量: {unique_count}/5")
    print(f"测试结果: {'✓ 通过' if unique_count == 5 else '✗ 失败'}")
    print()


def test_database_locking():
    """测试数据库锁定机制"""
    print("=" * 70)
    print("测试2: 数据库锁定机制")
    print("=" * 70)
    
    db = DatabaseManager(DB_CONFIG)
    
    try:
        # 检查表结构
        print("\n步骤1: 检查数据库表结构...")
        conn = db.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_COMMENT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'mac_vod'
                  AND COLUMN_NAME IN ('vod_fetch_worker', 'vod_fetch_time', 'vod_fetch_lock_time')
            """)
            columns = cursor.fetchall()
            
            if len(columns) == 3:
                print("✓ 新字段已添加:")
                for col in columns:
                    print(f"  - {col['COLUMN_NAME']}: {col['COLUMN_TYPE']}")
            else:
                print(f"✗ 缺少字段，只找到 {len(columns)} 个")
                print("请先执行 sql/migration.sql")
                return
        
        # 检查索引
        print("\n步骤2: 检查索引...")
        cursor.execute("""
            SHOW INDEX FROM mac_vod
            WHERE Key_name IN ('vod_fetch_worker', 'vod_fetch_lock_time')
        """)
        indexes = cursor.fetchall()
        
        if len(indexes) >= 2:
            print("✓ 索引已创建:")
            for idx in indexes:
                print(f"  - {idx['Key_name']}: {idx['Column_name']}")
        else:
            print(f"✗ 缺少索引，只找到 {len(indexes)} 个")
        
        conn.close()
        
        # 测试锁定功能
        print("\n步骤3: 测试原子锁定功能...")
        worker_id = get_worker_id()
        print(f"使用设备标识: {worker_id}")
        
        videos = db.lock_videos_atomically(worker_id, limit=5)
        
        if videos:
            print(f"✓ 成功锁定 {len(videos)} 个视频:")
            for v in videos[:3]:  # 只显示前3个
                print(f"  - ID:{v['vod_id']} {v['vod_name']}")
            if len(videos) > 3:
                print(f"  ... 还有 {len(videos) - 3} 个")
            
            # 验证锁定信息
            conn = db.get_connection()
            with conn.cursor() as cursor:
                video_ids = [v['vod_id'] for v in videos]
                placeholders = ','.join(['%s'] * len(video_ids))
                cursor.execute(f"""
                    SELECT vod_id, vod_fetch_worker, vod_fetch_time, vod_fetch_lock_time
                    FROM mac_vod
                    WHERE vod_id IN ({placeholders})
                """, video_ids)
                
                locked = cursor.fetchall()
                all_locked = all(
                    row['vod_fetch_worker'] == worker_id and 
                    row['vod_fetch_time'] > 0 and
                    row['vod_fetch_lock_time'] > 0
                    for row in locked
                )
                
                if all_locked:
                    print("✓ 锁定信息正确设置")
                else:
                    print("✗ 锁定信息设置有误")
            
            conn.close()
            
            # 清理测试数据（释放锁定）
            print("\n步骤4: 清理测试锁定...")
            conn = db.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE mac_vod 
                    SET vod_fetch_worker = '',
                        vod_fetch_time = 0,
                        vod_fetch_lock_time = 0
                    WHERE vod_fetch_worker = %s
                """, (worker_id,))
                conn.commit()
                print(f"✓ 已清理 {cursor.rowcount} 个视频的锁定")
            conn.close()
            
        else:
            print("ℹ 没有可锁定的视频（可能所有视频都已处理）")
            print("这不影响功能，只是说明当前没有待处理的视频")
        
        print("\n" + "=" * 70)
        print("数据库锁定测试完成！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 确保清理
        try:
            conn = db.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE mac_vod 
                    SET vod_fetch_worker = '',
                        vod_fetch_time = 0,
                        vod_fetch_lock_time = 0
                    WHERE vod_fetch_worker = %s
                """, (worker_id,))
                conn.commit()
            conn.close()
        except:
            pass


def test_concurrent_locking():
    """测试并发锁定（模拟两台设备）"""
    print("\n" + "=" * 70)
    print("测试3: 并发锁定模拟")
    print("=" * 70)
    
    db = DatabaseManager(DB_CONFIG)
    
    try:
        # 模拟设备A
        print("\n模拟设备A锁定...")
        worker_a = "TEST_DEVICE_A_12345678"
        videos_a = db.lock_videos_atomically(worker_a, limit=3)
        
        if videos_a:
            print(f"✓ 设备A锁定 {len(videos_a)} 个视频")
            ids_a = set(v['vod_id'] for v in videos_a)
            
            # 模拟设备B
            print("\n模拟设备B锁定...")
            worker_b = "TEST_DEVICE_B_87654321"
            videos_b = db.lock_videos_atomically(worker_b, limit=3)
            
            if videos_b:
                print(f"✓ 设备B锁定 {len(videos_b)} 个视频")
                ids_b = set(v['vod_id'] for v in videos_b)
                
                # 检查是否有重叠
                overlap = ids_a & ids_b
                if not overlap:
                    print("✓ 无重复锁定（完美！）")
                else:
                    print(f"✗ 发现 {len(overlap)} 个重复锁定的视频: {overlap}")
            else:
                print("ℹ 设备B没有锁定到视频")
        else:
            print("ℹ 设备A没有锁定到视频")
        
        # 清理
        print("\n清理测试数据...")
        conn = db.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE mac_vod 
                SET vod_fetch_worker = '',
                    vod_fetch_time = 0,
                    vod_fetch_lock_time = 0
                WHERE vod_fetch_worker IN (%s, %s)
            """, (worker_a, worker_b))
            conn.commit()
            print(f"✓ 已清理 {cursor.rowcount} 个视频的锁定")
        conn.close()
        
        print("\n" + "=" * 70)
        print("并发锁定测试完成！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("多设备并发功能测试")
    print("=" * 70 + "\n")
    
    # 运行测试
    test_worker_id_generation()
    test_database_locking()
    test_concurrent_locking()
    
    print("\n" + "=" * 70)
    print("所有测试完成！")
    print("=" * 70)
