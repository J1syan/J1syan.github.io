---
title: 'Caffeine LoadingCache 源码调用链解析：从 get() 到你的业务代码'
description: '一步步追踪 Caffeine LoadingCache.get() 的完整调用链，看清楚你的 CacheLoader 是如何被框架调用的。适合想理解缓存框架内部机制的开发者。'
pubDate: '2025-06-12'
category: 'Java'
tags: ['Caffeine', '缓存', '源码分析', 'Java', 'LoadingCache']
---

## 写在前面

你在项目中用了 Caffeine，写了 `CacheLoader` 的 `load()` 方法，然后调用 `cache.get(key)` 就能拿到值。但你有没有想过：**你写的 `load()` 方法，是怎么被 Caffeine 调用的？**

这篇文章不是讲 Caffeine 怎么用，而是带你一步步追踪源码，看清楚整个调用链。读完之后，你会对"框架如何回调业务代码"这件事有更深的理解。

---

## 从你写的代码开始

一切从这里开始：

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

然后调用：

```java
public V get(String key) {
    Object value = caffeineCache.get(key);
    if (value == NULL_VALUE) {
        return null;
    }
    return (V) value;
}
```

问题来了：`caffeineCache.get(key)` 这一行，最终是怎么走到你写的 `loadFromRedisOrSource` 的？

---

## 先搞清楚：new CacheLoader(){...} 是什么？

你可能会问：`CacheLoader` 是接口，接口能 `new` 吗？

答案是：**不能，但可以 `new 接口(){...}` 创建匿名内部类**。

```java
// 你写的
new CacheLoader<String, Object>() {
    @Override
    public Object load(String key) { ... }
    @Override
    public Object reload(String key, Object oldValue) { ... }
}

// 编译器实际做的事情（你看不到，但它确实生成了）
class AnonymousCacheLoader implements CacheLoader<String, Object> {
    @Override
    public Object load(String key) { return loadFromRedisOrSource(key, sourceLoader); }
    @Override
    public Object reload(String key, Object oldValue) { ... }
}
// 然后：.build(new AnonymousCacheLoader());
```

所以 `new CacheLoader(){...}` 创建的是**一个实现了 CacheLoader 接口的对象**，里面装的就是你写的加载逻辑。

这个对象会被传给 Caffeine，Caffeine 在合适的时机调用它。

---

## 开始追踪：一层一层剥开调用链

我们的目标是：从 `caffeineCache.get(key)` 追到你写的 `loadFromRedisOrSource`。

### 第1站：LoadingCache.get(key) — 接口声明

`caffeineCache` 的类型是 `LoadingCache<String, Object>`，这是一个接口：

```java
// LoadingCache.java
public interface LoadingCache<K, V> extends Cache<K, V> {
    V get(K key);  // 只有声明，没有实现
}
```

**在 IDEA 里点击只能看到接口**，因为这一层确实没有实现体。

怎么办？**`Ctrl + Alt + B`（Find Implementations）**，找谁实现了这个接口。

---

### 第2站：LocalLoadingCache.get(key) — default 实现

找到实现后，看到：

```java
// LocalLoadingCache.java 第57-59行
interface LocalLoadingCache<K, V> extends LocalManualCache<K, V>, LoadingCache<K, V> {

    Function<K, V> mappingFunction();  // 接口方法，没有实现体

    @Override
    default V get(K key) {
        return cache().computeIfAbsent(key, mappingFunction());
    }
}
```

**关键代码：** `cache().computeIfAbsent(key, mappingFunction())`

这里做了什么？

- `cache()` 返回底层的 ConcurrentHashMap
- `computeIfAbsent`：如果 key 存在，直接返回值；如果不存在，执行 `mappingFunction()` 加载

问题来了：**`mappingFunction()` 是接口方法，返回值从哪来？**

继续 `Ctrl + Alt + B`，找谁实现了 `mappingFunction()`。

---

### 第3站：BoundedLocalLoadingCache — 真正的实现

追到这里：

```java
// BoundedLocalCache.java 第4443-4466行
static final class BoundedLocalLoadingCache<K, V>
    extends BoundedLocalManualCache<K, V> implements LocalLoadingCache<K, V> {

    final Function<K, V> mappingFunction;  // 成员变量！

    // 构造方法：build(loader) 时调用
    BoundedLocalLoadingCache(Caffeine<K, V> builder, CacheLoader<? super K, V> loader) {
        super(builder, loader);
        requireNonNull(loader);
        mappingFunction = newMappingFunction(loader);  // 构造时创建并存起来
        bulkMappingFunction = newBulkMappingFunction(loader);
    }

    @Override
    public Function<K, V> mappingFunction() {
        return mappingFunction;  // getter，返回成员变量
    }
}
```

**原来 `mappingFunction()` 只是个 getter！**

那 `mappingFunction` 这个成员变量是什么时候赋值的？看构造方法：

```java
mappingFunction = newMappingFunction(loader);  // 第4453行
```

**构造时创建，存到成员变量，运行时只是取出来用。**

类比一下：

```java
// 构造时：造钥匙，存起来
Function<K, V> mappingFunction = newMappingFunction(loader);

// 运行时：拿钥匙，用起来
public Function<K, V> mappingFunction() {
    return mappingFunction;  // getter = 取出
}
```

那 `newMappingFunction(loader)` 里面做了什么？点进去看。

---

### 第4站：newMappingFunction — 把 CacheLoader 包装成 Function

```java
// LocalLoadingCache.java 第180-193行
static <K, V> Function<K, V> newMappingFunction(CacheLoader<? super K, V> cacheLoader) {
    return key -> {
        try {
            return cacheLoader.load(key);  // 调用你写的 load() 方法！
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

**真相大白！**

这个静态方法做的事情是：**把你的 `CacheLoader` 包装成一个 `Function`**。

为什么需要包装？因为 `computeIfAbsent` 需要的参数类型是 `Function<K, V>`，不是 `CacheLoader`。

这个 lambda 里调用的 `cacheLoader.load(key)`，`cacheLoader` 是谁？

**就是你 `new CacheLoader(){...}` 创建的那个匿名内部类对象。**

---

### 第5站：回到你的代码 — loadFromRedisOrSource

到这里，调用链从 Caffeine 框架回到了你的业务代码：

```java
// 你写的匿名内部类中的 load 方法
@Override
public Object load(String key) {
    return loadFromRedisOrSource(key, sourceLoader);
}
```

**完整路径：**

```
caffeineCache.get(key)
    → LocalLoadingCache.get(key)
        → cache().computeIfAbsent(key, mappingFunction())
            → mappingFunction.apply(key)  // key 不存在时
                → cacheLoader.load(key)
                    → loadFromRedisOrSource(key, sourceLoader)
```

---

## 构造阶段发生了什么？

你调用 `build(loader)` 时，Caffeine 做了什么？

```java
// Caffeine.java 第1066-1075行
public LoadingCache<K1, V1> build(CacheLoader<? super K1, V1> loader) {
    Caffeine<K1, V1> self = (Caffeine<K1, V1>) this;
    return isBounded() || refreshAfterWrite()
        ? new BoundedLocalCache.BoundedLocalLoadingCache<>(self, loader)   // 有淘汰策略
        : new UnboundedLocalCache.UnboundedLocalLoadingCache<>(self, loader);  // 无淘汰策略
}
```

根据你是否配置了淘汰策略，创建不同的实现类：

| 条件 | 创建的实现类 | 特点 |
|------|------------|------|
| 配了 `maximumSize` / `expireAfterWrite` / `refreshAfterWrite` | `BoundedLocalLoadingCache` | 有界，支持淘汰 |
| 什么都没配 | `UnboundedLocalLoadingCache` | 无界 |

**两个实现类的核心逻辑一样**：都在构造时调用 `newMappingFunction(loader)` 把你的 loader 包装成 Function 存起来。

---

## 完整调用链图

把整个过程画出来：

```
【构造阶段】build(loader)
    │
    ▼
Caffeine.build(loader)
    │
    ├── 配了淘汰策略
    │       │
    │       ▼
    │   new BoundedLocalLoadingCache(self, loader)
    │       │
    │       ▼
    │   构造方法内部：
    │     mappingFunction = newMappingFunction(loader)
    │       │
    │       ▼
    │     return key -> cacheLoader.load(key)  // 包装成 lambda
    │       │
    │       ▼
    │     Function 对象存到成员变量
    │
    └── 没配淘汰策略
            │
            ▼
        new UnboundedLocalLoadingCache(self, loader)  // 逻辑一样


【运行阶段】caffeineCache.get(key)
    │
    ▼
LoadingCache.get(key)                    // 接口声明
    │
    ▼
LocalLoadingCache.get(key)               // default 实现
    │  cache().computeIfAbsent(key, mappingFunction())
    │
    ├── key 存在 → 直接返回缓存值
    │
    └── key 不存在 → 执行 mappingFunction.apply(key)
            │
            ▼
        BoundedLocalLoadingCache.mappingFunction()  // 取出成员变量
            │
            ▼
        lambda 执行：cacheLoader.load(key)
            │
            ▼
        你写的 load() 方法
            │
            ▼
        loadFromRedisOrSource(key, sourceLoader)
            │
            ├── 查 Redis → 命中则返回
            │
            └── Redis 未命中 → 调用 sourceLoader 回源
```

---

## refresh 刷新链路

如果你配了 `refreshAfterWrite`，刷新时走的链路略有不同：

```
LocalLoadingCache.refresh(key)           // 异步刷新
    │
    ├── 缓存有旧值
    │       │
    │       ▼
    │   cacheLoader().asyncReload(key, oldValue, executor)
    │       │
    │       ▼
    │   你写的 reload() → loadFromRedisOnly(key)  // 只查 Redis，不回源
    │
    └── 缓存无值
            │
            ▼
        cacheLoader().asyncLoad(key, executor)
            │
            ▼
        你写的 load() → loadFromRedisOrSource(key, sourceLoader)
```

**`load()` vs `reload()` 的区别：**

| 方法 | 什么时候调用 | 做什么 |
|------|------------|--------|
| `load()` | 首次加载 / 过期重新加载 | 查 Redis + 回源（查 DB/RPC） |
| `reload()` | `refreshAfterWrite` 触发的异步刷新 | 只查 Redis，不回源；异常时保留旧值 |

---

## 源码追踪的小技巧

追踪框架源码时，容易"跳晕"。我的方法是：**每一步只追一个问题**。

| 你看到的 | 你的问题 | 操作 |
|---------|---------|------|
| `LoadingCache.get(key)` | 谁实现了 get？ | `Ctrl + Alt + B` |
| `mappingFunction()` | 谁实现了 mappingFunction？ | `Ctrl + Alt + B` |
| `newMappingFunction(loader)` | 里面做了什么？ | 点进去看 |
| `cacheLoader.load(key)` | cacheLoader 是谁？ | 回想构造时传入的参数 |

**不要一次跳多层**，一层一层追，每步确认"这一步的实现类/返回值是什么"，就不会乱。

---

## IDEA 查看源码的操作

| 操作 | 快捷键 / 路径 |
|------|-------------|
| 查看实现类 | 光标放接口上 → `Ctrl + Alt + B` |
| 下载源码 | 打开 class 文件 → 点击顶部 "Download sources" |
| 手动附加源码 | `File → Project Structure → Libraries → + Sources` |
| 源码 JAR 路径 | `~/.m2/repository/com/github/ben-manes/caffeine/caffeine/3.1.8/caffeine-3.1.8-sources.jar` |

---

## 总结：调用链的核心逻辑

1. **构造阶段**：`build(loader)` 把你的 `CacheLoader` 包装成 `Function`，存到缓存对象的成员变量
2. **运行阶段**：`get(key)` 调用 `computeIfAbsent`，未命中时取出 `Function` 执行
3. **回调你的代码**：`Function` 内部调用 `cacheLoader.load(key)`，走到你写的加载逻辑

**核心设计**：Caffeine 不直接持有你的 `CacheLoader`，而是把它包装成 `Function`，因为 `ConcurrentHashMap.computeIfAbsent` 需要的是 `Function` 类型。

这样设计的好处：你的加载逻辑和 Caffeine 的缓存管理逻辑解耦，Caffeine 只需要在合适的时机调用这个 `Function`，不关心里面做什么。

---

## 最后

源码追踪不是看一遍就懂的，建议你打开 IDEA，跟着这篇文章自己走一遍。

当你能不看文章，自己从 `get(key)` 追到 `load()`，就真正理解了框架回调业务代码的机制。
