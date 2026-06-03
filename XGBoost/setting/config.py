data_path = "sleep_health_dataset.csv"

model_dict = {
    "cognitive_performance_score" :
        {"task_type": "regression", "model_name": "cognitive_performance_score"},
    "sleep_disorder_risk" :
        {"task_type": "regression", "model_name": "sleep_disorder_risk"},
    "sleep_duration_hrs" :
        {"task_type": "regression", "model_name": "sleep_duration_hrs"},
    "sleep_latency_mins" :
        {"task_type": "regression", "model_name": "sleep_latency_mins"},
    "deep_sleep_percentage" :
        {"task_type": "regression", "model_name": "deep_sleep_percentage"},
    "rem_percentage" :
        {"task_type": "regression", "model_name": "rem_percentage"},
    "felt_rested" :
        {"task_type": "classification", "model_name": "felt_rested"},
    "mental_health_condition" :
        {"task_type": "classification", "model_name": "mental_health_condition"},
    "occupation" :
        {"task_type": "classification", "model_name": "occupation"},
} # 这是拿model命名的

mask_feature_list = {
    "cognitive_performance_score":
        [
         # 可能影响睡眠质量的环境因素
         'room_temperature_celsius', 'occupation', 'country', 'season', 'day_type', 'shift_work',
         # 可能影响睡眠质量的行为因素
         'caffeine_mg_before_bed', 'alcohol_units_before_bed',
         'screen_time_before_bed_mins', 'steps_that_day',
         'nap_duration_mins', 'work_hours_that_day', 'exercise_day', 'sleep_aid_used',
         # 明显目标列
         'sleep_disorder_risk'],
    "sleep_disorder_risk" :
        [
         # 可能影响睡眠质量的环境因素
         'room_temperature_celsius', 'occupation', 'country', 'season', 'day_type', 'shift_work',
         # 可能影响睡眠质量的行为因素
         'caffeine_mg_before_bed', 'alcohol_units_before_bed',
         'screen_time_before_bed_mins', 'steps_that_day',
         'nap_duration_mins', 'work_hours_that_day', 'exercise_day', 'sleep_aid_used',
         # 明显目标列
         'cognitive_performance_score'],
    "sleep_duration_hrs":
        [
         # 睡眠相关指标
         'sleep_quality_score', 'rem_percentage', 'deep_sleep_percentage',
         'sleep_latency_mins', 'wake_episodes_per_night', 'weekend_sleep_diff_hrs',
         'felt_rested',
         # 明显目标列
         'cognitive_performance_score', 'sleep_disorder_risk'],
    "sleep_latency_mins":
        [
         # 睡眠相关指标
         'sleep_duration_hrs', 'sleep_quality_score', 'rem_percentage', 'deep_sleep_percentage',
         'wake_episodes_per_night', 'weekend_sleep_diff_hrs', 'felt_rested',
         # 明显目标列
         'cognitive_performance_score', 'sleep_disorder_risk'],
    "deep_sleep_percentage" :
        [
         # 睡眠相关指标
         'sleep_duration_hrs', 'sleep_quality_score', 'rem_percentage',
         'sleep_latency_mins', 'wake_episodes_per_night', 'weekend_sleep_diff_hrs', 'felt_rested',
         # 明显目标列
         'cognitive_performance_score', 'sleep_disorder_risk'],
    "rem_percentage" :
        [
         # 睡眠相关指标
         'sleep_duration_hrs', 'sleep_quality_score', 'deep_sleep_percentage',
         'sleep_latency_mins', 'wake_episodes_per_night', 'weekend_sleep_diff_hrs', 'felt_rested',
         # 明显目标列
         'cognitive_performance_score', 'sleep_disorder_risk'],
    "felt_rested":
        [
         # 睡眠相关指标
         'sleep_duration_hrs', 'sleep_quality_score', 'rem_percentage', 'deep_sleep_percentage',
         'sleep_latency_mins', 'wake_episodes_per_night', 'weekend_sleep_diff_hrs',
         # 明显目标列
         'cognitive_performance_score', 'sleep_disorder_risk'],
    "mental_health_condition":
        ['cognitive_performance_score', 'sleep_disorder_risk', 'felt_rested'],
    "occupation":
        ['cognitive_performance_score', 'sleep_disorder_risk', 'felt_rested'],
} # 这是拿target_name命名的

id_column = [
    'person_id'  # 作为唯一标识列，不进行处理
]

numeric_feature = [
    # 个人身体指标/特质
    'age', 'heart_rate_resting_bpm', 'stress_score', 'bmi',
    # 睡眠相关指标
    'sleep_duration_hrs', 'sleep_quality_score',
    'rem_percentage', 'deep_sleep_percentage',
    'sleep_latency_mins', 'wake_episodes_per_night',
    'weekend_sleep_diff_hrs',
    # 可能影响睡眠质量的环境因素
    'room_temperature_celsius',
    # 可能影响睡眠质量的行为因素
    'caffeine_mg_before_bed', 'alcohol_units_before_bed',
    'screen_time_before_bed_mins', 'steps_that_day',
    'nap_duration_mins', 'work_hours_that_day',
    # 明显目标列
    'cognitive_performance_score',
] # 数值特征列（需要归一化）

categorical_feature = [
    # 个人身体指标/特质
    'gender', 'mental_health_condition', 'chronotype',
    # 睡眠相关的指标
    'felt_rested',
    # 可能影响睡眠质量的环境因素
    'occupation', 'country', 'season',
    'day_type', 'shift_work',
    # 可能影响睡眠质量的行为因素
    'exercise_day', 'sleep_aid_used',
    # 明显目标列
    'sleep_disorder_risk', # 这个严格来说是有序分类
] # 分类特征列（转为 category 类型）

cat_order_map = {
    'gender': ['男', '女', '其他'],                      # 对应 value 0,1,2
    'mental_health_condition': ['Healthy', 'Anxiety', 'Depression', 'Both'],
    'chronotype': ['Morning', 'Evening', 'Neutral'],
    'felt_rested': ['未恢复', '休息好了'],
    'occupation': ['Student', 'Manager', 'Doctor', 'Teacher', 'Nurse', 'Sales',
                   'Lawyer', 'Software Engineer', 'Driver', 'Freelancer', 'Retired', 'Homemaker'],
    'country': ['Canada', 'USA', 'UK', 'Japan', 'Brazil', 'Italy', 'India', 'Germany',
                'South Korea', 'Australia', 'France', 'Sweden', 'Netherlands', 'Spain', 'Mexico'],
    'season': ['Spring', 'Summer', 'Autumn', 'Winter'],
    'day_type': ['Weekday', 'Weekend'],
    'shift_work': ['否', '是'],
    'exercise_day': ['否', '是'],
    'sleep_aid_used': ['否', '是'],
} # Java 端完全一致的类别顺序