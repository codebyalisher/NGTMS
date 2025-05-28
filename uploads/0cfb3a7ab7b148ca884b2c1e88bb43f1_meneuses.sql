-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 26, 2025 at 06:55 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ngtms_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `meneuses`
--

CREATE TABLE `meneuses` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `parent_id` bigint(20) UNSIGNED DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `page_path` text DEFAULT NULL,
  `encryption_salt` char(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `meneuses`
--

INSERT INTO `meneuses` (`id`, `name`, `parent_id`, `status`, `created_at`, `updated_at`, `page_path`, `encryption_salt`) VALUES
(7, 'Tickets', NULL, 1, '2025-05-14 17:39:26', '2025-05-14 17:39:26', 'eyJpdiI6Im41SXlrdHpWd001aHVKdTVhQUFTTFE9PSIsInZhbHVlIjoiR3l4WWJXTWdhdWdFMk9wbWc2YlI2VzJlajBabHFkK05xbVliWmZmTnVSN1hyYjZqQWdqbkc4VktQU0t4UzZBQldVZjA4dW1Hakc4TzJXclE0em41SHc9PSIsIm1hYyI6IjE1NzZiZTZlMzMwMjgyZmRlNGJjODliMDgwMzExZWFjYzA1ZTEwMmFjMmY1MmNiOWQyNTQ5ZTNiNjQ2NWMyMjAiLCJ0YWciOiIifQ==', 'd4fb9951-a2e4-4508-b927-476c1b17f551'),
(8, 'Timesheet', NULL, 1, '2025-05-14 17:39:57', '2025-05-14 17:39:57', 'eyJpdiI6IjRJNjlHb1lZTThaejdmbDdMNHlEeGc9PSIsInZhbHVlIjoiS3RDajM4dUhKTGFIUi9TS2kzMVhJa1N6eGwzUmVCL3FLbnEwdCt2aEF5bC9tQlNwdCtoNVlKNSthZy9qRGRyVWJKb25Ka1JlZGNyOVoyUVFSOHR1eHc9PSIsIm1hYyI6IjlmNGEyNjRkMWM1OWM2YWIwM2JmNjQ5N2EzOWFkNDY4NDA3NzIwYTZhY2UwZDU4OTA4ODdiNTE3MjUyZTE1NzAiLCJ0YWciOiIifQ==', 'b0bc7441-8449-4879-adca-b1e96b25b395');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `meneuses`
--
ALTER TABLE `meneuses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `encryption_salt` (`encryption_salt`),
  ADD KEY `meneuses_parent_id_foreign` (`parent_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `meneuses`
--
ALTER TABLE `meneuses`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `meneuses`
--
ALTER TABLE `meneuses`
  ADD CONSTRAINT `meneuses_parent_id_foreign` FOREIGN KEY (`parent_id`) REFERENCES `meneuses` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
