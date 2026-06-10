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
sudo apt install libboost-python-dev
```

### 1.4 build boost library
```
wget https://archives.boost.io/release/1.71.0/source/boost_1_71_0.tar.gz
tar -xzvf boost_1_71_0.tar.gz
cd boost_1_71_0
./bootstrap.sh --with-python=python2.7
./b2 --with-python
cd ./stage/lib
sudo cp libboost_python27* /usr/lib/x86_64-linux-gnu/
sudo ln -s /usr/lib/x86_64-linux-gnu/libboost_python27.so /usr/lib/x86_64-linux-gnu/libboost_python.so
```
## 2. 編譯環境
接下來步驟與RL-Cache提供相同 https://github.com/quovadim/RL-Cache
```
git clone https://github.com/WVadim/RL-Cache
cd RL-Cache
```

```
make all
cd feature_collector
make all
cd ../reward_collector
make all
```
## 3. 加入本篇實驗設置與trace
https://drive.google.com/drive/folders/1DnF42yNx2osQW5oodMWjnwbprHUEyT46?usp=sharing
- 將experiments/內容放入 RL-Cache/experiments/中  (實驗設置)
- 將data/內容放入 RL-Cache/data/中  (Trace)

### 3.1 對trace做預處理
```
cd RL-Cache
./gather_data.sh data/train/ data/train_rewarded/
python2.7 collect_statistics.py statistics/train -r=train -i=2
```

### 3.2 訓練

```
python2.7 train.py train -t=15 -v
```
訓練出的模型生成於 `/RL-Cache/experiments/train/adm`

### 3.3 測試
- `/RL-Cache/experiments/train/adm` 複製到 `RL-Cache/experiments/wiki_seg0`  ~ `RL-Cache/experiments/wiki_seg9`
- 針對 `wiki_seg0` ~ `wiki_seg9`做測試。以下用`wiki_seg0`示範。  
  對test trace預處理(3.1步驟)
  ```
  ./gather_data.sh data/wiki_seg0/ data/wiki_seg0_rewarded/
  python2.7 collect_statistics.py statistics/wiki_seg0 -r=wiki_seg0 -i=2
  ```
  跑測試
  ```
  python2.7 test.py wiki_seg0 wiki_seg0
  ```
  結果儲存於`RL-Cache/tests/wiki_seg0/wiki_seg0/`
  每100請求紀錄一個pickle檔，透過`RL_Cache_result.py`
  ```
  python2.7 RL_Cache_result.py ~/Desktop/RL-Cache/tests/wiki_seg0/wiki_seg0
  ```




## 備註
- 已有嘗試使用GPU版本TensorFlow，環境較難安裝且未有明顯加速故只說明CPU版本TensorFlow。
