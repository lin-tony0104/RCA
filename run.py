#全部流程:
#呼叫eviction.py , admission_policy.py 做決策
# #收集訓練資料給TCN
import json
import sys

from CacheEvaluator import CacheEvaluator


import importlib
# policies
# from policies.LRU.LRU import LRU_policy
# from policies.LFU.LFU import LFU_policy
# from policies.ETM_AEP.ETM_AEP import ETM_AEP_policy
# from policies.ASC_IP.ASC_IP import ASC_IP_policy
# from policies.AdaptSize.AdaptSize import Adaptsize_policy
policy_registry={
    "LRU":"policies.LRU.LRU:LRU_policy",
    "AdaptSize":"policies.AdaptSize.AdaptSize:Adaptsize_policy",
    "FOO":"policies.FOO.FOO:FOO_policy",
    "TinyLFU":"policies.TinyLFU.TinyLFU:TinyLFU_policy",



    "RCA":"policies.RCA.RCA:RCA_policy",
    "RCA_prob":"policies.RCA_prob.RCA:RCA_policy",
    "RCA_val":"policies.RCA_val.RCA:RCA_policy",
    "RCA_Clip":"policies.RCA_Clip.RCA:RCA_policy",
    "RCA_EMACacheCost":"policies.RCA_EMACacheCost.RCA:RCA_policy",
    "RCA_aging":"policies.RCA_aging.RCA:RCA_policy",
    "RCA_Init":"policies.RCA_Init.RCA:RCA_policy",


    }


# from policies.my_method import my_method

def load_policy(policy_name):
    module_path, class_name = policy_registry[policy_name].split(":")
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def parse_config(exp_name):
    
    #開啟config
    config=None
    config_path="experiments/"+exp_name+"/config.json"
    with open(config_path,"r") as f:
        config=json.load(f)

    #拆出各自config
    basic_config=config["basic_config"]
    policy_config=config["policy_config"]
    evaluator_config=config["evaluator_config"]

    #初始化各功能
    trace_path = "trace/"+basic_config["trace"]
    policy_class = load_policy(basic_config["policy"])
    policy = policy_class(policy_config)
    evaluator = CacheEvaluator(evaluator_config, exp_name)


    return policy,trace_path,evaluator, config




if __name__ == "__main__":
    #取得實驗名稱
    if len(sys.argv)==2:
        try:
            exp=sys.argv[1]
            open("experiments/"+exp+"/config.json",'r')
        except Exception as e:
            print(e)
            sys.exit()
    else:
        print("參數格式:")
        print("python run.py [experiment_name]")
        print("EX: python run.py 05_wikI_LRU_seg0")
        sys.exit()
    # exp_name=sys.argv[1]
    # exp_name="exampleLFU"
    # exp_name="exampleLRU"
    # exp_name="TCN_test"
    # exp_name="TCN_twitter"
    
    policy,trace_path,evaluator, config= parse_config(exp) # 設置完的policy 和 policy



    print("config: ")
    print(json.dumps(config, indent=4, ensure_ascii=False))  # ✅漂亮縮排

    with open(trace_path,"r")as f:
        for req in f:
            temp=req.split()
            o_id = temp[0]
            o_size = temp[1]
            o_features = temp[2:]
            hit , debug_msg=policy.request(o_id,o_size,o_features)
            evaluator.record(hit,o_size, debug_msg) #會順便show進度
        evaluator.save_result()

    print("config: ")
    print(json.dumps(config, indent=4, ensure_ascii=False))  # ✅漂亮縮排
