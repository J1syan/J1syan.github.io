---
title: 'Spring Cloud 知识汇总'
description: '基于 spring-cloud-learning-lab 实际项目代码整理的 Spring Cloud 微服务架构知识汇总，涵盖 Nacos、Sentinel、Gateway、OpenFeign、Seata 等核心组件。'
pubDate: '2026-05-01'
category: '技术栈'
tags: ['Spring Cloud', 'Nacos', 'Sentinel', 'Gateway', 'OpenFeign', 'Seata', '微服务', '分布式']
---

# Spring Cloud 知识汇总

> 基于 spring-cloud-learning-lab 实际项目代码整理，参考 spring-cloud-demo 和 study-cloud 项目笔记

---

## 一、微服务架构基础

### 1.1 单体架构

**特点：** 所有功能都打包在一个应用中部署。

**优点：**
- 简单，一个项目搞定
- 容易部署，一次打包发布
- 容易测试，不用联调多个服务

**缺点：**
- 无法应对高并发，单实例处理能力有限
- 升级困难，一个小改动需要全量发布
- 技术栈单一，无法针对不同业务用不同语言

### 1.2 集群架构

集群是在单体基础上的扩展：

- **副本**：单体应用的复制，多跑几个一样的实例
- **集群**：多个应用实例同时运行，每个实例处理一部分请求
- **负载均衡**：将请求均匀分发给多个实例，避免单个实例过载
- **路由**：用户先访问一个域名，通过网关（负载均衡服务器），再分发到多个服务器

**为什么需要集群？**
- 数据库也需要集群，避免单台数据库压力过大
- 可以弹性扩缩容，根据流量增加或减少实例

### 1.3 分布式/微服务架构

**为什么还需要分布式？**
- 某个业务模块（如订单）需要频繁升级，分布式可以独立部署
- 不同模块可能用不同语言实现性能最佳（如直播功能用C++，订单用Java）
- 按业务拆分成多个微服务，可以独立开发、测试、部署、升级、扩展
- 数据库也可以按业务拆分，每个服务只管理自己的数据

### 1.4 部署架构演进

每个服务器不再部署一个完整应用，而是部署多个微服务模块：

- 对于访问量大的模块，部署多个实例
- **避免单点故障**：不要把同一个服务的所有实例都放在同一台服务器上
- **RPC远程调用**：服务部署在不同服务器上，需要通过HTTP+JSON等方式互相调用

### 1.5 注册中心

远程调用时，需要知道服务地址，并且知道哪台服务器可能挂掉。

- **服务注册**：每个微服务启动时，将自己的信息（IP、端口）注册到注册中心
- **服务发现**：微服务调用其他服务时，先从注册中心获取服务列表，再发起调用

### 1.6 配置中心

每个微服务都需要配置文件，配置可能经常变动：

- 统一管理所有配置的修改
- 统一推送配置变更，支持热更新

### 1.7 服务熔断

**服务雪崩**：某个服务挂掉后，依赖它的服务也会等待响应，最终整个系统崩溃。

**解决方案**：快速失败机制，某个服务挂掉时直接返回错误，不无限等待。

### 1.8 请求路由（网关）

网关识别请求后，也依赖服务发现：
- 用户请求中带有 `/order`，网关识别后分发到订单服务
- 用户请求中带有 `/product`，网关识别后分发到商品服务

### 1.9 分布式事务

有些业务需要同时操作多个数据库：
- 订单新增需要同时更新订单库和用户库（用户积分）
- 需要保证多个服务的操作要么全部成功，要么全部回滚

![一个操作涉及多个微服务](/images/一个操作涉及多个微服务.svg)

---

## 二、Nacos服务注册与发现

### 2.1 Nacos简介

Nacos是阿里巴巴开源的服务注册和配置中心，集成了服务注册发现、配置管理、服务管理等功能。

### 2.2 Nacos安装

使用Docker快速启动：

```yaml
# docker-compose.yml
services:
  nacos:
    image: nacos/nacos-server:v2.5.1
    container_name: learning-nacos
    environment:
      MODE: standalone
      NACOS_AUTH_ENABLE: "false"
    ports:
      - "8848:8848"
      - "9848:9848"
      - "9849:9849"
```

启动后访问 `http://127.0.0.1:8848/nacos/`，默认账号密码都是 `nacos`。

### 2.3 服务注册配置

在 `application.yml` 中配置Nacos：

```yaml
server:
  port: 9000

spring:
  application:
    name: service-product
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
```

**POM依赖**（在 `services` 父pom中统一管理）：
```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>
```

**启动类注解**：

```java
@EnableDiscoveryClient
@SpringBootApplication
public class ProductApplication {
    public static void main(String[] args) {
        SpringApplication.run(ProductApplication.class, args);
    }
}
```

> **注意**：`@EnableDiscoveryClient` 在较新版本中可以省略，Spring Cloud会自动识别Nacos注册中心。

### 2.4 服务注册关闭

如果只想消费服务而不注册自己，可以关闭注册：

```yaml
spring:
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
        register-enabled: false  # 关闭服务注册
```

> **注意**：需要显式声明 `false`，注解方式无法控制。

### 2.5 服务发现原理

服务发现的本质就是两步：

1. 从Nacos查实例列表
2. 拼URL发HTTP请求

调用链示例：

```
浏览器
  -> service-order:8000/order/createByDiscovery
  -> service-order 去 Nacos 查 service-product 实例
  -> Nacos 返回 192.168.1.105:9000
  -> service-order 拼出 http://192.168.1.105:9000/product/1
  -> RestTemplate 发 HTTP 请求
  -> service-product 返回商品 JSON
  -> service-order 把商品塞进订单里返回
```

核心代码：

```java
List<ServiceInstance> instances = discoveryClient.getInstances("service-product");
ServiceInstance instance = instances.get(0);  // 取第一个，无负载均衡
String url = "http://" + instance.getHost() + ":" + instance.getPort() + "/product/" + productId;
Product product = restTemplate.getForObject(url, Product.class);
```

---

## 三、服务调用方式演进

### 3.0 远程调用基本流程

![远程调用基本流程](/images/远程调用基本流程.svg)

远程调用的核心步骤：

![远程调用步骤](/images/远程调用步骤.svg)

### 3.1 DiscoveryClient + RestTemplate（手动方式）

最原始的手动调用方式，自己查实例、拼URL、发请求：

```java
@Override
public Order createByDiscoveryClient(Long productId, Long userId) {
    // 1. 去Nacos查service-product的可用实例
    List<ServiceInstance> instances = discoveryClient.getInstances("service-product");
    if (instances.isEmpty()) {
        throw new IllegalStateException("service-product has no available instance");
    }
    // 2. 取第一个实例（无负载均衡）
    ServiceInstance instance = instances.get(0);
    // 3. 手动拼URL
    String url = "http://" + instance.getHost() + ":" + instance.getPort() + "/product/" + productId;
    // 4. 发HTTP请求
    Product product = restTemplate.getForObject(url, Product.class);
    return buildOrder(product, userId);
}
```

**缺点**：
- 代码繁琐，每个远程调用都要写一遍
- 没有负载均衡，只能取第一个实例
- 业务代码耦合了服务发现的细节

### 3.2 LoadBalancer + RestTemplate（负载均衡方式）

通过 `@LoadBalanced` 注解，RestTemplate自动集成负载均衡：

**配置类**：

```java
@Configuration
public class RestTemplateConfig {
    @Bean
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

**调用代码**：

```java
@Override
public Order createByRestTemplate(Long productId, Long userId) {
    // 直接用服务名调用，LoadBalancer自动解析为真实IP+端口
    Product product = restTemplate.getForObject("http://service-product/product/" + productId, Product.class);
    return buildOrder(product, userId);
}
```

**工作原理**：
- `@LoadBalanced` 会给 RestTemplate 添加一个拦截器
- 拦截器发现URL是服务名（如 `http://service-product/...`），就去Nacos查实例
- 从实例列表中选择一个（默认轮询），替换成真实地址
- 再发HTTP请求

![客户端负载均衡与服务端负载均衡](/images/客户端负载均衡与服务端负载均衡.svg)

**测试负载均衡**：在IDEA中设置不同端口启动多个product实例，多次调用order接口可以看到返回的端口变化。

### 3.3 OpenFeign声明式调用

Feign将远程调用声明为Java接口，业务代码完全不需要拼URL：

![OpenFeign的远程调用](/images/OpenFeign的远程调用.svg)

**1. FeignClient接口**：

```java
@FeignClient(value = "service-product", fallback = ProductFeignClientFallback.class)
public interface ProductFeignClient {
    @GetMapping("/product/{id}")
    Product getProductById(@PathVariable("id") Long id);
}
```

**2. Fallback降级处理**：

![OpenFeign的Fallback](/images/OpenFeign的Fallback.svg)

```java
@Slf4j
@Component
public class ProductFeignClientFallback implements ProductFeignClient {
    @Override
    public Product getProductById(Long id) {
        // 降级返回兜底数据
        return new Product(id, "fallback-product", BigDecimal.ZERO, 0);
    }
}
```

**3. 请求拦截器（添加请求头）**：

![OpenFeign的拦截器](/images/OpenFeign的拦截器.svg)

```java
@Slf4j
@Component
public class XTokenRequestInterceptor implements RequestInterceptor {
    @Override
    public void apply(RequestTemplate template) {
        template.header("X-Token", UUID.randomUUID().toString());
        log.info("X-Token: {}", UUID.randomUUID().toString());
    }
}
```

**4. 业务调用**：

```java
@SentinelResource(value = "createOrder", blockHandler = "createOrderBlockHandler")
public Order createByFeign(Long productId, Long userId) {
    Product product = productFeignClient.getProductById(productId);
    return buildOrder(product, userId);
}
```

**5. 配置开启Feign+Sentinel集成**：

```yaml
feign:
  sentinel:
    enabled: true

logging:
  level:
    com.learning.order.feign: debug  # 打印Feign请求详情
```

**启动类开启Feign**：

```java
@EnableFeignClients
@EnableDiscoveryClient
@SpringBootApplication
public class OrderApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderApplication.class, args);
    }
}
```

**三种调用方式对比**：

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| DiscoveryClient | 清晰展示底层原理 | 代码繁琐，无负载均衡 | 学习原理 |
| @LoadBalanced | 自动负载均衡 | 仍需拼URL | 简单调用 |
| OpenFeign | 声明式接口，最简洁 | 有一定学习成本 | 生产环境推荐 |

---

## 四、Nacos配置中心

### 4.1 配置中心解决的问题

- 配置文件改动需要重启服务
- 多环境配置管理混乱（dev、test、prod）
- 配置分散在各服务中，难以统一管理

### 4.2 配置中心配置

在 `application.yml` 中连接Nacos配置中心：

![配置信息优先级](/images/配置信息优先级.svg)

```yaml
spring:
  application:
    name: service-order
  cloud:
    nacos:
      config:
        server-addr: 127.0.0.1:8848
        import-check:
          enabled: false  # 关闭配置导入检查
```

### 4.3 配置属性绑定

使用 `@ConfigurationProperties` 绑定自定义配置：

```java
@Data
@Component
@ConfigurationProperties(prefix = "order")
public class OrderProperties {
    String timeout;
    String comment;
}
```

本地配置文件：

```yaml
order:
  timeout: "3000"
  comment: "default order settings"
```

### 4.4 配置隔离

Nacos通过三个维度管理配置：

- **Namespace（命名空间）**：隔离不同环境（dev、test、prod）
- **Group（分组）**：代表某个微服务或某组服务
- **Data ID（配置ID）**：配置文件名称，对应具体配置

![Nacos数据隔离解决方案](/images/Nacos数据隔离解决方案.svg)

**多环境配置示例**（spring-cloud-demo参考）：

```yaml
spring:
  profiles:
    active: dev
  application:
    name: service-order
  cloud:
    nacos:
      config:
        namespace: ${spring.profiles.active:public}
---
# dev环境
spring:
  config:
    import:
      - nacos:common.yaml?group=order
      - nacos:database.yaml?group=order
    activate:
      on-profile: dev
---
# test环境
spring:
  config:
    import:
      - nacos:common.yaml?group=order
      - nacos:database.yaml?group=order
      - nacos:haha.yaml?group=order
    activate:
      on-profile: test
```

### 4.5 配置监听

可以监听Nacos配置变化：

```java
@Bean
ApplicationRunner applicationRunner(NacosConfigManager nacosConfigManager) {
    return args -> {
        ConfigService configService = nacosConfigManager.getConfigService();
        configService.addListener("service-order.yaml", "DEFAULT_GROUP", new Listener() {
            @Override
            public Executor getExecutor() {
                return Executors.newFixedThreadPool(4);
            }
            @Override
            public void receiveConfigInfo(String configInfo) {
                System.out.println("配置变化: " + configInfo);
            }
        });
    };
}
```

---

## 五、Sentinel限流与熔断

### 5.1 Sentinel简介

Sentinel通过流量控制、熔断降级、热点参数等多个维度保护服务稳定性。

![Sentinel架构原理](/images/Sentinel架构原理.svg)

**核心概念**：
- **资源**：需要保护的服务或方法
- **规则**：定义限流、熔断等策略
- **规则存储和推送**：通过Dashboard管理规则

### 5.2 基础配置

![Sentinel工作原理](/images/Sentinel工作原理.svg)

```yaml
spring:
  cloud:
    sentinel:
      transport:
        dashboard: 127.0.0.1:8080
      eager: false  # false表示启动时不初始化，true表示启动就连接Dashboard
```

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
</dependency>
```

启动Sentinel Dashboard（Docker）：

```yaml
sentinel:
    image: bladex/sentinel-dashboard:1.8.8
    container_name: learning-sentinel
    ports:
      - "8080:8858"
```

### 5.3 @SentinelResource注解

用于标记需要Sentinel保护的资源方法：

```java
// 普通方法限流/熔断
@SentinelResource(value = "createOrder", blockHandler = "createOrderBlockHandler")
public Order createByFeign(Long productId, Long userId) {
    Product product = productFeignClient.getProductById(productId);
    return buildOrder(product, userId);
}

// 对应的blockHandler方法，参数必须与原方法相同，最后加BlockException
public Order createOrderBlockHandler(Long productId, Long userId, BlockException e) {
    Order order = new Order();
    order.setId(0L);
    order.setUserId(userId);
    order.setNickname("blocked-user");
    order.setAddress("Sentinel blocked: " + e.getClass().getSimpleName());
    order.setTotalAmount(BigDecimal.ZERO);
    return order;
}
```

**@SentinelResource参数说明**：
- `value`：资源名称，在Dashboard中显示
- `blockHandler`：Sentinel规则触发时的处理方法（限流/熔断时调用）
- `fallback`：业务异常兜底方法（业务报错时调用）

### 5.4 热点参数限流

针对经常被访问的参数进行细粒度限流：

```java
@GetMapping("/order/seckill")
@SentinelResource(value = "seckill-order", fallback = "seckillFallback")
public Order seckill(@RequestParam(required = false) Long userId,
                     @RequestParam(defaultValue = "1000") Long productId) {
    return orderService.createByFeign(productId, userId == null ? 0L : userId);
}

public Order seckillFallback(Long userId, Long productId, Throwable throwable) {
    Order order = new Order();
    order.setId(0L);
    order.setUserId(userId);
    order.setAddress("fallback: " + throwable.getClass().getSimpleName());
    return order;
}
```

在Dashboard中配置热点参数规则，例如：

![Sentinel热点规则概述](/images/Sentinel热点规则概述.png)

![根据需求1配置热点规则](/images/根据需求1配置热点规则.png)
![根据需求2编辑热点规则](/images/根据需求2编辑热点规则.png)
![根据需求3配置热点规则](/images/根据需求3配置热点规则.png)
- userId参数，QPS限制为1
- VIP用户（特定userId），QPS限制为20
- 下架商品（特定productId），禁止访问

### 5.5 自定义异常处理

Sentinel默认的异常处理不符合业务需求，可以自定义：

![Sentinel异常处理](/images/Sentinel异常处理.svg)

```java
@Component
public class MyBlockExceptionHandler implements BlockExceptionHandler {
    private final ObjectMapper objectMapper;

    @Override
    public void handle(HttpServletRequest request,
                       HttpServletResponse response,
                       String resourceName,
                       BlockException e) throws Exception {
        response.setStatus(429);
        response.setContentType("application/json;charset=utf-8");
        PrintWriter writer = response.getWriter();
        writer.write(objectMapper.writeValueAsString(
            R.error(429, resourceName + " 被Sentinel限制: " + e.getClass())
        ));
        writer.flush();
        writer.close();
    }
}
```

### 5.6 流控规则

![Sentinel流控](/images/Sentinel流控.svg)

**三种策略**：

![Sentinel流控模式](/images/Sentinel流控模式.svg)

![Sentinel的流控模式](/images/Sentinel的流控模式.png)

- **直接**：直接对资源本身限流
- **关联**：关联资源达到阈值时，限制当前资源（如写请求过大时限制读请求）
- **链路**：不同调用链路对同一资源设置不同规则

**流控效果**：

![Sentinel流控效果](/images/Sentinel流控效果.svg)

![Sentinel设置流控阈值类型](/images/Sentinel设置流控阈值类型.png)

- **快速失败**：超过阈值直接拒绝
- **Warm Up**：预热模式，逐渐放开限流
- **匀速排队**：让请求以恒定速度通过

### 5.7 熔断降级

![断路器工作原理](/images/断路器工作原理.svg)

**断路器工作原理**：
1. **关闭状态**：正常调用服务
2. **打开状态**：失败次数达到阈值，停止调用，直接返回兜底数据
3. **半开状态**：等待一段时间后，允许少量请求通过
4. **恢复关闭**：如果半开状态下的请求成功，则认为服务恢复，关闭断路器

![配置异常数的熔断规则](/images/配置异常数的熔断规则.png)
![配置异常比例的熔断规则](/images/配置异常比例的熔断规则.png)
![配置慢调用比例的熔断规则](/images/配置慢调用比例的熔断规则.png)

**与OpenFeign的fallback配合**：

![有无熔断规则的比较](/images/有无熔断规则的比较.svg)

```yaml
feign:
  sentinel:
    enabled: true
```

当Feign调用失败时，先触发fallback降级，同时Sentinel统计失败次数，达到阈值后熔断。

---

## 六、Gateway网关

### 6.1 Gateway简介

为所有微服务提供统一的网关入口，功能包括：
- 统一入口
- 请求路由（依赖服务发现）
- 负载均衡
- 流量控制
- 身份认证
- 协议转换（HTTP → RPC）
- 安全防护

![Gateway的概述](/images/Gateway的概述.svg)

**Gateway vs GatewayMVC**：
- **Gateway**：基于WebFlux，支持异步非阻塞（推荐使用）
- **GatewayMVC**：基于Servlet，支持阻塞，已停止维护

### 6.2 核心组件

- **Route（路由）**：定义请求如何转发到哪个服务
- **Predicate（断言）**：匹配条件，决定请求是否匹配某条路由
- **Filter（过滤器）**：对请求和响应做处理

![Gateway路由的工作原理](/images/Gateway路由的工作原理.svg)

### 6.3 路由配置

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-route
          uri: lb://service-order          # lb:// 表示负载均衡
          predicates:
            - Path=/api/order/**           # 断言：路径匹配
          filters:
            - RewritePath=/api/order/?(?<segment>.*), /$\{segment}  # 路径重写
            - OnceToken=X-Response-Token,uuid  # 自定义过滤器
          order: 1                          # 优先级，越小越先匹配
        - id: product-route
          uri: lb://service-product
          predicates:
            - Path=/api/product/**
          filters:
            - RewritePath=/api/product/?(?<segment>.*), /$\{segment}
          order: 2
        - id: vip-demo-route
          uri: https://example.com
          predicates:
            - Path=/vip-demo
            - Vip=user,learning            # 自定义断言
          order: 99
```

**路径重写解释**：
- 请求 `/api/order/order/create` 
- RewritePath 去掉前缀 `/api/order`
- 实际转发到后端 `/order/create`

![RewritePath过滤器](/images/RewritePath过滤器.svg)

### 6.4 自定义谓词（Predicate）

自定义VIP断言，根据请求参数判断是否匹配路由：

```java
@Component
public class VipRoutePredicateFactory extends AbstractRoutePredicateFactory<VipRoutePredicateFactory.Config> {
    
    public VipRoutePredicateFactory() {
        super(Config.class);
    }

    // 定义 shortcutFieldOrder，对应配置中的 Vip=user,learning
    @Override
    public List<String> shortcutFieldOrder() {
        return List.of("param", "value");
    }

    // 匹配逻辑
    @Override
    public Predicate<ServerWebExchange> apply(Config config) {
        return exchange -> {
            ServerHttpRequest request = exchange.getRequest();
            String first = request.getQueryParams().getFirst(config.getParam());
            return StringUtils.hasText(first) && first.equals(config.getValue());
        };
    }

    public static class Config {
        private String param;   // 请求参数名，如 user
        private String value;   // 期望值，如 learning
        
        public String getParam() { return param; }
        public void setParam(String param) { this.param = param; }
        public String getValue() { return value; }
        public void setValue(String value) { this.value = value; }
    }
}
```

使用：请求 `http://gateway:7000/vip-demo?user=learning` 时匹配该路由。

### 6.5 全局过滤器（GlobalFilter）

对所有请求都生效的过滤器，常用于日志、鉴权等：

![Gateway过滤器](/images/Gateway过滤器.svg)

```java
@Component
public class RtGlobalFilter implements GlobalFilter, Ordered {
    private static final Logger log = LoggerFactory.getLogger(RtGlobalFilter.class);

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        long start = System.currentTimeMillis();
        log.info("gateway request start: {}", request.getURI());
        
        return chain.filter(exchange).doFinally(signalType ->
            log.info("gateway request end: {}, cost={}ms", request.getURI(), System.currentTimeMillis() - start)
        );
    }

    @Override
    public int getOrder() {
        return 0;  // 越小越先执行
    }
}
```

### 6.6 局部过滤器（GatewayFilter）

只对特定路由生效的过滤器，自定义OnceToken过滤器：

```java
@Component
public class OnceTokenGatewayFilterFactory extends AbstractNameValueGatewayFilterFactory {
    @Override
    public GatewayFilter apply(NameValueConfig config) {
        return (exchange, chain) -> chain.filter(exchange).then(Mono.fromRunnable(() -> {
            ServerHttpResponse response = exchange.getResponse();
            String value = "uuid".equalsIgnoreCase(config.getValue())
                    ? UUID.randomUUID().toString()
                    : config.getValue();
            response.getHeaders().add(config.getName(), value);
        }));
    }
}
```

配置使用：

```yaml
filters:
  - OnceToken=X-Response-Token,uuid  # config.name=X-Response-Token, config.value=uuid
```

**执行流程**：

```
请求进入 Gateway
  ↓
匹配路由（Predicate 判断 Path、Vip 等）
  ↓
合并 GlobalFilter + 当前路由的 GatewayFilter，按 order 排序
  ↓
pre阶段：请求转发前执行（chain.filter(exchange) 之前）
  ↓
转发到后端服务（负载均衡）
  ↓
后端响应回来
  ↓
post阶段：按相反方向执行（doFinally 或 then 中的逻辑）
  ↓
返回响应给前端
```

### 6.7 CORS配置

全局CORS配置：

```yaml
spring:
  cloud:
    gateway:
      globalcors:
        cors-configurations:
          '[/**]':
            allowed-origin-patterns: '*'
            allowed-headers: '*'
            allowed-methods: '*'
```

---

## 七、Seata分布式事务

### 7.1 为什么需要分布式事务

本地事务只能保证单个数据库的操作一致性。分布式系统中，一个业务可能涉及多个服务、多个数据库：
- 下订单服务操作 order_db
- 扣库存服务操作 storage_db
- 扣余额服务操作 account_db

需要保证这些操作要么全部成功，要么全部回滚。

### 7.2 Seata基础架构

![Seata演示示例分布式事务解决方案](/images/Seata演示示例分布式事务解决方案.png)

**三个核心角色**：

| 角色 | 缩写 | 职责 | 示例 |
|------|------|------|------|
| Transaction Coordinator | TC | 协调全局事务，管理分支事务状态 | Seata Server |
| Transaction Manager | TM | 开启和结束全局事务 | seata-business服务 |
| Resource Manager | RM | 管理分支事务，注册到TC | seata-storage/order/account |

**调用链**：

```
seata-business.purchase (TM)
  -> seata-storage.deduct (RM1)
  -> seata-order.create (RM2)
       -> seata-account.debit (RM3)
```

### 7.3 Seata配置

**application.yml**：

```yaml
spring:
  application:
    name: seata-account
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848

seata:
  enabled: true  # 启用Seata（lab项目中默认false，需改为true）
  tx-service-group: learning_tx_group  # 事务分组
```

**POM依赖**：

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-seata</artifactId>
</dependency>
```

### 7.4 AT模式工作原理（默认模式）

![Seata二阶提交协议](/images/Seata二阶提交协议.svg)

**一阶段**：
- 每个RM执行本地SQL
- 解析SQL，保存执行前后的数据镜像到 `undo_log` 表
- 提交本地事务
- 向TC报告分支事务状态

**二阶段（全部成功）**：
- TC通知所有RM提交，删除 `undo_log` 记录

**二阶段（某个失败，需要回滚）**：
- TC通知所有RM回滚
- RM根据 `undo_log` 生成反向SQL
- 执行反向SQL恢复数据
- 删除 `undo_log` 记录

### 7.5 四种事务模式

| 模式 | 特点 | 适用场景 |
|------|------|----------|
| **AT模式** | 自动管理，基于undo_log回滚，默认模式 | 大多数业务场景 |
| **XA模式** | 基于数据库本身事务，一阶段不提交，阻塞等待 | 对一致性要求极高的场景 |
| **TCC模式** | 自定义Confirm/Cancel操作，灵活控制回滚 | 非数据库操作（短信、邮件等） |
| **SAGA模式** | 结合消息队列，适用于长事务 | 审批流程、订单状态流转等 |

### 7.6 业务调用示例

**BusinessService（TM，全局事务入口）**：

```java
@Service
public class BusinessServiceImpl implements BusinessService {
    @Autowired
    private StorageFeignClient storageFeignClient;
    @Autowired
    private OrderFeignClient orderFeignClient;

    @GlobalTransactional  // 标记全局事务
    public void purchase(String userId, String commodityCode, int count) {
        // 1. 扣库存
        storageFeignClient.deduct(commodityCode, count);
        // 2. 下订单（内部会调用减余额）
        orderFeignClient.create(userId, commodityCode, count);
    }
}
```

如果任何一个分支事务失败，TC会协调所有已成功的分支回滚。

![Seata演示示例流程](/images/Seata演示示例流程.svg)

### 7.7 环境准备

**Docker启动MySQL和Seata**：

```yaml
mysql:
  image: mysql:8.0.32
  container_name: learning-mysql
  environment:
    MYSQL_ROOT_PASSWORD: root
    MYSQL_DATABASE: seata_lab
  ports:
    - "3306:3306"
  volumes:
    - ./docs/seata-lab.sql:/docker-entrypoint-initdb.d/01-seata-lab.sql:ro

seata:
  image: apache/seata-server:2.1.0
  container_name: learning-seata
  environment:
    SEATA_IP: 127.0.0.1
    SEATA_PORT: 8091
    STORE_MODE: file
  ports:
    - "8091:8091"
    - "7091:7091"
```

---

## 八、项目模块关系

### 8.1 整体架构

```
                    ┌─────────────┐
                    │   Gateway    │  端口: 7000
                    │  统一入口    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
      ┌───────▼──────┐ ┌──▼────────┐ ┌─▼──────────┐
      │ service-order │ │ service   │ │ seata-     │
      │  端口:8000   │ │ -product  │ │ business   │
      │  OpenFeign    │ │ 端口:9000 │ │ 端口:11004 │
      │  Sentinel     │ │           │ └───┬───────┘
      └───────┬──────┘ └───────────┘       │
              │                  ┌─────────┼─────────┐
              │                  │         │         │
      ┌───────▼──────┐ ┌────────▼┐ ┌──────▼┐ ┌──────▼──────┐
      │ Nacos Config  │ │ seata-  │ │seata- │ │ seata-      │
      │  Nacos Disc   │ │ storage │ │ order │ │ account     │
      └──────────────┘ │端口:11002│ │端口:  │ │ 端口:11001  │
                       └─────────┘ │ 11003 │ └─────────────┘
                                   └───────┘
```

### 8.2 依赖关系

```
spring-cloud-learning-lab (父POM)
├── model              # 公共实体类（Order, Product, R）
├── services (services父POM)
│   ├── service-product    # 商品服务：Nacos注册 + Sentinel
│   ├── service-order      # 订单服务：Nacos注册+发现 + OpenFeign + Sentinel + 配置中心
│   ├── seata-account      # 账户服务：Seata分布式事务
│   ├── seata-storage      # 库存服务：Seata分布式事务
│   ├── seata-order        # Seata订单服务：Seata分布式事务
│   └── seata-business     # 事务入口服务：@GlobalTransactional
└── gateway              # 网关服务：路由 + 谓词 + 过滤器
```

### 8.3 技术栈版本

| 技术 | 版本 |
|------|------|
| Java | 17 |
| Spring Boot | 3.3.4 |
| Spring Cloud | 2023.0.3 |
| Spring Cloud Alibaba | 2023.0.3.2 |
| Nacos | 2.5.1 |
| Sentinel | 1.8.8 |
| Seata | 2.1.0 |

---

## 九、核心概念对比总结

### 9.1 服务调用方式

| 方式 | 特点 | 负载均衡 | 适用场景 |
|------|------|----------|----------|
| DiscoveryClient | 手动查实例、拼URL | 无 | 学习原理 |
| RestTemplate + @LoadBalanced | 自动负载均衡 | 有（轮询） | 简单场景 |
| OpenFeign | 声明式接口 | 有（内置） | 生产推荐 |

### 9.2 Sentinel vs OpenFeign fallback

| 功能 | Sentinel blockHandler | OpenFeign fallback |
|------|----------------------|---------------------|
| 触发时机 | Sentinel规则触发（限流/熔断） | 服务调用失败/异常 |
| 处理内容 | 流量控制、熔断降级 | 服务不可用时的兜底 |
| 注解参数 | `blockHandler` | `fallback` |

### 9.3 Gateway组件

| 组件 | 作用 | 类比 |
|------|------|------|
| Route | 定义转发规则 | 路由器的一条规则 |
| Predicate | 匹配请求条件 | 判断条件（if） |
| GatewayFilter | 单条路由的过滤器 | 针对特定页面的处理 |
| GlobalFilter | 全局过滤器 | 所有页面都适用的处理 |

### 9.4 Seata角色

| 角色 | 对应 | 职责 |
|------|------|------|
| TC | Seata Server | 事务协调器，管理全局事务 |
| TM | 调用方服务 | 开启/提交/回滚全局事务 |
| RM | 被调用的服务 | 注册分支事务，执行本地事务 |

---

## 十、常用验证命令

### 10.1 基础接口

```bash
# 商品服务
curl 'http://localhost:9000/product/1'

# 订单服务 - 三种调用方式
curl 'http://localhost:8000/order/create?productId=1&userId=100'
curl 'http://localhost:8000/order/createByDiscovery?productId=1&userId=100'
curl 'http://localhost:8000/order/createByRestTemplate?productId=1&userId=100'
curl 'http://localhost:8000/order/create?productId=1&userId=100'

# 配置读取
curl 'http://localhost:8000/order/config'

# 秒杀接口（热点参数限流）
curl 'http://localhost:8000/order/seckill?userId=6&productId=666'

# 网关路由
curl -i 'http://localhost:7000/api/product/product/1'
curl -i 'http://localhost:7000/api/order/order/create?productId=1&userId=100'

# VIP断言测试
curl 'http://localhost:7000/vip-demo?user=learning'
```

### 10.2 服务管理命令

```bash
# 启动基础服务
docker compose up -d nacos sentinel

# 启动Seata相关服务
docker compose up -d mysql seata

# 编译项目
mvn -DskipTests compile

# 单独启动某个服务
mvn -pl services/service-product spring-boot:run
mvn -pl services/service-order spring-boot:run
mvn -pl gateway spring-boot:run
```

---

## 十一、复习要点

### 必答题

1. **注册中心解决什么问题？**
   答：服务之间互相不知道对方的地址，注册中心统一管理服务注册和发现，服务启动时注册自己，调用时从注册中心获取实例列表。

2. **Nacos中服务名和实例的关系？**
   答：服务名是一个逻辑标识（如service-product），一个服务名下可以有多个实例（不同IP+端口），实例是物理部署单元。

3. **RestTemplate、DiscoveryClient、OpenFeign的区别？**
   答：DiscoveryClient只负责查实例列表；RestTemplate负责发HTTP请求，配合@LoadBalanced可实现负载均衡；OpenFeign是声明式接口，把HTTP调用封装成Java方法，最简洁。

4. **Sentinel限流、熔断、热点参数的区别？**
   答：限流控制请求频率（QPS）；熔断是服务不稳定时自动停止调用，快速失败；热点参数是对特定参数值进行细粒度限流（如VIP用户更高阈值）。

5. **Gateway的Predicate、Filter、GlobalFilter的区别？**
   答：Predicate是匹配条件，决定请求走哪条路由；Filter是路由级别的过滤器，只对特定路由生效；GlobalFilter是全局过滤器，对所有路由生效。

6. **Seata的TC、TM、RM分别是谁？**
   答：TC是Seata Server，协调全局事务；TM是业务入口服务（如seata-business），开启和结束全局事务；RM是各个参与事务的微服务，管理各自的本地分支事务。

7. **项目各模块负责什么？**
   - model：公共实体类
   - service-product：商品服务
   - service-order：订单服务，演示三种调用方式
   - gateway：网关，统一入口和路由
   - seata-*：分布式事务演示
