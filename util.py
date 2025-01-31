def min_max_scale(value, old_min, old_max, new_min, new_max):
    """
    แปลงค่าจากช่วงเดิมไปยังช่วงใหม่โดยใช้ Min-Max Scaling

    Parameters:
    value (float): ค่าที่ต้องการแปลง
    old_min (float): ค่าต่ำสุดของช่วงเดิม
    old_max (float): ค่าสูงสุดของช่วงเดิม
    new_min (float): ค่าต่ำสุดของช่วงใหม่
    new_max (float): ค่าสูงสุดของช่วงใหม่

    Returns:
    float: ค่าที่ถูกแปลงให้อยู่ในช่วงใหม่
    """
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


from datetime import datetime, timedelta

def adjust_date_based_on_day_v3(t):
    today = datetime.strptime(t, '%Y-%m-%d')
    LDate = today - timedelta(days=365) 
    return LDate.strftime('%Y-%m-%d'),today.strftime('%Y-%m-%d') # ส่งกลับเป็นสตริงในรูปแบบ YYYY-MM-DD

def adjust_date_based_on_day_v2():
    today = datetime.now()
    LDate = today - timedelta(days=365) 
    return LDate.strftime('%Y-%m-%d'),today.strftime('%Y-%m-%d') # ส่งกลับเป็นสตริงในรูปแบบ YYYY-MM-DD

def adjust_date_based_on_day_v1():
    today = datetime.now()
    #today = datetime(2025, 2, 1, 15, 55, 19, 974539)
    weekday = today.weekday()

    if weekday == 0:  # วันจันทร์
        result_date = today - timedelta(days=3)  # วันศุกร์ที่ผ่านมา
    elif weekday in [5, 6]:  # วันเสาร์หรือวันอาทิตย์
        result_date = today - timedelta(days=weekday-4)  # วันศุกร์ที่ผ่านมา
    else:  # วันธรรมดาอื่นๆ
        result_date = today - timedelta(days=1)  # ลดลงหนึ่งวัน

    LDate = result_date - timedelta(days=365) 
    return LDate.strftime('%Y-%m-%d'),result_date.strftime('%Y-%m-%d') # ส่งกลับเป็นสตริงในรูปแบบ YYYY-MM-DD