---
title: 'Caffeine LoadingCache.get() 源码调用链解析'
description: '从 get(key) 一路追到 loadFromRedisOrSource，理清 CacheLoader 是如何被 Caffeine 调用的。'
pubDate: '2026-06-13'
category: '源码分析'
tags: ['Caffeine', '缓存', '源码分析', 'Java']
---

## 起点：示例代码

```java
// TwoLevelCache.java 构造方法
this.caffeineCache = Caffeine.newBuilder()
    .maximumSize(maxSize)
    .expireAfterWrite(expireSeconds, TimeUnit.SECONDS)
    .refreshAfterWrite(refreshSeconds, TimeUnit.SECONDS)
    .recordStats()
    .build(new CacheLoader<String, Object>() {
        @Override
        public Object load(String key) {
            return loadFromRedisOrSource(key, sourceLoader);
        }

        @Override
        public Object reload(String key, Object oldValue) {
            try {
                Object fromRedis = loadFromRedisOnly(key);
                return fromRedis != null ? fromRedis : oldValue;
            } catch (Exception e) {
                log.warn("两级缓存reload异常, key={}", key, e);
                return oldValue;
            }
        }
    });
```

```java
// TwoLevelCache.java get方法
public V get(String key) {
    Object value = caffeineCache.get(key);
    if (value == NULL_VALUE) {
        return null;
    }
    return (V) value;
}
```

目标：理清 `caffeineCache.get(key)` 到 `loadFromRedisOrSource` 的完整调用链路。

---

## new CacheLoader(){...} 的本质

`new CacheLoader<String, Object>() {...}` 不是实例化接口，是创建**匿名内部类**。

Java 语法规定接口不能直接 `new`，但 `new 接口(){...}` 会由编译器自动生成一个实现类：

```java
// 示例
new CacheLoader<String, Object>() {
    @Override
    public Object load(String key) { ... }
    @Override
    public Object reload(String key, Object oldValue) { ... }
}

// 编译器等价生成（运行时不可见，但确实存在）
class AnonymousCacheLoader implements CacheLoader<String, Object> {
    @Override
    public Object load(String key) { return loadFromRedisOrSource(key, sourceLoader); }
    @Override
    public Object reload(String key, Object oldValue) { ... }
}
// 然后：.build(new AnonymousCacheLoader());
```

所以 `new CacheLoader(){...}` 创建的是**加载逻辑对象**，传给 Caffeine，由 Caffeine 在合适的时机调用。

---

## 源码调用链：一层一层追

### 第1层：caffeineCache.get(key) → 谁实现了 get？

`caffeineCache` 的声明类型是 `LoadingCache<String, Object>`，这是接口：

```java
// LoadingCache.java
public interface LoadingCache<K, V> extends Cache<K, V> {
    V get(K key);  // 只有声明
}
```

IDEA 点击只能看到接口声明。`Ctrl+Alt+B` 找实现。

![LoadingCache.get() 接口声明](/images/caffeine-loadingcache/1.png)

---

### 第2层：LocalLoadingCache.get(key)

```java
// LocalLoadingCache.java 第57-59行
interface LocalLoadingCache<K, V> extends LocalManualCache<K, V>, LoadingCache<K, V> {

    Function<K, V> mappingFunction();  // 接口方法

    @Override
    default V get(K key) {
        return cache().computeIfAbsent(key, mappingFunction());
    }
}
```

**关键：** `cache().computeIfAbsent(key, mappingFunction())`

- `cache()` 返回底层 ConcurrentHashMap
- `computeIfAbsent`：key 存在直接返回，不存在才执行 mappingFunction
- `mappingFunction()` 是接口方法，返回值从哪来？`Ctrl+Alt+B` 找实现

![LocalLoadingCache.get() 实现](/images/caffeine-loadingcache/2.png)

---

### 第3层：BoundedLocalLoadingCache.mappingFunction()

```java
// BoundedLocalCache.java 第4443-4466行
static final class BoundedLocalLoadingCache<K, V>
    extends BoundedLocalManualCache<K, V> implements LocalLoadingCache<K, V> {

    final Function<K, V> mappingFunction;  // 成员变量

    BoundedLocalLoadingCache(Caffeine<K, V> builder, CacheLoader<? super K, V> loader) {
        super(builder, loader);
        requireNonNull(loader);
        mappingFunction = newMappingFunction(loader);  // 构造时创建
        bulkMappingFunction = newBulkMappingFunction(loader);
    }

    @Override
    public Function<K, V> mappingFunction() {
        return mappingFunction;  // getter，返回成员变量
    }
}
```

**mappingFunction() 和 newMappingFunction() 的关系：**

| 方法 | 类型 | 什么时候调用 | 做什么 |
|------|------|------------|--------|
| `newMappingFunction(loader)` | 静态方法 | 构造时（build） | 把 CacheLoader 包装成 Function |
| `mappingFunction()` | 实例方法（getter） | 运行时（get） | 取出构造时存的 Function |

类比：
```java
// 构造时：造钥匙，存起来
Function<K, V> mappingFunction = newMappingFunction(loader);

// 运行时：拿钥匙
public Function<K, V> mappingFunction() {
    return mappingFunction;
}
```

`newMappingFunction(loader)` 里面做了什么？

![BoundedLocalLoadingCache 构造](/images/caffeine-loadingcache/3.png)
![newMappingFunction 实现](/images/caffeine-loadingcache/4.png)

---

### 第4层：newMappingFunction — 把 CacheLoader 包装成 Function

```java
// LocalLoadingCache.java 第180-193行
static <K, V> Function<K, V> newMappingFunction(CacheLoader<? super K, V> cacheLoader) {
    return key -> {
        try {
            return cacheLoader.load(key);  // 调用自定义 load()
        } catch (RuntimeException e) {
            throw e;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new CompletionException(e);
        } catch (Exception e) {
            throw new CompletionException(e);
        }
    };
}
```

包装的原因：`computeIfAbsent` 需要的参数类型是 `Function<K, V>`，不是 `CacheLoader`。`cacheLoader.load(key)` 里的 `cacheLoader` 是 `new CacheLoader(){...}` 创建的匿名类对象。

---

### 第5层：自定义 load()

```java
@Override
public Object load(String key) {
    return loadFromRedisOrSource(key, sourceLoader);
}
```

到这里，调用链从 Caffeine 框架回到业务代码。

![isBounded 判断逻辑](/images/caffeine-loadingcache/5.png)

---

## build(loader) 构造时的选择

```java
// Caffeine.java 第1066-1075行
public LoadingCache<K1, V1> build(CacheLoader<? super K1, V1> loader) {
    Caffeine<K1, V1> self = (Caffeine<K1, V1>) this;
    return isBounded() || refreshAfterWrite()
        ? new BoundedLocalCache.BoundedLocalLoadingCache<>(self, loader)
        : new UnboundedLocalCache.UnboundedLocalLoadingCache<>(self, loader);
}
```

| 条件 | 创建的实现类 | 底层存储 |
|------|------------|---------|
| 配了 `maximumSize` / `expireAfterWrite` / `refreshAfterWrite` | `BoundedLocalLoadingCache` | 有界，支持淘汰 |
| 什么都没配 | `UnboundedLocalLoadingCache` | 无界 |

两个实现类的 `mappingFunction` 逻辑一样：`mappingFunction = newMappingFunction(loader)`。

---

## 完整调用链路图

```
【构造阶段】build(loader)
    │
    ▼
Caffeine.build(loader)
    │
    ├── isBounded() || refreshAfterWrite() 为 true
    │       │
    │       ▼
    │   new BoundedLocalLoadingCache(self, loader)
    │       │
    │       ▼
    │   构造方法：
    │     mappingFunction = newMappingFunction(loader)
    │       │
    │       ▼
    │     return key -> cacheLoader.load(key)  // 包装成 Function
    │
    └── 否则
            │
            ▼
        new UnboundedLocalLoadingCache(self, loader)


【运行阶段】caffeineCache.get(key)
    │
    ▼
LoadingCache.get(key)                    // 接口声明
    │  → Ctrl+Alt+B
    ▼
LocalLoadingCache.get(key)               // default 实现
    │  cache().computeIfAbsent(key, mappingFunction())
    │
    │  mappingFunction() 返回值从哪来？
    │  → Ctrl+Alt+B
    ▼
BoundedLocalLoadingCache.mappingFunction()
    │  return mappingFunction;           // 取出成员变量
    │
    ├── key 存在 → 直接返回缓存值
    │
    └── key 不存在 → 执行 mappingFunction.apply(key)
            │
            ▼
        lambda 执行：cacheLoader.load(key)
            │
            ▼
        自定义 load()
            │
            ▼
        loadFromRedisOrSource(key, sourceLoader)
```

---

## refresh 刷新链路

`refreshAfterWrite` 到期后，下次访问触发异步刷新：

```
LocalLoadingCache.refresh(key)
    │
    ├── 缓存有旧值 → cacheLoader().asyncReload(key, oldValue, executor)
    │       │
    │       ▼
    │   自定义 reload() → loadFromRedisOnly(key)  // 只查 Redis
    │
    └── 缓存无值   → cacheLoader().asyncLoad(key, executor)
            │
            ▼
        自定义 load() → loadFromRedisOrSource(key, sourceLoader)
```

---

## 源码追踪方法

**用 Ctrl+Alt+B 逐层找实现类：**

| 当前位置 | 要确认的内容 | 操作 |
|---------|-------------|------|
| `LoadingCache.get(key)` | 谁实现了 get？ | `Ctrl+Alt+B` |
| `mappingFunction()` | 谁实现了？ | `Ctrl+Alt+B` |
| `newMappingFunction(loader)` | 里面做了什么？ | 点进去看 |
| `cacheLoader.load(key)` | cacheLoader 是谁？ | 就是构造时传入的匿名类 |

逐层跟踪，每层确认实现类/返回值。

---

## 核心总结

- `new CacheLoader(){...}` 创建的是匿名内部类，装着自定义加载逻辑
- `build(loader)` 时，Caffeine 把 loader 包装成 Function 存到成员变量
- `get(key)` 调用 `computeIfAbsent(key, mappingFunction())`，`mappingFunction()` 只是 getter
- 未命中时执行 Function，内部调用 `cacheLoader.load(key)`，走到业务代码
- `load()`：首次加载/过期重新加载 → Redis + 回源
- `reload()`：异步刷新 → 只查 Redis，不回源，异常保留旧值
