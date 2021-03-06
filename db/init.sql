
set names utf8mb4;

DROP TABLE IF EXISTS news_item;
-- news title
CREATE TABLE news_item(
  `news_id` INT NOT NULL AUTO_INCREMENT,
  `source` VARCHAR(32) NOT NULL,
  `url` VARCHAR(128) NOT NULL,
  `title` VARCHAR(128) NOT NULL,
  `category` VARCHAR(16) NOT NULL,
  `last_update_time` TIMESTAMP,
  `date` DATE,
  PRIMARY KEY (news_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='news item';

DROP TABLE IF EXISTS news_paragraph;
-- news paragraph
CREATE TABLE news_paragraph(
  `para_id` INT NOT NULL AUTO_INCREMENT,
  `news_id` INT NOT NULL,
  `para_content` TEXT,
  `is_image` TINYINT,
  `date` DATE,
  PRIMARY KEY (para_id),
  KEY (news_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='paragraph content';


DROP TABLE IF EXISTS cached_url;
CREATE TABLE  cached_url(
  `id` INT NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(128) NOT NULL,
  `source` VARCHAR(32) NOT NULL,
  `date` DATE,
  PRIMARY KEY (id),
  KEY(source),
  KEY(date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='cached URL';