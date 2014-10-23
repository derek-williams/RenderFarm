-------------------------------
--- Create database 'hydra' ---
-------------------------------

CREATE DATABASE IF NOT EXISTS `hydra`
	DEFAULT CHARSET=latin1
	DEFAULT COLLATE

--------------------------
--- Create table 'log' ---
--------------------------

CREATE TABLE IF NOT EXISTS `log`
(
	`log_id` INT(10) unsigned NOT NULL AUTO_INCREMENT,
	`log_timestamp` TIMESTAMP,
	`log_level` ENUM('DEBUG','INFO','WARN','ERROR','CRITICAL'),
	`log_hostname` VARCHAR(64) NOT NULL,
	`log_lineno` VARCHAR(64) NOT NULL,
	`log_msg` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`log_id`)
	-- Additional keys
	
) 
ENGINE=InnoDB 
DEFAULT CHARSET=latin1
AUTO_INCREMENT=1
;
	

------------------------------
--- Create table 'job' ---
------------------------------

CREATE TABLE IF NOT EXISTS `job`
(
	`job_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`job_origin_hostname` VARCHAR(64) NOT NULL,
	`job_priority` ENUM('LOW', 'MED', 'HIGH', 'CRITICAL'),
	`job_status` ENUM('WAIT', 'RUNNING', 'SUCCESS', 'FAILED'),
	`job_pickle` BLOB,
	PRIMARY KEY (`job_id`)
	-- Additional keys
	
) 
ENGINE=InnoDB 
DEFAULT CHARSET=latin1
AUTO_INCREMENT=1
;
