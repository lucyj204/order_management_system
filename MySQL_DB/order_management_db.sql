CREATE DATABASE order_management;

USE order_management;

CREATE TABLE `order` (
order_id MEDIUMINT UNSIGNED AUTO_INCREMENT,
order_status VARCHAR(10) DEFAULT 'DRAFT',
PRIMARY KEY (order_id));

CREATE TABLE order_line (
product_name VARCHAR(100),
product_quantity SMALLINT UNSIGNED,
order_id MEDIUMINT UNSIGNED,
status VARCHAR(10) DEFAULT 'DRAFT',
FOREIGN KEY (order_id) REFERENCES `order`(order_id))
;

ALTER TABLE order_line ADD UNIQUE product_order_index (order_id, product_name);   