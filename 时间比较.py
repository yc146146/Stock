# import time
# def compare_time(time1,time2):
#     s_time = time.mktime(time.strptime(time1,'%Y-%m-%d'))
#     e_time = time.mktime(time.strptime(time2,'%Y-%m-%d'))
#     print('s_time is:',s_time)
#     print('e_time is:',e_time)
#     return int(s_time) - int(e_time)

# result = compare_time('2017-04-17','2017-04-19')
# print('the compare result is:',result)


import datetime
date1 = datetime.datetime.strptime("2017-04-17","%Y-%m-%d")
date2 = datetime.datetime.strptime("2017-04-19","%Y-%m-%d")
# 结果:47
print((date2 - date1).days)