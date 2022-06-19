# %%
import pandas as pd
import yfinance as yf
import bt
from lib.maa import SelectRelativeMomentum
%matplotlib inline

#########################################
# Code For Relative Momentum Strategy(RM)
#########################################

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'를 이용하여 가격 조정
tickers = ["SPY", "QQQ", "VWO", "TLT"]
_d = yf.download(tickers, start="2006-01-01", end="2019-12-12")
d = _d['Adj Close'].dropna()
print(d.head())

# %%


def get_momentum_strategy(name, lookbacks, lookback_weights):
    layer = [
        bt.algos.RunMonthly(),
        bt.algos.SelectAll(),
        SelectRelativeMomentum(
            lookbacks=[pd.DateOffset(months=e) for e in lookbacks],
            lookback_weights=lookback_weights
        ),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance(),
        bt.algos.PrintTempData()
    ]
    return bt.Strategy(name, layer)


# %%
# Benchmark
bm_layer = [
    bt.algos.RunMonthly(),
    bt.algos.SelectAll(),
    bt.algos.WeighEqually(),
    bt.algos.Rebalance()
]
bm_st = bt.Strategy('Benchmark', bm_layer)
benchmark = bt.Backtest(bm_st, d)

# %%

# 모멘텀 가중치를 바꾸어가며 테스트
test1 = bt.Backtest(
    get_momentum_strategy('m6:2:1', [1, 3, 6], [6, 2, 1]), d)
test2 = bt.Backtest(
    get_momentum_strategy('m5:3:2', [1, 3, 6], [5, 3, 2]), d)
test3 = bt.Backtest(
    get_momentum_strategy('m1:1:1', [1, 3, 6], [1, 1, 1]), d)
test4 = bt.Backtest(
    get_momentum_strategy('m2:3:5', [1, 3, 6], [2, 3, 5]), d)
test5 = bt.Backtest(
    get_momentum_strategy('m1:2:6', [1, 3, 6], [1, 2, 6]), d)
test6 = bt.Backtest(
    get_momentum_strategy('m12:4:2:1', [1, 3, 6, 12], [12, 4, 2, 1]), d)

# %%
res = bt.run(benchmark, test1, test2, test3, test4, test5, test6)

# %%
res.display()

# %%
res.plot()

# %%
# res.prices

# %%
# res.stats
