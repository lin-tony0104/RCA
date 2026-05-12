import subprocess
import sys
# 可用policy列表：
# TinyLFU, LRU, AdaptSize, FOO, 
# RCA, RCA-aging, RCA-EMACacheCost, RCA-Clip, RCA-Init ,RCA-val, RCA-prob


if len(sys.argv)==4:
    try:
        cache_size = sys.argv[1]
        trace = sys.argv[2]
        policy = sys.argv[3]

    except Exception as e:
        print(e)
        sys.exit()
else:
    print("參數格式:")
    print("python run_script.py <cache_size>, <trace>, <policy>")
    print("EX: python run_script.py 05 wiki RCA")
    sys.exit()




# cache_size ="05"
# trace ="wiki"
# policy="RCA-aging"


exps = [f"{cache_size}_{trace}_{policy}_seg{i}" for i in range(10)]


for exp in exps:
    # run() 會等待程序執行完畢才繼續下一個迴圈
    print(f"正在執行: {exp}...")
    subprocess.run(["python", "run.py", exp], check=True)

print("所有腳本已按順序執行完畢！")
