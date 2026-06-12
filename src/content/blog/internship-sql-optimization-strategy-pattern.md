---
title: '实习笔记：SQL 优化与策略模式重构实战'
description: '实习期间的两个核心贡献：SQL 性能优化（2w+ms → 10ms，2000 倍提升）+ 策略模式重构（消除数百行 if-else）。包含完整排查思路、优化前后 SQL 对比、Java/Go 双语言实现。'
pubDate: '2025-06-12'
category: '后端开发'
tags: ['SQL', 'Java', 'Go', '性能优化']
---

## 某管理机构平台

**用户规模：** 2w+ 活跃用户

### 功能与架构

机构风险评估管理平台，采用四层架构：总行 → 省行 → 市分行 → 被管理机构，每层配备管理员和操作员角色。

**核心业务：**

1. **风险评估流程：** 管理员发起评估任务 → 指定待评估机构 → 机构填报风险/交易信息（SM4加密存储）→ 系统自动计算得分并汇总 → 前端回显计算字段 → 导出 Excel 报表

2. **文件类任务：** 总行任务全国可见；下属分行任务默认下级可见，需总行审批才能全局共享

**技术栈：** 小程序(TS) + 后端 Go + gRPC + Redis

---

### 关键数据表

| 表名 | 说明 |
|------|------|
| 用户信息表 | 所有用户信息，手机号等敏感字段 SM4 加密 |
| 用户标记表 | 角色权限：管理员标记、权限等级、身份标记等 |
| 机构表 | 关联被管理用户与所属机构及银行 |
| 银行表 | 银行 ID 及对应银行信息 |

---

### 核心贡献

#### 贡献 1：SQL 性能优化 — 测试环境 CPU 飙升问题

**S - 情境 (Situation)**

测试环境突然出现 CPU 占用率飙升至 85%-86%，影响系统稳定性。经排查，某页面加载极其缓慢，涉及 1w+ 机构数据的查询操作。

**T - 任务 (Task)**

定位并解决慢查询问题，将 SQL 执行时间从 2w+ms 优化到可接受范围，确保生产环境稳定运行。

**A - 行动 (Action)**

1. **问题定位：** 通过 SQL 日志定位慢查询，发现 Count 查询携带冗余 LEFT JOIN（user + role 全表扫描构建派生表），且 IN 列表包含 1400+ 个 agency ID

2. **根因分析：** Count 和列表 Find 共用 query 对象，导致统计查询无需的用户信息也被关联；IN 列表过长导致 SQL 报文膨胀

3. **优化实施：**
   - 拆分 Count 和 Find 查询，Count 仅保留必要 JOIN 条件
   - 用 `agency.bank_id IN (bankIds)` 替代 `agency.id IN (agencyIds)`，bankIds 仅几个到几十个
   - 添加复合索引：`idx_agency_bank_flag`、`idx_user_agency_flag_role`、`idx_role_flag_type`、`idx_bank_parent_flag`

**R - 结果 (Result)**

- SQL 执行时间：2w+ms → 30ms（语句优化）→ 10ms（加索引）
- CPU 占用率恢复正常
- 查询性能提升约 2000 倍

---

#### 贡献 2：策略模式重构 — 字段计算逻辑优化

**S - 情境 (Situation)**

风险评估模块涉及大量字段计算，每个字段有两种填充方式：DIRECT（直接填值）和 CALC（计算得出）。业务规则会随时间变化：某个字段今天用 DIRECT，下个月可能改成 CALC，后续可能又改回 DIRECT。

**T - 任务 (Task)**

原有实现用数百行 if-else 根据 tag 分发计算逻辑，每次新增字段或切换填充类型都需要侵入核心代码，可读性差、维护成本高、测试风险大。需要重构为可扩展、易维护的架构。

**A - 行动 (Action)**

1. **抽象策略接口：** 定义 `CalcStrategy` 接口，包含 `tag()` 和 `calculate()` 方法

2. **策略实现：** 将每种计算逻辑封装为独立策略类（OrderCalcStrategy、PaymentCalcStrategy、DirectStrategy 等），DIRECT 也作为策略之一

3. **工厂模式：** 创建 `CalcStrategyFactory`，维护 `tag → strategy` 映射，Spring 自动注入所有策略实现

4. **编排服务：** `JsonFillService` 解密 JSON 后遍历字段，通过工厂获取策略执行计算

**R - 结果 (Result)**

- 消除数百行 if-else，代码行数减少约 60%
- 新增字段类型：仅需新建策略类，无需修改核心代码（开闭原则）
- 切换填充类型：仅需配置或更换策略实现，零侵入
- 单元测试覆盖：每个策略可独立测试，测试粒度更细

---

## SQL 优化实战

### 排查思路

1. **定位问题源头：** 用户反馈字段错误或页面加载缓慢，先确认是后端逻辑还是 SQL 层面问题

2. **复现路径追踪：** 根据截图定位页面 URL，结合 AI 分析调用链路。本项目有 SQL 操作日志，提取对应 SQL 即可获取表数据

3. **本地复现验证：** 导入数据本地复现，判断是偶发性故障还是系统性业务逻辑问题

4. **针对性修复：** 若为业务逻辑问题，定位并修改对应 SQL

---

### 案例 1：测试环境 CPU 飙升至 86%

**业务场景：** 省行管理员查看辖区全部机构详情，涉及 1w+ 机构

#### 原始 SQL

```sql
SELECT count(*) FROM `agency`
INNER JOIN bank ON bank.id = agency.bank_id
LEFT JOIN (
    SELECT user.name, user.desensitize_phone_number, user.agency_id
    FROM user
    INNER JOIN role ON role.id = user.role_id
    WHERE role.flag = 1 AND role.role_type = 1 AND role.type = 2 AND user.flag = 1
) a ON a.agency_id = agency.id
WHERE bank.flag = 1 AND agency.flag = 1
AND agency.id IN (112, 113, 114, ..., 1575)  -- 1400+ 个 ID
```

#### 问题分析

**问题 1：冗余 JOIN 拖累 COUNT 查询**

核心需求是「统计机构数量」，与用户姓名、电话无关。但代码复用 query 对象做 Count 和 Find，导致：

- `LEFT JOIN (SELECT ... FROM user INNER JOIN role ...)` — 全表扫描 user + role 构建派生表
- `DISTINCT agency.*` — 额外排序去重开销

**问题 2：超长 IN 列表**

原始流程：`bankIds → 查询银行下全部机构 → 得到 1400+ agencyIds → agency.id IN (...)`

1400+ 个 ID 导致 SQL 报文膨胀，解析器和优化器开销随列表长度线性增长

#### 优化方案

**方案 1：基础 query 精简化**

```sql
SELECT agency.*
FROM agency
INNER JOIN bank ON bank.id = agency.bank_id
WHERE bank.flag = 1 AND agency.flag = 1
```

query 仅承载 WHERE 过滤条件，user 子查询 JOIN、DISTINCT、展示字段移至列表查询单独附加

**方案 2：bank_id 替代 agency.id IN**

`agency.bank_id IN (bankIds)` 与 `agency.id IN (agencyIds)` 在含 `agency.flag = 1` 条件时业务等价，而 bankIds 通常仅几个到几十个，避免额外查询

#### 优化后 SQL

**Count 查询：**
```sql
SELECT count(*) FROM `agency`
INNER JOIN bank ON bank.id = agency.bank_id
WHERE bank.flag = 1 AND agency.flag = 1
AND agency.bank_id IN (1, 5, 8, ...)
```

**分页列表查询：**
```sql
SELECT DISTINCT agency.*, a.name AS user_name, ...
FROM `agency`
INNER JOIN bank ON bank.id = agency.bank_id
LEFT JOIN (
    SELECT user.name, user.desensitize_phone_number, user.agency_id
    FROM user INNER JOIN role ...
) a ON a.agency_id = agency.id
WHERE bank.flag = 1 AND agency.flag = 1
AND agency.bank_id IN (1, 5, 8, ...)
LIMIT 20 OFFSET 0
```

#### 索引优化

```sql
-- agency 表：支撑 bank_id 过滤 + flag 过滤
CREATE INDEX idx_agency_bank_flag ON agency(bank_id, flag);

-- user 表：支撑 user 子查询的关联与过滤
CREATE INDEX idx_user_agency_flag_role ON user(agency_id, flag, role_id);

-- role 表：支撑 user 子查询中对 role 的过滤
CREATE INDEX idx_role_flag_type ON role(flag, role_type, type, id);

-- bank 表：支撑 GetBankIdsByParentId 的层级查询
CREATE INDEX idx_bank_parent_flag ON bank(parent_bank_id, flag);
```

**优化效果：** 2w+ms → 10ms

---

### 案例 2：用户需求修改 SQL

#### 问题 2.1：字段拼接错误

**用户反馈：** 浙江某分行查看文件类任务，发布者显示为其他省份分行

**定位：** 查询字段拼接错误，用于查询银行的字段误用用户 ID（恰巧与分行 ID 一致）

**修复：** 修改为对应机构 ID

#### 问题 2.2：新增任务可见范围

**需求：** 当前机构可查看所属分行发布的任务，以及上级省行任务

**实现：** 构建 bankId 表，包含对应分行和省行，使用 IN 查询

**注意：** 测试数据中全国总行任务全部可见，需排除避免混淆

---

## 策略模式重构

### 业务痛点：字段填充类型可切换

风险评估流程中，前端传入的 JSON 数组经 SM4 加密存入数据库，结构为两层 `[[{...}]]`。每个字段有两种填充方式：

- **DIRECT：** 直接使用前端传入的值
- **CALC：** 根据表达式计算得出

**问题：业务规则会随时间变化。**

某个字段今天用 DIRECT（直接填值），下个月可能改成 CALC（需要计算），半年后可能又改回 DIRECT。每次切换都要：

1. 找到对应的 if-else 分支
2. 修改判断逻辑
3. 可能还要调整计算表达式
4. 回归测试相关功能

原有实现用数百行 if-else 根据 tag 分发：

```java
// 原有代码片段
if ("order".equals(tag)) {
    // 订单计算逻辑
    result = amount * taxRate + amount;
} else if ("payment".equals(tag)) {
    // 支付计算逻辑
    result = principal * rate * periods;
} else if ("direct".equals(tag)) {
    // 直接填值
    result = source.get("value");
} else if ("refund".equals(tag)) {
    // ... 更多分支
}
// ... 数百行
```

**维护成本高：**
- 新增字段类型：侵入核心代码，加 else-if 分支
- 切换填充类型：修改条件判断，可能影响其他分支
- 代码可读性差：数百行 if-else 难以理解业务意图
- 测试成本高：修改核心逻辑需回归所有相关场景

---

### 解决思路：策略模式 + 工厂

核心思想：**把「用什么方式填充」这个决策从代码里解耦出来，变成可配置的策略。**

```
前端传入 → SM4加密存DB → 取用时解密 → 解析[[{tag:"order",...}]]
                                              ↓
                                    根据tag路由到对应策略
                                              ↓
                                    strategy.calculate(item)
                                              ↓
                                    结果写回item返回前端
```

**关键设计：**

- **tag：** 路由键，标识字段类型（如 "order"、"payment"、"direct"）
- **CalcStrategy：** 策略接口，定义统一的计算方法
- **CalcStrategyFactory：** 工厂，维护 `tag → strategy` 映射，负责路由
- **DIRECT 也是策略：** 与计算策略平级，无需特殊处理

---

### Java 实现（Spring 自动注入）

#### 1. 策略接口

```java
public interface CalcStrategy {
    String tag();
    Object calculate(JSONObject source);
}
```

#### 2. 策略实现

```java
@Component
public class OrderCalcStrategy implements CalcStrategy {
    @Override
    public String tag() {
        return "order";
    }
    
    @Override
    public Object calculate(JSONObject source) {
        double amount = source.getDouble("amount");
        double taxRate = source.getDouble("taxRate");
        return amount * taxRate + amount;
    }
}

@Component
public class PaymentCalcStrategy implements CalcStrategy {
    @Override
    public String tag() {
        return "payment";
    }
    
    @Override
    public Object calculate(JSONObject source) {
        double principal = source.getDouble("principal");
        double rate = source.getDouble("rate");
        int periods = source.getInteger("periods");
        return principal * rate * periods;
    }
}

@Component
public class DirectStrategy implements CalcStrategy {
    @Override
    public String tag() {
        return "direct";
    }
    
    @Override
    public Object calculate(JSONObject source) {
        return source.get("value");
    }
}
```

#### 3. 工厂（Spring 自动注入）

```java
@Component
public class CalcStrategyFactory {
    
    private final Map<String, CalcStrategy> strategyMap;
    
    // Spring 自动注入所有 CalcStrategy 实现
    public CalcStrategyFactory(List<CalcStrategy> strategies) {
        this.strategyMap = strategies.stream()
            .collect(Collectors.toMap(CalcStrategy::tag, s -> s));
    }
    
    public CalcStrategy get(String tag) {
        CalcStrategy strategy = strategyMap.get(tag);
        if (strategy == null) {
            throw new IllegalArgumentException("Unknown tag: " + tag);
        }
        return strategy;
    }
}
```

#### 4. 编排服务

```java
@Service
public class JsonFillService {
    
    @Autowired
    private CalcStrategyFactory strategyFactory;
    
    public String process(String encryptedData) {
        // 1. 解密
        String json = SM4Util.decrypt(encryptedData);
        
        // 2. 解析两层 JSON
        JSONArray groups = JSON.parseArray(json);
        
        // 3. 遍历填充
        for (int i = 0; i < groups.size(); i++) {
            JSONArray group = groups.getJSONArray(i);
            for (int j = 0; j < group.size(); j++) {
                JSONObject item = group.getJSONObject(j);
                fillItem(item);
            }
        }
        
        return groups.toJSONString();
    }
    
    private void fillItem(JSONObject item) {
        String tag = item.getString("tag");
        CalcStrategy strategy = strategyFactory.get(tag);
        Object result = strategy.calculate(item);
        item.put("result", result);
    }
}
```

---

### Go 实现（手动注册）

#### 1. 策略接口

```go
type CalcStrategy interface {
    Tag() string
    Calculate(source map[string]interface{}) interface{}
}
```

#### 2. 策略实现

```go
type OrderCalcStrategy struct{}

func (s *OrderCalcStrategy) Tag() string {
    return "order"
}

func (s *OrderCalcStrategy) Calculate(source map[string]interface{}) interface{} {
    amount := source["amount"].(float64)
    taxRate := source["taxRate"].(float64)
    return amount*taxRate + amount
}

type PaymentCalcStrategy struct{}

func (s *PaymentCalcStrategy) Tag() string {
    return "payment"
}

func (s *PaymentCalcStrategy) Calculate(source map[string]interface{}) interface{} {
    principal := source["principal"].(float64)
    rate := source["rate"].(float64)
    periods := source["periods"].(int)
    return principal * rate * float64(periods)
}

type DirectStrategy struct{}

func (s *DirectStrategy) Tag() string {
    return "direct"
}

func (s *DirectStrategy) Calculate(source map[string]interface{}) interface{} {
    return source["value"]
}
```

#### 3. 工厂（手动注册）

```go
type CalcStrategyFactory struct {
    strategies map[string]CalcStrategy
}

func NewCalcStrategyFactory() *CalcStrategyFactory {
    f := &CalcStrategyFactory{
        strategies: make(map[string]CalcStrategy),
    }
    // 手动注册所有策略
    f.Register(&OrderCalcStrategy{})
    f.Register(&PaymentCalcStrategy{})
    f.Register(&DirectStrategy{})
    return f
}

func (f *CalcStrategyFactory) Register(s CalcStrategy) {
    f.strategies[s.Tag()] = s
}

func (f *CalcStrategyFactory) Get(tag string) CalcStrategy {
    strategy, ok := f.strategies[tag]
    if !ok {
        panic("Unknown tag: " + tag)
    }
    return strategy
}
```

#### 4. 编排服务

```go
func Process(encryptedData string) string {
    // 1. 解密
    json := SM4Decrypt(encryptedData)
    
    // 2. 解析两层 JSON
    var groups [][]map[string]interface{}
    json.Unmarshal([]byte(json), &groups)
    
    // 3. 工厂
    factory := NewCalcStrategyFactory()
    
    // 4. 遍历填充
    for i := range groups {
        for j := range groups[i] {
            item := groups[i][j]
            tag := item["tag"].(string)
            strategy := factory.Get(tag)
            result := strategy.Calculate(item)
            item["result"] = result
        }
    }
    
    result, _ := json.Marshal(groups)
    return string(result)
}
```

---

### 扩展方式

#### 新增策略

**Java：**
```java
@Component
public class RefundCalcStrategy implements CalcStrategy {
    public String tag() { return "refund"; }
    public Object calculate(JSONObject source) {
        // 退款计算逻辑
    }
}
// Spring 自动注入，无需改任何代码
```

**Go：**
```go
type RefundCalcStrategy struct{}

func (s *RefundCalcStrategy) Tag() string { return "refund" }
func (s *RefundCalcStrategy) Calculate(source map[string]interface{}) interface{} {
    // 退款计算逻辑
}

// 在 NewCalcStrategyFactory 中加一行注册
f.Register(&RefundCalcStrategy{})
```

#### 切换策略类型

某个 tag 从「计算」改为「直接填值」：

- **Java：** 修改配置或策略实现，无需改编排代码
- **Go：** 修改工厂注册，换一个策略实现