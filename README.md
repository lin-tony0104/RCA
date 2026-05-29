# RCA: Region-based Cost Admission for CDN Cache

本專案為 RCA（Region-based Cost Admission） 的實作，RCA 是一種針對內容傳遞網路（Content Delivery Network, CDN）所設計的快取准入策略（Cache Admission Policy）。

RCA 透過結合物件大小（Object Size）與重用距離（Reuse Distance）估計物件成本（Cost），並以大小分區（Region）維護區域成本統計資訊，動態決定物件是否應被准入快取，以降低快取污染並提升物件命中率（Object Hit Rate, OHR）。

本專案同時包含 RCA 消融實驗版本、基準方法、Trace 處理工具、實驗框架與評估工具。

## 1. Environment
* **OS**: Windows 10
* **Python**: 3.10.8  

## 2. Installation
### 2.1 Clone this project
  ```
  git clone https://github.com/lin-tony0104/RCA.git
  cd RCA
  ```
### 2.2 Create New Conda Environment
  ```
# 建立並進入環境 
conda env create -f env/RCA_based.yml
conda activate RCA_based
  ```

## 3. 專案架構
```text
.
├── experiment/                 # 實驗設定與結果
│   └── exp_name/               # 命名規則  <cache_size>_<trace_name>_<policy_name>_<seg_num>
│       ├── config.json         # 設定檔
│       └── result/
│           └── result.pkl      # 結果檔\
│
├── policies/                   # 快取策略資料夾
│   ├── policy_name/            # 策略實作
│   └── BasePolicy.py           # policy的抽象基底類別
│
├── trace/                      # Trace 與資料處理工具
│   ├── seg_wiki/               # 處理好的wiki_trace
│   │   ├──wiki_seg0
│   │   └── wiki_seg0_forFOO    
│   │
│   ├── build_FOO_trace.py      # 將tracce由 <o_id> <o_size> 改成FOO要求的輸入格是 <logit time> <o_id> <o_size>
│   ├── get_trace_info.py       # 取得trace統計資訊 (table 1)
│   ├── obj_pop.py              # 依請求次數由高至低排序繪製物件熱門度分析圖(fig 3)
│   ├── seg_trace.py            # 對trace等距抽樣10個2M的子trace。
│   └── sizeCDF.py              # 繪製物件大小分布累積分布圖 (fig 2)
│
├── utils/                      # 共用工具與資料結構
│   ├── MinHeap.py              # 最小堆
│   ├── MinHeap_test.py         # 最小堆測試
│   ├── MinMaxHeap.py           # 最大最小堆
│   └── deque.py                # 雙向佇列
│
├── env/                        # conda環境
│   ├── RCA_based.yml           # 基礎環境， 若要自行新增策略則可以此環境為基礎，加上自己的環境。
│   └── TinyLFU.yml             # TinyLFU環境
│

├── CacheEvaluator.py           # OHR,BHR維護、產出result.pkl。
├── TypeAU.py                   # Type A 不確定度分析
├── run.py                      # 實驗主程式入口
├── run_script.py               # 批次執行工具
├── show_result.py              # OHR 曲線繪製
├── show_result_diff.py         # 實驗結果比較
└── TypeAU.py                   # Type A 不確定度分析
```

## 4. 實作方法

### 4.1 RCA 系列方法
* **RCA**: 本研究提出之方法
* **RCA_Clip**: 移除 RD Clipping
* **RCA_Init**: 移除初始化機制
* **RCA_Aging**: 加入 Aging 機制
* **RCA_Prob**: 加入機率式准入
* **RCA_EMACacheCost**: 以 EMA 估計 Cache Cost
* **RCA_Val**: 使用 Value-Based Admission

### 4.2 比較方法
* **LRU**
* **TinyLFU**
* **AdaptSize**
* **RL-Cache**

## 5. 使用範例
### 5.1 執行單一實驗
  ```
python run.py 05_wiki_RCA_seg0
  ```
### 5.2 腳本執行seg0-seg1
  ```
python run_script.py 05 wiki RCA
```
此指令將執行 `05_wiki_RCA_seg0 `, `05_wiki_RCA_seg1` ... `05_wiki_RCA_seg9`

### 5.3 繪製 OHR 曲線
```
python show_result.py 05_wiki_RCA_seg0
```

### 5.4 比較兩組實驗
```
python show_result_diff.py 05_wiki_RCA_seg0 05_wiki_RCA-aging_seg0
```

### 5.5 Type A 不確定度
```
python TypeAu.py 05_wiki_LRU_seg0 05_wiki_LRU_seg1 05_wiki_LRU_seg2 05_wiki_LRU_seg3 05_wiki_LRU_seg4 05_wiki_LRU_seg5 05_wiki_LRU_seg6 05_wiki_LRU_seg7 05_wiki_LRU_seg8 05_wiki_LRU_seg9

```

## 6. 實驗設定
`experiment/` 內放置各個實驗資料夾。

每個實驗資料夾包含：
- 實驗配置檔
- 實驗執行結果
 
例如：

```text
experiment/
└── exp_name/
    ├── config.json
    └── result/result.pkl
```
exp_name命名規則為  `<cache_size>_<trace_name>_<policy_name>_<seg_num>`

其中 `config.json` 內容分三個部分：
- baslic_config:
  - policy: 指定當前使用`policy` 需與 `run.py`註冊表的key相同
  - trace: 指定使用trace
- policy_config:
  - cache_size: 快取大小
  - 其餘視policy可自行增加，此config會被傳給 policy做初始化
- evaluator_config
  - region: 為取樣間隔，每`region`個請求紀錄一個`OHR`。
  - warmup: 未使用
  - verbose: 是否在執行時顯示進度

設定檔範例:
```
{
    "basic_config": {
        "policy": "RCA",
        "trace": "seg_wiki/wiki_seg0"
    },
    "policy_config": {
        "cache_size": 3811783475,
        "region_size": 1000,
        "alpha": 0.9
    },
    "evaluator_config": {
        "region": 100,
        "warmup": 1000000,
        "verbose": true
    }
}
```

## 7. Trace處理工具
- `get_trace_info.py`: 取得trace統計資訊 (table 1)
- `sizeCDF.py`: 繪製物件大小分布累積分布圖 (fig 2)
- `obj_pop.py`: 依請求次數由高至低排序繪製物件熱門度分析圖(fig 3)
- `seg_trace.py`: 對trace等距抽樣10個2M的子trace。
- `build_FOO_trace.py`: 將trace格式改為FOO要求的<time> <o_id> <o_size>。

## 8. 資料集
本篇實驗使用之trace可於此下載:  
https://drive.google.com/drive/folders/1TZS0zZ12PBGBvPETkRrnHpgS9OgV80Ok?usp=sharing  
本篇使用之trace原始下載點:  
https://github.com/sunnyszy/lrb  

## 10. 新增策略
以新增LRU為例
1. 於 `policy/` 中新增策略資料夾 `policy/LRU/`
2. 於 `policy/LRU/` 中新增策略實作`policy/LRU/LRU.py` 
3. 於`LRU.py`實作`LRU_policy`類別，必須繼承BasePolicy並實作request方法。
4. `request`方法負責處理一次請求，並回傳該請求是否命中:  
```
   hit = policy.request(object_id, object_size, object_features)
```
透過此設計，主程式不需要知道各個策略的內部實作細節，只需要呼叫相同`request`方法即可執行不同策略

## 9. 備註
### 9.1 FOO標記資料生成
FOO需要事先使用`\policies\FOO\FOO_labeling\foo.exe`生成 標記資料才可跑實驗
具體步驟:   
  1. 準備原始trace，請求格式為 <o_id> <o_size>。  
  2. 使用`\trace\build_FOO_trace.py`生成trace_for_FOO，此時請求格式 <time> <o_id> <o_size>。
  3. 使用`\policies\FOO\FOO_labeling\foo.exe` 計算出帶FOO標籤的trace，此時請求格式為 <o_id> <o_size> <o_admit>  

### 9.2 完整早期其他實驗(ETM方法)
https://github.com/lin-tony0104/RCA-raw


