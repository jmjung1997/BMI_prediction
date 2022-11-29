import pandas as pd
import openpyxl

#2022-07-14~2022-10-05
#2022-10-09 기준 데이터 크기 84*8*322

#3D-Data 엑셀 읽기
df_Height=pd.read_excel('Data.xlsx',sheet_name='Height')
df_Weight=pd.read_excel('Data.xlsx',sheet_name='Weight')
df_Step=pd.read_excel('Data.xlsx',sheet_name='Step_Count')
df_Burned=pd.read_excel('Data.xlsx',sheet_name='Burned_Calorie')
df_Eat=pd.read_excel('Data.xlsx',sheet_name='Eat_Calorie')
df_Sleep=pd.read_excel('Data.xlsx',sheet_name='Sleep_Time')
df_BMI=pd.read_excel('Data.xlsx',sheet_name='BMI')
df_Label=pd.read_excel('Data.xlsx',sheet_name='BMI_Label')

#ID 정보 엑셀 읽기
df_ID=pd.read_excel('ID.xlsx',sheet_name='ID')
ID=df_ID['ID']

Countdf=9 # 읽는 df 개수 + 1(이름)
cols=len(df_ID)*(len(df_ID.columns)-1)

df_for_write_array=[[0 for j in range(Countdf)] for i in range(cols)]


for i in range(len(ID)):
    print("I : ", i)
    for j in range(len(df_ID.columns)-1):
        df_for_write_array[i*84+j][0]=ID[i]
        df_for_write_array[i*84+j][1]=df_Height[ID[i]][j]
        df_for_write_array[i*84+j][2]=df_Weight[ID[i]][j]
        df_for_write_array[i*84+j][3]=df_Step[ID[i]][j]
        df_for_write_array[i*84+j][4]=df_Burned[ID[i]][j]
        df_for_write_array[i*84+j][5]=df_Eat[ID[i]][j]
        df_for_write_array[i*84+j][6]=df_Sleep[ID[i]][j]
        df_for_write_array[i*84+j][7]=df_BMI[ID[i]][j]
        df_for_write_array[i*84+j][8]=df_Label[ID[i]][j]

# df_for_write_temp={
#     "Name":df_for_write_array[0:][0],
#     "Height":df_for_write_array[0:][1],
#     "Weight":df_for_write_array[0:][2],
#     "Step_Count":df_for_write_array[0:][3],
#     "Burned_Calorie":df_for_write_array[0:][4],
#     "Eat_Calorie":df_for_write_array[0:][5],
#     "Sleep_Time":df_for_write_array[0:][6],
#     "BMI":df_for_write_array[0:][7],
#     "BMI_Label":df_for_write_array[0:][8]}

#엑셀에 쓰는 부분
df_for_write=pd.DataFrame(df_for_write_array)
df_for_write.to_excel("Result.xlsx",sheet_name="Data")
