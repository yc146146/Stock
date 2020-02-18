import pandas as pd

file_all = pd.read_csv("./all.csv")
file_a = pd.read_csv("a.csv")
file_b = pd.read_csv("b.csv")


file_all.set_index("data", inplace=True)
file_a.set_index("data", inplace=True)
file_b.set_index("data", inplace=True)

file_a.rename(columns={"all_num":"a_num"}, inplace=True)

# print(file_all)
# print(file_a)
# print(file_b)

#交集
# res = pd.merge(file_all, file_a, how="inner", on="data")
#并集
# res = pd.merge(file_all, file_a, how="outer", on="data")
res = pd.merge(file_all, file_a, how="outer", on="data")
res = pd.merge(res, file_b, how="outer", on="data")

# res = pd.merge(file_all, file_a, how="left", on="data")
# res = pd.merge(file_all, file_a, how="right", on="data")

print(res)

