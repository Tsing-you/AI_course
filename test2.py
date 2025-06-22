import os
import random
from datetime import datetime, timedelta

import numpy as np

def generate_dummy_data_with_weekday(file_path, num_rows=107):
    """
    生成示例数据并保存为CSV文件，格式仿照hartData.csv，包含日期对应的“周几”，使用gbk编码。
    
    参数:
        file_path (str): 生成的文件路径
        num_rows (int): 生成的行数，默认为15
    """
    # 创建文件夹（如果不存在）
    # os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # 生成示例数据
    with open(file_path, 'w', encoding='gbk') as f:
        start_time = datetime(2025, 6, 6, 18, 41, 8)  # 起始时间
        base_heart_rate = 82  # 基础心率
        trend = 0  # 趋势项（模拟心率变化趋势）
        seasonal = 0  # 周期项（模拟心率的周期性变化）
        
        for i in range(num_rows):
            # 生成时间戳（每行增加2秒）
            current_time = start_time + timedelta(seconds=59 * i)
            timestamp_str = current_time.strftime("%Y.%m.%d %H:%M:%S.%f")[:-3]  # 格式化为"YYYY.MM.DD HH:MM:SS.sss"
            
            # 获取日期对应的星期几
            weekday_str = current_time.strftime("%A")  # 获取星期几（英文）
            # 将英文星期几转换为中文
            weekday_map = {
                "Monday": "周一心率",
                "Tuesday": "周一心率",
                "Wednesday": "周一心率",
                "Thursday": "周一心率",
                "Friday": "周一心率",
                "Saturday": "周一心率",
                "Sunday": "周一心率"
            }
            weekday_str = weekday_map.get(weekday_str, weekday_str)
            
            # 生成更接近真实的心率数据
            # 基础心率 + 随机波动 + 趋势项 + 周期项
            random_noise = random.gauss(0, 5)  # 随机噪声（正态分布）
            trend = 0.03 * i  # 模拟心率的长期趋势
            seasonal = 10 * np.sin(2 * np.pi * i / 70)  # 模拟心率的周期性变化
            heart_rate = int(base_heart_rate + random_noise + trend + seasonal)
            
            # 确保心率在合理范围内
            heart_rate = max(60, min(120, heart_rate)) 
            
            # # 在heart_rate生成代码后添加血氧生成逻辑
            # base_oxygen = 98  # 基础血氧值
            # oxygen_noise = random.gauss(0, 3)  # 更小的波动（正态分布）

            # # 与心率负相关（心率升高时血氧略降）
            # oxygen_corr = (base_heart_rate - heart_rate) * 0.1
            # blood_oxygen = base_oxygen + oxygen_noise + oxygen_corr

            # if blood_oxygen>= 98:
            #     blood_oxygen=random.randint(97, 100)

            # # 限制在合理范围并取整
            # blood_oxygen = int(round(max(90, min(100, blood_oxygen))))

            # 改进后的血氧生成逻辑（替换上述三行）
            base_oxygen = 97.5
            oxygen_noise = random.gauss(0, 2.5)  # 缩小随机波动幅度

            # 建立更符合生理特征的负相关（非线性关系）
            hr_deviation = heart_rate - base_heart_rate
            if hr_deviation > 20:  # 当心率显著升高时（>102）
                oxygen_corr = -0.2 * hr_deviation  # 加强负相关
            elif hr_deviation > 10:  # 心率中等升高（92-102）
                oxygen_corr = -0.1 * hr_deviation
            else:  # 正常波动范围
                oxygen_corr = -0.05 * hr_deviation

            # 引入与心率相同的周期项（但相位相反）
            oxygen_seasonal = -0.5 * np.sin(2 * np.pi * i / 70)  # 幅度减半且相位相反

            blood_oxygen = int(base_oxygen + oxygen_noise + oxygen_corr + oxygen_seasonal)

            blood_oxygen = max(90, min(100, round(blood_oxygen)))

            # 修改数据行格式（添加血氧列）
            line = f"{timestamp_str} {weekday_str}, {heart_rate}, {blood_oxygen}\n\n"
            
            # 写入文件
            f.write(line)
    
    print(f"生成文件成功：{file_path}")

if __name__ == "__main__":
    # 指定生成的文件路径
    output_file = "hartData_4.csv"
    
    # 生成示例数据
    generate_dummy_data_with_weekday(output_file)