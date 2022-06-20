# %%
import yfinance as yf
import bt
from btpp.strategy import saa_weight_strategy
%matplotlib inline


#########################################
# Code For Static Assets Allocation Strategy(SAA)
# 정적 자산배분 백테스트
# Couch Potato(CP)에 대해 알아보자 !!!
#########################################


# %%

#########################################
# d = bt.get(["spy", "agg"], start="2010-01-01")

portfolios = [
    # Couch Potato(CP)
    # https://lazyquant.xyz/allocation/detail/CP
    {
        "name": "CP_ORG",
        "weight": {"SPY": 0.5, "TIP": 0.5}
    },
    # CP custom
    {
        "name": "CP_ORG+",
        "weight": {"SPY": 0.4, "TIP": 0.4, "QQQ": 0.1, "SCHD": 0.1}
    },
    # CP AOA 60%
    {
        "name": "CP_AOA60",
        "weight": {"AOA": 0.6, "TIP": 0.4}
    },
    # CP AOA 60%+
    {
        "name": "CP_AOA60+",
        "weight": {"AOA": 0.6, "TIP": 0.2, "QQQ": 0.1, "SCHD": 0.1}
    },
    # CP AOR 50%
    {
        "name": "CP_AOR80",
        "weight": {"AOR": 0.80, "TIP": 0.2}
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

start_trading_date = "2000-01-01"
end_trading_date = "2021-12-12"
#########################################
# %%
_tickers = sum([list(it["weight"].keys()) for it in portfolios], [])
tickers = list(set(_tickers))
print("# Tickers: ")
print(tickers)

# %%
d = yf.download(tickers,
                start=start_trading_date,
                end=end_trading_date)['Adj Close'].dropna()
print(d.head())


# %%
strategys = [saa_weight_strategy(
    pf["name"],
    assets_with_weight=pf["weight"],
    run_term="yearly")
    for pf in portfolios]
tests = [bt.Backtest(s, d) for s in strategys]
res = bt.run(*tests)

# %%
res.display()

# %%
res.plot()

# %%
# dir(res)
