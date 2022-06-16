# %%
import pandas as pd
import yfinance as yf
import bt
%matplotlib inline

# 정적 자산배분 백테스트

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")

portfolios = [
    # 황금나비(Golden Butterfly, GB)
    # https://lazyquant.xyz/allocation/detail/GB
    {
        "name": "GB_ORG",  #
        "weight": {"SPY": 0.2, "QQQ": 0.2, "GLD": 0.2, "TLT": 0.2, "SHY": 0.2}
    },
    # 황금나비 커스텀(Golden Butterfly Custom, GB2)
    {
        "name": "GB_CT2",  # golden butterfly
        "weight": {"SPY": 0.2, "QQQ": 0.2, "GLD": 0.2, "TLT": 0.1, "SHY": 0.2, "SCHD": 0.1}
    },
    # 황금나비 커스텀(Golden Butterfly Custom, GB3)
    {
        "name": "GB_CT3",  # golden butterfly # Winner
        "weight": {"SPY": 0.2, "QQQ": 0.2, "GLD": 0.1, "TLT": 0.2, "SHY": 0.1, "TIP": 0.1, "SCHD": 0.1}
    },
    # 황금나비 변형1 AOM 50%
    {
        "name": "GB_AOM50",  # golden butterfly custom
        "weight": {"AOM": 0.5, "QQQ": 0.2, "GLD": 0.2, "SCHD": 0.1}
    },
    # 황금나비 변형2 AOM 40%
    {
        "name": "GB_AOM40_1",
        "weight": {"AOM": 0.40, "QQQ": 0.20, "GLD": 0.2, "SCHD": 0.2}
    },
    # 황금나비 변형2 AOM 40%
    {
        "name": "GB_AOM40_2",
        "weight": {"AOM": 0.40, "QQQ": 0.20, "GLD": 0.10, "SCHD": 0.20, "VNQ": 0.1}
    },
    # 황금나비 변형2 AOM 40%
    {
        "name": "GB_AOM40_3",
        "weight": {"AOM": 0.40, "QQQ": 0.20, "TIP": 0.10, "SCHD": 0.20, "VNQ": 0.1}
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
