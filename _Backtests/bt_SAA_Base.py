# %%
import yfinance as yf
import bt
from btpp.strategy import saa_weight_strategy
%matplotlib inline

#########################################
# Code For Static Assets Allocation Strategy(SAA)
# 정적 자산배분 백테스트
# 익히 알려진 자산배분 방법 백테스트
#########################################

# %%

#########################################
# d = bt.get(["spy", "agg"], start="2010-01-01")

portfolios = [
    # benchmark
    {
        "name": "BM",
        "weight": {"SPY": 1}
    },
    # 카우치 포테이토
    # https://lazyquant.xyz/allocation/detail/CP
    {
        "name": "CP",
        "weight": {"SPY": 0.50, "TIP": 0.50}
    },
    # 영구 포트폴리오(Permanent Portfolio, PP)
    # https://lazyquant.xyz/allocation/detail/PP
    {
        "name": "PP",
        "weight": {"SPY": 0.25, "GLD": 0.25, "TLT": 0.25, "BIL": 0.25}
    },
    # 황금나비(Golden Butterfly Portfolio, GB)
    # https://lazyquant.xyz/allocation/detail/GB
    {
        "name": "GB",
        "weight": {"SPY": 0.2, "QQQ": 0.2, "GLD": 0.2, "TLT": 0.2, "SHY": 0.2}
    },
    # 예일대 기금
    # https://lazyquant.xyz/allocation/detail/YE
    {
        "name": "YE",
        "weight": {"SPY": 0.30, "VNQ": 0.20, "VEA": 0.15, "EEM": 0.5, "TLT": 0.15, "TIP": 0.15}
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
