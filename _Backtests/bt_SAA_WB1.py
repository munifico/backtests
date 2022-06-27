# %%
import yfinance as yf
import bt
from btpp.strategy import saa_weight_strategy
%matplotlib inline

#########################################
# Code For Static Assets Allocation Strategy(SAA)
# 정적 자산배분 백테스트
# Warren Buffett 포트폴리오(WB)에 대해 알아보자 !!!
#########################################


# %%

#########################################

portfolios = [
    # Warren Buffett(WB)
    # https://lazyquant.xyz/allocation/detail/WB
    {
        "name": "WB_ORG",
        "weight": {"SPY": 0.9, "TIP": 0.1}
    },
    {
        "name": "WB1",
        "weight": {"SPY": 0.9, "TLT": 0.1}
    },
    {
        "name": "WB2",
        "weight": {"SPY": 0.9, "SHY": 0.1}
    },
    # CP custom
    {
        "name": "WB3",
        "weight": {"SPY": 0.45, "QQQ": 0.45, "TLT": 0.1}
    },
    {
        "name": "WB4",
        "weight": {"SPY": 0.45, "QQQ": 0.45, "TIP": 0.1}
    },
    # CP custom
    {
        "name": "WB5",
        "weight": {"SPY": 0.45, "QQQ": 0.45, "GLD": 0.1}
    },
    # Benchmark
    {
        "name": "WB6",
        "weight": {"SPY": 0.30, "QQQ": 0.30, "VNQ": 0.30, "TLT": 0.1}
    },
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
