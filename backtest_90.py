from hikyuu.interactive import *
from matplotlib import pylab as plt

plt.rcParams['interactive'] = False

newsm = []
for stock in sm:
    if stock.market == "SZ" or stock.market == "SH":
        if stock.start_datetime < Datetime("2022-01-01") and stock.last_datetime > Datetime("2023-07-11"):
            codeStr = str(stock.code)
            name = str(stock.name)
            if codeStr.startswith("0") or codeStr.startswith("6") or codeStr.startswith("3"):
                if not name.startswith("-") and not name.startswith("ST") and not name.startswith(
                        "*ST") and not name.endswith("退") and not name.startswith("XD") and not name.startswith("N"):
                    newsm.append(stock)

tradingCalendar = sm.get_trading_calendar(Query(-180), 'SH')
market_code = {}
trading_detail = {}

def tomorrowBuy(i):
    for stock in newsm:
        k = stock.get_kdata(Query(start=tradingCalendar[0], end=tradingCalendar[i + 90]))
        today_k = k[-1]
        pre_k = k[-2]
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
                    if (i + 92) < len(tradingCalendar):
                        weights = stock.get_weight(tradingCalendar[i + 90], tradingCalendar[i + 92])
                        # 排除分红除权的
                        if len(weights) == 0:
                            capital = LIUTONGPAN(k)[-1]
                            # 流通市值 20亿~500亿
                            if _this_close * capital > 20000 and _this_close * capital < 500000:
                                market_code[str(tradingCalendar[i + 90])] = stock.market_code
                                return

def todaySell(i):
    if i < 89 and market_code.get(str(tradingCalendar[i + 88])):
        k = sm[market_code[str(tradingCalendar[i + 88])]].get_kdata(Query(start=tradingCalendar[i + 89]))
        trading_detail[market_code.get(str(tradingCalendar[i + 88]))]["sell_price"] = round(k[0].close, 2)
        trading_detail[market_code.get(str(tradingCalendar[i + 88]))]["sell_time"] = str(tradingCalendar[i + 89])

def buy(i):
    if i < 90 and market_code.get(str(tradingCalendar[i + 89])):
        k = sm[market_code[str(tradingCalendar[i + 89])]].get_kdata(Query(start=tradingCalendar[i + 89]))
        trading_detail[market_code.get(str(tradingCalendar[i + 89]))] = {
            "buy_price": round(k[0].open, 2),
            "buy_time": str(tradingCalendar[i + 89])
        }

for i in range(0, 89):
    buy(i)
    todaySell(i)
    tomorrowBuy(i)

amount = 100000
start = 1
print("起始资金: %s" % amount)
for k in trading_detail.keys():
    detail = trading_detail[k]
    if detail.get("buy_price") and detail.get("sell_price"):
        buy_price = detail["buy_price"]
        buy_num = int(amount / buy_price / 100) * 100
        amount = amount - (buy_num * buy_price)
        sell_price = detail["sell_price"]
        amount = amount + (buy_num * sell_price)
        print("第 %s 次：【%s】 %s 买入数量：%s 买入价格：%s, %s 卖出数量：%s 卖出价格：%s, 总资金：%s" % (start, k, detail["buy_time"], buy_num, buy_price, detail["sell_time"], buy_num, sell_price, amount ))
        start = start+1
print("期末资金: %s" % amount)

