import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Dropout,Activation
from torch.utils.data import TensorDataset, DataLoader
from tensorflow.python.keras import metrics
from tensorflow.python import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import os
from imblearn.over_sampling import SMOTE
import math

# device 설정 (cuda:0 혹은 cpu)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")



path = "C:\\Users\\Lab01\\BMI\\modeling\\optimal_data\\"
file_list = os.listdir(path)
len(file_list)

optimal_acc=[]
optimal_loss=[]

def find_optimal(file):
    df=pd.read_excel('C:\\Users\\Lab01\\BMI\\modeling\\optimal_data\\{}'.format(file))
    df.head()
    X=df.iloc[:,1:7]
    y=df.iloc[:,-1]

    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    scaler = StandardScaler()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
#     X_train=X.iloc[:3375,:]
#     X_test=X.iloc[3375:,:]

#     y_train=y.iloc[:3375]
#     y_test=y.iloc[3375:]

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    smote = SMOTE(random_state=0)
    X_train_over,y_train_over = smote.fit_resample(X_train,y_train)
    print('SMOTE 적용 전 학습용 피처/레이블 데이터 세트: ', X_train.shape, y_train.shape)
    print('SMOTE 적용 후 학습용 피처/레이블 데이터 세트: ', X_train_over.shape, y_train_over.shape)
    print('SMOTE 적용 전 레이블 값 분포: \n', pd.Series(y_train).value_counts())
    print('SMOTE 적용 후 레이블 값 분포: \n', pd.Series(y_train_over).value_counts())

    X_train = torch.FloatTensor(X_train_over)
    X_test = torch.FloatTensor(X_test)
    y_train = torch.LongTensor(y_train_over)
    y_test = torch.LongTensor(y_test.to_numpy())

    train_dataset = TensorDataset(X_train, y_train)
    test_dataset=TensorDataset(X_test, y_test)

    train_dataloader = DataLoader(train_dataset, batch_size=16,shuffle=False)
    test_dataloader = DataLoader(test_dataset, batch_size=16,shuffle=False)

    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim


    class DNNModel(nn.Module):
        def __init__(self):
            super(DNNModel, self).__init__()
            self.input_layer = nn.Linear(6, 128)
            self.hidden_layer1 = nn.Linear(128, 256)
            self.hidden_layer2 = nn.Linear(256, 128)
            self.output_layer   = nn.Linear(128,3)
            self.relu = nn.ReLU()



        def forward(self, x):
            out =  self.relu(self.input_layer(x))
            out =  self.relu(self.hidden_layer1(out))
            out =  self.relu(self.hidden_layer2(out))
            out =  self.output_layer(out)
            return out



    # device 설정 (cuda:0 혹은 cpu)
    model = DNNModel() # Model 생성
    model.to(device)   # device 에 로드 (cpu or cuda)

    # 옵티마이저를 정의합니다. 옵티마이저에는 model.parameters()를 지정해야 합니다.
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 손실함수(loss function)을 지정합니다. Multi-Class Classification 이기 때문에 CrossEntropy 손실을 지정하였습니다.
    loss_fn = nn.CrossEntropyLoss()

    from tqdm import tqdm  # Progress Bar 출력

    def model_train(model, data_loader, loss_fn, optimizer, device):
        # 모델을 훈련모드로 설정합니다. training mode 일 때 Gradient 가 업데이트 됩니다. 반드시 train()으로 모드 변경을 해야 합니다.
        model.train()

        # loss와 accuracy 계산을 위한 임시 변수 입니다. 0으로 초기화합니다.
        running_loss = 0
        corr = 0

        # 예쁘게 Progress Bar를 출력하면서 훈련 상태를 모니터링 하기 위하여 tqdm으로 래핑합니다.
        prograss_bar = tqdm(data_loader)

        # mini-batch 학습을 시작합니다.
        for data, lbl in prograss_bar:
            # image, label 데이터를 device에 올립니다.
            data, lbl = data.to(device), lbl.to(device)
            # 누적 Gradient를 초기화 합니다.
            optimizer.zero_grad()

            # Forward Propagation을 진행하여 결과를 얻습니다.
            output = model(data)

            # 손실함수에 output, label 값을 대입하여 손실을 계산합니다.
            loss = loss_fn(output, lbl)

            # 오차역전파(Back Propagation)을 진행하여 미분 값을 계산합니다.
            loss.backward()

            # 계산된 Gradient를 업데이트 합니다.
            optimizer.step()

            # output의 max(dim=1)은 max probability와 max index를 반환합니다.
            # max probability는 무시하고, max index는 pred에 저장하여 label 값과 대조하여 정확도를 도출합니다.
            _, pred = output.max(dim=1)

            # pred.eq(lbl).sum() 은 정확히 맞춘 label의 합계를 계산합니다. item()은 tensor에서 값을 추출합니다.
            # 합계는 corr 변수에 누적합니다.
            corr += pred.eq(lbl).sum().item()

            # loss 값은 1개 배치의 평균 손실(loss) 입니다. data.size(0)은 배치사이즈(batch size) 입니다.
            # loss 와 data.size(0)를 곱하면 1개 배치의 전체 loss가 계산됩니다.
            # 이를 누적한 뒤 Epoch 종료시 전체 데이터셋의 개수로 나누어 평균 loss를 산출합니다.
            running_loss += loss.item() * data.size(0)

        # 누적된 정답수를 전체 개수로 나누어 주면 정확도가 산출됩니다.
        acc = corr / len(data_loader.dataset)

        # 평균 손실(loss)과 정확도를 반환합니다.
        # train_loss, train_acc
        return running_loss / len(data_loader.dataset), acc

    def model_evaluate(model, data_loader, loss_fn, device):
        # model.eval()은 모델을 평가모드로 설정을 바꾸어 줍니다.
        # dropout과 같은 layer의 역할 변경을 위하여 evaluation 진행시 꼭 필요한 절차 입니다.
        model.eval()

        # Gradient가 업데이트 되는 것을 방지 하기 위하여 반드시 필요합니다.
        with torch.no_grad():
            # loss와 accuracy 계산을 위한 임시 변수 입니다. 0으로 초기화합니다.
            corr = 0
            running_loss = 0

            # 배치별 evaluation을 진행합니다.
            for data, lbl in data_loader:
                # device에 데이터를 올립니다.
                data, lbl = data.to(device), lbl.to(device)

                # 모델에 Forward Propagation을 하여 결과를 도출합니다.
                output = model(data)

                # output의 max(dim=1)은 max probability와 max index를 반환합니다.
                # max probability는 무시하고, max index는 pred에 저장하여 label 값과 대조하여 정확도를 도출합니다.
                _, pred = output.max(dim=1)
                # pred.eq(lbl).sum() 은 정확히 맞춘 label의 합계를 계산합니다. item()은 tensor에서 값을 추출합니다.
                # 합계는 corr 변수에 누적합니다.
                corr += torch.sum(pred.eq(lbl)).item()

                # loss 값은 1개 배치의 평균 손실(loss) 입니다. data.size(0)은 배치사이즈(batch size) 입니다.
                # loss 와 data.size(0)를 곱하면 1개 배치의 전체 loss가 계산됩니다.
                # 이를 누적한 뒤 Epoch 종료시 전체 데이터셋의 개수로 나누어 평균 loss를 산출합니다.
                running_loss += loss_fn(output, lbl).item() * data.size(0)

            # validation 정확도를 계산합니다.
            # 누적한 정답숫자를 전체 데이터셋의 숫자로 나누어 최종 accuracy를 산출합니다.
            acc = corr / len(data_loader.dataset)

            # 결과를 반환합니다.
            # val_loss, val_acc
            return running_loss / len(data_loader.dataset), acc

    # 최대 Epoch을 지정합니다.
    num_epochs = 500

    max_acc = 0
    # Epoch 별 훈련 및 검증을 수행합니다.
    for epoch in range(num_epochs):
        # Model Training
        # 훈련 손실과 정확도를 반환 받습니다.
        train_loss, train_acc = model_train(model, train_dataloader, loss_fn, optimizer, device)

        # 검증 손실과 검증 정확도를 반환 받습니다.
        val_loss, val_acc = model_evaluate(model, test_dataloader, loss_fn, device)

        # val_loss 가 개선되었다면 min_loss를 갱신하고 model의 가중치(weights)를 저장합니다.
        if val_acc > max_acc:
            print(f'[INFO] val_acc has been improved from {max_acc:.5f} to {val_acc:.5f}. Saving Model!')
            max_acc = val_acc
            torch.save(model.state_dict(), 'DNNModel.pth')

        # Epoch 별 결과를 출력합니다.
        print(f'epoch {epoch+1:02d}, loss: {train_loss:.5f}, acc: {train_acc:.5f}, val_loss: {val_loss:.5f}, val_accuracy: {val_acc:.5f}')

    ## 저장한 가중치 로드 후 검증 성능 측정

    # 모델에 저장한 가중치를 로드합니다.
    model.load_state_dict(torch.load('DNNModel.pth'))

    # 최종 검증 손실(validation loss)와 검증 정확도(validation accuracy)를 산출합니다.
    final_loss, final_acc = model_evaluate(model, test_dataloader, loss_fn, device)
    print(f'evaluation loss: {final_loss:.5f}, evaluation accuracy: {final_acc:.5f}')
    optimal_acc.append(round(final_acc,4))
    optimal_loss.append(round(final_loss,4))
    print('---------------------------------------------------')
    print('{}번째 완료했습니다.'.format(len(optimal_acc)))
    print(optimal_acc)
    print('---------------------------------------------------')

for file in file_list:
    find_optimal(file);



