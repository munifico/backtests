# %%
import pandas as pd
import yfinance as yf
import bt
%matplotlib inline

# 정적 자산배분 백테스트
# Couch Potato(CP)에 대해 알아보자 !!!

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")

portfolios = [
    # Couch Potato(CP)
    # https://lazyquant.xyz/allocation/detail/CP
    {
        "name": "CP_ORG",
        "weight": {"SPY": 0.5, "SCHP": 0.5}
    },
    # CP custom
    {
        "name": "CP_ORG+",
        "weight": {"SPY": 0.4, "SCHP": 0.4, "QQQ": 0.1, "SCHD": 0.1}
    },
    # CP AOA 60%
    {
        "name": "CP_AOA60",
        "weight": {"AOA": 0.6, "SCHP": 0.4}
    },
    # CP AOA 60%+
    {
        "name": "CP_AOA60+",
        "weight": {"AOA": 0.6, "SCHP": 0.2, "QQQ": 0.1, "SCHD": 0.1}
    },
    # CP AOR 50%
    {
        "name": "CP_AOR80",
        "weight": {"AOR": 0.80, "SCHP": 0.2}
    },
    # GB AOM 40%
    {
        "name": "GB_AOM40",
        "weight": {"AOM": 0.40, "QQQ": 0.2, "SCHD": 0.2, "GLD": 0.1, "VNQ": 0.1}
    },
    # Benchmark
    {
        "name": "Benchmark",
        "weight": {"AOR": 1.0}
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
        # bt.algos.RunMonthly(),
        bt.algos.RunYearly(),
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
