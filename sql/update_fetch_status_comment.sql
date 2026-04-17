-- 更新 mac_vod 表中 vod_fetch_status 字段的注释
-- 反映新的状态值定义

ALTER TABLE mac_vod 
MODIFY COLUMN vod_fetch_status TINYINT(1) NOT NULL DEFAULT 1 
COMMENT '获取状态: 0=成功, 1=未处理, 2=多个结果, 3=搜索结果为空, 4=错误, 5=被限流, 6=匹配结果为空';

-- 验证更新
SHOW FULL COLUMNS FROM mac_vod WHERE Field = 'vod_fetch_status';
