# 程式結構

本專案主要分為 `/`、`experiment/`、`policy/`、`trace/`、`utils/`、`env/`五個部分。

## `/`



`/` 根目錄主要放置程式入口、結果展示工具。

根目錄包含：

- `run.py`  
  實驗主程式入口，用於執行指定實驗。  

  新增 policy 時，需在 `run.py` 開頭的 `policy_registry` 中註冊：  
  "A": "policies.A.A:A_policy"
  
  執行方式： 
  `python run.py <exp_name>`  

  範例：

  ```bash
  python run.py 05_wiki_LRU_seg0
  ```

---

- `run_script.py`  
  批次執行指定實驗的 `seg0 ~ seg9`。  

  執行方式：  
  `python run_script.py <cache_size> <trace> <policy>`  

  範例：

  ```bash
  python run_script.py 05 wiki LRU
  ```

  此指令會自動執行： `05_wiki_LRU_seg0` ~ `05_wiki_LRU_seg9`


---

- `show_result.py`  
  繪製實驗的命中率曲線圖。  
  可同時比較多個實驗結果。

  執行方式：  
  `python show_result.py <exp1> <exp2>`
 
  範例：

  ```bash
  python show_result.py 05_wiki_RCA_seg0 05_wiki_RCA-aging_seg0
  ```

---

- `show_result_diff.py`  
  比較兩個實驗結果差異。  

  會顯示：
  - OHR 差異曲線
  - 平均差異值

  差異計算方式為：

  ```text
  exp1 - exp2
  ```

  執行方式：  
  `python show_result_diff.py <exp1> <exp2>`

  範例：

  ```bash
  python show_result_diff.py 05_wiki_RCA_seg0 05_wiki_RCA-aging_seg0
  ```

  註：目前僅支援比較兩個實驗。

---

- `TypeAu.py`  
  計算實驗結果的 A 類不確定度（Type A Uncertainty）。  

  目前包含：
  - OHR 
  - WallTime 

  執行方式：  
  `python TypeAu.py <exp1> <exp2> ...`

  範例：

  ```bash
  python TypeAu.py 05_wiki_LRU_seg0 05_wiki_LRU_seg1 05_wiki_LRU_seg2 05_wiki_LRU_seg3 05_wiki_LRU_seg4 05_wiki_LRU_seg5 05_wiki_LRU_seg6 05_wiki_LRU_seg7 05_wiki_LRU_seg8 05_wiki_LRU_seg9
  ```
  
## `experiment/`

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
---

## `policy/`

`policy/` 內放置各種 cache policy 的實作。

所有 policy 類別皆需繼承 `BasePolicy`，並實作 `request` 方法。  

`request` 方法負責處理一次請求，並回傳該請求是否命中 cache：  
`hit = policy.request(object_id, object_size, object_features)`  

透過此設計，主程式不需要知道各個 policy 的內部實作細節，只需要呼叫相同的 `request` 介面即可執行不同策略。

---

## `trace/`

`trace/` 內放置實驗使用的 trace 檔案，以及 trace 處理相關工具。

內容包含：
- 原始 trace
- 切分後的 trace segment
- `get_trace_info.py`: 取得trace統計資訊 (table 1)
- `sizeCDF.py`: 繪製物件大小分布累積分布圖 (fig 2)
- `obj_pop.py`: 依請求次數由高至低排序繪製物件熱門度分析圖(fig 3)
- `seg_trace.py`: 對trace等距抽樣10個2M的子trace。
- `build_FOO_trace.py`: 將trace格式改為FOO要求的<time> <o_id> <o_size>。


---

## `utils/`

`utils/` 內放置 cache 實作常用到的資料結構與輔助工具。

---

## `env/`
- `RCA_based` : 所有方法的環境，包含policy及以外的程式環境(畫圖, 切資料等等)、(TinyLFU除外)。
- `TinyLFU` : TinyLFU的環境


# 實驗:
## 新增策略

---
## 新增實驗
---
## 跑實驗
---
## 實驗結果


# 附註:
FOO需要事先使用`\policies\FOO\FOO_labeling\foo.exe`生成 標記資料才可跑實驗
具體步驟:   
  1. 準備原始trace，請求格式為 <o_id> <o_size>。  
  2. 使用`\trace\build_FOO_trace.py`生成trace_for_FOO，此時請求格式 <time> <o_id> <o_size>。
  3. 使用`\policies\FOO\FOO_labeling\foo.exe` 計算出帶FOO標籤的trace，此時請求格式為 <o_id> <o_size> <o_admit>
  
