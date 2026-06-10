import os
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="result folder")
args = parser.parse_args()

folder = args.folder

result = []
files = []
#max_i = -1
for f in os.listdir(folder):
    if f.startswith("0_"):
        try:
            idx = int(f.split("_")[1])
            files.append((idx, f))
 #           max_i = max(max_i,idx)
        
        except ValueError:
            pass

files.sort(key=lambda x: x[0])

for _, filename in files:
    with open(os.path.join(folder, filename), "rb") as fp:
        data = pickle.load(fp)

    result.append(data["ML-LRU-DET-3635"][0][0])

#print(result)
print("OHR: ", sum(result)/len(result))
#print("last: ", max_i)

