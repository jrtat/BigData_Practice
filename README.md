# 数据集

[Kaggle](https://www.kaggle.com/datasets/mohankrishnathalla/sleep-health-and-daily-performance-dataset)

# 使用说明

详细流程见报告

# 技术栈（前端）

| 技术名 | 技术类型 | 
| :--- |  :--- |
| jQuery | JavaScript 工具库 | 
| ECharts |  JavaScript 绘图库 | 
| DataTables |  JavaScript 表格插件 | 
| Thymeleaf |  后端模板引擎 | 
| Bootstrap | CSS 样式框架 |
| Bootstrap Icons | 图标字体资源 |

# 技术栈（后端）

| 技术/框架 | 类型 | 在本项目中的应用 |
| :--- | :--- | :--- |
| **Java** | 编程语言 | 所有 `.java` 文件。 |
| **Spring Boot** | 应用框架 |  `FrontendApplication.java` 是启动入口。 |
| **Spring MVC** | Web 框架（Spring 子模块）  | 使用 `@Controller`、`@GetMapping`、`@PostMapping`、`@ResponseBody` 等注解。 |
| **Spring JDBC (`JdbcTemplate`)** | 数据访问工具（Spring 子模块）| 几乎每个 `Service` 类（如 `SleepHealthService`、`ComparisonService`）都在用它执行查询和聚合。 |
| **Spring Cache (`@Cacheable`)** | 缓存抽象（Spring 子模块） | `ComparisonService.getComparisonData()` 方法上标注了 `@Cacheable`。 |
| **XGBoost4j** | 机器学习库（Java 版 XGBoost）| `XgboostService.java` 中调用 `XGBoost.loadModel` 加载模型，用 `booster.predict` 进行预测。 |
| **Jackson** | JSON 处理库 | `@JsonProperty` 注解、`ObjectMapper` 的使用（在 `XgboostEvaluateService` 中读取 JSON 文件）。 |
| **SLF4J + Logback** | 日志门面 + 实现 | `LoggerFactory.getLogger(...)` 在 `XgboostEvaluateService` 等类中使用。 |
| **Thymeleaf** | 模板引擎（服务端渲染）| Controller 方法返回 `"pages/xxx"` 字符串，对应 `templates/pages/xxx.html` 模板文件。 |
| **Maven（或 Gradle）** | 项目构建工具（未直接显示，但隐含）| 项目根目录应该有 `pom.xml` 或 `build.gradle` 文件（未贴出，但标准 Spring Boot 项目会使用）。 |

# 前端项目

详见[github](https://github.com/oQAQo233/EchartsCooperation)
