-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2022-04-27 15:26:23
-- 伺服器版本： 10.4.24-MariaDB
-- PHP 版本： 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫: `mydatabase`
--

-- --------------------------------------------------------

--
-- 資料表結構 `訂單管理資料`
--

CREATE TABLE `訂單管理資料` (
  `訂單編號` int(11) NOT NULL,
  `商品名稱` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `金額` int(11) NOT NULL,
  `備註` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `訂單狀況` varchar(16) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `訂單管理資料`
--

INSERT INTO `訂單管理資料` (`訂單編號`, `商品名稱`, `金額`, `備註`, `訂單狀況`) VALUES
(1, 'HONDA', 1500, '康先生', '未處理'),
(3, 'Tanga_v2.0', 1200, '吳先生', '結案'),
(25, '森田氣泡水', 20, '嘪先生\n', '未處理'),
(123, 'HONDA', 875, '林先生', '已收到'),
(142, 'Iphone 13 pro', 3200, 'Eric', '未處理'),
(851, '泡泡口香糖', 25, '梁小姐\n', '已收到'),
(1314, '愛上你', 120, '李小姐', '已寄出'),
(1420, '可口可樂', 30, '', '結案'),
(5211, '野狼125', 554, '李先生', '未處理'),
(5566, '人氣天團CD', 1254, '陳先生', '已寄出'),
(40678, 'BMW', 200, '張小姐', '結案'),
(46678, 'TOYOTA', 1000, '陳先生', '已寄出'),
(55688, '勞斯萊斯', 1288, '周先生', '未處理');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `訂單管理資料`
--
ALTER TABLE `訂單管理資料`
  ADD PRIMARY KEY (`訂單編號`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `訂單管理資料`
--
ALTER TABLE `訂單管理資料`
  MODIFY `訂單編號` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55689;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
