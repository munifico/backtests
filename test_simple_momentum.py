# %%
import pandas as pd
import yfinance as yf
import bt
%matplotlib inline

# %%


def get_momentum_strategy(name, lookback_month):
    layer = [
        bt.algos.RunMonthly(),
        bt.algos.SelectAll(),
        bt.algos.SelectMomentum(
            n=1,
            lookback=pd.DateOffset(months=lookback_month),
            lag=pd.DateOffset(days=0)),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance()
    ]
    return bt.Strategy(name, layer)


# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'를 이용하여 가격 조정
d = yf.download(["spy", "qqq", "vwo", "tlt", "shy"],
                start="2010-01-01",
                end="2019-12-12")['Adj Close']
print(d.head())

# %%
# 1개월 수익률 최대 종목을 선택할 경우
test1 = bt.Backtest(get_momentum_strategy('m1', 1), d)
# 3개월 수익률 최대 종목을 선택할 경우
test3 = bt.Backtest(get_momentum_strategy('m3', 3), d)
# 6개월 수익률 최대 종목을 선택할 경우
test6 = bt.Backtest(get_momentum_strategy('m6', 6), d)
res = bt.run(test1, test3, test6)

# %%
res.display()

# %%
res.plot()

# %%
res.prices

# %%
res.stats

# %%
