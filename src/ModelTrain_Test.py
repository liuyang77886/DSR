# -*- coding: utf-8 -*-
#coding=utf-8  
"""
Created on Wed Jan 17 10:51:07 2018
模型工具类，提供模型训练，模型保存，模型导入操作
@author: John Kwok
"""
from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(2)    

import GetDataUtil
#import SparseFilter
import numpy as np
#%%
'''
# 声明训练集，数据集
X_train = []
X_test = []
y_train = []
y_test = []
'''
# 获取 训练/测试 数据集
X_train, X_test, y_train, y_test = GetDataUtil.dataInit()
#%%
# 将标签转换为one_hot稀疏值
from keras.utils import np_utils
y_train = np_utils.to_categorical(y_train-1,5)
y_test = np_utils.to_categorical(y_test-1,5)
#%%
#卷积神经网络input需要dim = 4
X_train = X_train[:,np.newaxis,:,:]
X_test = X_test[:,np.newaxis,:,:]
print(X_train.shape)
#%%
import time
import sklearn
from keras.optimizers import Adam
from sklearn.utils import shuffle
from keras.utils import plot_model
from keras.models import Model
from keras.layers import Input,Dense
from keras.layers.convolutional import Conv2D
from keras.layers.normalization import BatchNormalization
from keras.initializers import TruncatedNormal
from keras import regularizers
from keras.layers.core import Activation,Flatten
from keras.layers.pooling import MaxPooling2D,AveragePooling2D
from keras.layers.core import Dropout
# 
inputs = Input(shape = (1,30,300),name="Input")

x = Conv2D(filters = 128,
           kernel_size = (1,3),#尝试方形kernel 纵向也可能相关
           strides = (1,1),
           padding = 'same',
           use_bias = False,# 尝试加一下bias
           kernel_initializer = TruncatedNormal(stddev=0.0001),
           kernel_regularizer = regularizers.l2(0.1),
           name = "Conv1")(inputs)
x = BatchNormalization(axis = 1,name = "BN1")(x)# 尝试去掉BN
x = Activation('relu',name = 'relu1')(x)
x = MaxPooling2D(pool_size = (1,3),strides = (1,2),padding = 'same')(x)
x = Dropout(0.2)(x)#0.1zuoyou
x = Conv2D(filters = 128,
           kernel_size = (1,5),
           strides = (1,3),
           padding = 'same',
           use_bias = False,
           kernel_initializer = TruncatedNormal(stddev=0.001),
           kernel_regularizer = regularizers.l2(0.1),
           name = "Conv2")(x)
x = BatchNormalization(axis = 1,name = 'BN2')(x)
x = Activation('relu',name = 'relu2')(x)
x = MaxPooling2D(pool_size = (1,3),strides = (1,2),padding = 'same')(x)
x = Dropout(0.2)(x)
'''
x = Conv2D(filters = 128,
           kernel_size = (1,5),
           strides = (1,3),
           padding = 'same',
           use_bias = False,
           kernel_initializer = TruncatedNormal(stddev=0.001),
           kernel_regularizer = regularizers.l2(0.01),
           name = "Conv3")(x)
x = BatchNormalization(axis = 1,name = "BN3")(x)
x = Activation('relu',name = 'relu3')(x)
x = MaxPooling2D(pool_size = (1,3),strides = (1,2),padding = 'same')(x)
x = Dropout(0.2)(x)
'''
x = Flatten()(x)

x = Dense(2048,
          kernel_initializer = TruncatedNormal(stddev=0.01),
          kernel_regularizer = regularizers.l2(0.01),
#          activation='relu',
          name = "D1")(x)
x = BatchNormalization(axis = 1,name="D1_BN")(x)
x = Activation('relu',name = 'D1_relu')(x)
x = Dropout(0.1)(x)

x = Dense(1024,
#          activation='relu',
          kernel_initializer = TruncatedNormal(stddev=0.01),
          kernel_regularizer = regularizers.l2(0.01),
          name="D2")(x)
x = BatchNormalization(axis = 1,name="D2_BN")(x)
x = Activation('relu',name = 'D2_relu')(x)
'''
x = Dense(256,
          activation='relu',
          kernel_initializer = TruncatedNormal(stddev=0.1),
          kernel_regularizer = regularizers.l2(0.01),
          name="D3")(x)

x = BatchNormalization(axis = 1,name="D3_BN")(x)
x = Activation('relu',name = 'D3_relu')(x)
'''
out = Dense(5,activation='softmax',name="OutPut")(x)

model = Model(inputs = inputs,outputs = out)
model.compile(optimizer = 'RMSprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
print("正在训练网络，请耐心等候......")
X_train,y_train = shuffle(X_train,y_train,random_state=None)
startTime = time.clock()
trainLog = model.fit(X_train,
          y_train,
          validation_split = 0.03,
          batch_size=512,
          epochs=10,
          verbose=1
          )
endTime = time.clock()
# 注意，这里的时间window和linux不同
print("网络训练已完成 耗时%f 秒"%((float)(endTime - startTime)/10))

# 绘制模型的结构图 此处还出现点问题，待解a决
plot_model(model,
           to_file='model.png',
           show_shapes=True,
           show_layer_names=True)

'''注意：sklearn中的标签都不是稀疏的'''
from sklearn.metrics import classification_report
predict = model.predict(X_test)
print("测试集预测结果：")
print(classification_report(np.argmax(y_test,axis = 1),np.argmax(predict,axis = 1)))
# 打印混淆矩阵
print("测试集混淆矩阵：")
print(sklearn.metrics.confusion_matrix(np.argmax(y_test,axis = 1),np.argmax(predict,axis = 1)))

#%%
# from keras.models import load_model
# 保存模型
model.save('my_model.h5')

#%%
print(trainLog)
plot_model(model,
           to_file='model.png',
           show_shapes=True,
           show_layer_names=True)



#%%

#import matplotlib
#print(matplotlib.matplotlib_fname())


data_pic = np.load("JustifiedData.npy")
GetDataUtil.generatePic(data_pic)
