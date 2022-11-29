import pandas as pd
import openpyxl

#사이 평균으로 채우는 코드

'''
data.xlsx -> inputDataResult.xlsx 로 데이터를 채워주는 모듈입니다
data.xlsx의 Sheet1은 데이터 개수 * 3 의 형태로 만들어주시고 순서는 (ID, 날짜, Data Value) 입니다.
data.xlsx의 Sheet2는 데이터의 날짜가 추가된다면 날짜를 더 늘려주시고 ComputeDate 함수에서 늘어난 날짜만큼 노가다로 늘려주세요
                    ID의 개수가 늘어났다면 아무것도 하지 않으셔도 됩니다.
'''

#ComputeDate 만 데이터 날짜 개수 바뀔때마다 바꿔주면됨
def ComputeDate(string):
    if(string=="2022-07-14"): return 0
    elif(string=="2022-07-15"): return 1
    elif(string=="2022-07-16"): return 2
    elif(string=="2022-07-17"): return 3
    elif(string=="2022-07-18"): return 4
    elif(string=="2022-07-19"): return 5
    elif(string=="2022-07-20"): return 6
    elif(string=="2022-07-21"): return 7
    elif(string=="2022-07-22"): return 8
    elif(string=="2022-07-23"): return 9
    elif(string=="2022-07-24"): return 10
    elif(string=="2022-07-25"): return 11
    elif(string=="2022-07-26"): return 12
    elif(string=="2022-07-27"): return 13
    elif(string=="2022-07-28"): return 14
    elif(string=="2022-07-29"): return 15
    elif(string=="2022-07-30"): return 16
    elif(string=="2022-07-31"): return 17
    elif(string=="2022-08-01"): return 18
    elif(string=="2022-08-02"): return 19
    elif(string=="2022-08-03"): return 20
    elif(string=="2022-08-04"): return 21
    elif(string=="2022-08-05"): return 22
    elif(string=="2022-08-06"): return 23
    elif(string=="2022-08-07"): return 24
    elif(string=="2022-08-08"): return 25
    elif(string=="2022-08-09"): return 26
    elif(string=="2022-08-10"): return 27
    elif(string=="2022-08-11"): return 28
    elif(string=="2022-08-12"): return 29
    elif(string=="2022-08-13"): return 30
    elif(string=="2022-08-14"): return 31
    elif(string=="2022-08-15"): return 32
    elif(string=="2022-08-16"): return 33
    elif(string=="2022-08-17"): return 34
    elif(string=="2022-08-18"): return 35
    elif(string=="2022-08-19"): return 36
    elif(string=="2022-08-20"): return 37
    elif(string=="2022-08-21"): return 38
    elif(string=="2022-08-22"): return 39
    elif(string=="2022-08-23"): return 40
    elif(string=="2022-08-24"): return 41
    elif(string=="2022-08-25"): return 42
    elif(string=="2022-08-26"): return 43
    elif(string=="2022-08-27"): return 44
    elif(string=="2022-08-28"): return 45
    elif(string=="2022-08-29"): return 46
    elif(string=="2022-08-30"): return 47
    elif(string=="2022-08-31"): return 48
    elif(string=="2022-09-01"): return 49
    elif(string=="2022-09-02"): return 50
    elif(string=="2022-09-03"): return 51
    elif(string=="2022-09-04"): return 52
    elif(string=="2022-09-05"): return 53
    elif(string=="2022-09-06"): return 54
    elif(string=="2022-09-07"): return 55
    elif(string=="2022-09-08"): return 56
    elif(string=="2022-09-09"): return 57
    elif(string=="2022-09-10"): return 58
    elif(string=="2022-09-11"): return 59
    elif(string=="2022-09-12"): return 60
    elif(string=="2022-09-13"): return 61
    elif(string=="2022-09-14"): return 62
    elif(string=="2022-09-15"): return 63
    elif(string=="2022-09-16"): return 64
    elif(string=="2022-09-17"): return 65
    elif(string=="2022-09-18"): return 66
    elif(string=="2022-09-19"): return 67
    elif(string=="2022-09-20"): return 68
    elif(string=="2022-09-21"): return 69
    elif(string=="2022-09-22"): return 70
    elif(string=="2022-09-23"): return 71
    elif(string=="2022-09-24"): return 72
    elif(string=="2022-09-25"): return 73
    elif(string=="2022-09-26"): return 74
    elif(string=="2022-09-27"): return 75
    elif(string=="2022-09-28"): return 76
    elif(string=="2022-09-29"): return 77
    elif(string=="2022-09-30"): return 78
    elif(string=="2022-10-01"): return 79
    elif(string=="2022-10-02"): return 80
    elif(string=="2022-10-03"): return 81
    elif(string=="2022-10-04"): return 82
    elif(string=="2022-10-05"): return 83

#Sheet 1 엑셀 읽기
df1=pd.read_excel('data2.xlsx',sheet_name='Sheet1')

#Sheet 2 엑셀 읽기
df2=pd.read_excel('data2.xlsx',sheet_name='Sheet2')

#행 : cols, 열 : rows 이고 2차원 배열 생성
cols1=3
rows1=len(df1)
data=[[0 for j in range(cols1)] for i in range(rows1)]

#시트 1에서 데이터 읽어오기
Sheet1_ID=df1['ID']
Sheet1_date=df1['collect_datetime']
Sheet1_value=df1['b']
for i in range(len(df1)):
    data[i][0]=Sheet1_ID[i]
    data[i][1]=Sheet1_date[i]
    data[i][2]=Sheet1_value[i]

#Convert "pandas timestamp" to "str"
for i in range(len(data)):
    if(type(data[i][1])!=str):
        data[i][1]=data[i][1].strftime('%Y-%m-%d')

Sheet2_ID=df2['ID'] #ID

cols2=len(df2.columns)-1 # 날짜 개수
rows2=len(Sheet2_ID) # ID개수
df_for_write_array=[[0 for j in range(rows2)] for i in range(cols2)]

# 배열에 값을 추가하는 부분
for i in range(len(df1)):
    for j in range(len(df2)):
        if(Sheet2_ID[j]==data[i][0]):
            index=ComputeDate(data[i][1][0:10])
            df_for_write_array[index][j]=data[i][2]

for i in range(rows2): #ID
    showindex=[]
    for j in range(cols2): #날짜
        if (df_for_write_array[j][i]!=0):
            showindex.append(j)
    count=0
    if(len(showindex)!=0):
        while(count<84):
            if(count<showindex[0]):
                df_for_write_array[count][i]=df_for_write_array[showindex[0]][i]
            if (count > showindex[-1]):
                df_for_write_array[count][i]=df_for_write_array[showindex[-1]][i]
            count=count+1

        start = showindex[0]
        end=0
        count=start
        while(count<83):
            if(df_for_write_array[count][i]==0 and df_for_write_array[count+1][i]!=0) or (df_for_write_array[count][i]!=0 and df_for_write_array[count+1][i]==0):
                end=count+1
                for k in range(end-start):
                    df_for_write_array[start+k][i]=(df_for_write_array[start][i]+df_for_write_array[end][i])/2
            count = count + 1
    showindex.clear()

#엑셀에 쓰는 부분
df_for_write=pd.DataFrame(df_for_write_array)
df_for_write.to_excel("inputDataResult2.xlsx",sheet_name="Data")
