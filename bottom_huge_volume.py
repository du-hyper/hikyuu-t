from hikyuu.interactive import *
from matplotlib import pylab as plt

plt.rcParams['interactive'] = False

newsm = []
for stock in sm:
    if stock.market == "SZ" or stock.market == "SH":
        codeStr = str(stock.code)
        name = str(stock.name)
        if codeStr.startswith("0") or codeStr.startswith("6") or codeStr.startswith("3"):
            if not name.startswith("-") and not name.startswith("ST") and not name.startswith(
                    "*ST") and not name.endswith("退") and not name.startswith("XD") and not name.startswith("N"):
                newsm.append(stock)

res1 = []
res2 = []
res3 = []
res4 = []
res5 = []

for stock in newsm:
    k = stock.get_kdata(Query(-2))
    today_k = k[1]
    pre_k = k[0]
    volumeRatio = today_k.amount / pre_k.amount
    # 放量
    if volumeRatio > 2 and today_k.amount > 20000 and -2 < ROC(CLOSE(k), 1).to_np()[-1] < 9.95:
        res1.append(stock.name + stock.code)
        _this_close = today_k.close
        _this_open = today_k.open
        k = stock.get_kdata(Query(-90))
        ma20 = MA(CLOSE(k), 20).to_np()[-1]
        ma10 = MA(CLOSE(k), 10).to_np()[-1]
        ma5 = MA(CLOSE(k), 5).to_np()[-1]
        ma60 = MA(CLOSE(k), 60).to_np()[-1]
        # 一阳穿3线 收盘价>60日均线
        if _this_open < ma5 and _this_open < ma10 and _this_open < ma20 and _this_close > ma5 and _this_close > ma10 \
                and _this_close > ma20 and _this_close > ma60:
            res2.append(stock.name + stock.code)
            today_hsl = HSL(k).to_np()[-1]
            # 换手<20%
            if today_hsl < 20:
                res3.append(stock.name + stock.code)
                hhv90 = HHV(CLOSE(k), 90).to_np()[-1]
                # 光脚长上影
                if (abs(_this_open - today_k.low) / _this_close) < 0.005 and (
                        abs(today_k.high - _this_close) / _this_close) > 0.03:
                    res5.append(stock.name + stock.code)
                # 收盘价<90日最高价
                if _this_close < hhv90:
                    res4.append(stock.name + stock.code)
print("================================")
print("条件：【2倍放量 成交额>2亿 涨幅在-2 ~ 9.95之间】")
print("数量: %s" % len(res1))
print(res1)
print("================================")
print("条件：【2倍放量 成交额>2亿 涨幅在-2 ~ 9.95之间 一阳穿3线】")
print("数量: %s" % len(res2))
print(res2)
print("================================")
print("条件：【2倍放量 成交额>2亿 涨幅在-2 ~ 9.95之间 一阳穿3线 收盘价>60日线 换手<20%】")
print("数量: %s" % len(res3))
print(res3)
print("================================")
print("条件：【2倍放量 成交额>2亿 涨幅在-2 ~ 9.95之间 一阳穿3线 收盘价>60日线 换手<20% 收盘价<90日最高价】")
print("数量: %s" % len(res4))
print(res4)
print("================================")
print("条件：【2倍放量 成交额>2亿 涨幅在-2 ~ 9.95之间 一阳穿3线 收盘价>60日线 换手<20% 光脚长上影】")
print("数量: %s" % len(res5))
print(res5)
print("================================")

