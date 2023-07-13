from hikyuu.interactive import *
from matplotlib import pylab as plt

plt.rcParams['interactive'] = False
stk = sm['sh603608']
tradingCalendar = sm.get_trading_calendar(Query(-360), 'SH')

k = stk.get_kdata(Query(start=tradingCalendar[0]))
for ss in k:
    print(ss)
today_k = k[-1]
pre_k = k[-2]
print("info: %s" % stk)
print("今日K: %s" % today_k)
print("昨日K: %s" % pre_k)
print("涨幅: %s" % ROC(CLOSE(k), 1).to_np()[-1])
print("ma60: %s" % round(MA(CLOSE(k), 60).to_np()[-1], 2))
print("ma20: %s" % round(MA(CLOSE(k), 20).to_np()[-1], 2))
print("ma10: %s" % round(MA(CLOSE(k), 10).to_np()[-1], 2))
print("ma5: %s" % round(MA(CLOSE(k), 5).to_np()[-1], 2))
print("流通股: %s" % LIUTONGPAN(k)[-1])