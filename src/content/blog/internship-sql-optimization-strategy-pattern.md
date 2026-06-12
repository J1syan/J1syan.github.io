---
title: '实习笔记1'
description: '实习期间做的两件事：SQL性能优化和策略模式重构。'
pubDate: '2026-06-12'
category: '后端开发'
tags: ['SQL', 'Java', 'Go', '性能优化', '实习']
---

项目是一个机构风险评估管理平台，四层架构：总行 → 省行 → 市分行 → 被管理机构。技术栈是小程序(TS) + 后端 Go + gRPC + Redis。

---

## SQL 优化

### 问题

测试环境 CPU 占用率飙升到 85%-86%，某页面加载极其缓慢，涉及 1w+ 机构数据的查询。

### 排查

通过 SQL 日志定位到慢查询：

1. Count 查询携带了冗余的 LEFT JOIN（user + role 全表扫描构建派生表）
2. IN 列表包含 1400+ 个 agency ID，SQL 报文膨胀

Count 和列表 Find 共用了一个 query 对象，统计查询时把不需要的用户信息也关联进来了。

### 优化

**1. 拆分 Count 和 Find**

Count 查询只保留必要的 JOIN：

```sql
SELECT count(*) FROM agency
INNER JOIN bank ON bank.id = agency.bank_id
WHERE bank.flag = 1 AND agency.flag = 1
AND agency.bank_id IN (1, 5, 8, ...)
```

列表查询再附加 user 子查询和展示字段。

**2. bank_id 替换 agency.id IN**

用 `agency.bank_id IN (bankIds)` 代替 `agency.id IN (agencyIds)`。bankIds 通常只有几个到几十个，避免额外查询全部机构。

**3. 加索引**

```sql
CREATE INDEX idx_agency_bank_flag ON agency(bank_id, flag);
CREATE INDEX idx_user_agency_flag_role ON user(agency_id, flag, role_id);
CREATE INDEX idx_role_flag_type ON role(flag, role_type, type, id);
CREATE INDEX idx_bank_parent_flag ON bank(parent_bank_id, flag);
```

**效果：** 2w+ms → 30ms（语句优化）→ 10ms（加索引）

### 其他 SQL 修复

**字段拼接错误：** 查询银行的字段误用了用户 ID，导致发布者显示成其他省份分行。修正为对应机构 ID。

**新增任务可见范围：** 当前机构可查看所属分行和上级省行的任务。构建 bankId 表，用 IN 查询实现。

---

## 策略模式重构

### 背景

风险评估模块有大量字段计算，每个字段有两种填充方式：DIRECT（直接填值）和 CALC（计算得出）。业务规则会变化，某个字段今天用 DIRECT，下个月可能改成 CALC。

原有实现用几百行 if-else 根据 tag 分发计算逻辑，新增字段或切换填充类型都要改核心代码。

### 方案

用策略模式把计算逻辑拆成独立的策略类，通过工厂路由。

**流程：**

前端传入 → SM4加密存DB → 取用时解密 → 解析 `[[{tag:"order",...}]]` → 根据 tag 路由到对应策略 → 计算结果写回

### Java 实现（Spring 自动注入）

**策略接口：**

```java
public interface CalcStrategy {
    String tag();
    Object calculate(JSONObject source);
}
```

**策略实现：**

```java
@Component
public class OrderCalcStrategy implements CalcStrategy {
    public String tag() { return "order"; }
    public Object calculate(JSONObject source) {
        double amount = source.getDouble("amount");
        double taxRate = source.getDouble("taxRate");
        return amount * taxRate + amount;
    }
}

@Component
public class DirectStrategy implements CalcStrategy {
    public String tag() { return "direct"; }
    public Object calculate(JSONObject source) {
        return source.get("value");
    }
}
```

**工厂：**

```java
@Component
public class CalcStrategyFactory {
    private final Map<String, CalcStrategy> strategyMap;

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

**编排：**

```java
@Service
public class JsonFillService {
    @Autowired
    private CalcStrategyFactory strategyFactory;

    public String process(String encryptedData) {
        String json = SM4Util.decrypt(encryptedData);
        JSONArray groups = JSON.parseArray(json);

        for (int i = 0; i < groups.size(); i++) {
            JSONArray group = groups.getJSONArray(i);
            for (int j = 0; j < group.size(); j++) {
                JSONObject item = group.getJSONObject(j);
                String tag = item.getString("tag");
                CalcStrategy strategy = strategyFactory.get(tag);
                Object result = strategy.calculate(item);
                item.put("result", result);
            }
        }
        return groups.toJSONString();
    }
}
```

### Go 实现（手动注册）

**策略接口：**

```go
type CalcStrategy interface {
    Tag() string
    Calculate(source map[string]interface{}) interface{}
}
```

**工厂：**

```go
type CalcStrategyFactory struct {
    strategies map[string]CalcStrategy
}

func NewCalcStrategyFactory() *CalcStrategyFactory {
    f := &CalcStrategyFactory{strategies: make(map[string]CalcStrategy)}
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

**编排：**

```go
func Process(encryptedData string) string {
    json := SM4Decrypt(encryptedData)
    var groups [][]map[string]interface{}
    json.Unmarshal([]byte(json), &groups)

    factory := NewCalcStrategyFactory()

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

### 扩展

新增字段：新建策略类，Java 自动注入，Go 在工厂中加一行注册。

切换填充类型：换策略实现，不改动编排代码。
