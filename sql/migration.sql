-- ============================================
-- MacCMS 豆瓣评分获取 - 数据库迁移脚本
-- 执行前请备份数据库！
-- ============================================

-- 1. 为 mac_vod 表添加新字段
ALTER TABLE `mac_vod` 
ADD COLUMN `vod_fetch_status` TINYINT(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '评分获取状态：1=未获取，0=获取成功，2=获取失败（多个结果），3=获取失败（无结果），4=获取失败（其他错误）',
ADD COLUMN `vod_imdb_id` VARCHAR(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT 'IMDB ID',
ADD COLUMN `vod_imdb_votes` MEDIUMINT(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'IMDB 投票人数',
ADD COLUMN `vod_imdb_rating` DECIMAL(3, 1) UNSIGNED NOT NULL DEFAULT 0.0 COMMENT 'IMDB 评分';

-- 2. 为 vod_fetch_status 添加索引以优化查询
ALTER TABLE `mac_vod` ADD INDEX `vod_fetch_status` (`vod_fetch_status`);

-- 3. 添加处理设备标识字段（用于多设备并发）
ALTER TABLE `mac_vod` 
ADD COLUMN `vod_fetch_worker` VARCHAR(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '处理设备标识',
ADD COLUMN `vod_fetch_time` INT(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '开始获取时间戳',
ADD COLUMN `vod_fetch_lock_time` INT(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '锁定时间戳';

-- 4. 为新增字段添加索引
ALTER TABLE `mac_vod` 
ADD INDEX `vod_fetch_worker` (`vod_fetch_worker`),
ADD INDEX `vod_fetch_lock_time` (`vod_fetch_lock_time`);

-- 5. 验证字段是否添加成功
SELECT 
    COLUMN_NAME,
    COLUMN_TYPE,
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'mac_vod'
  AND COLUMN_NAME IN ('vod_fetch_status', 'vod_imdb_id', 'vod_imdb_votes', 'vod_imdb_rating', 'vod_fetch_worker', 'vod_fetch_time', 'vod_fetch_lock_time');

-- 6. 查看当前待处理的视频数量
SELECT 
    vod_fetch_status,
    COUNT(*) as count
FROM mac_vod
GROUP BY vod_fetch_status;

-- 7. 查看各设备处理情况
SELECT 
    vod_fetch_worker,
    vod_fetch_status,
    COUNT(*) as count
FROM mac_vod
WHERE vod_fetch_worker != ''
GROUP BY vod_fetch_worker, vod_fetch_status;

-- ============================================
-- 说明：
-- vod_fetch_status 状态码：
--   1 = 未获取（默认值，待处理）
--   0 = 获取成功
--   2 = 获取失败（匹配到多个结果）
--   3 = 获取失败（无搜索结果）
--   4 = 获取失败（其他错误）
-- ============================================
