-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: bloodbank
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `donation`
--

DROP TABLE IF EXISTS `donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `recipient_id` int DEFAULT NULL,
  `recipient_name` varchar(100) DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `unit_donated` int DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `recipient_id` (`recipient_id`),
  CONSTRAINT `donation_ibfk_1` FOREIGN KEY (`recipient_id`) REFERENCES `recipient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation`
--

LOCK TABLES `donation` WRITE;
/*!40000 ALTER TABLE `donation` DISABLE KEYS */;
INSERT INTO `donation` VALUES (1,1,'Anjali Sharma','AB+',1,'2025-04-05 10:30:00'),(2,2,'Safir Sayyed','B+',1,'2025-04-06 22:05:47'),(3,4,'Karan Kalawant','B+',1,'2025-04-07 01:53:49'),(4,5,'kunal kalawant','O-',1,'2025-04-07 03:27:39'),(5,6,'Palak Sharma','AB+',1,'2025-04-07 04:06:59'),(6,7,'Ashish Raut','B+',2,'2025-04-12 13:14:31'),(7,8,'Narendra Walunj','B-',3,'2025-04-12 13:14:35'),(8,9,'Sakina Bootwala','A+',2,'2025-04-12 13:18:00'),(9,10,'Neha Agarwal','O-',1,'2025-04-12 18:08:56'),(10,13,'Riya Shah','B-',1,'2025-04-13 05:55:52');
/*!40000 ALTER TABLE `donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor`
--

DROP TABLE IF EXISTS `donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor`
--

LOCK TABLES `donor` WRITE;
/*!40000 ALTER TABLE `donor` DISABLE KEYS */;
INSERT INTO `donor` VALUES (1,'Ayush Ohal',21,'ayush.ohal@example.com','A+','9876543210'),(2,'Anish Bancchod',25,'anish.bancchod@example.com','B-','9123456789'),(3,'Manthan Badgujar',30,'manthan.badgujar@example.com','O+','9988776655'),(4,'Hrishikesh Wakode',21,'hrishikesh.wakode@example.com','B+','8829644782'),(5,'Nachiket Joshi',18,'nachiket@example.com','B+','8789947483'),(6,'prathamesh londhe',29,'prathamesh@example.com','O-','8888997860'),(7,'Zafar Khan',21,'zafar@example.com','AB+','7768909765'),(8,'Pradhyut Singh',22,'pradhyut@example.com','A+','8885974882'),(9,'Saurabh Singh',24,'saurabh@example.com','B+','6879685586'),(10,'Ashlesha Raut',19,'ashlesha@example.com','B-','6879687989'),(11,'Anish Rathi',23,'anish@example.com','O-','9837593897');
/*!40000 ALTER TABLE `donor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `blood_group` varchar(5) DEFAULT NULL,
  `units_available` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `blood_group` (`blood_group`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,'A+',5),(2,'A-',6),(3,'B+',7),(4,'B-',3),(5,'AB+',3),(6,'AB-',3),(7,'O+',8),(8,'O-',4);
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipient`
--

DROP TABLE IF EXISTS `recipient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipient` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `units_required` int DEFAULT NULL,
  `hospital_name` varchar(100) DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `requested_by` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipient`
--

LOCK TABLES `recipient` WRITE;
/*!40000 ALTER TABLE `recipient` DISABLE KEYS */;
INSERT INTO `recipient` VALUES (1,'Anjali Sharma',28,'anjali.sharma@example.com','B-',1,'Ruby Hospital','9876501234','hospital','Approved'),(2,'Safir Sayyed',30,'safir@example.com','B+',1,'ruby hospital','8979657632','bloodbank','Approved'),(3,'Yashraj Koli',29,'yashraj@example.com','A-',1,'ruby hospital','1234567890','hospital','Rejected'),(4,'Karan Kalawant',31,'karan@example.com','B+',1,'ruby hospital','9898767657','hospital','Approved'),(5,'kunal kalawant',33,'kunal@example.com','O-',1,'ruby hospital','8988876778','hospital','Approved'),(6,'Palak Sharma',18,'palak@example.com','AB+',1,'ruby hospital','5678956789','hospital','Approved'),(7,'Ashish Raut',33,'ashish@example.com','B+',2,'ruby hospital','7786975890',NULL,'Approved'),(8,'Narendra Walunj',45,'narendra@example.com','B-',3,'ruby hospital','9895557664',NULL,'Approved'),(9,'Sakina Bootwala',34,'sakina@example.com','A+',2,'ruby hospital','9953995584',NULL,'Approved'),(10,'Neha Agarwal',45,'neha@example.com','O-',1,'ruby hospital','7859498900',NULL,'Approved'),(11,'Sanjana Sharma',55,'sanjana@example.com','A+',1,'ruby hospital','9986958554',NULL,'Rejected'),(12,'Aryan Tembhurne',29,'aryan@example.com','A+',1,'ruby hospital','9984638501',NULL,'Rejected'),(13,'Riya Shah',45,'riya@example.com','B-',1,'ruby hospital','8695958490',NULL,'Approved');
/*!40000 ALTER TABLE `recipient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  `hospital_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'ayush','scrypt:32768:8:1$PHv7F7y9IIC4p8OX$b4fe1818d16ae14f28e1715f5f022163a8ec01ad1951f1f7c2b47d2bef0a0dad2cb34919fb5f79fa32589f1e4874b89f95d465bb4ef1d1577bb2ac5f7100c3a2','bloodbank',NULL),(2,'anish','scrypt:32768:8:1$fWFkJQRjoh5wPN9q$b2d2c3b189889c75f598435382f25cfa99b7f577d813136689647fe5949630fd4955df623ec3be60f4be3c3d21171e05542dc5750bf418f0921048f7b80b82a7','hospital','ruby hospital');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-16 21:49:21
