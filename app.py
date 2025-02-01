from set_api import get_member_of_index
from set_api import indexType

from util import min_max_scale
from util import adjust_date_based_on_day_v3
import time

import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import datetime
 
#################################
#################################

# ส่วน config #
__DEPLOY__ = True  # ถ้าจะเอาขึ้นไปบน streamlit ให้ใช้ True 

#################################
#################################

if(not __DEPLOY__):
  from TvDatafeed import TvDatafeed
  from TvDatafeed import Interval

def loaddata():
    obj = TvDatafeed()
    df = get_member_of_index(indexType.set50)
    basket = list(df['symbol'])

    while True:
        k = 0  
        try:  
            for i in basket:
                symbol = i   
                df = obj.get_hist(symbol=symbol,exchange='SET',interval=Interval.in_daily,n_bars=500)
                df.to_csv(f'ds/{symbol}.csv')  
                k+=1 
                #print(i,end=',')
                time.sleep(1)  
            if(k==len(basket)):
                #print('success')  
                return True
            break  
        except:
            #print('.',end='.')
            time.sleep(1)
            pass

def reportProcess():
    #%config InlineBackend.figure_format='retina'
    plt.rcParams['figure.dpi'] = 200  # หรือใช้ 300 สำหรับความละเอียดสูงกว่า

    df = get_member_of_index(indexType.set50)
    basket = list(df['symbol'])

    fig,_ = plt.subplots(figsize=(14,8))
    returnDs = []
    zone_near_52weekhigh = []

    count_q1 = 0
    count_q2 = 0
    count_q3 = 0
    count_q4 = 0
    new_min, new_max = -1, 1   # ช่วงใหม่
    

    start_date,stop_date = adjust_date_based_on_day_v3(st.session_state.selected_date)
    #print(start_date,stop_date)
    #start_date = '2024-01-30'
    #stop_date = '2025-01-30'  
    folder = 'ds/'

    for i in basket:
        symbol = i
        df = pd.read_csv(f'{folder}/{symbol}.csv')
        df['datetime'] = pd.to_datetime(df['datetime']).dt.date # เอาเวลาออกเช่น 09:00:00  
        df['datetime'] = pd.to_datetime(df['datetime'])  
        df = df[(df['datetime']<=stop_date) & (df['datetime']>=start_date)]  
        close = df[['close']]
        
        pmax = df['close'].max()
        pmin = df['close'].min()
        lastNDay = df['close'].tail(22).iloc[0]
        last = df.close.iloc[-1]  

        rocNday = (last/lastNDay)-1

        pct_chgMax = 1 - ((pmax - last)/last)
        pct_chgNDay = 1 - ((pmax - lastNDay)/lastNDay)
        scaled_value = min_max_scale(last, pmin, pmax, new_min, new_max)
        plt.scatter(rocNday,scaled_value,color='red',marker='*',s=100,label=i)
        returnDs.append(rocNday)

        if(rocNday>=0 and scaled_value>=0):
            count_q1+=1 
            if(scaled_value>=0.8):
                zone_near_52weekhigh.append(i)
                
        elif(rocNday<0 and scaled_value>=0):
            count_q2+=1 
        elif(rocNday<0 and scaled_value<0):
            count_q3+=1 
        elif(rocNday>=0 and scaled_value<0):
            count_q4+=1     
            
        plt.text(rocNday, scaled_value, i, fontsize=10, ha='right', va='bottom', color='black')  


    plt.xlim(min(returnDs)*1.1, max(returnDs)*1.1)  # ขยายขอบเขตของแกน X
    plt.ylim(-1.1, 1.1)  # ขยายขอบเขตของแกน X
    # เพิ่มเส้นแกน X และ Y
    plt.axhline(0, color='red',linewidth=0.8,linestyle='--')  # เส้นแกน Y ผ่านจุด 0
    plt.axvline(0, color='red',linewidth=0.8,linestyle='--')  # เส้นแกน X ผ่านจุด 0
    plt.axhline(0.8, color='green',linewidth=0.8,linestyle='--')  # เส้นแกน Y ผ่านจุด 0

    plt.title(f'Market Breadth 52WeekHigh-Low  {start_date}-{stop_date}')


    # ใส่จำนวนจุดในแต่ละ Quadrant
    plt.text((max(returnDs)*1.1)/2, 0.5, f"Q1: {count_q1}", fontsize=12, color='blue')  # Quadrant 1
    plt.text((min(returnDs)*1.1)/2, 0.5, f"Q2: {count_q2}", fontsize=12, color='blue')  # Quadrant 2
    plt.text((min(returnDs)*1.1)/2, -0.5, f"Q3: {count_q3}", fontsize=12, color='blue')  # Quadrant 3
    plt.text((max(returnDs)*1.1)/2, -0.5, f"Q4: {count_q4}", fontsize=12, color='blue')  # Quadrant 4
    plt.xlabel('ROC 22')
    plt.ylabel('52 Week high to low Range')
    plt.show()


    # แสดงกราฟใน Streamlit
    st.pyplot(fig)
    return True

def showreport():
    try:
       return reportProcess()
    except:
       return False   
    
def process_loaddata():
    try:
      return loaddata()
    except:
      return False  
    
def main():
    st.title("Market Breadth 52WeekHigh-Low")

    # สร้าง 2 คอลัมน์
    col1, col2 = st.columns(2)
    if col1.button("show report"):
      result = showreport()
      if(result):
        col1.success('load ข้อมูลสำเร็จ')
      else:
        col1.error('load ข้อมูลไม่สำเร็จ')  
    
    selected_date = col1.date_input("เลือกวันที่", datetime.date.today())
    if selected_date:
       st.session_state.selected_date = selected_date.strftime('%Y-%m-%d')
       #print(st.session_state.selected_date)

    if(not __DEPLOY__): 
        if col2.button("load new data"):
            with st.spinner("⏳ กำลังดำเนินการ... โปรดรอสักครู่"):
                result = process_loaddata()

            if result:
                col2.success('load ข้อมูลใหม่สำเร็จ')
            else:
                col2.error('load ข้อมูลใหม่ไม่สำเร็จ') 


if __name__ == "__main__":
    main()