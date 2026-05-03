---
title: 'SQL 必知必会：基础知识与 50 题实战'
description: 'SQL 核心知识点速查 + 牛客网 SQL 必知必会 50 道题完整题解，覆盖检索、过滤、聚合、子查询、联结、组合查询等考点。'
pubDate: '2026-05-04'
category: '数据库'
tags: ['SQL', 'MySQL', '牛客网', '聚合函数', 'JOIN', '子查询', 'GROUP BY']
---

## 配套资料

本文所有题目基于牛客网 [SQL 必知必会](https://www.nowcoder.com/exam/oj/ta?tpId=298) 题库，本地练习用的建表脚本和数据如下：

| 文件 | 说明 |
|------|------|
| `02_create_database.sql` | 建表脚本，含 5 张核心表 + 9 张扩展表 |
| `03_insert_data.sql` | 初始测试数据 |

**5 张核心表结构：**

- **Customers**（客户表）：cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email
- **Vendors**（供应商表）：vend_id, vend_name, vend_address, vend_city, vend_state, vend_zip, vend_country
- **Products**（产品表）：prod_id, vend_id, prod_name, prod_price, prod_desc
- **Orders**（订单表）：order_num, order_date, cust_id
- **OrderItems**（订单项表）：order_num, order_item, prod_id, quantity, item_price

**快速导入：**

```bash
mysql -u root -p < 02_create_database.sql
mysql -u root -p < 03_insert_data.sql
```

---

# 第一部分：SQL 基础知识

## 一、SQL 语句执行顺序

书写顺序和执行顺序不一样，理解执行顺序是写复杂查询的前提。

### 1.1 书写顺序

```sql
SELECT DISTINCT select_list
FROM left_table [JOIN right_table ON join_condition]
WHERE where_condition
GROUP BY group_by_list
HAVING having_condition
ORDER BY order_by_condition
LIMIT limit_number;
```

### 1.2 实际执行顺序

```
FROM → ON → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

**关键理解：** SELECT 在 WHERE 之后执行，所以 WHERE 里不能用 SELECT 定义的别名。同理 HAVING 可以用聚合结果过滤，WHERE 不行。

## 二、SQL 分类

| 分类 | 全称 | 用途 | 代表语句 |
|------|------|------|----------|
| DDL | Data Definition Language | 定义结构 | CREATE, DROP, ALTER |
| DML | Data Manipulation Language | 操作数据 | INSERT, UPDATE, DELETE |
| DQL | Data Query Language | 查询数据 | SELECT |
| DCL | Data Control Language | 控制权限 | GRANT, REVOKE |

## 三、常用函数速查

### 3.1 字符串函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `CONCAT(str1, str2)` | 拼接字符串 | `CONCAT('a', 'b')` → `'ab'` |
| `UPPER(str)` | 转大写 | `UPPER('abc')` → `'ABC'` |
| `LOWER(str)` | 转小写 | `LOWER('ABC')` → `'abc'` |
| `TRIM(str)` | 去首尾空格 | `TRIM(' hi ')` → `'hi'` |
| `SUBSTRING(str, pos, len)` | 截取子串 | `SUBSTRING('hello', 1, 3)` → `'hel'` |
| `LENGTH(str)` | 字符串长度 | `LENGTH('hi')` → `2` |
| `LEFT(str, n)` | 取左边 n 个字符 | `LEFT('hello', 2)` → `'he'` |
| `LPAD(str, len, pad)` | 左填充 | `LPAD('5', 3, '0')` → `'005'` |
| `REPLACE(str, old, new)` | 替换 | `REPLACE('abc', 'b', 'x')` → `'axc'` |

### 3.2 数值函数

| 函数 | 作用 |
|------|------|
| `ROUND(num, d)` | 四舍五入到 d 位小数 |
| `CEIL(num)` | 向上取整 |
| `FLOOR(num)` | 向下取整 |
| `ABS(num)` | 绝对值 |
| `MOD(n, m)` | 取余 |

### 3.3 日期函数

| 函数 | 作用 |
|------|------|
| `CURDATE()` | 当前日期 |
| `NOW()` | 当前日期时间 |
| `YEAR(date)` / `MONTH(date)` / `DAY(date)` | 提取年月日 |
| `DATE_FORMAT(date, fmt)` | 格式化日期 |
| `DATE_ADD(date, INTERVAL expr type)` | 日期加 |
| `DATEDIFF(d1, d2)` | 日期差（天） |

### 3.4 聚合函数

| 函数 | 作用 | 注意 |
|------|------|------|
| `COUNT(*)` | 总行数 | 包含 NULL |
| `COUNT(col)` | 非空行数 | 忽略 NULL |
| `COUNT(DISTINCT col)` | 去重计数 | — |
| `SUM(col)` | 求和 | 忽略 NULL |
| `AVG(col)` | 平均值 | 忽略 NULL |
| `MAX(col)` | 最大值 | — |
| `MIN(col)` | 最小值 | — |

## 四、连接类型

| 类型 | 关键字 | 返回内容 | 核心区别 |
|------|--------|----------|----------|
| 内连接 | `INNER JOIN` | 两表匹配的行 | 不匹配的全丢 |
| 左连接 | `LEFT JOIN` | 左表全部 + 右表匹配 | 右表无匹配填 NULL |
| 右连接 | `RIGHT JOIN` | 右表全部 + 左表匹配 | 左表无匹配填 NULL |
| 交叉连接 | `CROSS JOIN` | 笛卡尔积 | 每行组合 |
| 全连接 | `FULL JOIN` | 两表全部 | MySQL 不支持，用 UNION 模拟 |

**实战选择：** 大多数场景用 INNER JOIN；需要保留"没有匹配也显示"的记录时用 LEFT JOIN；全连接极少用。

## 五、子查询

| 类型 | 返回 | 典型用法 |
|------|------|----------|
| 标量子查询 | 单个值 | `WHERE price > (SELECT AVG(price) FROM t)` |
| 列子查询 | 一列值 | `WHERE id IN (SELECT ...)` |
| 行子查询 | 一行数据 | `WHERE (a, b) = (SELECT ...)` |
| 表子查询 | 一个表 | `FROM (SELECT ...) AS t` |
| 相关子查询 | 引用外部字段 | `WHERE salary > (SELECT AVG(...) FROM t2 WHERE t2.dept = t1.dept)` |

**性能建议：** 能用 JOIN 替代的子查询，JOIN 通常更快；相关子查询每行都要执行一次，数据量大时慎用。

## 六、常用关键字

| 关键字 | 用法 | 注意点 |
|--------|------|--------|
| `DISTINCT` | `SELECT DISTINCT col` | 去重，作用于所有选择列 |
| `LIMIT` | `LIMIT n` 或 `LIMIT offset, n` | MySQL 分页核心 |
| `LIKE` | `'张%'` / `'张_'` | `%` 任意字符，`_` 单字符；`%` 开头不走索引 |
| `IN` | `WHERE id IN (1, 2, 3)` | 多值匹配 |
| `BETWEEN` | `WHERE age BETWEEN 18 AND 25` | **闭区间**，含两端 |
| `IS NULL` | `WHERE email IS NULL` | NULL 只能用 `IS` 判断，不能用 `=` |

## 七、分组与过滤

```sql
SELECT department_id, COUNT(*) AS emp_count, AVG(salary) AS avg_sal
FROM employees
WHERE status = 'active'        -- 先过滤原始行
GROUP BY department_id          -- 再分组
HAVING COUNT(*) > 5            -- 最后过滤分组
ORDER BY avg_sal DESC;
```

**WHERE vs HAVING：** WHERE 过滤原始行（分组前），HAVING 过滤分组后结果。HAVING 能用聚合函数，WHERE 不能。

## 八、UNION

| 关键字 | 去重 | 性能 |
|--------|------|------|
| `UNION` | 是 | 稍慢（需排序去重） |
| `UNION ALL` | 否 | 更快 |

**要求：** 每个 SELECT 的列数和数据类型必须一致。

## 九、窗口函数（MySQL 8.0+）

```sql
SELECT name, dept, salary,
    ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS row_num,
    RANK()       OVER (PARTITION BY dept ORDER BY salary DESC) AS rank_num,
    DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dense_num
FROM employees;
```

| 函数 | 并列处理 | 示例（同薪 2 人） |
|------|----------|-------------------|
| `ROW_NUMBER` | 不并列 | 1, 2, 3 |
| `RANK` | 并列跳号 | 1, 1, 3 |
| `DENSE_RANK` | 并列不跳号 | 1, 1, 2 |

## 十、CASE 表达式

```sql
-- 搜索 CASE（更灵活，推荐）
SELECT name, salary,
    CASE
        WHEN salary >= 20000 THEN '高'
        WHEN salary >= 10000 THEN '中'
        ELSE '低'
    END AS salary_level
FROM employees;
```

## 十一、索引与优化要点

```sql
CREATE INDEX idx_name ON table_name(col);          -- 普通索引
CREATE UNIQUE INDEX idx_name ON table_name(col);   -- 唯一索引
CREATE INDEX idx_name ON table_name(col1, col2);   -- 复合索引
```

**索引失效常见场景：**

1. WHERE 中对列使用函数 → `WHERE YEAR(date) = 2020` 失效，改用范围查询
2. LIKE 以 `%` 开头 → 全表扫描
3. OR 连接不同索引列 → 可能失效
4. 隐式类型转换 → `WHERE varchar_col = 123` 失效

---

# 第二部分：SQL 必知必会 50 题实战

> 题目来源：牛客网 SQL 必知必会（SQL104 - SQL153），按章节分组，每题标注考点。

## 第一章：检索数据（SQL104 - SQL106）

### 1. SQL104 - 检索所有的 ID

**考点：** SELECT 基础查询

从 Customers 表中检索所有的 cust_id。

```sql
SELECT cust_id FROM Customers;
```

**题解：** 最基本的单列查询。实际工作中 `SELECT *` 尽量少用，明确写需要的列更高效、更安全。

---

### 2. SQL105 - 检索已订购产品清单（去重）

**考点：** DISTINCT 去重

检索所有已订购商品（prod_id）的**去重**清单。

```sql
SELECT DISTINCT prod_id FROM OrderItems;
```

**题解：** 同一产品可能出现在多个订单项中，DISTINCT 确保每个产品只出现一次。DISTINCT 作用于所有 SELECT 列的组合。

---

### 3. SQL106 - 检索所有列

**考点：** SELECT * 通配符

检索 Customers 表的所有列。

```sql
SELECT * FROM Customers;
```

**题解：** `*` 代表所有列。生产环境建议明确列名——减少数据传输、避免表结构变更导致的问题、提高可读性。

---

## 第二章：排序检索数据（SQL107 - SQL110）

### 4. SQL107 - 检索顾客名称并排序

**考点：** ORDER BY 单列排序

从 Customers 表中检索 cust_name 并按名称排序。

```sql
SELECT cust_name FROM Customers ORDER BY cust_name;
```

**题解：** ORDER BY 默认升序（ASC）。降序需要显式写 `DESC`。排序可以在 SELECT 中未出现的列上进行。

---

### 5. SQL108 - 对顾客 ID 和日期排序

**考点：** ORDER BY 多列排序

检索 cust_id 和 order_date，先按 cust_id 升序，再按 order_date 降序。

```sql
SELECT cust_id, order_date FROM Orders ORDER BY cust_id, order_date DESC;
```

**题解：** 多列排序时，按书写顺序确定优先级。DESC 只作用于它前面的列——这里 cust_id 仍是升序，order_date 降序。

---

### 6. SQL109 - 按数量和价格排序

**考点：** ORDER BY 多列降序

对 OrderItems 按 quantity 降序、item_price 降序排列。

```sql
SELECT quantity, item_price FROM OrderItems
ORDER BY quantity DESC, item_price DESC;
```

**题解：** 先按数量从多到少排，数量相同时再按价格从高到低排。每个 DESC 独立控制其前面的列。

---

### 7. SQL110 - 检查 SQL 语句

**考点：** SQL 语法检查

纠正语句错误：检索 prod_name 并按 prod_price 排序。

```sql
SELECT prod_name FROM Products ORDER BY prod_price ASC;
```

**题解：** ORDER BY 可以使用不在 SELECT 列表中的列来排序，这是合法的。ASC 可省略（默认值），写上更清晰。

---

## 第三章：过滤数据（SQL111 - SQL114）

### 8. SQL111 - 返回固定价格的产品

**考点：** WHERE 等值过滤

检索 prod_price 等于 3.49 的产品名称。

```sql
SELECT prod_name FROM Products WHERE prod_price = 3.49;
```

**题解：** SQL 相等用 `=`，不是 `==`。数值类型直接写数字，字符串类型需加引号。

---

### 9. SQL112 - 返回更高价格的产品

**考点：** WHERE 比较运算符

检索 prod_price 大于 5 的产品名称。

```sql
SELECT prod_name FROM Products WHERE prod_price > 5;
```

**题解：** 常用比较运算符：`=`、`!=`/`<>`、`>`、`<`、`>=`、`<=`。`<>` 是 SQL 标准写法，`!=` 也可以用。

---

### 10. SQL113 - 返回产品并按价格排序

**考点：** WHERE + ORDER BY 组合

检索 prod_price <= 10 的产品名称，按价格升序排列。

```sql
SELECT prod_name FROM Products WHERE prod_price <= 10 ORDER BY prod_price;
```

**题解：** WHERE 在 ORDER BY 之前执行（回顾执行顺序）。先过滤再排序，逻辑清晰。

---

### 11. SQL114 - 返回更多的产品

**考点：** SELECT 多列 + 排序

检索 prod_id、prod_name、prod_price，按价格升序。

```sql
SELECT prod_id, prod_name, prod_price FROM Products ORDER BY prod_price ASC;
```

**题解：** 选择多列用逗号分隔。ASC 可省略，默认升序。好的习惯：始终明确写出需要的列。

---

## 第四章：高级数据过滤（SQL115 - SQL118）

### 12. SQL115 - 检索供应商名称

**考点：** LIKE 通配符

检索 Vendors 表中 vend_name 以 "vendor" 开头的供应商。

```sql
SELECT vend_name FROM Vendors WHERE vend_name LIKE 'vendor%';
```

**题解：** `%` 匹配任意多个字符（含 0 个）。`'vendor%'` 匹配 "vendor a"、"vendor b" 等。注意 `%` 开头的 LIKE 会导致索引失效。

---

### 13. SQL116 - 检索特定供应商的低价产品

**考点：** AND 多条件过滤

检索 vend_id 为 'DLL01' 且 prod_price <= 4 的产品。

```sql
SELECT prod_id, prod_name FROM Products
WHERE vend_id = 'DLL01' AND prod_price <= 4;
```

**题解：** AND 要求所有条件同时满足。与 OR 的区别：AND 是"并且"，OR 是"或者"。AND 优先级高于 OR，混合使用时建议加括号。

---

### 14. SQL117 - 返回价格在 3 到 6 美元之间的产品

**考点：** BETWEEN 范围查询

检索 prod_price 在 3 到 6 之间（含端点）的产品名称和价格。

```sql
SELECT prod_name, prod_price FROM Products
WHERE prod_price BETWEEN 3 AND 6;
```

**题解：** BETWEEN 是**闭区间**，包含 3 和 6。等价于 `WHERE prod_price >= 3 AND prod_price <= 6`。

---

### 15. SQL118 - 纠错：NULL 值判断

**考点：** IS NULL 判断

纠正 `WHERE prod_price = NULL` 的写法。

```sql
SELECT prod_price FROM Products WHERE prod_price IS NULL;
```

**题解：** NULL 不是值，是"未知"状态。任何与 NULL 的比较（`= NULL`、`!= NULL`）结果都是 UNKNOWN，不会返回任何行。**必须用 `IS NULL` 或 `IS NOT NULL`。**

---

## 第五章：用通配符进行过滤（SQL119 - SQL122）

### 16. SQL119 - 检索产品名称和描述（一）

**考点：** LIKE % 前缀匹配

检索 prod_name 以 "Fish" 开头的产品。

```sql
SELECT prod_id, prod_name FROM Products WHERE prod_name LIKE 'Fish%';
```

**题解：** `'Fish%'` 匹配以 Fish 开头的任意长度字符串。最常用的 LIKE 模式，且能走索引（不以 % 开头）。

---

### 17. SQL120 - 检索产品名称和描述（二）

**考点：** LIKE % 包含匹配

检索 prod_name 包含 "bean bag" 的产品。

```sql
SELECT prod_id, prod_name FROM Products WHERE prod_name LIKE '%bean bag%';
```

**题解：** 前后都加 `%` 表示"包含"关系。注意这种写法无法利用索引，大数据量时考虑全文索引。

---

### 18. SQL121 - 检索产品名称和描述（三）

**考点：** LIKE + NOT LIKE 组合

检索 prod_desc 以 "Fish" 开头的产品。

```sql
SELECT prod_id, prod_name FROM Products WHERE prod_desc LIKE 'Fish%';
```

**题解：** 与 SQL119 类似，只是查询字段不同。如需排除"Fish "（Fish 加空格）的情况，可以加 `AND prod_desc NOT LIKE 'Fish %'`。

---

### 19. SQL122 - 检索产品名称和描述（四）

**考点：** LIKE _ 单字符通配符

检索 prod_name 以 "8" 开头且长度为 8 个字符的产品。

```sql
SELECT prod_id, prod_name FROM Products WHERE prod_name LIKE '8_______';
```

**题解：** `_` 精确匹配单个字符。`'8_______'` 表示以 8 开头 + 恰好 7 个任意字符 = 总长 8。比 `%` 更精确。

---

## 第六章：创建计算字段（SQL123 - SQL124）

### 20. SQL123 - 别名

**考点：** AS 别名

将 prod_name 重命名为 "Product Name"，prod_price 重命名为 "Product Price"。

```sql
SELECT prod_name AS 'Product Name', prod_price AS 'Product Price' FROM Products;
```

**题解：** AS 给列起别名。别名含空格或特殊字符时必须加引号。别名用于：提高可读性、在应用层映射字段名、子查询中引用。

---

### 21. SQL124 - 打折计算

**考点：** 计算字段（算术运算）

计算每种产品购买 100 件的总价，命名为 "Total Price"。

```sql
SELECT prod_id, prod_name, prod_price * 100 AS 'Total Price' FROM Products;
```

**题解：** SELECT 中可以使用 `+`、`-`、`*`、`/` 算术运算。计算结果可以用 AS 命名，否则列名为表达式本身，不利于阅读。

---

## 第七章：使用函数处理数据（SQL125 - SQL126）

### 22. SQL125 - 顾客登录名

**考点：** 字符串函数组合（LOWER + CONCAT + LEFT）

创建登录名：取 cust_name 的首字符 + 整个名字，转为小写。

```sql
SELECT LOWER(cust_name) AS cust_name,
       CONCAT(LEFT(cust_name, 1), SUBSTRING(cust_name, 2)) AS login_name
FROM Customers;
```

**题解：** 函数可以嵌套使用。`LEFT(str, 1)` 取首字符，`SUBSTRING(str, 2)` 取第二个字符起的所有字符，`CONCAT` 拼接，`LOWER` 转小写。实际应用中还需处理空格和特殊字符。

---

### 23. SQL126 - 返回 2020 年 1 月的所有订单

**考点：** 日期函数 / 日期范围查询

检索 2020 年 1 月的订单号和日期。

**写法一：BETWEEN（推荐，能走索引）**

```sql
SELECT order_num, order_date FROM Orders
WHERE order_date BETWEEN '2020-01-01' AND '2020-01-31';
```

**写法二：YEAR + MONTH（更直观，但索引失效）**

```sql
SELECT order_num, order_date FROM Orders
WHERE YEAR(order_date) = 2020 AND MONTH(order_date) = 1;
```

**题解：** 写法一用范围查询，不破坏索引；写法二对列使用函数，索引失效。**生产环境优先写法一。**

---

## 第八章：汇总数据（SQL127 - SQL129）

### 24. SQL127 - 确定已售出产品的总数

**考点：** SUM 聚合函数

统计 OrderItems 表中所有商品的数量总和。

```sql
SELECT SUM(quantity) AS items_ordered FROM OrderItems;
```

**题解：** `SUM(column)` 对数值列求和，自动忽略 NULL。聚合函数对整个表计算，返回单个值（标量结果）。

---

### 25. SQL128 - 确定产品 BR01 的总销量

**考点：** SUM + WHERE

统计 prod_id 为 'BR01' 的产品的总销售数量。

```sql
SELECT SUM(quantity) AS items_ordered FROM OrderItems WHERE prod_id = 'BR01';
```

**题解：** 先 WHERE 过滤，再 SUM 聚合。执行顺序：FROM → WHERE → SELECT → SUM。WHERE 缩小了聚合的范围。

---

### 26. SQL129 - 不超过 10 美元的最贵产品

**考点：** MAX + WHERE

从 Products 表中找出价格不超过 10 的最贵产品价格。

```sql
SELECT MAX(prod_price) AS max_price FROM Products WHERE prod_price <= 10;
```

**题解：** WHERE 先过滤出 <= 10 的产品，MAX 再从中找最大值。如果没有任何满足条件的记录，MAX 返回 NULL。

---

## 第九章：分组数据（SQL130 - SQL134）

### 27. SQL130 - 每个订单号各有多少行

**考点：** GROUP BY + COUNT

按 order_num 分组，统计每个订单有多少行项目。

```sql
SELECT order_num, COUNT(*) AS line_items FROM OrderItems GROUP BY order_num;
```

**题解：** GROUP BY 将数据按列值分组，每组返回一行聚合结果。`COUNT(*)` 计算每组行数。**SELECT 中的非聚合列必须出现在 GROUP BY 中。**

---

### 28. SQL131 - 每个供应商成本最低的产品

**考点：** MIN + GROUP BY

按 vend_id 分组，找出每个供应商的最低产品价格。

```sql
SELECT vend_id, MIN(prod_price) AS cheapest_item FROM Products GROUP BY vend_id;
```

**题解：** MIN 找每组的最小值。注意这里只返回最低价格，不返回对应的产品名称。如果要同时获取产品名，需要用子查询或窗口函数。

---

### 29. SQL132 - 确定最佳顾客

**考点：** 多表 JOIN + GROUP BY + ORDER BY + LIMIT

计算每个顾客的总消费金额，找出消费最高的。

```sql
SELECT o.cust_id, SUM(oi.quantity * oi.item_price) AS total_spent
FROM Orders o
INNER JOIN OrderItems oi ON o.order_num = oi.order_num
GROUP BY o.cust_id
ORDER BY total_spent DESC
LIMIT 1;
```

**题解：** 三步走：① JOIN 关联订单与订单项；② GROUP BY 按顾客分组，SUM 计算总消费；③ ORDER BY + LIMIT 取最高。如果有并列第一，LIMIT 1 只取一个。

---

### 30. SQL133 - 确定最佳顾客的另一种方式

**考点：** 相关子查询

用子查询方式实现 SQL132。

```sql
SELECT o.cust_id,
       (SELECT SUM(oi.quantity * oi.item_price)
        FROM OrderItems oi WHERE oi.order_num = o.order_num) AS total_spent
FROM Orders o
GROUP BY o.cust_id
ORDER BY total_spent DESC
LIMIT 1;
```

**题解：** 相关子查询对每个外部行都执行一次内部查询。逻辑等价但性能通常不如 JOIN 方式，数据量大时慎用。

---

### 31. SQL134 - 纠错：缺少 GROUP BY

**考点：** GROUP BY 语法规则

纠正缺少 GROUP BY 的语句。

```sql
-- 错误：SELECT 中有非聚合列 vend_id 但没有 GROUP BY
SELECT vend_id, COUNT(*) AS prod_count FROM Products;

-- 正确：
SELECT vend_id, COUNT(*) AS prod_count FROM Products GROUP BY vend_id;
```

**题解：** **核心规则：SELECT 中出现非聚合列，就必须在 GROUP BY 中声明。** 否则数据库不知道按什么分组，会报错。这是 SQL 面试高频考点。

---

## 第十章：使用子查询（SQL135 - SQL139）

### 32. SQL135 - 返回购买价格 >= 10 美元产品的顾客

**考点：** IN 子查询 + 多表关联

找出购买过价格 >= 10 美元产品的顾客。

```sql
SELECT cust_id, cust_name FROM Customers
WHERE cust_id IN (
    SELECT DISTINCT o.cust_id
    FROM Orders o
    INNER JOIN OrderItems oi ON o.order_num = oi.order_num
    INNER JOIN Products p ON oi.prod_id = p.prod_id
    WHERE p.prod_price >= 10
);
```

**题解：** 子查询思路：从内到外——先找出"谁买了贵东西"（三表 JOIN + WHERE），再用 IN 过滤顾客表。DISTINCT 去重，IN 处理多个匹配值。

---

### 33. SQL136 - 确定哪些订单购买了 BR01

**考点：** 单表 WHERE 子查询

找出包含产品 'BR01' 的订单号。

```sql
SELECT order_num, order_item, prod_id, quantity
FROM OrderItems WHERE prod_id = 'BR01';
```

**题解：** 最简单的单表过滤。如果只需要订单号（去重）：`SELECT DISTINCT order_num FROM OrderItems WHERE prod_id = 'BR01'`。

---

### 34. SQL137 - 返回购买 BR01 的顾客邮箱

**考点：** 嵌套子查询（多层 IN）

找出购买过 BR01 产品的顾客邮箱。

```sql
SELECT cust_email FROM Customers
WHERE cust_id IN (
    SELECT cust_id FROM Orders
    WHERE order_num IN (
        SELECT order_num FROM OrderItems WHERE prod_id = 'BR01'
    )
);
```

**题解：** 三层嵌套：最内层找"买了 BR01 的订单号"→ 中间层找"这些订单对应的顾客"→ 最外层找"这些顾客的邮箱"。逻辑清晰但层数多了可读性差，建议超过两层就改用 JOIN。

---

### 35. SQL138 - 返回每个顾客不同订单的总金额

**考点：** 多表 JOIN + GROUP BY 多列

计算每个顾客每个订单的总金额。

```sql
SELECT o.cust_id, o.order_num, SUM(oi.quantity * oi.item_price) AS order_total
FROM Orders o
INNER JOIN OrderItems oi ON o.order_num = oi.order_num
GROUP BY o.cust_id, o.order_num;
```

**题解：** GROUP BY 多列——按 cust_id 和 order_num 双维度分组。每个分组对应一个顾客的一个订单，SUM 计算该订单总金额。

---

### 36. SQL139 - 检索所有产品名称及对应销售总数

**考点：** LEFT JOIN + COALESCE

统计每种产品的总销售数量，没有销量的产品显示 0。

```sql
SELECT p.prod_name, COALESCE(SUM(oi.quantity), 0) AS sold_total
FROM Products p
LEFT JOIN OrderItems oi ON p.prod_id = oi.prod_id
GROUP BY p.prod_id, p.prod_name;
```

**题解：** LEFT JOIN 保证没有销量的产品也出现。COALESCE 将 NULL 转为 0——因为没匹配到订单项时 SUM 返回 NULL，显示 0 更直观。

---

## 第十一章：联结表（SQL140 - SQL144）

### 37. SQL140 - 返回顾客名称和相关订单号

**考点：** INNER JOIN

关联顾客和订单，返回顾客名称及对应订单号。

```sql
SELECT c.cust_name, o.order_num
FROM Customers c
INNER JOIN Orders o ON c.cust_id = o.cust_id
ORDER BY c.cust_name, o.order_num;
```

**题解：** INNER JOIN 只返回两表都有匹配的行。没有订单的顾客不会出现。表别名（c, o）让 SQL 更简洁。

---

### 38. SQL141 - 返回顾客名称、订单号及每个订单总价

**考点：** 三表 JOIN + GROUP BY

```sql
SELECT c.cust_name, o.order_num, SUM(oi.quantity * oi.item_price) AS order_total
FROM Customers c
INNER JOIN Orders o ON c.cust_id = o.cust_id
INNER JOIN OrderItems oi ON o.order_num = oi.order_num
GROUP BY c.cust_name, o.order_num
ORDER BY c.cust_name, o.order_num;
```

**题解：** 三表关联：Customers → Orders → OrderItems。按顾客+订单分组，SUM 算订单总价。多表 JOIN 时注意关联条件的准确性。

---

### 39. SQL142 - 用联结找购买 BR01 的订单号

**考点：** JOIN + WHERE（与子查询对比）

```sql
SELECT DISTINCT o.order_num
FROM Orders o
INNER JOIN OrderItems oi ON o.order_num = oi.order_num
WHERE oi.prod_id = 'BR01';
```

**题解：** 与 SQL136 的子查询方式对比，JOIN 方式通常更高效。DISTINCT 去重，因为一个订单可能有多个 BR01 的订单项。

---

### 40. SQL143 - 用联结找购买 BR01 的顾客邮箱

**考点：** 多表 JOIN + DISTINCT

```sql
SELECT DISTINCT c.cust_email
FROM Customers c
INNER JOIN Orders o ON c.cust_id = o.cust_id
INNER JOIN OrderItems oi ON o.order_num = oi.order_num
WHERE oi.prod_id = 'BR01';
```

**题解：** 与 SQL137 的嵌套子查询对比，JOIN 方式更简洁。DISTINCT 确保邮箱不重复。同一顾客可能多次购买 BR01，不 DISTINCT 会出多行。

---

### 41. SQL144 - 用联结确定最佳顾客

**考点：** JOIN + GROUP BY + ORDER BY + LIMIT

```sql
SELECT o.cust_id, SUM(oi.quantity * oi.item_price) AS total_spent
FROM Orders o
INNER JOIN OrderItems oi ON o.order_num = oi.order_num
GROUP BY o.cust_id
ORDER BY total_spent DESC
LIMIT 1;
```

**题解：** 与 SQL132 完全相同，只是强调用 JOIN 实现。结论：**同一需求，JOIN 通常比子查询更直观、更高效。**

---

## 第十二章：创建高级联结（SQL145 - SQL149）

### 42. SQL145 - 检索每个顾客的名称和所有订单号（含无订单）

**考点：** LEFT JOIN

```sql
SELECT c.cust_name, o.order_num
FROM Customers c
LEFT JOIN Orders o ON c.cust_id = o.cust_id
ORDER BY c.cust_name, o.order_num;
```

**题解：** LEFT JOIN 保留左表（Customers）全部记录。没有订单的顾客也会出现，order_num 显示 NULL。**INNER JOIN 做不到这一点。**

---

### 43. SQL146 - 检索每个顾客的名称和订单号（仅有效订单）

**考点：** INNER JOIN vs LEFT JOIN 对比

```sql
SELECT c.cust_name, o.order_num
FROM Customers c
INNER JOIN Orders o ON c.cust_id = o.cust_id
ORDER BY c.cust_name, o.order_num;
```

**题解：** 与 SQL145 对比：INNER JOIN 只返回有订单的顾客，LEFT JOIN 返回所有顾客。选择哪个取决于业务需求——是否要看到"没有订单的顾客"。

---

### 44. SQL147 - 返回产品名称和与之相关的订单号

**考点：** LEFT JOIN 产品与订单

```sql
SELECT p.prod_name, oi.order_num
FROM Products p
LEFT JOIN OrderItems oi ON p.prod_id = oi.prod_id
ORDER BY p.prod_name, oi.order_num;
```

**题解：** LEFT JOIN 确保所有产品都显示，未被购买的产品 order_num 为 NULL。这种"保留全部 + 显示关联"的模式非常常见。

---

### 45. SQL148 - 返回产品名称和每一项产品的总订单数

**考点：** LEFT JOIN + COUNT 分组

```sql
SELECT p.prod_name, COUNT(oi.order_num) AS order_count
FROM Products p
LEFT JOIN OrderItems oi ON p.prod_id = oi.prod_id
GROUP BY p.prod_id, p.prod_name
ORDER BY p.prod_name;
```

**题解：** `COUNT(oi.order_num)` 忽略 NULL（未被购买的产品计数为 0），而 `COUNT(*)` 会把 NULL 行也算为 1。**LEFT JOIN 下计数要用 COUNT(右表列)，不要用 COUNT(*)。**

---

### 46. SQL149 - 列出供应商及其可供产品的数量

**考点：** LEFT JOIN + COUNT 分组

```sql
SELECT v.vend_id, v.vend_name, COUNT(p.prod_id) AS prod_count
FROM Vendors v
LEFT JOIN Products p ON v.vend_id = p.vend_id
GROUP BY v.vend_id, v.vend_name
ORDER BY v.vend_name;
```

**题解：** 同 SQL148 模式：LEFT JOIN 保留所有供应商，COUNT(右表列) 正确计数（没产品的供应商为 0）。ORDER BY 名称排序更直观。

---

## 第十三章：组合查询（SQL150 - SQL153）

### 47. SQL150 - 将两个 SELECT 结合（不去重）

**考点：** UNION ALL

```sql
SELECT prod_id, prod_price FROM Products WHERE prod_price <= 5
UNION ALL
SELECT prod_id, prod_price FROM Products WHERE prod_price <= 10;
```

**题解：** UNION ALL 合并结果不去重。<= 5 的产品会重复出现（在两个查询中都满足）。适用于需要保留重复记录的场景。

---

### 48. SQL151 - 将两个 SELECT 结合（去重）

**考点：** UNION

```sql
SELECT prod_id, prod_price FROM Products WHERE prod_price <= 5
UNION
SELECT prod_id, prod_price FROM Products WHERE prod_price <= 10;
```

**题解：** UNION 自动去重，等价于 UNION ALL + DISTINCT。性能稍差（需排序去重）。能用 WHERE 单条查询解决的，不需要 UNION。

---

### 49. SQL152 - 组合产品名称和顾客名称

**考点：** UNION 跨表合并

```sql
SELECT prod_name AS name FROM Products
UNION
SELECT cust_name AS name FROM Customers
ORDER BY name;
```

**题解：** UNION 要求各 SELECT 列数和数据类型一致。这里合并两个表的名称列，用 AS 统一别名。ORDER BY 作用于整个 UNION 结果。

---

### 50. SQL153 - 纠错：UNION 列名不一致

**考点：** UNION 语法规范

确保 UNION 的各 SELECT 列名一致。

```sql
SELECT prod_name AS name FROM Products
UNION
SELECT cust_name AS name FROM Customers
ORDER BY name;
```

**题解：** UNION 规则：① 列数相同；② 数据类型兼容；③ 结果列名取第一个 SELECT 的列名。用 AS 统一别名是好习惯。

---

## 附录：50 题考点速查表

| 章节 | 题号 | 考点 |
|------|------|------|
| 一 | SQL104 | SELECT 单列查询 |
| 一 | SQL105 | DISTINCT 去重 |
| 一 | SQL106 | SELECT * 全列查询 |
| 二 | SQL107 | ORDER BY 单列排序 |
| 二 | SQL108 | ORDER BY 多列排序 |
| 二 | SQL109 | ORDER BY 多列降序 |
| 二 | SQL110 | SQL 语法检查 |
| 三 | SQL111 | WHERE 等值过滤 |
| 三 | SQL112 | WHERE 比较运算符 |
| 三 | SQL113 | WHERE + ORDER BY 组合 |
| 三 | SQL114 | SELECT 多列 + 排序 |
| 四 | SQL115 | LIKE % 通配符 |
| 四 | SQL116 | AND 多条件过滤 |
| 四 | SQL117 | BETWEEN 范围查询（闭区间） |
| 四 | SQL118 | IS NULL 判断（不能用 = NULL） |
| 五 | SQL119 | LIKE % 前缀匹配 |
| 五 | SQL120 | LIKE % 包含匹配 |
| 五 | SQL121 | LIKE + NOT LIKE 组合 |
| 五 | SQL122 | LIKE _ 单字符匹配 |
| 六 | SQL123 | AS 别名 |
| 六 | SQL124 | 计算字段（算术运算） |
| 七 | SQL125 | 字符串函数组合 |
| 七 | SQL126 | 日期函数 / 日期范围查询 |
| 八 | SQL127 | SUM 聚合函数 |
| 八 | SQL128 | SUM + WHERE 组合 |
| 八 | SQL129 | MAX + WHERE 组合 |
| 九 | SQL130 | GROUP BY + COUNT |
| 九 | SQL131 | MIN + GROUP BY |
| 九 | SQL132 | 多表 JOIN + GROUP BY + ORDER BY + LIMIT |
| 九 | SQL133 | 相关子查询实现分组统计 |
| 九 | SQL134 | GROUP BY 语法规则（必考） |
| 十 | SQL135 | IN 子查询 + 多表关联 |
| 十 | SQL136 | 单表 WHERE 子查询 |
| 十 | SQL137 | 嵌套子查询（多层 IN） |
| 十 | SQL138 | 多表 JOIN + GROUP BY 多列 |
| 十 | SQL139 | LEFT JOIN + COALESCE |
| 十一 | SQL140 | INNER JOIN 基础 |
| 十一 | SQL141 | 三表 JOIN + GROUP BY |
| 十一 | SQL142 | JOIN + WHERE（对比子查询） |
| 十一 | SQL143 | 多表 JOIN + DISTINCT |
| 十一 | SQL144 | JOIN + GROUP BY + ORDER BY + LIMIT |
| 十二 | SQL145 | LEFT JOIN（含无匹配记录） |
| 十二 | SQL146 | INNER JOIN vs LEFT JOIN 对比 |
| 十二 | SQL147 | LEFT JOIN 产品与订单 |
| 十二 | SQL148 | LEFT JOIN + COUNT 分组 |
| 十二 | SQL149 | LEFT JOIN + COUNT 分组（供应商维度） |
| 十三 | SQL150 | UNION ALL（不去重） |
| 十三 | SQL151 | UNION（去重） |
| 十三 | SQL152 | UNION 跨表合并 |
| 十三 | SQL153 | UNION 语法规范 |
