from hikyuu.interactive import *
from matplotlib import pylab as plt

plt.rcParams['interactive'] = False

newsm = []
for stock in sm:
    if stock.market == "SZ" or stock.market == "SH":
        if stock.last_datetime > Datetime("2023-07-12"):
            codeStr = str(stock.code)
            name = str(stock.name)
            if codeStr.startswith("0") or codeStr.startswith("6") or codeStr.startswith("3"):
                if not name.startswith("-") and not name.startswith("ST") and not name.startswith(
                        "*ST") and not name.endswith("退") and not name.startswith("XD") and not name.startswith("N"):
                    newsm.append(stock)
print(len(newsm))
for stock in newsm:
    k = stock.get_kdata(Query(-2))
    today_k = k[1]
    pre_k = k[0]
    volumeRatio = today_k.amount / pre_k.amount
    # 放量 涨幅0~7 成交额>2亿
    if volumeRatio > 2.5 and today_k.amount > 20000 and 0 < ROC(CLOSE(k), 1).to_np()[-1] < 7:
        _this_close = today_k.close
        _this_open = today_k.open
        ma20 = round(MA(CLOSE(k), 20).to_np()[-1], 2)
        ma10 = round(MA(CLOSE(k), 10).to_np()[-1], 2)
        ma5 = round(MA(CLOSE(k), 5).to_np()[-1], 2)
        ma60 = round(MA(CLOSE(k), 60).to_np()[-1], 2)
        # 阳线上穿5日 多头散发
        if _this_open < ma5 < _this_close and _this_close > ma60 and ma5 > ma10 > ma20:
            today_hsl = HSL(k).to_np()[-1]
            # 换手 8~30
            if today_hsl > 8 and today_hsl < 30:
                capital = LIUTONGPAN(k)[-1]
                # 流通市值 20亿~500亿
                if _this_close * capital > 20000 and _this_close * capital < 500000:
                    print("%s %s" % (stock.market_code, stock.name))
