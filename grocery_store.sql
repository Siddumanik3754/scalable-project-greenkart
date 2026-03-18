-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 20, 2025 at 06:14 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `grocery_store`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `Id` int(11) NOT NULL,
  `UserId` int(11) NOT NULL,
  `ShippingId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`Id`, `UserId`, `ShippingId`) VALUES
(1, 17, 0),
(2, 18, 0),
(3, 16, 0),
(5, 20, NULL),
(6, 21, NULL),
(7, 22, NULL),
(8, 23, NULL),
(9, 24, NULL),
(10, 25, NULL),
(11, 26, NULL),
(12, 28, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `cartproduct`
--

CREATE TABLE `cartproduct` (
  `CartId` int(11) NOT NULL,
  `ProductId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cartproduct`
--

INSERT INTO `cartproduct` (`CartId`, `ProductId`) VALUES
(1, 8),
(1, 7),
(1, 17),
(1, 14);

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `Id` int(11) NOT NULL,
  `UserId` int(11) NOT NULL,
  `Status` varchar(255) NOT NULL DEFAULT 'processing',
  `Total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`Id`, `UserId`, `Status`, `Total`) VALUES
(4, 1, 'processing', '2089.45'),
(5, 1, 'processing', '768.47'),
(6, 1, 'processing', '768.47'),
(7, 1, 'processing', '218.99'),
(8, 1, 'processing', '209.48'),
(9, 1, 'processing', '579.47'),
(15, 18, 'processing', '2469.96'),
(16, 16, 'processing', '648.48'),
(17, 16, 'processing', '889.47'),
(18, 16, 'processing', '549.48'),
(19, 18, 'processing', '3372.95'),
(20, 16, 'processing', '2159.97'),
(21, 16, 'processing', '119.99'),
(22, 18, 'processing', '218.99'),
(23, 20, 'processing', '1389.48'),
(24, 21, 'processing', '949.46'),
(25, 16, 'processing', '549.48'),
(26, 16, 'processing', '119.99'),
(27, 22, 'processing', '1559.46'),
(28, 16, 'processing', '4522.89'),
(29, 16, 'processing', '388.97'),
(30, 16, 'processing', '218.99'),
(31, 23, 'processing', '768.47'),
(32, 23, 'processing', '2584.46'),
(33, 24, 'processing', '2993.94'),
(34, 24, 'processing', '218.99'),
(35, 24, 'processing', '218.99'),
(36, 24, 'processing', '218.99'),
(37, 24, 'processing', '218.99'),
(38, 24, 'processing', '218.99'),
(39, 25, 'processing', '1527.47'),
(40, 25, 'processing', '218.99'),
(41, 25, 'processing', '297.00'),
(42, 26, 'processing', '99.00'),
(43, 26, 'processing', '99.00'),
(44, 26, 'processing', '317.99'),
(45, 26, 'processing', '119.99'),
(46, 26, 'processing', '99.00'),
(47, 26, 'processing', '89.49'),
(48, 26, 'processing', '579.98'),
(49, 26, 'processing', '198.00'),
(50, 26, 'processing', '89.99'),
(51, 25, 'processing', '218.99'),
(52, 25, 'processing', '99.00'),
(53, 28, 'processing', '218.99'),
(54, 28, 'processing', '99.00'),
(55, 28, 'processing', '678.98');

-- --------------------------------------------------------

--
-- Table structure for table `orderproduct`
--

CREATE TABLE `orderproduct` (
  `OrderId` int(11) NOT NULL,
  `ProductId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orderproduct`
--

INSERT INTO `orderproduct` (`OrderId`, `ProductId`) VALUES
(8, 6),
(8, 8),
(9, 16),
(9, 11),
(9, 8),
(15, 11),
(15, 10),
(15, 12),
(15, 6),
(16, 5),
(16, 8),
(16, 7),
(17, 8),
(17, 12),
(17, 17),
(18, 7),
(18, 8),
(19, 8),
(19, 12),
(19, 10),
(19, 11),
(19, 9),
(19, 14),
(19, 5),
(20, 7),
(20, 11),
(20, 10),
(21, 6),
(22, 5),
(22, 6),
(23, 10),
(23, 8),
(24, 16),
(24, 12),
(24, 6),
(24, 8),
(25, 8),
(25, 7),
(26, 6),
(27, 10),
(27, 16),
(27, 8),
(27, 15),
(28, 5),
(28, 6),
(28, 7),
(28, 8),
(28, 9),
(28, 10),
(28, 11),
(28, 12),
(28, 13),
(28, 14),
(28, 15),
(28, 16),
(28, 17),
(29, 5),
(29, 6),
(29, 16),
(29, 15),
(30, 5),
(30, 6),
(31, 5),
(31, 6),
(31, 8),
(31, 7),
(32, 5),
(32, 7),
(32, 10),
(32, 12),
(32, 14),
(33, 6),
(33, 8),
(33, 9),
(33, 10),
(33, 11),
(33, 14),
(33, 13),
(34, 5),
(34, 6),
(35, 5),
(35, 6),
(36, 5),
(36, 6),
(37, 5),
(37, 6),
(38, 5),
(38, 6),
(39, 5),
(39, 6),
(39, 7),
(39, 8),
(39, 9),
(40, 5),
(40, 6),
(41, 5),
(41, 5),
(41, 5),
(42, 5),
(43, 5),
(44, 5),
(44, 5),
(44, 6),
(45, 6),
(46, 5),
(47, 8),
(48, 6),
(48, 7),
(49, 5),
(49, 5),
(50, 16),
(51, 5),
(51, 6),
(52, 5),
(53, 5),
(53, 6),
(54, 5),
(55, 5),
(55, 6),
(55, 7);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `Id` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Description` varchar(255) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `Image` varchar(255) NOT NULL,
  `Category` varchar(255) NOT NULL,
  `product_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`Id`, `Name`, `Description`, `Price`, `Image`, `Category`, `product_id`) VALUES
(5, 'Bananas', 'Deliciously sweet and rich in potassium, bananas are a nutritious and energizing fruit that satisfies your taste buds and supports your active lifestyle.', '99.00', 'product-images/bananas.jpg', 'Fruit', '3'),
(6, 'Milk', 'Milk is a nutrient-rich food that is an excellent source of protein, calcium, and other essential vitamins and minerals.', '119.99', 'product-images/milk.jpg', 'Dairy', '4'),
(7, 'Eggs', 'Nutritious and versatile, these protein-rich gems are perfect for breakfast or baking, adding delicious flavor to your meals.', '459.99', 'product-images/eggs.jpg', 'Dairy', '5'),
(8, 'Bread', 'Wholesome and comforting, bread is a staple food that complements any meal with its soft texture and versatile flavors.', '89.49', 'product-images/bread.jpg', 'Bread', '6'),
(9, 'Cheese', 'Indulge in the delightful world of cheese, a diverse range of flavors and textures that adds a creamy and savory touch to your dishes.', '759.00', 'product-images/cheese.jpg', 'Dairy', '7'),
(10, 'Chicken', 'Tender and protein-packed, chicken is a versatile white meat that offers a lean and delicious option for your everyday meals.', '1299.99', 'product-images/chicken.jpg', 'Meat', '8'),
(11, 'Beef', 'Savor the rich taste of beef, a succulent red meat that brings a hearty and satisfying flavor to your favorite recipes.', '399.99', 'product-images/beef.jpg', 'Meat', '9'),
(12, 'Salmon', 'Dive into the goodness of salmon, a pink fish renowned for its delicate taste and abundant omega-3 fatty acids, promoting a healthy heart and brain.', '649.99', 'product-images/salmon.jpg', 'Fish', '10'),
(13, 'Apples', 'Enjoy the crisp and refreshing nature of apples, a delicious and nutritious fruit that adds a touch of sweetness to your snacks and recipes.', '249.99', 'product-images/apples.jpg', 'Fruit', '1'),
(14, 'Oranges', 'Experience the zesty and invigorating flavors of oranges, a citrus fruit bursting with vitamin C and a refreshing burst of citrusy goodness.', '75.49', 'product-images/oranges.jpg', 'Fruit', '2'),
(15, 'Grapes', 'Enjoy the sweet and refreshing taste of grapes, a versatile fruit that is perfect for snacking or adding to salads and desserts.', '79.99', 'product-images/grapes.jpg', 'Fruit', '15'),
(16, 'Tomatoes', 'Versatile and vibrant, tomatoes are a staple ingredient that adds a tangy and savory touch to your salads, sauces, and more.', '89.99', 'product-images/tomatoes.jpg', 'Vegetable', '16'),
(17, 'Strawberries', 'Sweet and juicy, strawberries are a delightful fruit that brings a burst of flavor to your desserts and snacks.', '149.99', 'product-images/strawberries.jpg', 'Fruit', '17');

-- --------------------------------------------------------

--
-- Table structure for table `shipping`
--

CREATE TABLE `shipping` (
  `Id` int(11) NOT NULL,
  `UserId` int(11) DEFAULT NULL,
  `Full_Name` varchar(255) DEFAULT NULL,
  `Street_Address` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State_Province` varchar(255) DEFAULT NULL,
  `Postal_Code` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `shipping`
--

INSERT INTO `shipping` (`Id`, `UserId`, `Full_Name`, `Street_Address`, `City`, `State_Province`, `Postal_Code`, `Country`) VALUES
(10, 17, 'Teddy G', 'Langas', 'Nakuru', 'Mombasa', '20200', 'Kenya'),
(11, 18, 'James W', 'Kiamunyi', 'Molo', 'Rift-Valley', '20100', 'Kenya'),
(13, 20, 'John Kelly', 'Mangu', 'Kericho', 'Rift-Valley', '011000', 'South Africa'),
(14, 21, 'Motty Blue', 'Wall street', 'New York', 'Boston', '120543', 'United States'),
(31, 16, 'John Foe', 'Kiamunyi', 'Meru', 'Central', '40320', 'Kenya'),
(32, 22, 'Joe Kamau', 'Karen', 'Nairobi', 'Central', '00100', 'Kenya'),
(34, 23, 'Kate Mambo', 'Kiamunyi', 'Mombasa', 'Mombasa', '00500', 'Kenya'),
(36, 24, 'user', 'user', 'mumbai', 'maharashtra', '400092', 'ind'),
(37, 25, 'user ', 'user', 'mumbai', 'maha', '123', 'ind'),
(38, 26, 'user', 'user', 'mumbai', 'maharashtra', '123', 'ind'),
(39, 28, 'user', 'user', 'mumbai', 'maharashtra', '123', 'ind');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `Id` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Phone` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`Id`, `Name`, `Email`, `Password`, `Phone`) VALUES
(11, 'Gregory Kibs', 'gregkibs@example.com', 'Greg', '0741123123'),
(12, 'Martin Luther', 'martinluther@example.com', 'Martin', '0712345678'),
(13, 'Roy Martin', 'roymartin@example.com', 'Roy', '0106320609'),
(14, 'Lawrence Kibs', 'lawrencekibs@example.com', 'Larry', '0792123123'),
(15, 'Gregory Remmie', 'gregrem@you.com', 'Remy', '0741321321'),
(16, 'John Foe', 'johnfoe@gmail.com', '$2b$12$6lafyk5ULE2xwv.FqyzyHuntN8VMwNRkae7mForvet9FgCz/p.0Aq', '0790320320'),
(17, 'Teddy Gift', 'teddyg@you.com', '$2b$12$AH3cEuTI0ru3Amkj3LIVJOp40QTycsjIfT9I9WqQsxsTrezUCiG1a', '0790192324'),
(18, 'James W', 'wjames@you.com', '$2b$12$7OIWlRTvdlnv6UEZ7Y888uwqADlhEHj6b9NOmAtDwkV2ZHt5nUly6', '0722123123'),
(19, 'Gregory Remmie', 'remmiegreg@you.com', '$2b$12$hZGNYxCVEaX7qH.TNt4GhuAgI5rKEDmHE6dFlyseEKU0g5v6GnoNy', '0741123123'),
(20, 'Kelly John', 'johnkelly@you.com', '$2b$12$HqVye1GyzqVucrGFUzeyDOGH.Wy.m8FCMCvbZDUnfzUXkqy4oMoPy', '0790234234'),
(21, 'Motty Blue', 'mottyb@you.com', '$2b$12$7YvOEYT0H2oF8VG9C1UzTeKO62OTWc2niFOczWQd89FoodvO/RCS6', '0102030405'),
(22, 'Joe Kamau', 'joekamau@gmail.com', '$2b$12$IMrW/4bFYS8Orff8MJA2g.AFHK4VAnzV90D7anpWR7rFimMT2ox.C', '0790500500'),
(23, 'Kate Mambo', 'mambokate@you.com', '$2b$12$xKRNgh//QHxoeVqlvEvdceUVjLCl9a4xjwGM7sIm3G91xGf2SwgBC', '0790192324'),
(24, 'user', 'user@gmail.com', '$2b$12$gZsrrIq8/zuZ4w0pT44Qme0pW2cP3DVa3UbLgeCKRiddF3QUdyEFe', '1234567891'),
(25, 'kunal', 'kunalproject025@gmail.com', '$2b$12$PP5gAAbqVhZmX2T0FWxoxukOT0/S5LhpvuZErYb5ewFfk/gRgORES', '9123456789'),
(26, 'kunal', 'kunaltalvatkar025@gmail.com', '$2b$12$lCbG2uhigZdKTn1Je/CKAemew0ZCETVwk.LShgHqTeCtGKa7BVILe', '9123456789'),
(27, 'asd', 'admin@frb.com', '$2b$12$2nZBfqPi1x1fniAjLENNh.Yymn32utKkKAb7e8ozk4aD4.hXKuKIu', '123'),
(28, 'kunal', 'talvatkarkunal@gmail.com', '$2b$12$0wqp4tmp9lr4BW2d.iS7auvIrPHY8NMZG/pKrlmDKtwNq551NGY8.', '1234');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `UserId` (`UserId`),
  ADD KEY `ShippingId` (`ShippingId`);

--
-- Indexes for table `cartproduct`
--
ALTER TABLE `cartproduct`
  ADD KEY `CartId` (`CartId`),
  ADD KEY `ProductId` (`ProductId`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `UserId` (`UserId`);

--
-- Indexes for table `orderproduct`
--
ALTER TABLE `orderproduct`
  ADD KEY `OrderId` (`OrderId`),
  ADD KEY `ProductId` (`ProductId`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `shipping`
--
ALTER TABLE `shipping`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `UserId` (`UserId`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `unique_email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `shipping`
--
ALTER TABLE `shipping`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `Cart_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `user` (`Id`),
  ADD CONSTRAINT `Cart_ibfk_2` FOREIGN KEY (`ShippingId`) REFERENCES `shipping` (`Id`);

--
-- Constraints for table `cartproduct`
--
ALTER TABLE `cartproduct`
  ADD CONSTRAINT `CartProduct_ibfk_1` FOREIGN KEY (`CartId`) REFERENCES `cart` (`Id`),
  ADD CONSTRAINT `CartProduct_ibfk_2` FOREIGN KEY (`ProductId`) REFERENCES `product` (`Id`);

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `Order_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `user` (`Id`);

--
-- Constraints for table `orderproduct`
--
ALTER TABLE `orderproduct`
  ADD CONSTRAINT `OrderProduct_ibfk_1` FOREIGN KEY (`OrderId`) REFERENCES `order` (`Id`),
  ADD CONSTRAINT `OrderProduct_ibfk_2` FOREIGN KEY (`ProductId`) REFERENCES `product` (`Id`);

--
-- Constraints for table `shipping`
--
ALTER TABLE `shipping`
  ADD CONSTRAINT `Shipping_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `user` (`Id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
