---
title: 'Java 设计模式实践笔记'
description: '从实际开发场景出发，梳理单例、工厂、模板方法、责任链、策略五种常用设计模式的核心要点与代码实践。'
pubDate: '2026-05-03'
category: '技术栈'
tags: ['Java', '设计模式', '单例模式', '工厂模式', '模板方法', '责任链', '策略模式']
---

## 前言

设计模式学了好几遍，每次看的时候都懂，写代码的时候还是想不起来用。后来发现问题是学的方式不对——背定义没用，得把模式和自己写过的代码对应起来。

这篇文章是我整理的五种最常用模式的实践笔记，每个模式都从"什么时候需要它"开始，再给代码，最后总结要点。核心目标：**下次写代码的时候能想起来用。**

---

## 一、单例模式

**什么时候需要？** 系统里某个对象只需要一份就够了，多了反而出问题。比如配置管理器、数据库连接池、日志对象。

### 1.1 四种实现方式

#### 饿汉式 —— 简单粗暴，类加载就创建

```java
public class ConfigurationManager {
    private static final ConfigurationManager INSTANCE = new ConfigurationManager();
    private Properties config = new Properties();

    private ConfigurationManager() { loadConfig(); }

    public static ConfigurationManager getInstance() { return INSTANCE; }

    public String getConfig(String key) { return config.getProperty(key); }
}
```

线程安全（JVM 类加载保证），但不管用不用都会创建。

#### 懒汉式 + DCL —— 延迟加载，经典写法

```java
public class DatabaseConnectionPool {
    private static volatile DatabaseConnectionPool instance;

    private DatabaseConnectionPool() {}

    public static DatabaseConnectionPool getInstance() {
        if (instance == null) {                          // 第一次检查
            synchronized (DatabaseConnectionPool.class) {
                if (instance == null) {                  // 第二次检查
                    instance = new DatabaseConnectionPool();
                }
            }
        }
        return instance;
    }
}
```

两个要点：
- **两次检查**：防止多个线程同时通过第一次检查后重复创建
- **volatile**：防止 `new` 操作的指令重排序导致其他线程拿到未初始化完成的对象

指令重排序的问题：`instance = new X()` 在 JVM 中分为三步（分配内存 → 初始化对象 → 指向引用），步骤 2 和 3 可能被调换，导致引用已赋值但对象未初始化。

#### 静态内部类 —— 推荐，简洁安全

```java
public class CacheManager {
    private CacheManager() {}

    private static class Holder {
        private static final CacheManager INSTANCE = new CacheManager();
    }

    public static CacheManager getInstance() { return Holder.INSTANCE; }
}
```

懒加载（调用 `getInstance()` 时才加载内部类）、线程安全（JVM 保证）、零锁开销。

#### 枚举 —— 最安全

```java
public enum LoggerManager {
    INSTANCE;
    public void log(String message) { System.out.println("[LOG] " + message); }
}

LoggerManager.INSTANCE.log("系统启动");
```

天然防止反射攻击和反序列化破坏。

### 1.2 Spring 中的单例

Spring Bean 默认就是单例，`@Service`、`@Component` 标注的类整个容器只有一个实例。

这也意味着 **Controller 里不能用成员变量存请求数据**——所有请求共享同一个 Controller 实例，成员变量是共享的。

### 1.3 小结

| 实现方式 | 懒加载 | 线程安全 | 难度 | 推荐场景 |
|---------|--------|---------|------|---------|
| 饿汉式 | 否 | 天然安全 | 低 | 对象轻量、肯定会被用到 |
| DCL | 是 | volatile 保证 | 中 | 需要延迟加载的大对象 |
| 静态内部类 | 是 | 天然安全 | 低 | **日常首选** |
| 枚举 | 否 | 天然安全 | 低 | 需要序列化安全 / 代码极简 |

---

## 二、工厂模式

**什么时候需要？** 创建对象的逻辑散落在各处，或者创建过程比较复杂，需要把"创建"和"使用"分离。

### 2.1 简单工厂

一个工厂搞定所有产品，适合产品种类少且稳定的场景。

```java
public interface PaymentMethod {
    void pay(double amount);
}

public class AlipayPayment implements PaymentMethod {
    @Override
    public void pay(double amount) { System.out.println("支付宝: ￥" + amount); }
}

public class WechatPayment implements PaymentMethod {
    @Override
    public void pay(double amount) { System.out.println("微信: ￥" + amount); }
}

public class PaymentFactory {
    public static PaymentMethod create(String type) {
        return switch (type) {
            case "alipay" -> new AlipayPayment();
            case "wechat" -> new WechatPayment();
            default -> throw new IllegalArgumentException("不支持的支付方式: " + type);
        };
    }
}
```

调用方只和接口打交道，不关心具体实现：

```java
PaymentMethod payment = PaymentFactory.create("alipay");
payment.pay(100.00);
```

**问题**：新增支付方式要改工厂代码，违反开闭原则。

### 2.2 工厂方法

每个产品配一个工厂，新增产品不需要改已有代码。

```java
public interface PaymentFactory {
    PaymentMethod create();
}

public class AlipayFactory implements PaymentFactory {
    @Override public PaymentMethod create() { return new AlipayPayment(); }
}

public class WechatFactory implements PaymentFactory {
    @Override public PaymentMethod create() { return new WechatPayment(); }
}
```

要加京东支付，只需要新建 `JdFactory`，不动其他类。

### 2.3 抽象工厂

创建一整套配套产品（产品族），比如 MySQL 需要 Connection + Command + DataReader 三件套，PostgreSQL 也需要一套。

```java
public interface DatabaseFactory {
    Connection createConnection();
    Command createCommand();
    DataReader createDataReader();
}

// MySQL 一整套
public class MySqlFactory implements DatabaseFactory { /* ... */ }
// PostgreSQL 一整套
public class PostgresFactory implements DatabaseFactory { /* ... */ }
```

切换数据库只改一个工厂对象：

```java
DatabaseFactory factory = new PostgresFactory(); // 就改这一行
Application app = new Application(factory);
app.run();
```

### 2.4 小结

| 工厂类型 | 特点 | 适用场景 |
|---------|------|---------|
| 简单工厂 | 一个工厂包揽，新增产品要改工厂 | 产品少且稳定 |
| 工厂方法 | 一个产品一个工厂，新增产品加个工厂类 | 产品频繁扩展 |
| 抽象工厂 | 创建配套产品族，切换族只换一个工厂 | 多套配套组件需要整体切换 |

---

## 三、模板方法模式

**什么时候需要？** 多个处理流程的步骤一样，只是每步的具体实现不同。把公共骨架提到父类，子类只实现差异部分。

### 3.1 经典场景：数据导入导出

不管 CSV 还是 Excel，流程都是：读取 → 验证 → 转换 → 写入 → 清理。区别只在"怎么读""怎么转""怎么写"。

```java
public abstract class DataProcessor {

    // final 修饰，子类不能改流程
    public final void process(String source, String target) {
        List<Map<String, Object>> data = readData(source);

        if (shouldValidate()) {    // 钩子：要不要验证
            validateData(data);
        }

        List<Map<String, Object>> transformed = transformData(data);
        writeData(transformed, target);

        if (shouldCleanup()) {     // 钩子：要不要清理
            cleanup();
        }
    }

    // 子类必须实现
    protected abstract List<Map<String, Object>> readData(String source);
    protected abstract List<Map<String, Object>> transformData(List<Map<String, Object>> data);
    protected abstract void writeData(List<Map<String, Object>> data, String target);

    // 钩子方法：子类选择性覆盖
    protected boolean shouldValidate() { return true; }
    protected boolean shouldCleanup() { return false; }
    protected void validateData(List<Map<String, Object>> data) { /* 默认实现 */ }
    protected void cleanup() { /* 默认实现 */ }
}
```

子类只需要实现三个抽象方法，钩子方法按需覆盖：

```java
public class CsvDataProcessor extends DataProcessor {
    @Override protected List<Map<String, Object>> readData(String source) { /* 读 CSV */ }
    @Override protected List<Map<String, Object>> transformData(List<Map<String, Object>> data) { /* 转 CSV */ }
    @Override protected void writeData(List<Map<String, Object>> data, String target) { /* 写 CSV */ }
}

public class ExcelDataProcessor extends DataProcessor {
    // 三个抽象方法同上
    @Override protected boolean shouldCleanup() { return true; }  // Excel 需要清临时文件
    @Override protected void cleanup() { /* 清理 Excel 临时文件 */ }
}
```

### 3.2 三个关键机制

- **final 模板方法**：定义流程骨架，子类不能改顺序
- **abstract 方法**：子类必须实现的步骤
- **钩子方法**：提供默认行为，子类按需覆盖（`shouldValidate()` 控制要不要执行，`validateData()` 控制怎么执行）

### 3.3 模板方法 vs 策略模式

| 维度 | 模板方法 | 策略模式 |
|------|---------|---------|
| 变的是什么 | 步骤的细节 | 整个算法 |
| 实现方式 | 继承 | 组合 |
| 类比 | 汉堡流水线（步骤固定，配料不同） | 导航选路线（整体策略可切换） |

### 3.4 小结

模板方法的精髓在于**控制反转**——不是子类调父类，而是父类调子类（Hollywood Principle）。流程由父类掌控，子类只负责填充细节。开闭原则在这里体现为：新增一种处理方式只需加子类，不修改父类。

---

## 四、责任链模式

**什么时候需要？** 请求需要经过多个处理环节，每个环节决定是自己处理还是往下传。

### 4.1 经典场景：审批流程

请假审批：组长批 → 经理批 → 总监批，金额小的组长直接批了，大的要往上递。

```java
public abstract class ApprovalHandler {
    protected ApprovalHandler next;

    public ApprovalHandler setNext(ApprovalHandler next) {
        this.next = next;
        return next;  // 返回 next，支持链式调用
    }

    public abstract boolean handle(Order order);
}

public class AmountHandler extends ApprovalHandler {
    private double limit;
    private String name;

    public AmountHandler(double limit, String name) {
        this.limit = limit;
        this.name = name;
    }

    @Override
    public boolean handle(Order order) {
        if (order.getAmount() <= limit) {
            System.out.println(name + " 审批通过 (￥" + order.getAmount() + ")");
            return true;
        }
        if (next != null) {
            System.out.println(name + " 超出权限，转上级");
            return next.handle(order);
        }
        System.out.println("无人能审批");
        return false;
    }
}
```

构建和使用：

```java
ApprovalHandler chain = new AmountHandler(1000, "组长");
chain.setNext(new AmountHandler(5000, "经理"))
     .setNext(new AmountHandler(50000, "总监"));

chain.handle(new Order(500, "文具"));    // 组长直接批
chain.handle(new Order(80000, "服务器")); // 一直递到总监
```

### 4.2 两种传播模式

| 模式 | 行为 | 典型场景 |
|------|------|---------|
| 找到能处理的就停 | 某个环节处理后不再传递 | 审批流、异常处理 |
| 每个环节都处理 | 所有环节依次执行 | 日志链、过滤器链 |

日志处理链就是第二种模式：同一条日志，控制台打印、写文件、发邮件——每个环节都要处理。

### 4.3 实际开发中的责任链

日常开发里其实经常遇到：
- **Servlet Filter**：请求经过 `AuthenticationFilter → LoggingFilter → EncodingFilter → Servlet`
- **Spring Security FilterChain**：每个过滤器检查一项安全规则
- **Spring Interceptor**：`preHandle → Controller → postHandle → afterCompletion`

### 4.4 小结

责任链的核心价值是**解耦**——发送者不需要知道请求会被谁处理，每个处理器也不需要知道整条链长什么样。新增或删除一个处理器，只需要调整链的组装方式，不影响其他处理器的逻辑。

---

## 五、策略模式

**什么时候需要？** 同一功能有多种实现方式，需要在运行时动态切换。

### 5.1 经典场景：多种支付方式

```java
public interface PaymentStrategy {
    void pay(double amount);
}

public class AlipayStrategy implements PaymentStrategy {
    @Override public void pay(double amount) { System.out.println("支付宝: ￥" + amount); }
}

public class WechatStrategy implements PaymentStrategy {
    @Override public void pay(double amount) { System.out.println("微信: ￥" + amount); }
}

// 上下文：持有策略引用
public class ShoppingCart {
    private PaymentStrategy paymentStrategy;

    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }

    public void checkout(double total) {
        paymentStrategy.pay(total);
    }
}
```

运行时切换：

```java
ShoppingCart cart = new ShoppingCart();
cart.setPaymentStrategy(new AlipayStrategy());
cart.checkout(100.00);

cart.setPaymentStrategy(new WechatStrategy());
cart.checkout(200.00);
```

### 5.2 策略模式消灭不了 if-else

这是一个常见误解。if-else 不会消失，只是从业务代码移到了策略选择的地方：

```java
public static PaymentStrategy getStrategy(String type) {
    return switch (type) {
        case "alipay" -> new AlipayStrategy();
        case "wechat" -> new WechatStrategy();
        default -> throw new IllegalArgumentException("未知支付方式");
    };
}
```

策略模式的价值在于：
1. **策略选择和策略执行分离**——改策略不影响业务逻辑
2. **新增策略不影响已有代码**——加一个实现类就行
3. **每个策略独立测试**

### 5.3 枚举策略

策略种类固定且不多时，用枚举更简洁：

```java
public enum PaymentType {
    ALIPAY("支付宝") {
        @Override public void pay(double amount) { System.out.println("支付宝: ￥" + amount); }
    },
    WECHAT("微信支付") {
        @Override public void pay(double amount) { System.out.println("微信: ￥" + amount); }
    };

    private final String name;
    PaymentType(String name) { this.name = name; }
    public abstract void pay(double amount);
}

PaymentType.ALIPAY.pay(100.00);
```

好处：不需要单独的策略类，编译期类型安全，新增策略加枚举值即可。

### 5.4 策略 vs 状态

| 维度 | 策略模式 | 状态模式 |
|------|---------|---------|
| 切换驱动 | 外部主动选择 | 内部状态变化自动触发 |
| 类比 | 遥控器切制冷/制热 | 空调检测到温度达标自动停机 |
| 侧重点 | 算法可替换 | 状态驱动的行为变化 |

### 5.5 小结

策略模式的精髓是**面向接口编程**——上下文只依赖策略接口，不依赖具体实现。切换实现只需要换一个策略对象，业务代码完全不用改。结合工厂模式使用时，策略的选择和创建都能统一管理。

---

## 总结

### 五个模式的分工

```
策略   → 同一件事不同做法，想换就换
模板方法 → 流程定好了，细节你来填
责任链  → 请求沿链条传递，谁处理谁知道
工厂   → 不用管怎么造，告诉我要什么就行
单例   → 全系统只有一份，别多造
```

### 选型速查

| 你遇到的情况 | 用什么 |
|------------|--------|
| 一个类被反复 new，而且大家都用同一个实例 | 单例 |
| 创建对象有一堆 if-else 判断类型 | 工厂 |
| 多个类流程一样，只是中间步骤不同 | 模板方法 |
| 处理逻辑需要排队串联 | 责任链 |
| 同一功能有多种实现，需要动态切换 | 策略 |

### 个人心得

1. **别为了用模式而用模式。** 两种支付方式用简单工厂就够了，三种以内不需要策略模式。
2. **先识别问题，再选模式。** 不是"我要用单例"，而是"这个对象全局只需要一份"。
3. **模式经常组合使用。** 策略 + 工厂（策略的选择交给工厂）、责任链 + 策略（链上每个节点通过策略决定下一步）、模板方法 + 工厂（工厂创建处理器实例）。
4. **Spring 框架里全是设计模式。** Bean 默认单例、`FactoryBean` 是工厂、`AbstractApplicationContext.refresh()` 是模板方法、`FilterChain` 是责任链、`Resource` 的不同实现是策略。理解了模式，读 Spring 源码会顺畅很多。
