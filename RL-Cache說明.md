# RL-Cache
本篇直接使用RL-CACHE作者提供的code來跑實驗，連結為: https://github.com/quovadim/RL-Cache
實驗流程接照著作者說明即可，其餘環境建置說明如下。

## 1. Environment
### 1.1 安裝python2.7
```
sudo apt install python2.7
sudo apt install curl
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2.7 get-pip.py
```

### 1.2 安裝python相關lib
```
pip install "grpcio<1.30.0"
pip install tensorflow==1.15.0 keras==2.2.4 numpy matplotlib hurry.filesize tqdm
```

### 1.3 安裝c++環境
```
sudo apt install build-essential
sudo apt install python2.7-dev
```

### 1.4 build boost library
```
wget https://archives.boost.io/release/1.71.0/source/boost_1_71_0.tar.gz
tar -xzvf boost_1_71_0.tar.gz
cd boost_1_71_0
./bootstrap.sh --with-python=python2.7
./b2 --with-python
cd ~/Desktop/boost_1_71_0/stage/lib
sudo cp libboost_python27* /usr/lib/x86_64-linux-gnu/
sudo ln -s /usr/lib/x86_64-linux-gnu/libboost_python27.so /usr/lib/x86_64-linux-gnu/libboost_python.so
```


## 2. trace
### 2.1 train data
### 2.2 test data
  
