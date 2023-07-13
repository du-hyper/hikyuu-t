
from hikyuu.interactive import *
from matplotlib import pylab as plt

plt.rcParams['interactive'] = False


tradingCalendar = sm.get_trading_calendar(Query(-90), 'SH')
print(str(tradingCalendar[0]))
# bottom huge volume 天创时尚 sh603608
LIUTONGPAN
stk = sm['sh603608']
print(stk.get_finance_info())
print(stk.start_datetime > Datetime("2016-02-17"))
k = stk.get_kdata(Query(start=tradingCalendar[0], end=tradingCalendar[21]))
print(LIUTONGPAN(k)[-1])
print(k[-2])
KRecord
KData
print(k[0].close)
print(k[1].close)
print(MA(CLOSE(k), 20).to_np()[-1])
# today_k = k[1]
# pre_k = k[0]
# print(pre_k.amount)
# print(today_k.amount)
# print(today_k.amount / pre_k.amount)
# zf = today_k.high / today_k.low
# print("振幅： %s" % roundDown(((zf - 1) * 100), 2))
#
# today_roc = ROC(CLOSE(k), 1).to_np()[-1]
# print("涨幅： %s" % roundDown(today_roc, 2))
#
# today_hsl = HSL(k).to_np()[-1]
# print("换手率： %s" % roundDown(today_hsl, 2))
#
# t = stk.get_trans_list(Query(start=Datetime.today()))
# buyMax = 0
# sellMax = 0
# auctionMax = 0
# for m in t:
#     if m.direct == 0:
#         buyMax = max(m.vol, buyMax)
#     elif m.direct == 1:
#         sellMax = max(m.vol, sellMax)
#     else:
#         auctionMax = max(m.vol, auctionMax)
#
# print("分时最大买： %s" % buyMax)
# print("分时最大卖： %s" % sellMax)
# print("分时最大平： %s" % auctionMax)