-- ====================================
-- SQL必知必会 - 数据库建表脚本
-- 适配MySQL数据库
-- ====================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS sql_bizhibihui DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE sql_bizhibihui;

-- ====================================
-- 1. Customers 客户表
-- ====================================
DROP TABLE IF EXISTS `Customers`;
CREATE TABLE `Customers` (
    `cust_id` VARCHAR(255) NOT NULL COMMENT '客户ID',
    `cust_name` VARCHAR(255) NOT NULL COMMENT '客户姓名',
    `cust_address` VARCHAR(255) DEFAULT NULL COMMENT '客户地址',
    `cust_city` VARCHAR(255) DEFAULT NULL COMMENT '客户城市',
    `cust_state` VARCHAR(255) DEFAULT NULL COMMENT '客户州',
    `cust_zip` VARCHAR(255) DEFAULT NULL COMMENT '客户邮编',
    `cust_country` VARCHAR(255) DEFAULT NULL COMMENT '客户国家',
    `cust_contact` VARCHAR(255) DEFAULT NULL COMMENT '客户联系人',
    `cust_email` VARCHAR(255) DEFAULT NULL COMMENT '客户邮箱',
    PRIMARY KEY (`cust_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户表';

-- ====================================
-- 2. Vendors 供应商表
-- ====================================
DROP TABLE IF EXISTS `Vendors`;
CREATE TABLE `Vendors` (
    `vend_id` VARCHAR(255) NOT NULL COMMENT '供应商ID',
    `vend_name` VARCHAR(255) NOT NULL COMMENT '供应商名称',
    `vend_address` VARCHAR(255) DEFAULT NULL COMMENT '供应商地址',
    `vend_city` VARCHAR(255) DEFAULT NULL COMMENT '供应商城市',
    `vend_state` VARCHAR(255) DEFAULT NULL COMMENT '供应商州',
    `vend_zip` VARCHAR(255) DEFAULT NULL COMMENT '供应商邮编',
    `vend_country` VARCHAR(255) DEFAULT NULL COMMENT '供应商国家',
    PRIMARY KEY (`vend_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='供应商表';

-- ====================================
-- 3. Products 产品表
-- ====================================
DROP TABLE IF EXISTS `Products`;
CREATE TABLE `Products` (
    `prod_id` VARCHAR(255) NOT NULL COMMENT '产品ID',
    `vend_id` VARCHAR(255) NOT NULL COMMENT '供应商ID',
    `prod_name` VARCHAR(255) NOT NULL COMMENT '产品名称',
    `prod_price` DECIMAL(10, 2) NOT NULL COMMENT '产品价格',
    `prod_desc` TEXT COMMENT '产品描述',
    PRIMARY KEY (`prod_id`),
    KEY `idx_vend_id` (`vend_id`),
    CONSTRAINT `fk_products_vendors` FOREIGN KEY (`vend_id`) REFERENCES `Vendors` (`vend_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品表';

-- ====================================
-- 4. Orders 订单表
-- ====================================
DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders` (
    `order_num` INT NOT NULL COMMENT '订单号',
    `order_date` DATETIME NOT NULL COMMENT '订单日期',
    `cust_id` VARCHAR(255) NOT NULL COMMENT '客户ID',
    PRIMARY KEY (`order_num`),
    KEY `idx_cust_id` (`cust_id`),
    CONSTRAINT `fk_orders_customers` FOREIGN KEY (`cust_id`) REFERENCES `Customers` (`cust_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- ====================================
-- 5. OrderItems 订单项表
-- ====================================
DROP TABLE IF EXISTS `OrderItems`;
CREATE TABLE `OrderItems` (
    `order_num` INT NOT NULL COMMENT '订单号',
    `order_item` INT NOT NULL COMMENT '订单项号',
    `prod_id` VARCHAR(255) NOT NULL COMMENT '产品ID',
    `quantity` INT NOT NULL COMMENT '数量',
    `item_price` DECIMAL(10, 2) NOT NULL COMMENT '项目价格',
    PRIMARY KEY (`order_num`, `order_item`),
    KEY `idx_order_num` (`order_num`),
    KEY `idx_prod_id` (`prod_id`),
    CONSTRAINT `fk_orderitems_orders` FOREIGN KEY (`order_num`) REFERENCES `Orders` (`order_num`),
    CONSTRAINT `fk_orderitems_products` FOREIGN KEY (`prod_id`) REFERENCES `Products` (`prod_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单项表';

-- ====================================
-- 6. Films 电影表（部分题目使用）
-- ====================================
DROP TABLE IF EXISTS `Films`;
CREATE TABLE `Films` (
    `film_id` INT NOT NULL COMMENT '电影ID',
    `title` VARCHAR(255) NOT NULL COMMENT '电影标题',
    `description` TEXT COMMENT '电影描述',
    `release_year` INT DEFAULT NULL COMMENT '发行年份',
    `language_id` INT DEFAULT NULL COMMENT '语言ID',
    `original_language_id` INT DEFAULT NULL COMMENT '原始语言ID',
    `rental_duration` INT DEFAULT NULL COMMENT '租借时长',
    `rental_rate` DECIMAL(5, 2) DEFAULT NULL COMMENT '租借费率',
    `length` INT DEFAULT NULL COMMENT '电影时长',
    `replacement_cost` DECIMAL(5, 2) DEFAULT NULL COMMENT '重置费用',
    `rating` VARCHAR(10) DEFAULT NULL COMMENT '评级',
    `special_features` VARCHAR(255) DEFAULT NULL COMMENT '特殊特性',
    `last_update` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
    PRIMARY KEY (`film_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影表';

-- ====================================
-- 7. Categories 电影分类表
-- ====================================
DROP TABLE IF EXISTS `Categories`;
CREATE TABLE `Categories` (
    `category_id` INT NOT NULL COMMENT '分类ID',
    `name` VARCHAR(255) NOT NULL COMMENT '分类名称',
    `last_update` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
    PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影分类表';

-- ====================================
-- 8. Film_Category 电影分类关联表
-- ====================================
DROP TABLE IF EXISTS `Film_Category`;
CREATE TABLE `Film_Category` (
    `film_id` INT NOT NULL COMMENT '电影ID',
    `category_id` INT NOT NULL COMMENT '分类ID',
    `last_update` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
    PRIMARY KEY (`film_id`, `category_id`),
    KEY `idx_category_id` (`category_id`),
    CONSTRAINT `fk_film_category_films` FOREIGN KEY (`film_id`) REFERENCES `Films` (`film_id`),
    CONSTRAINT `fk_film_category_categories` FOREIGN KEY (`category_id`) REFERENCES `Categories` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影分类关联表';

-- ====================================
-- 9. Actors 演员表
-- ====================================
DROP TABLE IF EXISTS `Actors`;
CREATE TABLE `Actors` (
    `actor_id` INT NOT NULL COMMENT '演员ID',
    `first_name` VARCHAR(255) NOT NULL COMMENT '名字',
    `last_name` VARCHAR(255) NOT NULL COMMENT '姓氏',
    `last_update` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
    PRIMARY KEY (`actor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='演员表';

-- ====================================
-- 10. Employees 员工表（部分题目使用）
-- ====================================
DROP TABLE IF EXISTS `Employees`;
CREATE TABLE `Employees` (
    `emp_no` INT NOT NULL COMMENT '员工编号',
    `birth_date` DATE NOT NULL COMMENT '出生日期',
    `first_name` VARCHAR(255) NOT NULL COMMENT '名字',
    `last_name` VARCHAR(255) NOT NULL COMMENT '姓氏',
    `gender` ENUM('M', 'F') NOT NULL COMMENT '性别',
    `hire_date` DATE NOT NULL COMMENT '入职日期',
    PRIMARY KEY (`emp_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工表';

-- ====================================
-- 11. Salaries 薪水表
-- ====================================
DROP TABLE IF EXISTS `Salaries`;
CREATE TABLE `Salaries` (
    `emp_no` INT NOT NULL COMMENT '员工编号',
    `salary` INT NOT NULL COMMENT '薪水',
    `from_date` DATE NOT NULL COMMENT '起始日期',
    `to_date` DATE NOT NULL COMMENT '结束日期',
    PRIMARY KEY (`emp_no`, `from_date`),
    CONSTRAINT `fk_salaries_employees` FOREIGN KEY (`emp_no`) REFERENCES `Employees` (`emp_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='薪水表';

-- ====================================
-- 12. Departments 部门表
-- ====================================
DROP TABLE IF EXISTS `Departments`;
CREATE TABLE `Departments` (
    `dept_no` VARCHAR(255) NOT NULL COMMENT '部门编号',
    `dept_name` VARCHAR(255) NOT NULL COMMENT '部门名称',
    PRIMARY KEY (`dept_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='部门表';

-- ====================================
-- 13. Dept_Emp 员工部门关联表
-- ====================================
DROP TABLE IF EXISTS `Dept_Emp`;
CREATE TABLE `Dept_Emp` (
    `emp_no` INT NOT NULL COMMENT '员工编号',
    `dept_no` VARCHAR(255) NOT NULL COMMENT '部门编号',
    `from_date` DATE NOT NULL COMMENT '起始日期',
    `to_date` DATE NOT NULL COMMENT '结束日期',
    PRIMARY KEY (`emp_no`, `dept_no`),
    KEY `idx_dept_no` (`dept_no`),
    CONSTRAINT `fk_dept_emp_employees` FOREIGN KEY (`emp_no`) REFERENCES `Employees` (`emp_no`),
    CONSTRAINT `fk_dept_emp_departments` FOREIGN KEY (`dept_no`) REFERENCES `Departments` (`dept_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工部门关联表';

-- ====================================
-- 14. Titles 职位表
-- ====================================
DROP TABLE IF EXISTS `Titles`;
CREATE TABLE `Titles` (
    `emp_no` INT NOT NULL COMMENT '员工编号',
    `title` VARCHAR(255) NOT NULL COMMENT '职位',
    `from_date` DATE NOT NULL COMMENT '起始日期',
    `to_date` DATE DEFAULT NULL COMMENT '结束日期',
    PRIMARY KEY (`emp_no`, `title`, `from_date`),
    CONSTRAINT `fk_titles_employees` FOREIGN KEY (`emp_no`) REFERENCES `Employees` (`emp_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='职位表';

-- ====================================
-- 简化版表（用于部分基础题目）
-- ====================================

-- 简化版客户表
DROP TABLE IF EXISTS `Customers_Simple`;
CREATE TABLE `Customers_Simple` (
    `cust_id` VARCHAR(255) DEFAULT NULL COMMENT '客户ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='简化版客户表';

-- 简化版订单项表
DROP TABLE IF EXISTS `OrderItems_Simple`;
CREATE TABLE `OrderItems_Simple` (
    `prod_id` VARCHAR(255) NOT NULL COMMENT '商品ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='简化版订单项表';
