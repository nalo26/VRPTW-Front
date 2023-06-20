import os
import math

from file_parser import parse

for file in os.listdir("datas"):
    if not file.endswith(".vrp"):
        continue

    with open(os.path.join("datas", file), "r") as f:
        content = f.read()
        data = parse(content)
    # print(data)
    sum_demand = sum([c["demand"] for c in data["clients"][1:]])
    capacity = data["headers"]["MAX_QUANTITY"]
    min_truck = math.ceil(sum_demand / capacity)

    print(f"{file}: {min_truck}")
