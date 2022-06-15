# %%
import pandas as pd
import yfinance as yf
import bt
%matplotlib inline

# %%
# https: // pmorissette.github.io/bt/_modules/bt/algos.html#StatTotalReturn


class StatRelativeReturn(bt.Algo):

    def __init__(
        self,
        lookbacks=[
            pd.DateOffset(months=1),
            pd.DateOffset(months=3),
            pd.DateOffset(months=6),
            pd.DateOffset(months=12)
        ],
        lookback_weights=[0.3, 0.3, 0.3, 0],
        lag=pd.DateOffset(days=0)
    ):

        super(StatRelativeReturn, self).__init__()
        self.lookbacks = lookbacks
        self.lookback_weights = lookback_weights
        self.lag = lag

    def __call__(self, target):
        stat = []
        selected = target.temp["selected"]
        for i, lookback in enumerate(self.lookbacks):
            t0 = target.now - self.lag
            prc = target.universe.loc[t0 - lookback: t0, selected]
            stat.append(prc.calc_total_return() * self.lookback_weights[i])
        target.temp["stat"] = sum(stat)
        return True
# %%
# https://pmorissette.github.io/bt/_modules/bt/algos.html#SelectMomentum


class SelectRelativeMomentum(bt.AlgoStack):

    def __init__(
        self,
        n=1,
        lookbacks=[
            pd.DateOffset(months=1),
            pd.DateOffset(months=3),
            pd.DateOffset(months=6),
            pd.DateOffset(months=12)
        ],
        lookback_weights=[0.3, 0.3, 0.3, 0],
        lag=pd.DateOffset(days=0),
        sort_descending=True,
        all_or_none=False
    ):
        super(SelectRelativeMomentum, self).__init__(
            StatRelativeReturn(
                lookbacks=lookbacks,
                lookback_weights=lookback_weights,
                lag=lag
            ),
            bt.algos.SelectN(
                n=n,
                sort_descending=sort_descending,
                all_or_none=all_or_none
            ),
        )


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
test1 = bt.Backtest(get_momentum_strategy('m1', [1, 3, 6], [1, 1, 1]), d)
# 3개월 수익률 최대 종목을 선택할 경우
test3 = bt.Backtest(get_momentum_strategy('m3', [1, 3, 6], [6, 2, 1]), d)
# 6개월 수익률 최대 종목을 선택할 경우
test6 = bt.Backtest(get_momentum_strategy('m6', [1, 3, 6], [1, 2, 6]), d)
res = bt.run(test1, test3, test6)

# %%
res.display()

# %%
res.plot()

# %%
# res.prices

# %%
# res.stats

# %%
