# 数据集

[Kaggle](https://www.kaggle.com/datasets/mohankrishnathalla/sleep-health-and-daily-performance-dataset)

# 使用说明

详细流程见结课报告&PPT

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

| 技术/框架 | 技术类型 | 在本项目中的应用 |
| :--- | :--- | :--- |
| **Java** | 编程语言 | 全部 |
| **Spring Boot** | 应用框架 |  `FrontendApplication.java` 是启动入口。 |
| **Spring MVC** | Spring 子模块  | Web 框架 |
| **Spring JDBC (`JdbcTemplate`)** |Spring 子模块|  数据访问工具 |
| **Spring Cache (`@Cacheable`)** | Spring 子模块 | 缓存抽象 |
| **XGBoost4j** | 机器学习库| 调用 `XGBoost.loadModel` 加载模型，调用 `booster.predict` 进行预测。 |
| **Jackson** | JSON 处理库 | 在 `XgboostEvaluateService` 中读取 JSON 文件 |
| **SLF4J + Logback** | 日志门面+实现 | 在 `XgboostEvaluateService` 等类中使用。 |
| **Thymeleaf** | 模板引擎 | 服务端渲染 |
| **Maven（或 Gradle）** | 项目构建工具| 构筑项目环境 |

# 前端项目

详见[github](https://github.com/oQAQo233/EchartsCooperation)
