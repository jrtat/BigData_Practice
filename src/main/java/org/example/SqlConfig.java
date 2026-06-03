package org.example;

import java.util.*;

public class SqlConfig {

    public static final String HDFS_PATH = "hdfs://namenode:9000/user/hadoop/sleep_data/sleep_health_dataset.csv";
    // 文件在HDFS中的路径
    public static final String VIEW_NAME = "sleep_table";
    // 创建的临时视图的名字（好像没什么用）

    public static final String JDBC_URL = "jdbc:mysql://192.168.17.1:3306/sleep_db?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true";
    // 指定连接的 MySQL 数据库为 sleep_db
    public static final String JDBC_USER = "spark";
    // 指定 JDBC 用户名（Mysql中创建的用户）
    public static final String JDBC_PASSWORD = "Spark5523";
    // 指定 JDBC 密码（Mysql中创建的密码）
    public static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    // 指定 JDBC 驱动（驱动名）

    public static final List<String> TABLE_LIST = new ArrayList<>(); // 表名列表
    public static final Map<String, String> SQL_MAP = new LinkedHashMap<>(); // <表名, SQL语句>
    static {

        // ========== SleepStructure 子表 ==========
        SQL_MAP.put("sub_sleep_structure",
                "SELECT person_id, age, gender, chronotype, mental_health_condition, " +
                        "sleep_duration_hrs, rem_percentage, deep_sleep_percentage, " +
                        "sleep_quality_score, wake_episodes_per_night " +
                        "FROM sleep_table");

        // ========== SleepHealth 子表 ==========
        SQL_MAP.put("sub_sleep_basic",
                "SELECT person_id, age, gender, occupation, bmi, country " +
                        "FROM sleep_table");

        SQL_MAP.put("sub_sleep_metrics",
                "SELECT person_id, sleep_duration_hrs, sleep_quality_score, " +
                        "rem_percentage, deep_sleep_percentage, sleep_latency_mins, wake_episodes_per_night " +
                        "FROM sleep_table");

        // ========== SleepHealthService 子表 ==========
        SQL_MAP.put("sub_sleep_health",
                "SELECT person_id, age, occupation, chronotype, sleep_disorder_risk, " +
                        "sleep_duration_hrs, sleep_quality_score, stress_score " +
                        "FROM sleep_table");

        SQL_MAP.put("sub_sleep_behavior",
                "SELECT person_id, caffeine_mg_before_bed, alcohol_units_before_bed, " +
                        "screen_time_before_bed_mins, exercise_day, steps_that_day, nap_duration_mins, " +
                        "work_hours_that_day, sleep_aid_used " +
                        "FROM sleep_table");

        SQL_MAP.put("sub_sleep_environment",
                "SELECT person_id, stress_score, heart_rate_resting_bpm, room_temperature_celsius, " +
                        "weekend_sleep_diff_hrs, shift_work, cognitive_performance_score, " +
                        "sleep_disorder_risk, felt_rested " +
                        "FROM sleep_table");

        // ========== 可提前聚合的视图 ==========
        SQL_MAP.put("agg_dashboard_stats",
                "SELECT COUNT(*) AS totalRecords, " +
                        "AVG(sleep_duration_hrs) AS avgSleepDuration, " +
                        "AVG(sleep_quality_score) AS avgSleepQuality, " +
                        "AVG(stress_score) AS avgStressScore " +
                        "FROM sleep_table");

        SQL_MAP.put("agg_disorder_risk",
                "SELECT sleep_disorder_risk AS name, COUNT(*) AS value " +
                        "FROM sleep_table GROUP BY sleep_disorder_risk");

        SQL_MAP.put("agg_quality_by_chronotype",
                "SELECT chronotype AS name, AVG(sleep_quality_score) AS value " +
                        "FROM sleep_table GROUP BY chronotype");

        // ========== MedicalService 子表 ==========
        SQL_MAP.put("sub_bedtime_behavior",
                "SELECT occupation AS groupName, " +
                        "COUNT(*) AS peopleCount, " +
                        "ROUND(AVG(screen_time_before_bed_mins), 1) AS avgScreen, " +
                        "ROUND(AVG(sleep_latency_mins), 1) AS avgLatency, " +
                        "ROUND(AVG(caffeine_mg_before_bed), 1) AS avgCaffeine, " +
                        "ROUND(AVG(alcohol_units_before_bed), 1) AS avgAlcohol " +
                        "FROM sleep_table GROUP BY occupation HAVING peopleCount > 5");

        // ========== MapService 子表 ==========
        SQL_MAP.put("sub_country_distribution",
                "SELECT country AS name, COUNT(*) AS value, " +
                        "AVG(sleep_duration_hrs) AS avgDuration, " +
                        "AVG(sleep_quality_score) AS avgQuality " +
                        "FROM sleep_table GROUP BY country ORDER BY value DESC");

        // ========== DistributionService 子表 ==========
        SQL_MAP.put("sub_distribution_data",
                "SELECT age, gender, occupation, bmi, country, " +
                        "sleep_duration_hrs, sleep_quality_score, rem_percentage, " +
                        "deep_sleep_percentage, sleep_latency_mins, wake_episodes_per_night " +
                        "FROM sleep_table");

        // ========== ComparisonService 子表 ==========
        SQL_MAP.put("sub_comparison_data",
                "SELECT age, gender, occupation, bmi, country, " +
                        "sleep_duration_hrs, sleep_quality_score, rem_percentage, " +
                        "deep_sleep_percentage, sleep_latency_mins, wake_episodes_per_night " +
                        "FROM sleep_table");

        // ========== HeatmapService 子表 ==========
        SQL_MAP.put("sub_heatmap_data",
                "SELECT sleep_duration_hrs, sleep_quality_score, stress_score, " +
                        "room_temperature_celsius, weekend_sleep_diff_hrs, sleep_latency_mins, " +
                        "wake_episodes_per_night, bmi, heart_rate_resting_bpm, age " +
                        "FROM sleep_table");

        // SQL_MAP.put("sleep_health_dataset", "SELECT * FROM sleep_table");

        TABLE_LIST.addAll(SQL_MAP.keySet()); // 初始化 TABLE_LIST
    }
}