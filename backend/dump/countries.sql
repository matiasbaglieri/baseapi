/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.1.3
 Source Server Type    : MySQL
 Source Server Version : 50737
 Source Host           : localhost:3306
 Source Schema         : baseapi

 Target Server Type    : MySQL
 Target Server Version : 50737
 File Encoding         : 65001

 Date: 08/06/2025 19:22:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for countries
-- ----------------------------
DROP TABLE IF EXISTS `countries`;
CREATE TABLE `countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) DEFAULT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `iso3` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `iso2` varchar(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numeric_code` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phonecode` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `capital` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `currency` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `currency_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `currency_symbol` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tld` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `native` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nationality` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timezones` json DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `emoji` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `emojiU` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `region` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subregion` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_countries_iso3` (`iso3`),
  KEY `ix_countries_iso2` (`iso2`),
  KEY `ix_countries_country_id` (`country_id`),
  KEY `ix_countries_name` (`name`),
  KEY `ix_countries_region` (`region`),
  KEY `ix_countries_subregion` (`subregion`),
  KEY `ix_countries_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=250 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of countries
-- ----------------------------
BEGIN;
INSERT INTO `countries` VALUES (1, 2, 'Aland Islands', 'ALA', 'AX', '248', '+358', 'Mariehamn', 'EUR', 'Euro', '€', '.ax', 'Åland', 'Aland Island', 'null', 60.1167, 19.9, '🇦🇽', 'U+1F1E6 U+1F1FD', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (2, 3, 'Albania', 'ALB', 'AL', '008', '+355', 'Tirana', 'ALL', 'Albanian lek', 'Lek', '.al', 'Shqipëria', 'Albanian ', 'null', 41, 20, '🇦🇱', 'U+1F1E6 U+1F1F1', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (3, 4, 'Algeria', 'DZA', 'DZ', '012', '+213', 'Algiers', 'DZD', 'Algerian dinar', 'دج', '.dz', 'الجزائر', 'Algerian', 'null', 28, 3, '🇩🇿', 'U+1F1E9 U+1F1FF', 'Africa', 'Northern Africa');
INSERT INTO `countries` VALUES (4, 5, 'American Samoa', 'ASM', 'AS', '016', '+1', 'Pago Pago', 'USD', 'United States dollar', '$', '.as', 'American Samoa', 'American Samoan', 'null', -14.3333, -170, '🇦🇸', 'U+1F1E6 U+1F1F8', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (5, 6, 'Andorra', 'AND', 'AD', '020', '+376', 'Andorra la Vella', 'EUR', 'Euro', '€', '.ad', 'Andorra', 'Andorran', 'null', 42.5, 1.5, '🇦🇩', 'U+1F1E6 U+1F1E9', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (6, 7, 'Angola', 'AGO', 'AO', '024', '+244', 'Luanda', 'AOA', 'Angolan kwanza', 'Kz', '.ao', 'Angola', 'Angolan', 'null', -12.5, 18.5, '🇦🇴', 'U+1F1E6 U+1F1F4', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (7, 8, 'Anguilla', 'AIA', 'AI', '660', '+1', 'The Valley', 'XCD', 'Eastern Caribbean dollar', '$', '.ai', 'Anguilla', 'Anguillan', 'null', 18.25, -63.1667, '🇦🇮', 'U+1F1E6 U+1F1EE', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (8, 9, 'Antarctica', 'ATA', 'AQ', '010', '+672', NULL, 'AAD', 'Antarctican dollar', '$', '.aq', 'Antarctica', 'Antarctic', 'null', -74.65, 4.48, '🇦🇶', 'U+1F1E6 U+1F1F6', 'Polar', NULL);
INSERT INTO `countries` VALUES (9, 10, 'Antigua and Barbuda', 'ATG', 'AG', '028', '+1', 'St. John\'s', 'XCD', 'Eastern Caribbean dollar', '$', '.ag', 'Antigua and Barbuda', 'Antiguan or Barbudan', 'null', 17.05, -61.8, '🇦🇬', 'U+1F1E6 U+1F1EC', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (10, 11, 'Argentina', 'ARG', 'AR', '032', '+54', 'Buenos Aires', 'ARS', 'Argentine peso', '$', '.ar', 'Argentina', 'Argentine', 'null', -34, -64, '🇦🇷', 'U+1F1E6 U+1F1F7', 'Americas', 'South America');
INSERT INTO `countries` VALUES (11, 12, 'Armenia', 'ARM', 'AM', '051', '+374', 'Yerevan', 'AMD', 'Armenian dram', '֏', '.am', 'Հայաստան', 'Armenian', 'null', 40, 45, '🇦🇲', 'U+1F1E6 U+1F1F2', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (12, 13, 'Aruba', 'ABW', 'AW', '533', '+297', 'Oranjestad', 'AWG', 'Aruban florin', 'ƒ', '.aw', 'Aruba', 'Aruban', 'null', 12.5, -69.9667, '🇦🇼', 'U+1F1E6 U+1F1FC', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (13, 14, 'Australia', 'AUS', 'AU', '036', '+61', 'Canberra', 'AUD', 'Australian dollar', '$', '.au', 'Australia', 'Australian', 'null', -27, 133, '🇦🇺', 'U+1F1E6 U+1F1FA', 'Oceania', 'Australia and New Zealand');
INSERT INTO `countries` VALUES (14, 15, 'Austria', 'AUT', 'AT', '040', '+43', 'Vienna', 'EUR', 'Euro', '€', '.at', 'Österreich', 'Austrian', 'null', 47.3333, 13.3333, '🇦🇹', 'U+1F1E6 U+1F1F9', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (15, 16, 'Azerbaijan', 'AZE', 'AZ', '031', '+994', 'Baku', 'AZN', 'Azerbaijani manat', 'm', '.az', 'Azərbaycan', 'Azerbaijani, Azeri', 'null', 40.5, 47.5, '🇦🇿', 'U+1F1E6 U+1F1FF', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (16, 18, 'Bahrain', 'BHR', 'BH', '048', '+973', 'Manama', 'BHD', 'Bahraini dinar', '.د.ب', '.bh', '‏البحرين', 'Bahraini', 'null', 26, 50.55, '🇧🇭', 'U+1F1E7 U+1F1ED', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (17, 19, 'Bangladesh', 'BGD', 'BD', '050', '+880', 'Dhaka', 'BDT', 'Bangladeshi taka', '৳', '.bd', 'Bangladesh', 'Bangladeshi', 'null', 24, 90, '🇧🇩', 'U+1F1E7 U+1F1E9', 'Asia', 'Southern Asia');
INSERT INTO `countries` VALUES (18, 20, 'Barbados', 'BRB', 'BB', '052', '+1', 'Bridgetown', 'BBD', 'Barbadian dollar', 'Bds$', '.bb', 'Barbados', 'Barbadian', 'null', 13.1667, -59.5333, '🇧🇧', 'U+1F1E7 U+1F1E7', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (19, 21, 'Belarus', 'BLR', 'BY', '112', '+375', 'Minsk', 'BYN', 'Belarusian ruble', 'Br', '.by', 'Белару́сь', 'Belarusian', 'null', 53, 28, '🇧🇾', 'U+1F1E7 U+1F1FE', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (20, 22, 'Belgium', 'BEL', 'BE', '056', '+32', 'Brussels', 'EUR', 'Euro', '€', '.be', 'België', 'Belgian', 'null', 50.8333, 4, '🇧🇪', 'U+1F1E7 U+1F1EA', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (21, 23, 'Belize', 'BLZ', 'BZ', '084', '+501', 'Belmopan', 'BZD', 'Belize dollar', '$', '.bz', 'Belize', 'Belizean', 'null', 17.25, -88.75, '🇧🇿', 'U+1F1E7 U+1F1FF', 'Americas', 'Central America');
INSERT INTO `countries` VALUES (22, 24, 'Benin', 'BEN', 'BJ', '204', '+229', 'Porto-Novo', 'XOF', 'West African CFA franc', 'CFA', '.bj', 'Bénin', 'Beninese, Beninois', 'null', 9.5, 2.25, '🇧🇯', 'U+1F1E7 U+1F1EF', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (23, 25, 'Bermuda', 'BMU', 'BM', '060', '+1', 'Hamilton', 'BMD', 'Bermudian dollar', '$', '.bm', 'Bermuda', 'Bermudian, Bermudan', 'null', 32.3333, -64.75, '🇧🇲', 'U+1F1E7 U+1F1F2', 'Americas', 'Northern America');
INSERT INTO `countries` VALUES (24, 26, 'Bhutan', 'BTN', 'BT', '064', '+975', 'Thimphu', 'BTN', 'Bhutanese ngultrum', 'Nu.', '.bt', 'ʼbrug-yul', 'Bhutanese', 'null', 27.5, 90.5, '🇧🇹', 'U+1F1E7 U+1F1F9', 'Asia', 'Southern Asia');
INSERT INTO `countries` VALUES (25, 27, 'Bolivia', 'BOL', 'BO', '068', '+591', 'Sucre', 'BOB', 'Bolivian boliviano', 'Bs.', '.bo', 'Bolivia', 'Bolivian', 'null', -17, -65, '🇧🇴', 'U+1F1E7 U+1F1F4', 'Americas', 'South America');
INSERT INTO `countries` VALUES (26, 155, 'Bonaire, Sint Eustatius and Saba', 'BES', 'BQ', '535', '+599', 'Kralendijk', 'USD', 'United States dollar', '$', '.an', 'Caribisch Nederland', 'Bonaire', 'null', 12.15, -68.2667, '🇧🇶', 'U+1F1E7 U+1F1F6', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (27, 28, 'Bosnia and Herzegovina', 'BIH', 'BA', '070', '+387', 'Sarajevo', 'BAM', 'Bosnia and Herzegovina convertible mark', 'KM', '.ba', 'Bosna i Hercegovina', 'Bosnian or Herzegovinian', 'null', 44, 18, '🇧🇦', 'U+1F1E7 U+1F1E6', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (28, 29, 'Botswana', 'BWA', 'BW', '072', '+267', 'Gaborone', 'BWP', 'Botswana pula', 'P', '.bw', 'Botswana', 'Motswana, Botswanan', 'null', -22, 24, '🇧🇼', 'U+1F1E7 U+1F1FC', 'Africa', 'Southern Africa');
INSERT INTO `countries` VALUES (29, 30, 'Bouvet Island', 'BVT', 'BV', '074', '+55', NULL, 'NOK', 'Norwegian krone', 'ko', '.bv', 'Bouvetøya', 'Bouvet Island', 'null', -54.4333, 3.4, '🇧🇻', 'U+1F1E7 U+1F1FB', NULL, NULL);
INSERT INTO `countries` VALUES (30, 31, 'Brazil', 'BRA', 'BR', '076', '+55', 'Brasilia', 'BRL', 'Brazilian real', 'R$', '.br', 'Brasil', 'Brazilian', 'null', -10, -55, '🇧🇷', 'U+1F1E7 U+1F1F7', 'Americas', 'South America');
INSERT INTO `countries` VALUES (31, 32, 'British Indian Ocean Territory', 'IOT', 'IO', '086', '+246', 'Diego Garcia', 'USD', 'United States dollar', '$', '.io', 'British Indian Ocean Territory', 'BIOT', 'null', -6, 71.5, '🇮🇴', 'U+1F1EE U+1F1F4', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (32, 33, 'Brunei', 'BRN', 'BN', '096', '+673', 'Bandar Seri Begawan', 'BND', 'Brunei dollar', 'B$', '.bn', 'Negara Brunei Darussalam', 'Bruneian', 'null', 4.5, 114.667, '🇧🇳', 'U+1F1E7 U+1F1F3', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (33, 34, 'Bulgaria', 'BGR', 'BG', '100', '+359', 'Sofia', 'BGN', 'Bulgarian lev', 'Лв.', '.bg', 'България', 'Bulgarian', 'null', 43, 25, '🇧🇬', 'U+1F1E7 U+1F1EC', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (34, 35, 'Burkina Faso', 'BFA', 'BF', '854', '+226', 'Ouagadougou', 'XOF', 'West African CFA franc', 'CFA', '.bf', 'Burkina Faso', 'Burkinabe', 'null', 13, -2, '🇧🇫', 'U+1F1E7 U+1F1EB', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (35, 36, 'Burundi', 'BDI', 'BI', '108', '+257', 'Bujumbura', 'BIF', 'Burundian franc', 'FBu', '.bi', 'Burundi', 'Burundian', 'null', -3.5, 30, '🇧🇮', 'U+1F1E7 U+1F1EE', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (36, 37, 'Cambodia', 'KHM', 'KH', '116', '+855', 'Phnom Penh', 'KHR', 'Cambodian riel', 'KHR', '.kh', 'Kâmpŭchéa', 'Cambodian', 'null', 13, 105, '🇰🇭', 'U+1F1F0 U+1F1ED', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (37, 38, 'Cameroon', 'CMR', 'CM', '120', '+237', 'Yaounde', 'XAF', 'Central African CFA franc', 'FCFA', '.cm', 'Cameroon', 'Cameroonian', 'null', 6, 12, '🇨🇲', 'U+1F1E8 U+1F1F2', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (38, 39, 'Canada', 'CAN', 'CA', '124', '+1', 'Ottawa', 'CAD', 'Canadian dollar', '$', '.ca', 'Canada', 'Canadian', 'null', 60, -95, '🇨🇦', 'U+1F1E8 U+1F1E6', 'Americas', 'Northern America');
INSERT INTO `countries` VALUES (39, 40, 'Cape Verde', 'CPV', 'CV', '132', '+238', 'Praia', 'CVE', 'Cape Verdean escudo', '$', '.cv', 'Cabo Verde', 'Verdean', 'null', 16, -24, '🇨🇻', 'U+1F1E8 U+1F1FB', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (40, 41, 'Cayman Islands', 'CYM', 'KY', '136', '+1', 'George Town', 'KYD', 'Cayman Islands dollar', '$', '.ky', 'Cayman Islands', 'Caymanian', 'null', 19.5, -80.5, '🇰🇾', 'U+1F1F0 U+1F1FE', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (41, 42, 'Central African Republic', 'CAF', 'CF', '140', '+236', 'Bangui', 'XAF', 'Central African CFA franc', 'FCFA', '.cf', 'Ködörösêse tî Bêafrîka', 'Central African', 'null', 7, 21, '🇨🇫', 'U+1F1E8 U+1F1EB', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (42, 43, 'Chad', 'TCD', 'TD', '148', '+235', 'N\'Djamena', 'XAF', 'Central African CFA franc', 'FCFA', '.td', 'Tchad', 'Chadian', 'null', 15, 19, '🇹🇩', 'U+1F1F9 U+1F1E9', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (43, 44, 'Chile', 'CHL', 'CL', '152', '+56', 'Santiago', 'CLP', 'Chilean peso', '$', '.cl', 'Chile', 'Chilean', 'null', -30, -71, '🇨🇱', 'U+1F1E8 U+1F1F1', 'Americas', 'South America');
INSERT INTO `countries` VALUES (44, 45, 'China', 'CHN', 'CN', '156', '+86', 'Beijing', 'CNY', 'Chinese yuan', '¥', '.cn', '中国', 'Chinese', 'null', 35, 105, '🇨🇳', 'U+1F1E8 U+1F1F3', 'Asia', 'Eastern Asia');
INSERT INTO `countries` VALUES (45, 46, 'Christmas Island', 'CXR', 'CX', '162', '+61', 'Flying Fish Cove', 'AUD', 'Australian dollar', '$', '.cx', 'Christmas Island', 'Christmas Island', 'null', -10.5, 105.667, '🇨🇽', 'U+1F1E8 U+1F1FD', 'Oceania', 'Australia and New Zealand');
INSERT INTO `countries` VALUES (46, 47, 'Cocos (Keeling) Islands', 'CCK', 'CC', '166', '+61', 'West Island', 'AUD', 'Australian dollar', '$', '.cc', 'Cocos (Keeling) Islands', 'Cocos Island', 'null', -12.5, 96.8333, '🇨🇨', 'U+1F1E8 U+1F1E8', 'Oceania', 'Australia and New Zealand');
INSERT INTO `countries` VALUES (47, 48, 'Colombia', 'COL', 'CO', '170', '+57', 'Bogotá', 'COP', 'Colombian peso', '$', '.co', 'Colombia', 'Colombian', 'null', 4, -72, '🇨🇴', 'U+1F1E8 U+1F1F4', 'Americas', 'South America');
INSERT INTO `countries` VALUES (48, 49, 'Comoros', 'COM', 'KM', '174', '+269', 'Moroni', 'KMF', 'Comorian franc', 'CF', '.km', 'Komori', 'Comoran, Comorian', 'null', -12.1667, 44.25, '🇰🇲', 'U+1F1F0 U+1F1F2', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (49, 50, 'Congo', 'COG', 'CG', '178', '+242', 'Brazzaville', 'XAF', 'Congolese Franc', 'CDF', '.cg', 'République du Congo', 'Congolese', 'null', -1, 15, '🇨🇬', 'U+1F1E8 U+1F1EC', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (50, 52, 'Cook Islands', 'COK', 'CK', '184', '+682', 'Avarua', 'NZD', 'New Zealand dollar', '$', '.ck', 'Cook Islands', 'Cook Island', 'null', -21.2333, -159.767, '🇨🇰', 'U+1F1E8 U+1F1F0', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (51, 53, 'Costa Rica', 'CRI', 'CR', '188', '+506', 'San Jose', 'CRC', 'Costa Rican colón', '₡', '.cr', 'Costa Rica', 'Costa Rican', 'null', 10, -84, '🇨🇷', 'U+1F1E8 U+1F1F7', 'Americas', 'Central America');
INSERT INTO `countries` VALUES (52, 54, 'Cote D\'Ivoire (Ivory Coast)', 'CIV', 'CI', '384', '+225', 'Yamoussoukro', 'XOF', 'West African CFA franc', 'CFA', '.ci', NULL, 'Ivorian', 'null', 8, -5, '🇨🇮', 'U+1F1E8 U+1F1EE', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (53, 55, 'Croatia', 'HRV', 'HR', '191', '+385', 'Zagreb', 'EUR', 'Euro', '€', '.hr', 'Hrvatska', 'Croatian', 'null', 45.1667, 15.5, '🇭🇷', 'U+1F1ED U+1F1F7', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (54, 56, 'Cuba', 'CUB', 'CU', '192', '+53', 'Havana', 'CUP', 'Cuban peso', '$', '.cu', 'Cuba', 'Cuban', 'null', 21.5, -80, '🇨🇺', 'U+1F1E8 U+1F1FA', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (55, 249, 'Curaçao', 'CUW', 'CW', '531', '+599', 'Willemstad', 'ANG', 'Netherlands Antillean guilder', 'ƒ', '.cw', 'Curaçao', 'Curacaoan', 'null', 12.1167, -68.9333, '🇨🇼', 'U+1F1E8 U+1F1FC', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (56, 57, 'Cyprus', 'CYP', 'CY', '196', '+357', 'Nicosia', 'EUR', 'Euro', '€', '.cy', 'Κύπρος', 'Cypriot', 'null', 35, 33, '🇨🇾', 'U+1F1E8 U+1F1FE', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (57, 58, 'Czech Republic', 'CZE', 'CZ', '203', '+420', 'Prague', 'CZK', 'Czech koruna', 'Kč', '.cz', 'Česká republika', 'Czech', 'null', 49.75, 15.5, '🇨🇿', 'U+1F1E8 U+1F1FF', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (58, 51, 'Democratic Republic of the Congo', 'COD', 'CD', '180', '+243', 'Kinshasa', 'CDF', 'Congolese Franc', 'FC', '.cd', 'République démocratique du Congo', 'Congolese', 'null', NULL, 25, '🇨🇩', 'U+1F1E8 U+1F1E9', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (59, 59, 'Denmark', 'DNK', 'DK', '208', '+45', 'Copenhagen', 'DKK', 'Danish krone', 'Kr.', '.dk', 'Danmark', 'Danish', 'null', 56, 10, '🇩🇰', 'U+1F1E9 U+1F1F0', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (60, 60, 'Djibouti', 'DJI', 'DJ', '262', '+253', 'Djibouti', 'DJF', 'Djiboutian franc', 'Fdj', '.dj', 'Djibouti', 'Djiboutian', 'null', 11.5, 43, '🇩🇯', 'U+1F1E9 U+1F1EF', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (61, 61, 'Dominica', 'DMA', 'DM', '212', '+1', 'Roseau', 'XCD', 'Eastern Caribbean dollar', '$', '.dm', 'Dominica', 'Dominican', 'null', 15.4167, -61.3333, '🇩🇲', 'U+1F1E9 U+1F1F2', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (62, 62, 'Dominican Republic', 'DOM', 'DO', '214', '+1', 'Santo Domingo', 'DOP', 'Dominican peso', '$', '.do', 'República Dominicana', 'Dominican', 'null', 19, -70.6667, '🇩🇴', 'U+1F1E9 U+1F1F4', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (63, 64, 'Ecuador', 'ECU', 'EC', '218', '+593', 'Quito', 'USD', 'United States dollar', '$', '.ec', 'Ecuador', 'Ecuadorian', 'null', -2, -77.5, '🇪🇨', 'U+1F1EA U+1F1E8', 'Americas', 'South America');
INSERT INTO `countries` VALUES (64, 65, 'Egypt', 'EGY', 'EG', '818', '+20', 'Cairo', 'EGP', 'Egyptian pound', 'ج.م', '.eg', 'مصر‎', 'Egyptian', 'null', 27, 30, '🇪🇬', 'U+1F1EA U+1F1EC', 'Africa', 'Northern Africa');
INSERT INTO `countries` VALUES (65, 66, 'El Salvador', 'SLV', 'SV', '222', '+503', 'San Salvador', 'USD', 'United States dollar', '$', '.sv', 'El Salvador', 'Salvadoran', 'null', 13.8333, -88.9167, '🇸🇻', 'U+1F1F8 U+1F1FB', 'Americas', 'Central America');
INSERT INTO `countries` VALUES (66, 67, 'Equatorial Guinea', 'GNQ', 'GQ', '226', '+240', 'Malabo', 'XAF', 'Central African CFA franc', 'FCFA', '.gq', 'Guinea Ecuatorial', 'Equatorial Guinean, Equatoguinean', 'null', 2, 10, '🇬🇶', 'U+1F1EC U+1F1F6', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (67, 68, 'Eritrea', 'ERI', 'ER', '232', '+291', 'Asmara', 'ERN', 'Eritrean nakfa', 'Nfk', '.er', 'ኤርትራ', 'Eritrean', 'null', 15, 39, '🇪🇷', 'U+1F1EA U+1F1F7', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (68, 69, 'Estonia', 'EST', 'EE', '233', '+372', 'Tallinn', 'EUR', 'Euro', '€', '.ee', 'Eesti', 'Estonian', 'null', 59, 26, '🇪🇪', 'U+1F1EA U+1F1EA', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (69, 212, 'Eswatini', 'SWZ', 'SZ', '748', '+268', 'Mbabane', 'SZL', 'Lilangeni', 'E', '.sz', 'Swaziland', 'Swazi', 'null', -26.5, 31.5, '🇸🇿', 'U+1F1F8 U+1F1FF', 'Africa', 'Southern Africa');
INSERT INTO `countries` VALUES (70, 70, 'Ethiopia', 'ETH', 'ET', '231', '+251', 'Addis Ababa', 'ETB', 'Ethiopian birr', 'Nkf', '.et', 'ኢትዮጵያ', 'Ethiopian', 'null', 8, 38, '🇪🇹', 'U+1F1EA U+1F1F9', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (71, 71, 'Falkland Islands', 'FLK', 'FK', '238', '+500', 'Stanley', 'FKP', 'Falkland Islands pound', '£', '.fk', 'Falkland Islands', 'Falkland Island', 'null', -51.75, -59, '🇫🇰', 'U+1F1EB U+1F1F0', 'Americas', 'South America');
INSERT INTO `countries` VALUES (72, 72, 'Faroe Islands', 'FRO', 'FO', '234', '+298', 'Torshavn', 'DKK', 'Danish krone', 'Kr.', '.fo', 'Føroyar', 'Faroese', 'null', 62, -7, '🇫🇴', 'U+1F1EB U+1F1F4', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (73, 73, 'Fiji Islands', 'FJI', 'FJ', '242', '+679', 'Suva', 'FJD', 'Fijian dollar', 'FJ$', '.fj', 'Fiji', 'Fijian', 'null', -18, 175, '🇫🇯', 'U+1F1EB U+1F1EF', 'Oceania', 'Melanesia');
INSERT INTO `countries` VALUES (74, 74, 'Finland', 'FIN', 'FI', '246', '+358', 'Helsinki', 'EUR', 'Euro', '€', '.fi', 'Suomi', 'Finnish', 'null', 64, 26, '🇫🇮', 'U+1F1EB U+1F1EE', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (75, 75, 'France', 'FRA', 'FR', '250', '+33', 'Paris', 'EUR', 'Euro', '€', '.fr', 'France', 'French', 'null', 46, 2, '🇫🇷', 'U+1F1EB U+1F1F7', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (76, 76, 'French Guiana', 'GUF', 'GF', '254', '+594', 'Cayenne', 'EUR', 'Euro', '€', '.gf', 'Guyane française', 'French Guianese', 'null', 4, -53, '🇬🇫', 'U+1F1EC U+1F1EB', 'Americas', 'South America');
INSERT INTO `countries` VALUES (77, 77, 'French Polynesia', 'PYF', 'PF', '258', '+689', 'Papeete', 'XPF', 'CFP franc', '₣', '.pf', 'Polynésie française', 'French Polynesia', 'null', -15, -140, '🇵🇫', 'U+1F1F5 U+1F1EB', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (78, 78, 'French Southern Territories', 'ATF', 'TF', '260', '+262', 'Port-aux-Francais', 'EUR', 'Euro', '€', '.tf', 'Territoire des Terres australes et antarctiques fr', 'French Southern Territories', 'null', -49.25, 69.167, '🇹🇫', 'U+1F1F9 U+1F1EB', 'Africa', 'Southern Africa');
INSERT INTO `countries` VALUES (79, 79, 'Gabon', 'GAB', 'GA', '266', '+241', 'Libreville', 'XAF', 'Central African CFA franc', 'FCFA', '.ga', 'Gabon', 'Gabonese', 'null', -1, 11.75, '🇬🇦', 'U+1F1EC U+1F1E6', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (80, 81, 'Georgia', 'GEO', 'GE', '268', '+995', 'Tbilisi', 'GEL', 'Georgian lari', 'ლ', '.ge', 'საქართველო', 'Georgian', 'null', 42, 43.5, '🇬🇪', 'U+1F1EC U+1F1EA', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (81, 82, 'Germany', 'DEU', 'DE', '276', '+49', 'Berlin', 'EUR', 'Euro', '€', '.de', 'Deutschland', 'German', 'null', 51, 9, '🇩🇪', 'U+1F1E9 U+1F1EA', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (82, 83, 'Ghana', 'GHA', 'GH', '288', '+233', 'Accra', 'GHS', 'Ghanaian cedi', 'GH₵', '.gh', 'Ghana', 'Ghanaian', 'null', 8, -2, '🇬🇭', 'U+1F1EC U+1F1ED', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (83, 84, 'Gibraltar', 'GIB', 'GI', '292', '+350', 'Gibraltar', 'GIP', 'Gibraltar pound', '£', '.gi', 'Gibraltar', 'Gibraltar', 'null', 36.1333, -5.35, '🇬🇮', 'U+1F1EC U+1F1EE', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (84, 85, 'Greece', 'GRC', 'GR', '300', '+30', 'Athens', 'EUR', 'Euro', '€', '.gr', 'Ελλάδα', 'Greek, Hellenic', 'null', 39, 22, '🇬🇷', 'U+1F1EC U+1F1F7', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (85, 86, 'Greenland', 'GRL', 'GL', '304', '+299', 'Nuuk', 'DKK', 'Danish krone', 'Kr.', '.gl', 'Kalaallit Nunaat', 'Greenlandic', 'null', 72, -40, '🇬🇱', 'U+1F1EC U+1F1F1', 'Americas', 'Northern America');
INSERT INTO `countries` VALUES (86, 87, 'Grenada', 'GRD', 'GD', '308', '+1', 'St. George\'s', 'XCD', 'Eastern Caribbean dollar', '$', '.gd', 'Grenada', 'Grenadian', 'null', 12.1167, -61.6667, '🇬🇩', 'U+1F1EC U+1F1E9', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (87, 88, 'Guadeloupe', 'GLP', 'GP', '312', '+590', 'Basse-Terre', 'EUR', 'Euro', '€', '.gp', 'Guadeloupe', 'Guadeloupe', 'null', 16.25, -61.5833, '🇬🇵', 'U+1F1EC U+1F1F5', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (88, 89, 'Guam', 'GUM', 'GU', '316', '+1', 'Hagatna', 'USD', 'United States dollar', '$', '.gu', 'Guam', 'Guamanian, Guambat', 'null', 13.4667, 144.783, '🇬🇺', 'U+1F1EC U+1F1FA', 'Oceania', 'Micronesia');
INSERT INTO `countries` VALUES (89, 90, 'Guatemala', 'GTM', 'GT', '320', '+502', 'Guatemala City', 'GTQ', 'Guatemalan quetzal', 'Q', '.gt', 'Guatemala', 'Guatemalan', 'null', 15.5, -90.25, '🇬🇹', 'U+1F1EC U+1F1F9', 'Americas', 'Central America');
INSERT INTO `countries` VALUES (90, 91, 'Guernsey', 'GGY', 'GG', '831', '+44', 'St Peter Port', 'GBP', 'British pound', '£', '.gg', 'Guernsey', 'Channel Island', 'null', 49.4667, -2.58333, '🇬🇬', 'U+1F1EC U+1F1EC', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (91, 92, 'Guinea', 'GIN', 'GN', '324', '+224', 'Conakry', 'GNF', 'Guinean franc', 'FG', '.gn', 'Guinée', 'Guinean', 'null', 11, -10, '🇬🇳', 'U+1F1EC U+1F1F3', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (92, 93, 'Guinea-Bissau', 'GNB', 'GW', '624', '+245', 'Bissau', 'XOF', 'West African CFA franc', 'CFA', '.gw', 'Guiné-Bissau', 'Bissau-Guinean', 'null', 12, -15, '🇬🇼', 'U+1F1EC U+1F1FC', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (93, 94, 'Guyana', 'GUY', 'GY', '328', '+592', 'Georgetown', 'GYD', 'Guyanese dollar', '$', '.gy', 'Guyana', 'Guyanese', 'null', 5, -59, '🇬🇾', 'U+1F1EC U+1F1FE', 'Americas', 'South America');
INSERT INTO `countries` VALUES (94, 95, 'Haiti', 'HTI', 'HT', '332', '+509', 'Port-au-Prince', 'HTG', 'Haitian gourde', 'G', '.ht', 'Haïti', 'Haitian', 'null', 19, -72.4167, '🇭🇹', 'U+1F1ED U+1F1F9', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (95, 96, 'Heard Island and McDonald Islands', 'HMD', 'HM', '334', '+672', NULL, 'AUD', 'Australian dollar', '$', '.hm', 'Heard Island and McDonald Islands', 'Heard Island or McDonald Islands', 'null', -53.1, 72.5167, '🇭🇲', 'U+1F1ED U+1F1F2', NULL, NULL);
INSERT INTO `countries` VALUES (96, 97, 'Honduras', 'HND', 'HN', '340', '+504', 'Tegucigalpa', 'HNL', 'Honduran lempira', 'L', '.hn', 'Honduras', 'Honduran', 'null', 15, -86.5, '🇭🇳', 'U+1F1ED U+1F1F3', 'Americas', 'Central America');
INSERT INTO `countries` VALUES (97, 98, 'Hong Kong S.A.R.', 'HKG', 'HK', '344', '+852', 'Hong Kong', 'HKD', 'Hong Kong dollar', '$', '.hk', '香港', 'Hong Kong, Hong Kongese', 'null', 22.25, 114.167, '🇭🇰', 'U+1F1ED U+1F1F0', 'Asia', 'Eastern Asia');
INSERT INTO `countries` VALUES (98, 99, 'Hungary', 'HUN', 'HU', '348', '+36', 'Budapest', 'HUF', 'Hungarian forint', 'Ft', '.hu', 'Magyarország', 'Hungarian, Magyar', 'null', 47, 20, '🇭🇺', 'U+1F1ED U+1F1FA', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (99, 100, 'Iceland', 'ISL', 'IS', '352', '+354', 'Reykjavik', 'ISK', 'Icelandic króna', 'ko', '.is', 'Ísland', 'Icelandic', 'null', 65, -18, '🇮🇸', 'U+1F1EE U+1F1F8', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (100, 101, 'India', 'IND', 'IN', '356', '+91', 'New Delhi', 'INR', 'Indian rupee', '₹', '.in', 'भारत', 'Indian', 'null', 20, 77, '🇮🇳', 'U+1F1EE U+1F1F3', 'Asia', 'Southern Asia');
INSERT INTO `countries` VALUES (101, 102, 'Indonesia', 'IDN', 'ID', '360', '+62', 'Jakarta', 'IDR', 'Indonesian rupiah', 'Rp', '.id', 'Indonesia', 'Indonesian', 'null', -5, 120, '🇮🇩', 'U+1F1EE U+1F1E9', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (102, 103, 'Iran', 'IRN', 'IR', '364', '+98', 'Tehran', 'IRR', 'Iranian rial', '﷼', '.ir', 'ایران', 'Iranian, Persian', 'null', 32, 53, '🇮🇷', 'U+1F1EE U+1F1F7', 'Asia', 'Southern Asia');
INSERT INTO `countries` VALUES (103, 104, 'Iraq', 'IRQ', 'IQ', '368', '+964', 'Baghdad', 'IQD', 'Iraqi dinar', 'د.ع', '.iq', 'العراق', 'Iraqi', 'null', 33, 44, '🇮🇶', 'U+1F1EE U+1F1F6', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (104, 105, 'Ireland', 'IRL', 'IE', '372', '+353', 'Dublin', 'EUR', 'Euro', '€', '.ie', 'Éire', 'Irish', 'null', 53, -8, '🇮🇪', 'U+1F1EE U+1F1EA', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (105, 106, 'Israel', 'ISR', 'IL', '376', '+972', 'Jerusalem', 'ILS', 'Israeli new shekel', '₪', '.il', 'יִשְׂרָאֵל', 'Israeli', 'null', 31.5, 34.75, '🇮🇱', 'U+1F1EE U+1F1F1', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (106, 107, 'Italy', 'ITA', 'IT', '380', '+39', 'Rome', 'EUR', 'Euro', '€', '.it', 'Italia', 'Italian', 'null', 42.8333, 12.8333, '🇮🇹', 'U+1F1EE U+1F1F9', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (107, 108, 'Jamaica', 'JAM', 'JM', '388', '+1', 'Kingston', 'JMD', 'Jamaican dollar', 'J$', '.jm', 'Jamaica', 'Jamaican', 'null', 18.25, -77.5, '🇯🇲', 'U+1F1EF U+1F1F2', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (108, 109, 'Japan', 'JPN', 'JP', '392', '+81', 'Tokyo', 'JPY', 'Japanese yen', '¥', '.jp', '日本', 'Japanese', 'null', 36, 138, '🇯🇵', 'U+1F1EF U+1F1F5', 'Asia', 'Eastern Asia');
INSERT INTO `countries` VALUES (109, 110, 'Jersey', 'JEY', 'JE', '832', '+44', 'Saint Helier', 'GBP', 'British pound', '£', '.je', 'Jersey', 'Channel Island', 'null', 49.25, -2.16667, '🇯🇪', 'U+1F1EF U+1F1EA', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (110, 111, 'Jordan', 'JOR', 'JO', '400', '+962', 'Amman', 'JOD', 'Jordanian dinar', 'ا.د', '.jo', 'الأردن', 'Jordanian', 'null', 31, 36, '🇯🇴', 'U+1F1EF U+1F1F4', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (111, 112, 'Kazakhstan', 'KAZ', 'KZ', '398', '+7', 'Astana', 'KZT', 'Kazakhstani tenge', 'лв', '.kz', 'Қазақстан', 'Kazakhstani, Kazakh', 'null', 48, 68, '🇰🇿', 'U+1F1F0 U+1F1FF', 'Asia', 'Central Asia');
INSERT INTO `countries` VALUES (112, 113, 'Kenya', 'KEN', 'KE', '404', '+254', 'Nairobi', 'KES', 'Kenyan shilling', 'KSh', '.ke', 'Kenya', 'Kenyan', 'null', 1, 38, '🇰🇪', 'U+1F1F0 U+1F1EA', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (113, 114, 'Kiribati', 'KIR', 'KI', '296', '+686', 'Tarawa', 'AUD', 'Australian dollar', '$', '.ki', 'Kiribati', 'I-Kiribati', 'null', 1.41667, 173, '🇰🇮', 'U+1F1F0 U+1F1EE', 'Oceania', 'Micronesia');
INSERT INTO `countries` VALUES (114, 248, 'Kosovo', 'XKX', 'XK', '926', '+383', 'Pristina', 'EUR', 'Euro', '€', '.xk', 'Republika e Kosovës', 'Kosovar, Kosovan', 'null', 42.5613, 20.3403, '🇽🇰', 'U+1F1FD U+1F1F0', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (115, 117, 'Kuwait', 'KWT', 'KW', '414', '+965', 'Kuwait City', 'KWD', 'Kuwaiti dinar', 'ك.د', '.kw', 'الكويت', 'Kuwaiti', 'null', 29.5, 45.75, '🇰🇼', 'U+1F1F0 U+1F1FC', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (116, 118, 'Kyrgyzstan', 'KGZ', 'KG', '417', '+996', 'Bishkek', 'KGS', 'Kyrgyzstani som', 'лв', '.kg', 'Кыргызстан', 'Kyrgyzstani, Kyrgyz, Kirgiz, Kirghiz', 'null', 41, 75, '🇰🇬', 'U+1F1F0 U+1F1EC', 'Asia', 'Central Asia');
INSERT INTO `countries` VALUES (117, 119, 'Laos', 'LAO', 'LA', '418', '+856', 'Vientiane', 'LAK', 'Lao kip', '₭', '.la', 'ສປປລາວ', 'Lao, Laotian', 'null', 18, 105, '🇱🇦', 'U+1F1F1 U+1F1E6', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (118, 120, 'Latvia', 'LVA', 'LV', '428', '+371', 'Riga', 'EUR', 'Euro', '€', '.lv', 'Latvija', 'Latvian', 'null', 57, 25, '🇱🇻', 'U+1F1F1 U+1F1FB', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (119, 121, 'Lebanon', 'LBN', 'LB', '422', '+961', 'Beirut', 'LBP', 'Lebanese pound', '£', '.lb', 'لبنان', 'Lebanese', 'null', 33.8333, 35.8333, '🇱🇧', 'U+1F1F1 U+1F1E7', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (120, 122, 'Lesotho', 'LSO', 'LS', '426', '+266', 'Maseru', 'LSL', 'Lesotho loti', 'L', '.ls', 'Lesotho', 'Basotho', 'null', -29.5, 28.5, '🇱🇸', 'U+1F1F1 U+1F1F8', 'Africa', 'Southern Africa');
INSERT INTO `countries` VALUES (121, 123, 'Liberia', 'LBR', 'LR', '430', '+231', 'Monrovia', 'LRD', 'Liberian dollar', '$', '.lr', 'Liberia', 'Liberian', 'null', 6.5, -9.5, '🇱🇷', 'U+1F1F1 U+1F1F7', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (122, 124, 'Libya', 'LBY', 'LY', '434', '+218', 'Tripolis', 'LYD', 'Libyan dinar', 'د.ل', '.ly', '‏ليبيا', 'Libyan', 'null', 25, 17, '🇱🇾', 'U+1F1F1 U+1F1FE', 'Africa', 'Northern Africa');
INSERT INTO `countries` VALUES (123, 125, 'Liechtenstein', 'LIE', 'LI', '438', '+423', 'Vaduz', 'CHF', 'Swiss franc', 'CHf', '.li', 'Liechtenstein', 'Liechtenstein', 'null', 47.2667, 9.53333, '🇱🇮', 'U+1F1F1 U+1F1EE', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (124, 126, 'Lithuania', 'LTU', 'LT', '440', '+370', 'Vilnius', 'EUR', 'Euro', '€', '.lt', 'Lietuva', 'Lithuanian', 'null', 56, 24, '🇱🇹', 'U+1F1F1 U+1F1F9', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (125, 127, 'Luxembourg', 'LUX', 'LU', '442', '+352', 'Luxembourg', 'EUR', 'Euro', '€', '.lu', 'Luxembourg', 'Luxembourg, Luxembourgish', 'null', 49.75, 6.16667, '🇱🇺', 'U+1F1F1 U+1F1FA', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (126, 128, 'Macau S.A.R.', 'MAC', 'MO', '446', '+853', 'Macao', 'MOP', 'Macanese pataca', '$', '.mo', '澳門', 'Macanese, Chinese', 'null', 22.1667, 113.55, '🇲🇴', 'U+1F1F2 U+1F1F4', 'Asia', 'Eastern Asia');
INSERT INTO `countries` VALUES (127, 130, 'Madagascar', 'MDG', 'MG', '450', '+261', 'Antananarivo', 'MGA', 'Malagasy ariary', 'Ar', '.mg', 'Madagasikara', 'Malagasy', 'null', -20, 47, '🇲🇬', 'U+1F1F2 U+1F1EC', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (128, 131, 'Malawi', 'MWI', 'MW', '454', '+265', 'Lilongwe', 'MWK', 'Malawian kwacha', 'MK', '.mw', 'Malawi', 'Malawian', 'null', -13.5, 34, '🇲🇼', 'U+1F1F2 U+1F1FC', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (129, 132, 'Malaysia', 'MYS', 'MY', '458', '+60', 'Kuala Lumpur', 'MYR', 'Malaysian ringgit', 'RM', '.my', 'Malaysia', 'Malaysian', 'null', 2.5, 112.5, '🇲🇾', 'U+1F1F2 U+1F1FE', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (130, 133, 'Maldives', 'MDV', 'MV', '462', '+960', 'Male', 'MVR', 'Maldivian rufiyaa', 'Rf', '.mv', 'Maldives', 'Maldivian', 'null', 3.25, 73, '🇲🇻', 'U+1F1F2 U+1F1FB', 'Asia', 'Southern Asia');
INSERT INTO `countries` VALUES (131, 134, 'Mali', 'MLI', 'ML', '466', '+223', 'Bamako', 'XOF', 'West African CFA franc', 'CFA', '.ml', 'Mali', 'Malian, Malinese', 'null', 17, -4, '🇲🇱', 'U+1F1F2 U+1F1F1', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (132, 135, 'Malta', 'MLT', 'MT', '470', '+356', 'Valletta', 'EUR', 'Euro', '€', '.mt', 'Malta', 'Maltese', 'null', 35.8333, 14.5833, '🇲🇹', 'U+1F1F2 U+1F1F9', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (133, 136, 'Man (Isle of)', 'IMN', 'IM', '833', '+44', 'Douglas, Isle of Man', 'GBP', 'British pound', '£', '.im', 'Isle of Man', 'Manx', 'null', 54.25, -4.5, '🇮🇲', 'U+1F1EE U+1F1F2', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (134, 137, 'Marshall Islands', 'MHL', 'MH', '584', '+692', 'Majuro', 'USD', 'United States dollar', '$', '.mh', 'M̧ajeļ', 'Marshallese', 'null', 9, 168, '🇲🇭', 'U+1F1F2 U+1F1ED', 'Oceania', 'Micronesia');
INSERT INTO `countries` VALUES (135, 138, 'Martinique', 'MTQ', 'MQ', '474', '+596', 'Fort-de-France', 'EUR', 'Euro', '€', '.mq', 'Martinique', 'Martiniquais, Martinican', 'null', 14.6667, -61, '🇲🇶', 'U+1F1F2 U+1F1F6', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (136, 139, 'Mauritania', 'MRT', 'MR', '478', '+222', 'Nouakchott', 'MRU', 'Mauritanian ouguiya', 'UM', '.mr', 'موريتانيا', 'Mauritanian', 'null', 20, -12, '🇲🇷', 'U+1F1F2 U+1F1F7', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (137, 140, 'Mauritius', 'MUS', 'MU', '480', '+230', 'Port Louis', 'MUR', 'Mauritian rupee', '₨', '.mu', 'Maurice', 'Mauritian', 'null', -20.2833, 57.55, '🇲🇺', 'U+1F1F2 U+1F1FA', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (138, 141, 'Mayotte', 'MYT', 'YT', '175', '+262', 'Mamoudzou', 'EUR', 'Euro', '€', '.yt', 'Mayotte', 'Mahoran', 'null', -12.8333, 45.1667, '🇾🇹', 'U+1F1FE U+1F1F9', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (139, 142, 'Mexico', 'MEX', 'MX', '484', '+52', 'Ciudad de México', 'MXN', 'Mexican peso', '$', '.mx', 'México', 'Mexican', 'null', 23, -102, '🇲🇽', 'U+1F1F2 U+1F1FD', 'Americas', 'Northern America');
INSERT INTO `countries` VALUES (140, 143, 'Micronesia', 'FSM', 'FM', '583', '+691', 'Palikir', 'USD', 'United States dollar', '$', '.fm', 'Micronesia', 'Micronesian', 'null', 6.91667, 158.25, '🇫🇲', 'U+1F1EB U+1F1F2', 'Oceania', 'Micronesia');
INSERT INTO `countries` VALUES (141, 144, 'Moldova', 'MDA', 'MD', '498', '+373', 'Chisinau', 'MDL', 'Moldovan leu', 'L', '.md', 'Moldova', 'Moldovan', 'null', 47, 29, '🇲🇩', 'U+1F1F2 U+1F1E9', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (142, 145, 'Monaco', 'MCO', 'MC', '492', '+377', 'Monaco', 'EUR', 'Euro', '€', '.mc', 'Monaco', 'Monegasque, Monacan', 'null', 43.7333, 7.4, '🇲🇨', 'U+1F1F2 U+1F1E8', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (143, 146, 'Mongolia', 'MNG', 'MN', '496', '+976', 'Ulan Bator', 'MNT', 'Mongolian tögrög', '₮', '.mn', 'Монгол улс', 'Mongolian', 'null', 46, 105, '🇲🇳', 'U+1F1F2 U+1F1F3', 'Asia', 'Eastern Asia');
INSERT INTO `countries` VALUES (144, 147, 'Montenegro', 'MNE', 'ME', '499', '+382', 'Podgorica', 'EUR', 'Euro', '€', '.me', 'Црна Гора', 'Montenegrin', 'null', 42.5, 19.3, '🇲🇪', 'U+1F1F2 U+1F1EA', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (145, 148, 'Montserrat', 'MSR', 'MS', '500', '+1', 'Plymouth', 'XCD', 'Eastern Caribbean dollar', '$', '.ms', 'Montserrat', 'Montserratian', 'null', 16.75, -62.2, '🇲🇸', 'U+1F1F2 U+1F1F8', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (146, 149, 'Morocco', 'MAR', 'MA', '504', '+212', 'Rabat', 'MAD', 'Moroccan dirham', 'DH', '.ma', 'المغرب', 'Moroccan', 'null', 32, -5, '🇲🇦', 'U+1F1F2 U+1F1E6', 'Africa', 'Northern Africa');
INSERT INTO `countries` VALUES (147, 150, 'Mozambique', 'MOZ', 'MZ', '508', '+258', 'Maputo', 'MZN', 'Mozambican metical', 'MT', '.mz', 'Moçambique', 'Mozambican', 'null', -18.25, 35, '🇲🇿', 'U+1F1F2 U+1F1FF', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (148, 151, 'Myanmar', 'MMR', 'MM', '104', '+95', 'Nay Pyi Taw', 'MMK', 'Burmese kyat', 'K', '.mm', 'မြန်မာ', 'Burmese', 'null', 22, 98, '🇲🇲', 'U+1F1F2 U+1F1F2', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (149, 152, 'Namibia', 'NAM', NULL, '516', '+264', 'Windhoek', 'NAD', 'Namibian dollar', '$', '.na', 'Namibia', 'Namibian', 'null', -22, 17, '🇳🇦', 'U+1F1F3 U+1F1E6', 'Africa', 'Southern Africa');
INSERT INTO `countries` VALUES (150, 153, 'Nauru', 'NRU', 'NR', '520', '+674', 'Yaren', 'AUD', 'Australian dollar', '$', '.nr', 'Nauru', 'Nauruan', 'null', -0.533333, 166.917, '🇳🇷', 'U+1F1F3 U+1F1F7', 'Oceania', 'Micronesia');
INSERT INTO `countries` VALUES (151, 154, 'Nepal', 'NPL', 'NP', '524', '+977', 'Kathmandu', 'NPR', 'Nepalese rupee', '₨', '.np', 'नपल', 'Nepali, Nepalese', 'null', 28, 84, '🇳🇵', 'U+1F1F3 U+1F1F5', 'Asia', 'Southern Asia');
INSERT INTO `countries` VALUES (152, 156, 'Netherlands', 'NLD', 'NL', '528', '+31', 'Amsterdam', 'EUR', 'Euro', '€', '.nl', 'Nederland', 'Dutch, Netherlandic', 'null', 52.5, 5.75, '🇳🇱', 'U+1F1F3 U+1F1F1', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (153, 157, 'New Caledonia', 'NCL', 'NC', '540', '+687', 'Noumea', 'XPF', 'CFP franc', '₣', '.nc', 'Nouvelle-Calédonie', 'New Caledonian', 'null', -21.5, 165.5, '🇳🇨', 'U+1F1F3 U+1F1E8', 'Oceania', 'Melanesia');
INSERT INTO `countries` VALUES (154, 158, 'New Zealand', 'NZL', 'NZ', '554', '+64', 'Wellington', 'NZD', 'New Zealand dollar', '$', '.nz', 'New Zealand', 'New Zealand, NZ', 'null', -41, 174, '🇳🇿', 'U+1F1F3 U+1F1FF', 'Oceania', 'Australia and New Zealand');
INSERT INTO `countries` VALUES (155, 159, 'Nicaragua', 'NIC', 'NI', '558', '+505', 'Managua', 'NIO', 'Nicaraguan córdoba', 'C$', '.ni', 'Nicaragua', 'Nicaraguan', 'null', 13, -85, '🇳🇮', 'U+1F1F3 U+1F1EE', 'Americas', 'Central America');
INSERT INTO `countries` VALUES (156, 160, 'Niger', 'NER', 'NE', '562', '+227', 'Niamey', 'XOF', 'West African CFA franc', 'CFA', '.ne', 'Niger', 'Nigerien', 'null', 16, 8, '🇳🇪', 'U+1F1F3 U+1F1EA', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (157, 161, 'Nigeria', 'NGA', 'NG', '566', '+234', 'Abuja', 'NGN', 'Nigerian naira', '₦', '.ng', 'Nigeria', 'Nigerian', 'null', 10, 8, '🇳🇬', 'U+1F1F3 U+1F1EC', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (158, 162, 'Niue', 'NIU', 'NU', '570', '+683', 'Alofi', 'NZD', 'New Zealand dollar', '$', '.nu', 'Niuē', 'Niuean', 'null', -19.0333, -169.867, '🇳🇺', 'U+1F1F3 U+1F1FA', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (159, 163, 'Norfolk Island', 'NFK', 'NF', '574', '+672', 'Kingston', 'AUD', 'Australian dollar', '$', '.nf', 'Norfolk Island', 'Norfolk Island', 'null', -29.0333, 167.95, '🇳🇫', 'U+1F1F3 U+1F1EB', 'Oceania', 'Australia and New Zealand');
INSERT INTO `countries` VALUES (160, 115, 'North Korea', 'PRK', 'KP', '408', '+850', 'Pyongyang', 'KPW', 'North Korean Won', '₩', '.kp', '북한', 'North Korean', 'null', 40, 127, '🇰🇵', 'U+1F1F0 U+1F1F5', 'Asia', 'Eastern Asia');
INSERT INTO `countries` VALUES (161, 129, 'North Macedonia', 'MKD', 'MK', '807', '+389', 'Skopje', 'MKD', 'Denar', 'ден', '.mk', 'Северна Македонија', 'Macedonian', 'null', 41.8333, 22, '🇲🇰', 'U+1F1F2 U+1F1F0', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (162, 164, 'Northern Mariana Islands', 'MNP', 'MP', '580', '+1', 'Saipan', 'USD', 'United States dollar', '$', '.mp', 'Northern Mariana Islands', 'Northern Marianan', 'null', 15.2, 145.75, '🇲🇵', 'U+1F1F2 U+1F1F5', 'Oceania', 'Micronesia');
INSERT INTO `countries` VALUES (163, 165, 'Norway', 'NOR', 'NO', '578', '+47', 'Oslo', 'NOK', 'Norwegian krone', 'ko', '.no', 'Norge', 'Norwegian', 'null', 62, 10, '🇳🇴', 'U+1F1F3 U+1F1F4', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (164, 166, 'Oman', 'OMN', 'OM', '512', '+968', 'Muscat', 'OMR', 'Omani rial', '.ع.ر', '.om', 'عمان', 'Omani', 'null', 21, 57, '🇴🇲', 'U+1F1F4 U+1F1F2', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (165, 167, 'Pakistan', 'PAK', 'PK', '586', '+92', 'Islamabad', 'PKR', 'Pakistani rupee', '₨', '.pk', 'پاکستان', 'Pakistani', 'null', 30, 70, '🇵🇰', 'U+1F1F5 U+1F1F0', 'Asia', 'Southern Asia');
INSERT INTO `countries` VALUES (166, 168, 'Palau', 'PLW', 'PW', '585', '+680', 'Melekeok', 'USD', 'United States dollar', '$', '.pw', 'Palau', 'Palauan', 'null', 7.5, 134.5, '🇵🇼', 'U+1F1F5 U+1F1FC', 'Oceania', 'Micronesia');
INSERT INTO `countries` VALUES (167, 169, 'Palestinian Territory Occupied', 'PSE', 'PS', '275', '+970', 'East Jerusalem', 'ILS', 'Israeli new shekel', '₪', '.ps', 'فلسطين', 'Palestinian', 'null', 31.9, 35.2, '🇵🇸', 'U+1F1F5 U+1F1F8', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (168, 170, 'Panama', 'PAN', 'PA', '591', '+507', 'Panama City', 'PAB', 'Panamanian balboa', 'B/.', '.pa', 'Panamá', 'Panamanian', 'null', 9, -80, '🇵🇦', 'U+1F1F5 U+1F1E6', 'Americas', 'Central America');
INSERT INTO `countries` VALUES (169, 171, 'Papua New Guinea', 'PNG', 'PG', '598', '+675', 'Port Moresby', 'PGK', 'Papua New Guinean kina', 'K', '.pg', 'Papua Niugini', 'Papua New Guinean, Papuan', 'null', -6, 147, '🇵🇬', 'U+1F1F5 U+1F1EC', 'Oceania', 'Melanesia');
INSERT INTO `countries` VALUES (170, 172, 'Paraguay', 'PRY', 'PY', '600', '+595', 'Asuncion', 'PYG', 'Paraguayan guarani', '₲', '.py', 'Paraguay', 'Paraguayan', 'null', -23, -58, '🇵🇾', 'U+1F1F5 U+1F1FE', 'Americas', 'South America');
INSERT INTO `countries` VALUES (171, 173, 'Peru', 'PER', 'PE', '604', '+51', 'Lima', 'PEN', 'Peruvian sol', 'S/.', '.pe', 'Perú', 'Peruvian', 'null', -10, -76, '🇵🇪', 'U+1F1F5 U+1F1EA', 'Americas', 'South America');
INSERT INTO `countries` VALUES (172, 174, 'Philippines', 'PHL', 'PH', '608', '+63', 'Manila', 'PHP', 'Philippine peso', '₱', '.ph', 'Pilipinas', 'Philippine, Filipino', 'null', 13, 122, '🇵🇭', 'U+1F1F5 U+1F1ED', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (173, 175, 'Pitcairn Island', 'PCN', 'PN', '612', '+870', 'Adamstown', 'NZD', 'New Zealand dollar', '$', '.pn', 'Pitcairn Islands', 'Pitcairn Island', 'null', -25.0667, -130.1, '🇵🇳', 'U+1F1F5 U+1F1F3', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (174, 176, 'Poland', 'POL', 'PL', '616', '+48', 'Warsaw', 'PLN', 'Polish złoty', 'zł', '.pl', 'Polska', 'Polish', 'null', 52, 20, '🇵🇱', 'U+1F1F5 U+1F1F1', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (175, 177, 'Portugal', 'PRT', 'PT', '620', '+351', 'Lisbon', 'EUR', 'Euro', '€', '.pt', 'Portugal', 'Portuguese', 'null', 39.5, -8, '🇵🇹', 'U+1F1F5 U+1F1F9', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (176, 178, 'Puerto Rico', 'PRI', 'PR', '630', '+1', 'San Juan', 'USD', 'United States dollar', '$', '.pr', 'Puerto Rico', 'Puerto Rican', 'null', 18.25, -66.5, '🇵🇷', 'U+1F1F5 U+1F1F7', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (177, 179, 'Qatar', 'QAT', 'QA', '634', '+974', 'Doha', 'QAR', 'Qatari riyal', 'ق.ر', '.qa', 'قطر', 'Qatari', 'null', 25.5, 51.25, '🇶🇦', 'U+1F1F6 U+1F1E6', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (178, 180, 'Reunion', 'REU', 'RE', '638', '+262', 'Saint-Denis', 'EUR', 'Euro', '€', '.re', 'La Réunion', 'Reunionese, Reunionnais', 'null', -21.15, 55.5, '🇷🇪', 'U+1F1F7 U+1F1EA', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (179, 181, 'Romania', 'ROU', 'RO', '642', '+40', 'Bucharest', 'RON', 'Romanian leu', 'lei', '.ro', 'România', 'Romanian', 'null', 46, 25, '🇷🇴', 'U+1F1F7 U+1F1F4', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (180, 182, 'Russia', 'RUS', 'RU', '643', '+7', 'Moscow', 'RUB', 'Russian ruble', '₽', '.ru', 'Россия', 'Russian', 'null', 60, 100, '🇷🇺', 'U+1F1F7 U+1F1FA', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (181, 183, 'Rwanda', 'RWA', 'RW', '646', '+250', 'Kigali', 'RWF', 'Rwandan franc', 'FRw', '.rw', 'Rwanda', 'Rwandan', 'null', -2, 30, '🇷🇼', 'U+1F1F7 U+1F1FC', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (182, 184, 'Saint Helena', 'SHN', 'SH', '654', '+290', 'Jamestown', 'SHP', 'Saint Helena pound', '£', '.sh', 'Saint Helena', 'Saint Helenian', 'null', -15.95, -5.7, '🇸🇭', 'U+1F1F8 U+1F1ED', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (183, 185, 'Saint Kitts and Nevis', 'KNA', 'KN', '659', '+1', 'Basseterre', 'XCD', 'Eastern Caribbean dollar', '$', '.kn', 'Saint Kitts and Nevis', 'Kittitian or Nevisian', 'null', 17.3333, -62.75, '🇰🇳', 'U+1F1F0 U+1F1F3', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (184, 186, 'Saint Lucia', 'LCA', 'LC', '662', '+1', 'Castries', 'XCD', 'Eastern Caribbean dollar', '$', '.lc', 'Saint Lucia', 'Saint Lucian', 'null', 13.8833, -60.9667, '🇱🇨', 'U+1F1F1 U+1F1E8', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (185, 187, 'Saint Pierre and Miquelon', 'SPM', 'PM', '666', '+508', 'Saint-Pierre', 'EUR', 'Euro', '€', '.pm', 'Saint-Pierre-et-Miquelon', 'Saint-Pierrais or Miquelonnais', 'null', 46.8333, -56.3333, '🇵🇲', 'U+1F1F5 U+1F1F2', 'Americas', 'Northern America');
INSERT INTO `countries` VALUES (186, 188, 'Saint Vincent and the Grenadines', 'VCT', 'VC', '670', '+1', 'Kingstown', 'XCD', 'Eastern Caribbean dollar', '$', '.vc', 'Saint Vincent and the Grenadines', 'Saint Vincentian, Vincentian', 'null', 13.25, -61.2, '🇻🇨', 'U+1F1FB U+1F1E8', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (187, 189, 'Saint-Barthelemy', 'BLM', 'BL', '652', '+590', 'Gustavia', 'EUR', 'Euro', '€', '.bl', 'Saint-Barthélemy', 'Barthelemois', 'null', 18.5, -63.4167, '🇧🇱', 'U+1F1E7 U+1F1F1', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (188, 190, 'Saint-Martin (French part)', 'MAF', 'MF', '663', '+590', 'Marigot', 'EUR', 'Euro', '€', '.mf', 'Saint-Martin', 'Saint-Martinoise', 'null', 18.0833, -63.95, '🇲🇫', 'U+1F1F2 U+1F1EB', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (189, 191, 'Samoa', 'WSM', 'WS', '882', '+685', 'Apia', 'WST', 'Samoan tālā', 'SAT', '.ws', 'Samoa', 'Samoan', 'null', -13.5833, -172.333, '🇼🇸', 'U+1F1FC U+1F1F8', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (190, 192, 'San Marino', 'SMR', 'SM', '674', '+378', 'San Marino', 'EUR', 'Euro', '€', '.sm', 'San Marino', 'Sammarinese', 'null', 43.7667, 12.4167, '🇸🇲', 'U+1F1F8 U+1F1F2', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (191, 193, 'Sao Tome and Principe', 'STP', 'ST', '678', '+239', 'Sao Tome', 'STN', 'Dobra', 'Db', '.st', 'São Tomé e Príncipe', 'Sao Tomean', 'null', 1, 7, '🇸🇹', 'U+1F1F8 U+1F1F9', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (192, 194, 'Saudi Arabia', 'SAU', 'SA', '682', '+966', 'Riyadh', 'SAR', 'Saudi riyal', '﷼', '.sa', 'المملكة العربية السعودية', 'Saudi, Saudi Arabian', 'null', 25, 45, '🇸🇦', 'U+1F1F8 U+1F1E6', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (193, 195, 'Senegal', 'SEN', 'SN', '686', '+221', 'Dakar', 'XOF', 'West African CFA franc', 'CFA', '.sn', 'Sénégal', 'Senegalese', 'null', 14, -14, '🇸🇳', 'U+1F1F8 U+1F1F3', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (194, 196, 'Serbia', 'SRB', 'RS', '688', '+381', 'Belgrade', 'RSD', 'Serbian dinar', 'din', '.rs', 'Србија', 'Serbian', 'null', 44, 21, '🇷🇸', 'U+1F1F7 U+1F1F8', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (195, 197, 'Seychelles', 'SYC', 'SC', '690', '+248', 'Victoria', 'SCR', 'Seychellois rupee', 'SRe', '.sc', 'Seychelles', 'Seychellois', 'null', -4.58333, 55.6667, '🇸🇨', 'U+1F1F8 U+1F1E8', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (196, 198, 'Sierra Leone', 'SLE', 'SL', '694', '+232', 'Freetown', 'SLL', 'Sierra Leonean leone', 'Le', '.sl', 'Sierra Leone', 'Sierra Leonean', 'null', 8.5, -11.5, '🇸🇱', 'U+1F1F8 U+1F1F1', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (197, 199, 'Singapore', 'SGP', 'SG', '702', '+65', 'Singapur', 'SGD', 'Singapore dollar', '$', '.sg', 'Singapore', 'Singaporean', 'null', 1.36667, 103.8, '🇸🇬', 'U+1F1F8 U+1F1EC', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (198, 250, 'Sint Maarten (Dutch part)', 'SXM', 'SX', '534', '+1721', 'Philipsburg', 'ANG', 'Netherlands Antillean guilder', 'ƒ', '.sx', 'Sint Maarten', 'Sint Maarten', 'null', 18.0333, -63.05, '🇸🇽', 'U+1F1F8 U+1F1FD', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (199, 200, 'Slovakia', 'SVK', 'SK', '703', '+421', 'Bratislava', 'EUR', 'Euro', '€', '.sk', 'Slovensko', 'Slovak', 'null', 48.6667, 19.5, '🇸🇰', 'U+1F1F8 U+1F1F0', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (200, 201, 'Slovenia', 'SVN', 'SI', '705', '+386', 'Ljubljana', 'EUR', 'Euro', '€', '.si', 'Slovenija', 'Slovenian, Slovene', 'null', 46.1167, 14.8167, '🇸🇮', 'U+1F1F8 U+1F1EE', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (201, 202, 'Solomon Islands', 'SLB', 'SB', '090', '+677', 'Honiara', 'SBD', 'Solomon Islands dollar', 'Si$', '.sb', 'Solomon Islands', 'Solomon Island', 'null', -8, 159, '🇸🇧', 'U+1F1F8 U+1F1E7', 'Oceania', 'Melanesia');
INSERT INTO `countries` VALUES (202, 203, 'Somalia', 'SOM', 'SO', '706', '+252', 'Mogadishu', 'SOS', 'Somali shilling', 'Sh.so.', '.so', 'Soomaaliya', 'Somali, Somalian', 'null', 10, 49, '🇸🇴', 'U+1F1F8 U+1F1F4', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (203, 204, 'South Africa', 'ZAF', 'ZA', '710', '+27', 'Pretoria', 'ZAR', 'South African rand', 'R', '.za', 'South Africa', 'South African', 'null', -29, 24, '🇿🇦', 'U+1F1FF U+1F1E6', 'Africa', 'Southern Africa');
INSERT INTO `countries` VALUES (204, 205, 'South Georgia', 'SGS', 'GS', '239', '+500', 'Grytviken', 'GBP', 'British pound', '£', '.gs', 'South Georgia', 'South Georgia or South Sandwich Islands', 'null', -54.5, -37, '🇬🇸', 'U+1F1EC U+1F1F8', 'Americas', 'South America');
INSERT INTO `countries` VALUES (205, 116, 'South Korea', 'KOR', 'KR', '410', '+82', 'Seoul', 'KRW', 'Won', '₩', '.kr', '대한민국', 'South Korean', 'null', 37, 127.5, '🇰🇷', 'U+1F1F0 U+1F1F7', 'Asia', 'Eastern Asia');
INSERT INTO `countries` VALUES (206, 206, 'South Sudan', 'SSD', 'SS', '728', '+211', 'Juba', 'SSP', 'South Sudanese pound', '£', '.ss', 'South Sudan', 'South Sudanese', 'null', 7, 30, '🇸🇸', 'U+1F1F8 U+1F1F8', 'Africa', 'Middle Africa');
INSERT INTO `countries` VALUES (207, 207, 'Spain', 'ESP', 'ES', '724', '+34', 'Madrid', 'EUR', 'Euro', '€', '.es', 'España', 'Spanish', 'null', 40, -4, '🇪🇸', 'U+1F1EA U+1F1F8', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (208, 208, 'Sri Lanka', 'LKA', 'LK', '144', '+94', 'Colombo', 'LKR', 'Sri Lankan rupee', 'Rs', '.lk', 'śrī laṃkāva', 'Sri Lankan', 'null', 7, 81, '🇱🇰', 'U+1F1F1 U+1F1F0', 'Asia', 'Southern Asia');
INSERT INTO `countries` VALUES (209, 209, 'Sudan', 'SDN', 'SD', '729', '+249', 'Khartoum', 'SDG', 'Sudanese pound', '.س.ج', '.sd', 'السودان', 'Sudanese', 'null', 15, 30, '🇸🇩', 'U+1F1F8 U+1F1E9', 'Africa', 'Northern Africa');
INSERT INTO `countries` VALUES (210, 210, 'Suriname', 'SUR', 'SR', '740', '+597', 'Paramaribo', 'SRD', 'Surinamese dollar', '$', '.sr', 'Suriname', 'Surinamese', 'null', 4, -56, '🇸🇷', 'U+1F1F8 U+1F1F7', 'Americas', 'South America');
INSERT INTO `countries` VALUES (211, 211, 'Svalbard and Jan Mayen Islands', 'SJM', 'SJ', '744', '+47', 'Longyearbyen', 'NOK', 'Norwegian krone', 'ko', '.sj', 'Svalbard og Jan Mayen', 'Svalbard', 'null', 78, 20, '🇸🇯', 'U+1F1F8 U+1F1EF', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (212, 213, 'Sweden', 'SWE', 'SE', '752', '+46', 'Stockholm', 'SEK', 'Swedish krona', 'ko', '.se', 'Sverige', 'Swedish', 'null', 62, 15, '🇸🇪', 'U+1F1F8 U+1F1EA', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (213, 214, 'Switzerland', 'CHE', 'CH', '756', '+41', 'Bern', 'CHF', 'Swiss franc', 'CHf', '.ch', 'Schweiz', 'Swiss', 'null', 47, 8, '🇨🇭', 'U+1F1E8 U+1F1ED', 'Europe', 'Western Europe');
INSERT INTO `countries` VALUES (214, 215, 'Syria', 'SYR', 'SY', '760', '+963', 'Damascus', 'SYP', 'Syrian pound', 'LS', '.sy', 'سوريا', 'Syrian', 'null', 35, 38, '🇸🇾', 'U+1F1F8 U+1F1FE', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (215, 216, 'Taiwan', 'TWN', 'TW', '158', '+886', 'Taipei', 'TWD', 'New Taiwan dollar', '$', '.tw', '臺灣', 'Chinese, Taiwanese', 'null', 23.5, 121, '🇹🇼', 'U+1F1F9 U+1F1FC', 'Asia', 'Eastern Asia');
INSERT INTO `countries` VALUES (216, 217, 'Tajikistan', 'TJK', 'TJ', '762', '+992', 'Dushanbe', 'TJS', 'Tajikistani somoni', 'SM', '.tj', 'Тоҷикистон', 'Tajikistani', 'null', 39, 71, '🇹🇯', 'U+1F1F9 U+1F1EF', 'Asia', 'Central Asia');
INSERT INTO `countries` VALUES (217, 218, 'Tanzania', 'TZA', 'TZ', '834', '+255', 'Dodoma', 'TZS', 'Tanzanian shilling', 'TSh', '.tz', 'Tanzania', 'Tanzanian', 'null', -6, 35, '🇹🇿', 'U+1F1F9 U+1F1FF', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (218, 219, 'Thailand', 'THA', 'TH', '764', '+66', 'Bangkok', 'THB', 'Thai baht', '฿', '.th', 'ประเทศไทย', 'Thai', 'null', 15, 100, '🇹🇭', 'U+1F1F9 U+1F1ED', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (219, 17, 'The Bahamas', 'BHS', 'BS', '044', '+1', 'Nassau', 'BSD', 'Bahamian dollar', 'B$', '.bs', 'Bahamas', 'Bahamian', 'null', 24.25, -76, '🇧🇸', 'U+1F1E7 U+1F1F8', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (220, 80, 'The Gambia ', 'GMB', 'GM', '270', '+220', 'Banjul', 'GMD', 'Gambian dalasi', 'D', '.gm', 'Gambia', 'Gambian', 'null', 13.4667, -16.5667, '🇬🇲', 'U+1F1EC U+1F1F2', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (221, 63, 'Timor-Leste', 'TLS', 'TL', '626', '+670', 'Dili', 'USD', 'United States dollar', '$', '.tl', 'Timor-Leste', 'Timorese', 'null', -8.83333, 125.917, '🇹🇱', 'U+1F1F9 U+1F1F1', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (222, 220, 'Togo', 'TGO', 'TG', '768', '+228', 'Lome', 'XOF', 'West African CFA franc', 'CFA', '.tg', 'Togo', 'Togolese', 'null', 8, 1.16667, '🇹🇬', 'U+1F1F9 U+1F1EC', 'Africa', 'Western Africa');
INSERT INTO `countries` VALUES (223, 221, 'Tokelau', 'TKL', 'TK', '772', '+690', NULL, 'NZD', 'New Zealand dollar', '$', '.tk', 'Tokelau', 'Tokelauan', 'null', -9, -172, '🇹🇰', 'U+1F1F9 U+1F1F0', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (224, 222, 'Tonga', 'TON', 'TO', '776', '+676', 'Nuku\'alofa', 'TOP', 'Tongan paʻanga', '$', '.to', 'Tonga', 'Tongan', 'null', -20, -175, '🇹🇴', 'U+1F1F9 U+1F1F4', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (225, 223, 'Trinidad and Tobago', 'TTO', 'TT', '780', '+1', 'Port of Spain', 'TTD', 'Trinidad and Tobago dollar', '$', '.tt', 'Trinidad and Tobago', 'Trinidadian or Tobagonian', 'null', 11, -61, '🇹🇹', 'U+1F1F9 U+1F1F9', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (226, 224, 'Tunisia', 'TUN', 'TN', '788', '+216', 'Tunis', 'TND', 'Tunisian dinar', 'ت.د', '.tn', 'تونس', 'Tunisian', 'null', 34, 9, '🇹🇳', 'U+1F1F9 U+1F1F3', 'Africa', 'Northern Africa');
INSERT INTO `countries` VALUES (227, 225, 'Turkey', 'TUR', 'TR', '792', '+90', 'Ankara', 'TRY', 'Turkish lira', '₺', '.tr', 'Türkiye', 'Turkish', 'null', 39, 35, '🇹🇷', 'U+1F1F9 U+1F1F7', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (228, 226, 'Turkmenistan', 'TKM', 'TM', '795', '+993', 'Ashgabat', 'TMT', 'Turkmenistan manat', 'T', '.tm', 'Türkmenistan', 'Turkmen', 'null', 40, 60, '🇹🇲', 'U+1F1F9 U+1F1F2', 'Asia', 'Central Asia');
INSERT INTO `countries` VALUES (229, 227, 'Turks and Caicos Islands', 'TCA', 'TC', '796', '+1', 'Cockburn Town', 'USD', 'United States dollar', '$', '.tc', 'Turks and Caicos Islands', 'Turks and Caicos Island', 'null', 21.75, -71.5833, '🇹🇨', 'U+1F1F9 U+1F1E8', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (230, 228, 'Tuvalu', 'TUV', 'TV', '798', '+688', 'Funafuti', 'AUD', 'Australian dollar', '$', '.tv', 'Tuvalu', 'Tuvaluan', 'null', -8, 178, '🇹🇻', 'U+1F1F9 U+1F1FB', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (231, 229, 'Uganda', 'UGA', 'UG', '800', '+256', 'Kampala', 'UGX', 'Ugandan shilling', 'USh', '.ug', 'Uganda', 'Ugandan', 'null', 1, 32, '🇺🇬', 'U+1F1FA U+1F1EC', 'Africa', 'Eastern Africa');
INSERT INTO `countries` VALUES (232, 230, 'Ukraine', 'UKR', 'UA', '804', '+380', 'Kyiv', 'UAH', 'Ukrainian hryvnia', '₴', '.ua', 'Україна', 'Ukrainian', 'null', 49, 32, '🇺🇦', 'U+1F1FA U+1F1E6', 'Europe', 'Eastern Europe');
INSERT INTO `countries` VALUES (233, 231, 'United Arab Emirates', 'ARE', 'AE', '784', '+971', 'Abu Dhabi', 'AED', 'United Arab Emirates dirham', 'إ.د', '.ae', 'دولة الإمارات العربية المتحدة', 'Emirati, Emirian, Emiri', 'null', 24, 54, '🇦🇪', 'U+1F1E6 U+1F1EA', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (234, 232, 'United Kingdom', 'GBR', 'GB', '826', '+44', 'London', 'GBP', 'British pound', '£', '.uk', 'United Kingdom', 'British, UK', 'null', 54, -2, '🇬🇧', 'U+1F1EC U+1F1E7', 'Europe', 'Northern Europe');
INSERT INTO `countries` VALUES (235, 233, 'United States', 'USA', 'US', '840', '+1', 'Washington', 'USD', 'United States dollar', '$', '.us', 'United States', 'American', 'null', 38, -97, '🇺🇸', 'U+1F1FA U+1F1F8', 'Americas', 'Northern America');
INSERT INTO `countries` VALUES (236, 234, 'United States Minor Outlying Islands', 'UMI', 'UM', '581', '+1', NULL, 'USD', 'United States dollar', '$', '.us', 'United States Minor Outlying Islands', 'American', 'null', NULL, NULL, '🇺🇲', 'U+1F1FA U+1F1F2', 'Americas', 'Northern America');
INSERT INTO `countries` VALUES (237, 235, 'Uruguay', 'URY', 'UY', '858', '+598', 'Montevideo', 'UYU', 'Uruguayan peso', '$', '.uy', 'Uruguay', 'Uruguayan', 'null', -33, -56, '🇺🇾', 'U+1F1FA U+1F1FE', 'Americas', 'South America');
INSERT INTO `countries` VALUES (238, 236, 'Uzbekistan', 'UZB', 'UZ', '860', '+998', 'Tashkent', 'UZS', 'Uzbekistani soʻm', 'лв', '.uz', 'O‘zbekiston', 'Uzbekistani, Uzbek', 'null', 41, 64, '🇺🇿', 'U+1F1FA U+1F1FF', 'Asia', 'Central Asia');
INSERT INTO `countries` VALUES (239, 237, 'Vanuatu', 'VUT', 'VU', '548', '+678', 'Port Vila', 'VUV', 'Vanuatu vatu', 'VT', '.vu', 'Vanuatu', 'Ni-Vanuatu, Vanuatuan', 'null', -16, 167, '🇻🇺', 'U+1F1FB U+1F1FA', 'Oceania', 'Melanesia');
INSERT INTO `countries` VALUES (240, 238, 'Vatican City State (Holy See)', 'VAT', 'VA', '336', '+379', 'Vatican City', 'EUR', 'Euro', '€', '.va', 'Vaticano', 'Vatican', 'null', 41.9, 12.45, '🇻🇦', 'U+1F1FB U+1F1E6', 'Europe', 'Southern Europe');
INSERT INTO `countries` VALUES (241, 239, 'Venezuela', 'VEN', 'VE', '862', '+58', 'Caracas', 'VES', 'Bolívar', 'Bs', '.ve', 'Venezuela', 'Venezuelan', 'null', 8, -66, '🇻🇪', 'U+1F1FB U+1F1EA', 'Americas', 'South America');
INSERT INTO `countries` VALUES (242, 240, 'Vietnam', 'VNM', 'VN', '704', '+84', 'Hanoi', 'VND', 'Vietnamese đồng', '₫', '.vn', 'Việt Nam', 'Vietnamese', 'null', 16.1667, 107.833, '🇻🇳', 'U+1F1FB U+1F1F3', 'Asia', 'South-Eastern Asia');
INSERT INTO `countries` VALUES (243, 241, 'Virgin Islands (British)', 'VGB', 'VG', '092', '+1', 'Road Town', 'USD', 'United States dollar', '$', '.vg', 'British Virgin Islands', 'British Virgin Island', 'null', 18.4314, -64.623, '🇻🇬', 'U+1F1FB U+1F1EC', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (244, 242, 'Virgin Islands (US)', 'VIR', 'VI', '850', '+1', 'Charlotte Amalie', 'USD', 'United States dollar', '$', '.vi', 'United States Virgin Islands', 'U.S. Virgin Island', 'null', 18.34, -64.93, '🇻🇮', 'U+1F1FB U+1F1EE', 'Americas', 'Caribbean');
INSERT INTO `countries` VALUES (245, 243, 'Wallis and Futuna Islands', 'WLF', 'WF', '876', '+681', 'Mata Utu', 'XPF', 'CFP franc', '₣', '.wf', 'Wallis et Futuna', 'Wallis and Futuna, Wallisian or Futunan', 'null', -13.3, -176.2, '🇼🇫', 'U+1F1FC U+1F1EB', 'Oceania', 'Polynesia');
INSERT INTO `countries` VALUES (246, 244, 'Western Sahara', 'ESH', 'EH', '732', '+212', 'El-Aaiun', 'MAD', 'Moroccan dirham', 'MAD', '.eh', 'الصحراء الغربية', 'Sahrawi, Sahrawian, Sahraouian', 'null', 24.5, -13, '🇪🇭', 'U+1F1EA U+1F1ED', 'Africa', 'Northern Africa');
INSERT INTO `countries` VALUES (247, 245, 'Yemen', 'YEM', 'YE', '887', '+967', 'Sanaa', 'YER', 'Yemeni rial', '﷼', '.ye', 'اليَمَن', 'Yemeni', 'null', 15, 48, '🇾🇪', 'U+1F1FE U+1F1EA', 'Asia', 'Western Asia');
INSERT INTO `countries` VALUES (248, 246, 'Zambia', 'ZMB', 'ZM', '894', '+260', 'Lusaka', 'ZMW', 'Zambian kwacha', 'ZK', '.zm', 'Zambia', 'Zambian', 'null', -15, 30, '🇿🇲', 'U+1F1FF U+1F1F2', 'Africa', 'Southern Africa');
INSERT INTO `countries` VALUES (249, 247, 'Zimbabwe', 'ZWE', 'ZW', '716', '+263', 'Harare', 'ZWL', 'Zimbabwe Dollar', '$', '.zw', 'Zimbabwe', 'Zimbabwean', 'null', -20, 30, '🇿🇼', 'U+1F1FF U+1F1FC', 'Africa', 'Eastern Africa');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
