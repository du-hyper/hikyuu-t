from hikyuu.interactive import *
from matplotlib import pylab as plt

plt.rcParams['interactive'] = False


def getNextWeekDate(week):
    """获取指定日期的下一周周一日期"""
    from datetime import timedelta
    py_week = week.datetime()
    next_week_start = py_week + timedelta(days = 7 - py_week.weekday())
    return Datetime(next_week_start)


def DEMO_SG(self):
    """
    买入信号：周线MACD零轴下方底部金叉，即周线的DIF>DEA金叉时买入
    卖出信号：日线级别 跌破 20日均线

    参数：
    week_macd_n1：周线dif窗口
    week_macd_n2: 周线dea窗口
    week_macd_n3: 周线macd平滑窗口
    day_n: 日均线窗口
    """
    k = self.to
    if (len(k) == 0):
        return

    stk = k.get_stock()

    # -----------------------------
    # 计算日线级别的卖出信号
    # -----------------------------
    day_c = CLOSE(k)
    day_ma = MA(day_c, self.get_param("day_n"))
    day_x = day_c < day_ma  # 收盘价小于均线
    for i in range(day_x.discard, len(day_x)):
        if day_x[i] >= 1.0:
            self._add_sell_signal(k[i].datetime)

    # -----------------------------
    # 计算周线级别的买入信号
    # -----------------------------
    week_q = Query(k[0].datetime, k[-1].datetime.next_day(), ktype=Query.WEEK)
    week_k = k.get_stock().get_kdata(week_q)

    n1 = self.get_param("week_macd_n1")
    n2 = self.get_param("week_macd_n2")
    n3 = self.get_param("week_macd_n3")
    m = MACD(CLOSE(week_k), n1, n2, n3)
    fast = m.get_result(0)
    slow = m.get_result(1)

    discard = m.discard if m.discard > 1 else 1
    for i in range(discard, len(m)):
        if (fast[i - 1] < slow[i - 1] and fast[i] > slow[i]):
            # 当周计算的结果，只能作为下周一的信号
            self._add_buy_signal(week_k[i].datetime.next_week())


class DEMO_MM(MoneyManagerBase):
    """
    买入：30% （不明确，暂且当做当前现金的30%）
    卖出：已持仓股票数的50%
    """

    def __init__(self):
        super(DEMO_MM, self).__init__("MACD_MM")

    def _reset(self):
        pass

    def _clone(self):
        return DEMO_MM()

    def _get_buy_num(self, datetime, stk, price, risk, part_from):
        tm = self.tm
        cash = tm.current_cash

        # 可以不用考虑最小交易单位的问题，已经自动处理
        # num = int((cash * 0.3 // price // stk.atom) * stk.atom)
        return int(cash * 0.3 / price)  # 返回类型必须是int

    def _get_sell_num(self, datetime, stk, price, risk, part_from):
        tm = self.tm
        position = tm.get_position(datetime, stk)
        total_num = position.number
        num = int(total_num * 0.5)
        return num if num >= 100 else 0


#账户参数
init_cash = 100000 #账户初始资金
init_date = Datetime('2020-1-1') #账户建立日期
#信号指示器参数
week_n1 = 12
week_n2 = 26
week_n3 = 9
day_n = 20
#选定标的，及测试区间
stk = sm['sz000858']
start_date = Datetime('2020-1-1')  #如果是同一级别K线，可以使用索引号，使用了不同级别的K线数据，建议还是使用日期作为参数
end_date = Datetime()
#创建账户
my_tm = crtTM(date=init_date, init_cash = init_cash, cost_func=TC_FixedA())
#创建系统实例
my_sys = SYS_Simple()
#绑定账户
my_sys.tm = my_tm
#绑定信号指示器
my_sys.sg = crtSG(DEMO_SG,
              {'week_macd_n1': week_n1, 'week_macd_n2': week_n2, 'week_macd_n3': week_n3, 'day_n': day_n},
                'DEMO_SG')
my_sys.sg.set_param('alternate', False)
#绑定资金管理策略
my_sys.mm = DEMO_MM()

iodog.close()
q = Query(start_date, end_date, ktype=Query.DAY)
my_sys.run(stk, q)

# 将交易记录及持仓情况，保存在临时目录，可用Excel查看
# 临时目录一般设置在数据所在目录下的 tmp 子目录
# 如果打开了excel记录，再次运行系统前，记得先关闭excel文件，否则新的结果没法保存
my_tm.tocsv(sm.tmpdir())

# 绘制资金收益曲线（净收益）
# x = my_tm.get_profit_curve(stk.get_datetime_list(q), Query.DAY)
# 总资产曲线
# x = my_tm.getFundsCurve(stk.getDatetimeList(q), KQuery.DAY)
# x = PRICELIST(x)
# x.plot()

# 回测统计
per = Performance()
print(per.report(my_tm, Datetime.now()))

my_sys.plot()
MA(CLOSE(my_sys.to), 20).plot(new=False)
plt.show()

# 回测统计
# per = Performance()
# print(per.report(my_tm, Datetime.now()))

# my_sys.plot()
# MA(CLOSE(my_sys.to), 20).plot(new=False)