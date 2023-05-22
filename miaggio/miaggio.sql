-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 20. Apr 2023 um 13:42
-- Server-Version: 10.4.25-MariaDB
-- PHP-Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `miaggio`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `adress`
--

CREATE TABLE `adress` (
  `id` int(11) NOT NULL,
  `street` varchar(90) NOT NULL,
  `house_number` int(11) NOT NULL,
  `postal_code_id` int(5) NOT NULL COMMENT 'FK_postal_code'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `article`
--

CREATE TABLE `article` (
  `id` int(11) NOT NULL,
  `name` varchar(90) NOT NULL,
  `description` varchar(200) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `status` tinyint(1) NOT NULL COMMENT 'FK_delivery'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bill`
--

CREATE TABLE `bill` (
  `id` int(11) NOT NULL,
  `adress_id` int(11) NOT NULL COMMENT 'FK_adress',
  `payment_id` int(11) NOT NULL COMMENT 'FK_payment',
  `delivery_id` int(11) NOT NULL COMMENT 'FK_delivery'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL COMMENT 'FK_customer',
  `articles` int(11) NOT NULL COMMENT 'FK_article'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(90) NOT NULL,
  `description` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL COMMENT 'PK',
  `name` varchar(90) NOT NULL,
  `first_name` varchar(90) NOT NULL,
  `birthdate` date NOT NULL,
  `email` varchar(90) NOT NULL,
  `phone_number` int(20) NOT NULL,
  `password` varchar(90) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `delivery`
--

CREATE TABLE `delivery` (
  `id` int(11) NOT NULL,
  `deliverer` varchar(90) NOT NULL,
  `date_of_receival` date NOT NULL,
  `article_id` int(11) NOT NULL COMMENT 'FK_article'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `material`
--

CREATE TABLE `material` (
  `id` int(11) NOT NULL,
  `name` varchar(90) NOT NULL,
  `description` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `payment`
--

CREATE TABLE `payment` (
  `id` int(11) NOT NULL,
  `payment_method` varchar(90) NOT NULL,
  `sum` float NOT NULL,
  `cart_articles` int(11) NOT NULL COMMENT 'FK_cart',
  `customer_id` int(11) NOT NULL COMMENT 'FK_customer'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `postal_code`
--

CREATE TABLE `postal_code` (
  `id` int(5) NOT NULL,
  `city` varchar(90) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `adress`
--
ALTER TABLE `adress`
  ADD PRIMARY KEY (`id`),
  ADD KEY `postel_code_id` (`postal_code_id`);

--
-- Indizes für die Tabelle `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `bill`
--
ALTER TABLE `bill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `adress_id` (`adress_id`),
  ADD KEY `payment_id` (`payment_id`),
  ADD KEY `delivery_id` (`delivery_id`);

--
-- Indizes für die Tabelle `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `articles` (`articles`);

--
-- Indizes für die Tabelle `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `delivery`
--
ALTER TABLE `delivery`
  ADD PRIMARY KEY (`id`),
  ADD KEY `article_id` (`article_id`);

--
-- Indizes für die Tabelle `material`
--
ALTER TABLE `material`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cart_articles` (`cart_articles`),
  ADD KEY `customer_id_fk` (`customer_id`);

--
-- Indizes für die Tabelle `postal_code`
--
ALTER TABLE `postal_code`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `adress`
--
ALTER TABLE `adress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `article`
--
ALTER TABLE `article`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `bill`
--
ALTER TABLE `bill`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PK';

--
-- AUTO_INCREMENT für Tabelle `delivery`
--
ALTER TABLE `delivery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `material`
--
ALTER TABLE `material`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `payment`
--
ALTER TABLE `payment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `postal_code`
--
ALTER TABLE `postal_code`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `adress`
--
ALTER TABLE `adress`
  ADD CONSTRAINT `postel_code_id` FOREIGN KEY (`postal_code_id`) REFERENCES `postal_code` (`id`);

--
-- Constraints der Tabelle `bill`
--
ALTER TABLE `bill`
  ADD CONSTRAINT `adress_id` FOREIGN KEY (`adress_id`) REFERENCES `adress` (`id`),
  ADD CONSTRAINT `delivery_id` FOREIGN KEY (`delivery_id`) REFERENCES `delivery` (`id`),
  ADD CONSTRAINT `payment_id` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`);

--
-- Constraints der Tabelle `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `articles` FOREIGN KEY (`articles`) REFERENCES `article` (`id`),
  ADD CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`);

--
-- Constraints der Tabelle `delivery`
--
ALTER TABLE `delivery`
  ADD CONSTRAINT `article_id` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

--
-- Constraints der Tabelle `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `cart_articles` FOREIGN KEY (`cart_articles`) REFERENCES `cart` (`articles`),
  ADD CONSTRAINT `customer_id_fk` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
