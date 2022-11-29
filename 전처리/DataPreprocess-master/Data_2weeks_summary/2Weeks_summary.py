import pandas as pd
import openpyxl

df_weight=pd.read_excel('Data_2Weeks.xlsx',sheet_name='Weight')
df_step=pd.read_excel('Data_2Weeks.xlsx',sheet_name='Step_Count')
df_burn=pd.read_excel('Data_2Weeks.xlsx',sheet_name='Burned_Calorie')
df_eat=pd.read_excel('Data_2Weeks.xlsx',sheet_name='Eat_Calorie')
df_sleep=pd.read_excel('Data_2Weeks.xlsx',sheet_name='Sleep_Time')
df_BMI=pd.read_excel('Data_2Weeks.xlsx',sheet_name='BMI')
df_height=pd.read_excel('Data_2Weeks.xlsx',sheet_name='Height')

#ID 정보 엑셀 읽기
df_ID=pd.read_excel('ID.xlsx',sheet_name='ID')
ID=df_ID['ID']

Countdf=9 # 읽는 df 개수 + 2(이름, 라벨)
cols=len(df_ID)*(len(df_ID.columns)-1)

df_for_write_array_temp=[[0 for j in range(Countdf)] for i in range(cols)]
for i in range(len(ID)):
    for j in range(len(df_ID.columns)-1):
        df_for_write_array_temp[i*84+j][0]=ID[i]
        df_for_write_array_temp[i*84+j][1]=df_weight[ID[i]][j]
        df_for_write_array_temp[i*84+j][2]=df_BMI[ID[i]][j]
        df_for_write_array_temp[i*84+j][3]=df_step[ID[i]][j]
        df_for_write_array_temp[i*84+j][4]=df_burn[ID[i]][j]
        df_for_write_array_temp[i*84+j][5]=df_eat[ID[i]][j]
        df_for_write_array_temp[i*84+j][6]=df_sleep[ID[i]][j]
        df_for_write_array_temp[i*84+j][7]=df_height[ID[i]][j]

print(df_for_write_array_temp.shape())

def sum_columns(array,index1,index2):
    sum=0
    for i in range(14):
        # print("index1 : ",index1,"index2+i",index2+i)
        sum=sum+array[index1+i][index2]
    return sum/14

def label(weight_1day, weight_14day):
    if(weight_1day > weight_14day):
        return -1
    elif (weight_1day < weight_14day):
        return 1
    elif weight_14day==weight_1day:
        return 0

df_for_write_array=[[0 for j in range(Countdf)] for i in range(int(len(df_for_write_array_temp)/14))]
for j in range(int(cols / 84)):
    for i in range(84):  # 0~83
        if (i % 72 == 0):
            break
        df_for_write_array[72*j+i][0] = df_for_write_array_temp[84 * j + i][0]  # ID
        df_for_write_array[72*j+i][1] = sum_columns(df_for_write_array_temp, 84 * j + i, 1)  # weight
        df_for_write_array[72*j+i][2] = sum_columns(df_for_write_array_temp, 84 * j + i, 2)  # BMI
        df_for_write_array[72*j+i][3] = sum_columns(df_for_write_array_temp, 84 * j + i, 3)  # step
        df_for_write_array[72*j+i][4] = sum_columns(df_for_write_array_temp, 84 * j + i, 4)  # burn
        df_for_write_array[72*j+i][5] = sum_columns(df_for_write_array_temp, 84 * j + i, 5)  # eat
        df_for_write_array[72*j+i][6] = sum_columns(df_for_write_array_temp, 84 * j + i, 6)  # sleep
        df_for_write_array[72*j+i][7] = sum_columns(df_for_write_array_temp, 84 * j + i, 7)  # height
        df_for_write_array[72*j+i][8] = label(df_for_write_array_temp[84 * j + i][1], df_for_write_array_temp[84 * j - 1][1])

#엑셀에 쓰는 부분
df_for_write=pd.DataFrame(df_for_write_array)
df_for_write.to_excel("Result.xlsx",sheet_name="Data")

