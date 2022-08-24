CREATE TABLE `consult__tags` (
  `consult_tag_id` int NOT NULL AUTO_INCREMENT,
  `tag_id` int NOT NULL,
  `consult_id` int NOT NULL,
  PRIMARY KEY (`consult_tag_id`),
  UNIQUE KEY `consult_tag_id_UNIQUE` (`consult_tag_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
