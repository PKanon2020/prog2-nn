#宣言
import time
import matplotlib.pyplot as plt

import torch
from torchvision import datasets
import torchvision.transforms.v2 as transforms

import models

#データセットの前処理関数
ds_transform = transforms.Compose([
    transforms.ToImage(),
    transforms.ToDtype(torch.float32, scale = True)
])

#データ処理の読み込み
ds_train = datasets.FashionMNIST(
    root = 'data',
    train = True,
    download = True,
    transform = ds_transform
)

ds_test = datasets.FashionMNIST(
    root = 'data',
    train = False, #テスト用データセット
    download = True,
    transform = ds_transform
)

#ミニバッチのデータローダー
bs = 64
dataloader_train = torch.utils.data.DataLoader(
    ds_train,
    batch_size = bs,
    shuffle = True
)

dataloader_test = torch.utils.data.DataLoader(
    ds_test,
    batch_size = bs,
    shuffle = False
)

for image_batch,label_batch in dataloader_train:
    print(image_batch.shape)
    print(label_batch)
    break

model = models.MyModel()
loss_fn = torch.nn.CrossEntropyLoss()

learning_rate = 1e-3
optimizer = torch.optim.SGD(model.parameters(), lr = learning_rate)

acc_train = models.test_accuracy(model, dataloader_train)
print(f'test accuracy: {acc_train * 100:.3f}%')

acc_test = models.test_accuracy(model, dataloader_test)
print(f'test accuracy: {acc_test * 100:.3f}%')

#ロス関数の選択
loss_fn = torch.nn.CrossEntropyLoss()

#最適化手法の選択
learning_rate = 0.003
optimizer = torch.optim.SGD(model.parameters(),lr = learning_rate)

acc_test = models.test_accuracy(model, dataloader_test)
print(f'test accuracy: {acc_test*100:.2f}%')

n_epochs = 5

loss_train_history = []
loss_test_history = []
acc_train_history = []
acc_test_history = []

for k in range(n_epochs):
    print(f'epoch {k+1}/{n_epochs}', end=': ', flush = True)

    #1 epochの学習
    time_start = time.time()
    loss_train = models.train(model, dataloader_train, loss_fn,optimizer)
    time_end = time.time()
    loss_train_history.append(loss_train)
    print(f'train loss: {loss_train:.3f} ({time_end-time_start}s)', end=', ')
    print(f'train loss: {loss_train:.3f} ({time_end-time_start:.1f}s)', end=', ')
   
    loss_test = models.test(model, dataloader_test, loss_fn)
    loss_test_history.append(loss_test)
    print(f'test loss: {loss_test:.3f}', end=', ')

    #精度を計算する
    acc_train = models.test_accuracy(model, dataloader_train)
    acc_train_history.append(acc_train)
    print(f'train accuracy: {acc_train*100:.3f}%', end=', ')


    acc_test = models.test_accuracy(model, dataloader_test)
    acc_test_history.append(acc_test)
    print(f'test accuracy: {acc_test*100:.3f}%')

#グラフの出力
plt.plot(acc_train_history, label='train')
plt.plot(acc_test_history, label='test')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.grid()
plt.show()

plt.plot(loss_train_history, label='train')
plt.plot(loss_test_history, label='test')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.grid()
plt.show()
