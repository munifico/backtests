# %%
import pandas as pd
import yfinance as yf
import bt
%matplotlib inline

# 정적 자산배분 백테스트

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")

portfolios = [
    # benchmark
    {
        "name": "BM",  # Permanent Portfolio
        "weight": {"SPY": 1}
    },
    # 카우치 포테이토
    # https://lazyquant.xyz/allocation/detail/CP
    {
        "name": "CP",  # Permanent Portfolio
        "weight": {"SPY": 0.50, "TIP": 0.50}
    },
    # 영구 포트폴리오
    # https://lazyquant.xyz/allocation/detail/PP
    {
        "name": "PP",  # Permanent Portfolio
        "weight": {"SPY": 0.25, "GLD": 0.25, "TLT": 0.25, "BIL": 0.25}
    },
    # 황금나비
    # https://lazyquant.xyz/allocation/detail/GB
    {
        "name": "GB",  # golden butterfly
        "weight": {"SPY": 0.2, "QQQ": 0.2, "GLD": 0.2, "TLT": 0.2, "SHY": 0.2}
    },
    # 황금나비 변형
    #
    {
        "name": "GB2",  # golden butterfly custom
        "weight": {"SPY": 0.3, "QQQ": 0.3, "GLD": 0.2, "TLT": 0.1, "SHY": 0.1}
    },
    # 예일대 기금
    # https://lazyquant.xyz/allocation/detail/YE
    {
        "name": "YE",
        "weight": {"SPY": 0.30, "VNQ": 0.20, "VEA": 0.15, "EEM": 0.5, "TLT": 0.15, "TIP": 0.15}
    }
]

# %%
_tickers = sum([list(it["weight"].keys()) for it in portfolios], [])
tickers = list(set(_tickers))
print("# Tickers: ")
print(tickers)

# %%
d = yf.download(tickers,
                start="2010-01-01",
                end="2019-12-12")['Adj Close'].dropna()
print(d.head())


# %%
def get_strategy(name, weight):
    s_layer = [
        bt.algos.RunMonthly(),
        bt.algos.SelectAll(),
        # bt.algos.WeighEqually(),\
        bt.algos.WeighSpecified(**weight),
        bt.algos.Rebalance()
    ]
    return bt.Strategy(name, s_layer)


# %%
strategys = [get_strategy(pf["name"], pf["weight"]) for pf in portfolios]
tests = [bt.Backtest(s, d) for s in strategys]
res = bt.run(*tests)

# %%
res.display()

# %%
res.plot()

# %%
# dir(res)
