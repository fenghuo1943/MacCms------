/*
 Navicat Premium Dump SQL

 Source Server         : mariaDB10
 Source Server Type    : MariaDB
 Source Server Version : 101106 (10.11.6-MariaDB)
 Source Host           : 192.168.114.4:3307
 Source Schema         : maccms

 Target Server Type    : MariaDB
 Target Server Version : 101106 (10.11.6-MariaDB)
 File Encoding         : 65001

 Date: 15/04/2026 09:45:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for mac_actor
-- ----------------------------
DROP TABLE IF EXISTS `mac_actor`;
CREATE TABLE `mac_actor`  (
  `actor_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `type_id` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `type_id_1` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `actor_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_en` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_alias` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `actor_lock` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `actor_letter` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_sex` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_color` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_pic` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_blurb` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_area` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_height` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_weight` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_birthday` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_birtharea` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_blood` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_starsign` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_school` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_works` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_tag` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_class` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_level` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `actor_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `actor_time_add` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `actor_time_hits` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `actor_time_make` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `actor_hits` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `actor_hits_day` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `actor_hits_week` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `actor_hits_month` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `actor_score` decimal(3, 1) UNSIGNED NOT NULL DEFAULT 0.0,
  `actor_score_all` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `actor_score_num` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `actor_up` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `actor_down` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `actor_tpl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_jumpurl` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `actor_content` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`actor_id`) USING BTREE,
  INDEX `type_id`(`type_id`) USING BTREE,
  INDEX `type_id_1`(`type_id_1`) USING BTREE,
  INDEX `actor_name`(`actor_name`) USING BTREE,
  INDEX `actor_en`(`actor_en`) USING BTREE,
  INDEX `actor_letter`(`actor_letter`) USING BTREE,
  INDEX `actor_level`(`actor_level`) USING BTREE,
  INDEX `actor_time`(`actor_time`) USING BTREE,
  INDEX `actor_time_add`(`actor_time_add`) USING BTREE,
  INDEX `actor_sex`(`actor_sex`) USING BTREE,
  INDEX `actor_area`(`actor_area`) USING BTREE,
  INDEX `actor_up`(`actor_up`) USING BTREE,
  INDEX `actor_down`(`actor_down`) USING BTREE,
  INDEX `actor_tag`(`actor_tag`) USING BTREE,
  INDEX `actor_class`(`actor_class`) USING BTREE,
  INDEX `actor_score`(`actor_score`) USING BTREE,
  INDEX `actor_score_all`(`actor_score_all`) USING BTREE,
  INDEX `actor_score_num`(`actor_score_num`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_admin
-- ----------------------------
DROP TABLE IF EXISTS `mac_admin`;
CREATE TABLE `mac_admin`  (
  `admin_id` smallint(6) UNSIGNED NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `admin_pwd` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `admin_random` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `admin_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `admin_auth` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `admin_login_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `admin_login_ip` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `admin_login_num` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `admin_last_login_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `admin_last_login_ip` int(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`admin_id`) USING BTREE,
  INDEX `admin_name`(`admin_name`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_annex
-- ----------------------------
DROP TABLE IF EXISTS `mac_annex`;
CREATE TABLE `mac_annex`  (
  `annex_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `annex_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `annex_file` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `annex_size` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `annex_type` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`annex_id`) USING BTREE,
  INDEX `annex_time`(`annex_time`) USING BTREE,
  INDEX `annex_file`(`annex_file`) USING BTREE,
  INDEX `annex_type`(`annex_type`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 134 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_art
-- ----------------------------
DROP TABLE IF EXISTS `mac_art`;
CREATE TABLE `mac_art`  (
  `art_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `type_id` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `type_id_1` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `group_id` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `art_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_sub` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_en` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `art_letter` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_color` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_from` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_author` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_tag` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_class` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_pic` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_pic_thumb` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_pic_slide` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_pic_screenshot` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `art_blurb` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_jumpurl` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_tpl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_level` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `art_lock` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `art_points` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `art_points_detail` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `art_up` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `art_down` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `art_hits` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `art_hits_day` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `art_hits_week` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `art_hits_month` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `art_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `art_time_add` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `art_time_hits` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `art_time_make` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `art_score` decimal(3, 1) UNSIGNED NOT NULL DEFAULT 0.0,
  `art_score_all` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `art_score_num` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `art_rel_art` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_rel_vod` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_pwd` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_pwd_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `art_title` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `art_note` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `art_content` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`art_id`) USING BTREE,
  INDEX `type_id`(`type_id`) USING BTREE,
  INDEX `type_id_1`(`type_id_1`) USING BTREE,
  INDEX `art_level`(`art_level`) USING BTREE,
  INDEX `art_hits`(`art_hits`) USING BTREE,
  INDEX `art_time`(`art_time`) USING BTREE,
  INDEX `art_letter`(`art_letter`) USING BTREE,
  INDEX `art_down`(`art_down`) USING BTREE,
  INDEX `art_up`(`art_up`) USING BTREE,
  INDEX `art_tag`(`art_tag`) USING BTREE,
  INDEX `art_name`(`art_name`) USING BTREE,
  INDEX `art_enn`(`art_en`) USING BTREE,
  INDEX `art_hits_day`(`art_hits_day`) USING BTREE,
  INDEX `art_hits_week`(`art_hits_week`) USING BTREE,
  INDEX `art_hits_month`(`art_hits_month`) USING BTREE,
  INDEX `art_time_add`(`art_time_add`) USING BTREE,
  INDEX `art_time_make`(`art_time_make`) USING BTREE,
  INDEX `art_lock`(`art_lock`) USING BTREE,
  INDEX `art_score`(`art_score`) USING BTREE,
  INDEX `art_score_all`(`art_score_all`) USING BTREE,
  INDEX `art_score_num`(`art_score_num`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_card
-- ----------------------------
DROP TABLE IF EXISTS `mac_card`;
CREATE TABLE `mac_card`  (
  `card_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `card_no` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `card_pwd` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `card_money` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `card_points` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `card_use_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `card_sale_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `user_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `card_add_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `card_use_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`card_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `card_add_time`(`card_add_time`) USING BTREE,
  INDEX `card_use_time`(`card_use_time`) USING BTREE,
  INDEX `card_no`(`card_no`) USING BTREE,
  INDEX `card_pwd`(`card_pwd`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_cash
-- ----------------------------
DROP TABLE IF EXISTS `mac_cash`;
CREATE TABLE `mac_cash`  (
  `cash_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `cash_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `cash_points` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `cash_money` decimal(12, 2) UNSIGNED NOT NULL DEFAULT 0.00,
  `cash_bank_name` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `cash_bank_no` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `cash_payee_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `cash_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `cash_time_audit` int(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`cash_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `cash_status`(`cash_status`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_cj_content
-- ----------------------------
DROP TABLE IF EXISTS `mac_cj_content`;
CREATE TABLE `mac_cj_content`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `nodeid` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `url` char(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `title` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `data` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `nodeid`(`nodeid`) USING BTREE,
  INDEX `status`(`status`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_cj_history
-- ----------------------------
DROP TABLE IF EXISTS `mac_cj_history`;
CREATE TABLE `mac_cj_history`  (
  `md5` char(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`md5`) USING BTREE,
  INDEX `md5`(`md5`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Fixed;

-- ----------------------------
-- Table structure for mac_cj_node
-- ----------------------------
DROP TABLE IF EXISTS `mac_cj_node`;
CREATE TABLE `mac_cj_node`  (
  `nodeid` smallint(6) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `lastdate` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `sourcecharset` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `sourcetype` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `urlpage` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `pagesize_start` tinyint(3) UNSIGNED NOT NULL DEFAULT 0,
  `pagesize_end` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `page_base` char(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `par_num` tinyint(3) UNSIGNED NOT NULL DEFAULT 1,
  `url_contain` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `url_except` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `url_start` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `url_end` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `title_rule` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `title_html_rule` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `type_rule` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `type_html_rule` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `content_rule` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `content_html_rule` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `content_page_start` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `content_page_end` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `content_page_rule` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `content_page` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `content_nextpage` char(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `down_attachment` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `watermark` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `coll_order` tinyint(3) UNSIGNED NOT NULL DEFAULT 0,
  `customize_config` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `program_config` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `mid` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (`nodeid`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_collect
-- ----------------------------
DROP TABLE IF EXISTS `mac_collect`;
CREATE TABLE `mac_collect`  (
  `collect_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `collect_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `collect_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `collect_type` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `collect_mid` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `collect_appid` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `collect_appkey` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `collect_param` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `collect_filter` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `collect_filter_from` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `collect_filter_year` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '采集时，过滤年份',
  `collect_opt` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `collect_sync_pic_opt` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '同步图片选项，0-跟随全局，1-开启，2-关闭',
  PRIMARY KEY (`collect_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_comment
-- ----------------------------
DROP TABLE IF EXISTS `mac_comment`;
CREATE TABLE `mac_comment`  (
  `comment_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `comment_mid` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `comment_rid` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `comment_pid` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `comment_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `comment_name` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `comment_ip` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `comment_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `comment_content` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `comment_up` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `comment_down` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `comment_reply` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `comment_report` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `comment_mid`(`comment_mid`) USING BTREE,
  INDEX `comment_rid`(`comment_rid`) USING BTREE,
  INDEX `comment_time`(`comment_time`) USING BTREE,
  INDEX `comment_pid`(`comment_pid`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `comment_reply`(`comment_reply`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_gbook
-- ----------------------------
DROP TABLE IF EXISTS `mac_gbook`;
CREATE TABLE `mac_gbook`  (
  `gbook_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `gbook_rid` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `gbook_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `gbook_name` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `gbook_ip` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `gbook_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `gbook_reply_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `gbook_content` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `gbook_reply` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`gbook_id`) USING BTREE,
  INDEX `gbook_rid`(`gbook_rid`) USING BTREE,
  INDEX `gbook_time`(`gbook_time`) USING BTREE,
  INDEX `gbook_reply_time`(`gbook_reply_time`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `gbook_reply`(`gbook_reply`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_group
-- ----------------------------
DROP TABLE IF EXISTS `mac_group`;
CREATE TABLE `mac_group`  (
  `group_id` smallint(6) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `group_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `group_type` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `group_popedom` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `group_points_day` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `group_points_week` smallint(6) NOT NULL DEFAULT 0,
  `group_points_month` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `group_points_year` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `group_points_free` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`group_id`) USING BTREE,
  INDEX `group_status`(`group_status`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 4 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_link
-- ----------------------------
DROP TABLE IF EXISTS `mac_link`;
CREATE TABLE `mac_link`  (
  `link_id` smallint(6) UNSIGNED NOT NULL AUTO_INCREMENT,
  `link_type` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `link_name` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `link_sort` smallint(6) NOT NULL DEFAULT 0,
  `link_add_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `link_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `link_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `link_logo` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`link_id`) USING BTREE,
  INDEX `link_sort`(`link_sort`) USING BTREE,
  INDEX `link_type`(`link_type`) USING BTREE,
  INDEX `link_add_time`(`link_add_time`) USING BTREE,
  INDEX `link_time`(`link_time`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_malicious_domain
-- ----------------------------
DROP TABLE IF EXISTS `mac_malicious_domain`;
CREATE TABLE `mac_malicious_domain`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `domain` varchar(190) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '恶意域名或特征',
  `type` tinyint(1) NOT NULL DEFAULT 1 COMMENT '类型：1=域名 2=IP 3=JS特征',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '状态：1=启用 0=禁用',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '备注',
  `addtime` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '添加时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_domain`(`domain` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 59 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '恶意域名黑名单' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_manga
-- ----------------------------
DROP TABLE IF EXISTS `mac_manga`;
CREATE TABLE `mac_manga`  (
  `manga_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '漫画ID',
  `type_id` smallint(6) UNSIGNED NOT NULL DEFAULT 0 COMMENT '主分类ID',
  `type_id_1` smallint(6) UNSIGNED NOT NULL DEFAULT 0 COMMENT '副分类ID',
  `group_id` smallint(6) UNSIGNED NOT NULL DEFAULT 0 COMMENT '会员组ID',
  `manga_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '漫画名称',
  `manga_sub` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '副标题',
  `manga_en` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '英文名',
  `manga_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '状态(0=锁定,1=正常)',
  `manga_letter` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '首字母',
  `manga_color` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '标题颜色',
  `manga_from` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '来源',
  `manga_author` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '作者',
  `manga_tag` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '标签',
  `manga_class` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '扩展分类',
  `manga_pic` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '封面图',
  `manga_pic_thumb` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '封面缩略图',
  `manga_pic_slide` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '封面幻灯图',
  `manga_pic_screenshot` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '内容截图',
  `manga_blurb` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '简介',
  `manga_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '备注(例如：更新至xx话)',
  `manga_jumpurl` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '跳转URL',
  `manga_tpl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '独立模板',
  `manga_level` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '推荐级别',
  `manga_lock` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '锁定状态(0=未锁,1=已锁)',
  `manga_points` smallint(6) UNSIGNED NOT NULL DEFAULT 0 COMMENT '点播所需积分',
  `manga_points_detail` smallint(6) UNSIGNED NOT NULL DEFAULT 0 COMMENT '每章所需积分',
  `manga_up` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '顶数',
  `manga_down` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '踩数',
  `manga_hits` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '总点击数',
  `manga_hits_day` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '日点击数',
  `manga_hits_week` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '周点击数',
  `manga_hits_month` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '月点击数',
  `manga_time` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '更新时间',
  `manga_time_add` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '添加时间',
  `manga_time_hits` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '点击时间',
  `manga_time_make` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '生成时间',
  `manga_score` decimal(3, 1) UNSIGNED NOT NULL DEFAULT 0.0 COMMENT '平均评分',
  `manga_score_all` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '总评分',
  `manga_score_num` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '评分次数',
  `manga_rel_manga` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '关联漫画',
  `manga_rel_vod` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '关联视频',
  `manga_pwd` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '访问密码',
  `manga_pwd_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '密码跳转URL',
  `manga_content` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '详细介绍',
  `manga_serial` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '0' COMMENT '连载状态(文字)',
  `manga_total` mediumint(8) UNSIGNED NOT NULL DEFAULT 0 COMMENT '总章节数',
  `manga_chapter_from` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '章节来源',
  `manga_chapter_url` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '章节URL列表',
  `manga_last_update_time` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '最后更新时间戳',
  `manga_age_rating` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '年龄分级(0=全年龄,1=12+,2=18+)',
  `manga_orientation` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '阅读方向(1=左到右,2=右到左,3=垂直)',
  `manga_is_vip` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否VIP(0=否,1=是)',
  `manga_copyright_info` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '版权信息',
  PRIMARY KEY (`manga_id`) USING BTREE,
  INDEX `type_id`(`type_id`) USING BTREE,
  INDEX `type_id_1`(`type_id_1`) USING BTREE,
  INDEX `manga_level`(`manga_level`) USING BTREE,
  INDEX `manga_hits`(`manga_hits`) USING BTREE,
  INDEX `manga_time`(`manga_time`) USING BTREE,
  INDEX `manga_letter`(`manga_letter`) USING BTREE,
  INDEX `manga_down`(`manga_down`) USING BTREE,
  INDEX `manga_up`(`manga_up`) USING BTREE,
  INDEX `manga_tag`(`manga_tag`) USING BTREE,
  INDEX `manga_name`(`manga_name`) USING BTREE,
  INDEX `manga_en`(`manga_en`) USING BTREE,
  INDEX `manga_hits_day`(`manga_hits_day`) USING BTREE,
  INDEX `manga_hits_week`(`manga_hits_week`) USING BTREE,
  INDEX `manga_hits_month`(`manga_hits_month`) USING BTREE,
  INDEX `manga_time_add`(`manga_time_add`) USING BTREE,
  INDEX `manga_time_make`(`manga_time_make`) USING BTREE,
  INDEX `manga_lock`(`manga_lock`) USING BTREE,
  INDEX `manga_score`(`manga_score`) USING BTREE,
  INDEX `manga_score_all`(`manga_score_all`) USING BTREE,
  INDEX `manga_score_num`(`manga_score_num`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '漫画表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_msg
-- ----------------------------
DROP TABLE IF EXISTS `mac_msg`;
CREATE TABLE `mac_msg`  (
  `msg_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `msg_type` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `msg_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `msg_to` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `msg_code` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `msg_content` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `msg_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`msg_id`) USING BTREE,
  INDEX `msg_code`(`msg_code`) USING BTREE,
  INDEX `msg_time`(`msg_time`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_order
-- ----------------------------
DROP TABLE IF EXISTS `mac_order`;
CREATE TABLE `mac_order`  (
  `order_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `order_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `order_code` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `order_price` decimal(12, 2) UNSIGNED NOT NULL DEFAULT 0.00,
  `order_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `order_points` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `order_pay_type` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `order_pay_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `order_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `order_code`(`order_code`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `order_time`(`order_time`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_plog
-- ----------------------------
DROP TABLE IF EXISTS `mac_plog`;
CREATE TABLE `mac_plog`  (
  `plog_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_id_1` int(10) NOT NULL DEFAULT 0,
  `plog_type` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `plog_points` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `plog_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `plog_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`plog_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `plog_type`(`plog_type`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_role
-- ----------------------------
DROP TABLE IF EXISTS `mac_role`;
CREATE TABLE `mac_role`  (
  `role_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_rid` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `role_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_en` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `role_lock` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `role_letter` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_color` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_actor` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_pic` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_sort` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `role_level` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `role_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `role_time_add` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `role_time_hits` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `role_time_make` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `role_hits` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `role_hits_day` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `role_hits_week` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `role_hits_month` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `role_score` decimal(3, 1) UNSIGNED NOT NULL DEFAULT 0.0,
  `role_score_all` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `role_score_num` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `role_up` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `role_down` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `role_tpl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_jumpurl` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `role_content` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`role_id`) USING BTREE,
  INDEX `role_rid`(`role_rid`) USING BTREE,
  INDEX `role_name`(`role_name`) USING BTREE,
  INDEX `role_en`(`role_en`) USING BTREE,
  INDEX `role_letter`(`role_letter`) USING BTREE,
  INDEX `role_actor`(`role_actor`) USING BTREE,
  INDEX `role_level`(`role_level`) USING BTREE,
  INDEX `role_time`(`role_time`) USING BTREE,
  INDEX `role_time_add`(`role_time_add`) USING BTREE,
  INDEX `role_score`(`role_score`) USING BTREE,
  INDEX `role_score_all`(`role_score_all`) USING BTREE,
  INDEX `role_score_num`(`role_score_num`) USING BTREE,
  INDEX `role_up`(`role_up`) USING BTREE,
  INDEX `role_down`(`role_down`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_seo_script
-- ----------------------------
DROP TABLE IF EXISTS `mac_seo_script`;
CREATE TABLE `mac_seo_script`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '脚本名称',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '脚本内容',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '状态：1=启用 0=禁用',
  `addtime` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '添加时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '移动端SEO统计脚本' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_topic
-- ----------------------------
DROP TABLE IF EXISTS `mac_topic`;
CREATE TABLE `mac_topic`  (
  `topic_id` smallint(6) UNSIGNED NOT NULL AUTO_INCREMENT,
  `topic_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_en` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_sub` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `topic_sort` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `topic_letter` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_color` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_tpl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_type` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_pic` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_pic_thumb` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_pic_slide` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_key` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_des` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_blurb` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_level` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `topic_up` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `topic_down` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `topic_score` decimal(3, 1) UNSIGNED NOT NULL DEFAULT 0.0,
  `topic_score_all` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `topic_score_num` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `topic_hits` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `topic_hits_day` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `topic_hits_week` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `topic_hits_month` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `topic_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `topic_time_add` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `topic_time_hits` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `topic_time_make` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `topic_tag` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `topic_rel_vod` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `topic_rel_art` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `topic_content` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `topic_extend` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`topic_id`) USING BTREE,
  INDEX `topic_sort`(`topic_sort`) USING BTREE,
  INDEX `topic_level`(`topic_level`) USING BTREE,
  INDEX `topic_score`(`topic_score`) USING BTREE,
  INDEX `topic_score_all`(`topic_score_all`) USING BTREE,
  INDEX `topic_score_num`(`topic_score_num`) USING BTREE,
  INDEX `topic_hits`(`topic_hits`) USING BTREE,
  INDEX `topic_hits_day`(`topic_hits_day`) USING BTREE,
  INDEX `topic_hits_week`(`topic_hits_week`) USING BTREE,
  INDEX `topic_hits_month`(`topic_hits_month`) USING BTREE,
  INDEX `topic_time_add`(`topic_time_add`) USING BTREE,
  INDEX `topic_time`(`topic_time`) USING BTREE,
  INDEX `topic_time_hits`(`topic_time_hits`) USING BTREE,
  INDEX `topic_name`(`topic_name`) USING BTREE,
  INDEX `topic_en`(`topic_en`) USING BTREE,
  INDEX `topic_up`(`topic_up`) USING BTREE,
  INDEX `topic_down`(`topic_down`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_type
-- ----------------------------
DROP TABLE IF EXISTS `mac_type`;
CREATE TABLE `mac_type`  (
  `type_id` smallint(6) UNSIGNED NOT NULL AUTO_INCREMENT,
  `type_name` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_en` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_sort` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `type_mid` smallint(6) UNSIGNED NOT NULL DEFAULT 1,
  `type_pid` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `type_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `type_tpl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_tpl_list` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_tpl_detail` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_tpl_play` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_tpl_down` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_key` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_des` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_union` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_extend` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `type_logo` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_pic` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `type_jumpurl` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`type_id`) USING BTREE,
  INDEX `type_sort`(`type_sort`) USING BTREE,
  INDEX `type_pid`(`type_pid`) USING BTREE,
  INDEX `type_name`(`type_name`) USING BTREE,
  INDEX `type_en`(`type_en`) USING BTREE,
  INDEX `type_mid`(`type_mid`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 37 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_ulog
-- ----------------------------
DROP TABLE IF EXISTS `mac_ulog`;
CREATE TABLE `mac_ulog`  (
  `ulog_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `ulog_mid` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `ulog_type` tinyint(1) UNSIGNED NOT NULL DEFAULT 1,
  `ulog_rid` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `ulog_sid` tinyint(3) UNSIGNED NOT NULL DEFAULT 0,
  `ulog_nid` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `ulog_points` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `ulog_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`ulog_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ulog_mid`(`ulog_mid`) USING BTREE,
  INDEX `ulog_type`(`ulog_type`) USING BTREE,
  INDEX `ulog_rid`(`ulog_rid`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Fixed;

-- ----------------------------
-- Table structure for mac_user
-- ----------------------------
DROP TABLE IF EXISTS `mac_user`;
CREATE TABLE `mac_user`  (
  `user_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `group_id` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '0' COMMENT '会员组ID,多个用逗号分隔',
  `user_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_pwd` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_nick_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_qq` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_email` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_phone` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `user_portrait` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_portrait_thumb` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_openid_qq` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_openid_weixin` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_question` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_answer` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_points` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_points_froze` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_reg_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_reg_ip` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_login_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_login_ip` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_last_login_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_last_login_ip` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_login_num` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `user_extend` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `user_random` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `user_end_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_pid` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_pid_2` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `user_pid_3` int(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`) USING BTREE,
  INDEX `type_id`(`group_id`) USING BTREE,
  INDEX `user_name`(`user_name`) USING BTREE,
  INDEX `user_reg_time`(`user_reg_time`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_visit
-- ----------------------------
DROP TABLE IF EXISTS `mac_visit`;
CREATE TABLE `mac_visit`  (
  `visit_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int(10) UNSIGNED NULL DEFAULT 0,
  `visit_ip` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `visit_ly` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `visit_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`visit_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `visit_time`(`visit_time`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_vod
-- ----------------------------
DROP TABLE IF EXISTS `mac_vod`;
CREATE TABLE `mac_vod`  (
  `vod_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `type_id` smallint(6) NOT NULL DEFAULT 0,
  `type_id_1` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `group_id` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `vod_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_sub` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_en` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `vod_letter` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_color` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_tag` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_class` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pic` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pic_thumb` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pic_slide` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pic_screenshot` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `vod_actor` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_director` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_writer` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_behind` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_blurb` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pubdate` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_total` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_serial` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '0',
  `vod_tv` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_weekday` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_area` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_lang` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_year` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_version` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_state` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_author` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_jumpurl` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_tpl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_tpl_play` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_tpl_down` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_isend` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `vod_lock` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `vod_level` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `vod_copyright` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `vod_points` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `vod_points_play` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `vod_points_down` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `vod_hits` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_hits_day` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_hits_week` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_hits_month` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_duration` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_up` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_down` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_score` decimal(3, 1) UNSIGNED NOT NULL DEFAULT 0.0,
  `vod_score_all` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_score_num` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `vod_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `vod_time_add` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `vod_time_hits` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `vod_time_make` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `vod_trysee` smallint(6) UNSIGNED NOT NULL DEFAULT 0,
  `vod_douban_id` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `vod_douban_score` decimal(3, 1) UNSIGNED NOT NULL DEFAULT 0.0,
  `vod_reurl` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_rel_vod` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_rel_art` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pwd` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pwd_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pwd_play` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pwd_play_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pwd_down` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_pwd_down_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_content` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `vod_play_from` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_play_server` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_play_note` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_play_url` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `vod_down_from` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_down_server` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_down_note` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `vod_down_url` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `vod_plot` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `vod_plot_name` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `vod_plot_detail` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`vod_id`) USING BTREE,
  INDEX `type_id`(`type_id`) USING BTREE,
  INDEX `type_id_1`(`type_id_1`) USING BTREE,
  INDEX `vod_level`(`vod_level`) USING BTREE,
  INDEX `vod_hits`(`vod_hits`) USING BTREE,
  INDEX `vod_letter`(`vod_letter`) USING BTREE,
  INDEX `vod_name`(`vod_name`) USING BTREE,
  INDEX `vod_year`(`vod_year`) USING BTREE,
  INDEX `vod_area`(`vod_area`) USING BTREE,
  INDEX `vod_lang`(`vod_lang`) USING BTREE,
  INDEX `vod_tag`(`vod_tag`) USING BTREE,
  INDEX `vod_class`(`vod_class`) USING BTREE,
  INDEX `vod_lock`(`vod_lock`) USING BTREE,
  INDEX `vod_up`(`vod_up`) USING BTREE,
  INDEX `vod_down`(`vod_down`) USING BTREE,
  INDEX `vod_en`(`vod_en`) USING BTREE,
  INDEX `vod_hits_day`(`vod_hits_day`) USING BTREE,
  INDEX `vod_hits_week`(`vod_hits_week`) USING BTREE,
  INDEX `vod_hits_month`(`vod_hits_month`) USING BTREE,
  INDEX `vod_plot`(`vod_plot`) USING BTREE,
  INDEX `vod_points_play`(`vod_points_play`) USING BTREE,
  INDEX `vod_points_down`(`vod_points_down`) USING BTREE,
  INDEX `group_id`(`group_id`) USING BTREE,
  INDEX `vod_time_add`(`vod_time_add`) USING BTREE,
  INDEX `vod_time`(`vod_time`) USING BTREE,
  INDEX `vod_time_make`(`vod_time_make`) USING BTREE,
  INDEX `vod_actor`(`vod_actor`) USING BTREE,
  INDEX `vod_director`(`vod_director`) USING BTREE,
  INDEX `vod_score_all`(`vod_score_all`) USING BTREE,
  INDEX `vod_score_num`(`vod_score_num`) USING BTREE,
  INDEX `vod_total`(`vod_total`) USING BTREE,
  INDEX `vod_score`(`vod_score`) USING BTREE,
  INDEX `vod_version`(`vod_version`) USING BTREE,
  INDEX `vod_state`(`vod_state`) USING BTREE,
  INDEX `vod_isend`(`vod_isend`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 9271 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_vod_repeat
-- ----------------------------
DROP TABLE IF EXISTS `mac_vod_repeat`;
CREATE TABLE `mac_vod_repeat`  (
  `id1` int(10) UNSIGNED NULL DEFAULT NULL,
  `name1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  INDEX `name1`(`name1`(100) ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_vod_search
-- ----------------------------
DROP TABLE IF EXISTS `mac_vod_search`;
CREATE TABLE `mac_vod_search`  (
  `search_key` char(32) CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '搜索键（关键词md5）',
  `search_word` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '搜索关键词',
  `search_field` varchar(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '搜索字段名（可有多个，用|分隔）',
  `search_hit_count` bigint(20) UNSIGNED NOT NULL DEFAULT 0 COMMENT '搜索命中次数',
  `search_last_hit_time` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '最近命中时间',
  `search_update_time` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '添加时间',
  `search_result_count` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT '结果Id数量',
  `search_result_ids` mediumtext CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '搜索结果Id列表，英文半角逗号分隔',
  PRIMARY KEY (`search_key`) USING BTREE,
  INDEX `search_field`(`search_field` ASC) USING BTREE,
  INDEX `search_update_time`(`search_update_time` ASC) USING BTREE,
  INDEX `search_hit_count`(`search_hit_count` ASC) USING BTREE,
  INDEX `search_last_hit_time`(`search_last_hit_time` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'vod搜索缓存表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mac_website
-- ----------------------------
DROP TABLE IF EXISTS `mac_website`;
CREATE TABLE `mac_website`  (
  `website_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `type_id` smallint(5) UNSIGNED NOT NULL DEFAULT 0,
  `type_id_1` smallint(5) UNSIGNED NOT NULL DEFAULT 0,
  `website_name` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_sub` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_en` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_status` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `website_letter` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_color` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_lock` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `website_sort` int(10) NOT NULL DEFAULT 0,
  `website_jumpurl` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_pic` varchar(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_pic_screenshot` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `website_logo` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_area` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_lang` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_level` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `website_time` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `website_time_add` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `website_time_hits` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `website_time_make` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `website_time_referer` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `website_hits` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_hits_day` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_hits_week` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_hits_month` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_score` decimal(3, 1) UNSIGNED NOT NULL DEFAULT 0.0,
  `website_score_all` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_score_num` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_up` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_down` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_referer` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_referer_day` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_referer_week` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_referer_month` mediumint(8) UNSIGNED NOT NULL DEFAULT 0,
  `website_tag` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_class` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_remarks` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_tpl` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_blurb` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '',
  `website_content` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`website_id`) USING BTREE,
  INDEX `type_id`(`type_id`) USING BTREE,
  INDEX `type_id_1`(`type_id_1`) USING BTREE,
  INDEX `website_name`(`website_name`) USING BTREE,
  INDEX `website_en`(`website_en`) USING BTREE,
  INDEX `website_letter`(`website_letter`) USING BTREE,
  INDEX `website_sort`(`website_sort`) USING BTREE,
  INDEX `website_lock`(`website_lock`) USING BTREE,
  INDEX `website_time`(`website_time`) USING BTREE,
  INDEX `website_time_add`(`website_time_add`) USING BTREE,
  INDEX `website_time_referer`(`website_time_referer`) USING BTREE,
  INDEX `website_hits`(`website_hits`) USING BTREE,
  INDEX `website_hits_day`(`website_hits_day`) USING BTREE,
  INDEX `website_hits_week`(`website_hits_week`) USING BTREE,
  INDEX `website_hits_month`(`website_hits_month`) USING BTREE,
  INDEX `website_time_make`(`website_time_make`) USING BTREE,
  INDEX `website_score`(`website_score`) USING BTREE,
  INDEX `website_score_all`(`website_score_all`) USING BTREE,
  INDEX `website_score_num`(`website_score_num`) USING BTREE,
  INDEX `website_up`(`website_up`) USING BTREE,
  INDEX `website_down`(`website_down`) USING BTREE,
  INDEX `website_level`(`website_level`) USING BTREE,
  INDEX `website_tag`(`website_tag`) USING BTREE,
  INDEX `website_class`(`website_class`) USING BTREE,
  INDEX `website_referer`(`website_referer`) USING BTREE,
  INDEX `website_referer_day`(`website_referer_day`) USING BTREE,
  INDEX `website_referer_week`(`website_referer_week`) USING BTREE,
  INDEX `website_referer_month`(`website_referer_month`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
