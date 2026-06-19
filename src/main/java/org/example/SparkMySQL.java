package org.example;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

public class SparkMySQL {
    public static void main(String[] args) {

        SparkSession spark = SparkSession.builder()
                .appName("HDFS-SparkSQL-MySQL")
                .config("spark.sql.shuffle.partitions", "3")
                .getOrCreate();
        // 有了SparkSession，SparkSQL就能用了。
        // 这里没有写 .master("local[*]")，说明运行模式完全由 spark-submit --master 决定，代码只负责逻辑，不绑定环境，更灵活。
        // appName 设置应用名称，会显示在 Spark Web UI 上
        // config("spark.sql.shuffle.partitions", "3") 是 SparkSQL 内部的一个调优配置：当执行 GROUP BY、JOIN 等会引发 Shuffle 的操作时，Shuffle 后的分区数默认就是 3。

        Dataset<Row> df = spark.read()
                .option("header", "true")
                .option("inferSchema", "true")
                .csv(SqlConfig.HDFS_PATH);
        // SparkSQL 里“数据输入”的体现，从HDFS读取CSV文件，存入一个Dataset<Row>中
        // option("header", "true")：指定 CSV 第一行为列名
        // option("inferSchema", "true")：让 Spark 自动推断每列的数据类型（如整数、浮点数等），否则全部默认为字符串
        // 随后将数据加载到一个 Dataset<Row>（即 DataFrame）中
        // HDFS_PATH指向HDFS上的一个 CSV 文件。

        System.out.println("===== 从 HDFS 读取的原始数据 =====");
        df.show();
        df.printSchema();
        // 在控制台打印前 20 行数据和表结构。

        df.createOrReplaceTempView(SqlConfig.VIEW_NAME);
        // 将 DataFrame (df) 注册为一个临时视图 sleep_table，之后就可以用标准 SQL 语句来查询它

        for (String tableName : SqlConfig.TABLE_LIST) {
            String sql = SqlConfig.SQL_MAP.get(tableName); // 取出当前表名所对的SQL语句

            System.out.println("===== 执行 SQL 并写入表: " + tableName + " =====");
            Dataset<Row> result = spark.sql(sql); // 执行SQL语句
            result.show(); // 展示执行结果

            result.write()
                    .mode("overwrite")
                    .format("jdbc")
                    .option("dbtable", tableName)
                    .option("url", SqlConfig.JDBC_URL)
                    .option("user", SqlConfig.JDBC_USER)
                    .option("password", SqlConfig.JDBC_PASSWORD)
                    .option("driver", SqlConfig.JDBC_DRIVER)
                    .save();
            System.out.println("结果已写入 MySQL 表 " + tableName); // 向 MySQL 写入
            // 写入模式为 overwrite：如果表已存在，会先删除再重建（或清空数据），然后插入本次结果。
            // 使用 JDBC 格式写入，明确指定 MySQL 的 JDBC 驱动类 com.mysql.cj.jdbc.Driver。
            // 填入 先前指定的数据库信息
            // .save() 触发实际写入动作。

            Dataset<Row> readBack = spark.read()
                    .format("jdbc")
                    .option("dbtable", tableName)
                    .option("url", SqlConfig.JDBC_URL)
                    .option("user", SqlConfig.JDBC_USER)
                    .option("password", SqlConfig.JDBC_PASSWORD)
                    .option("driver", SqlConfig.JDBC_DRIVER)
                    .load();
            // 从 MySQL 中读取修改的表，存入一个 Dataset<Row> 中

            System.out.println("===== 从 MySQL 读回验证: " + tableName + " =====");
            readBack.show();
            // 在控制台打印前 20 行数据，验证是否成功

        } // 遍历配置中所有的表，分别执行 SQL、写入 MySQL 并验证

        spark.stop(); // 关闭 SparkSession 连接
    }
}
