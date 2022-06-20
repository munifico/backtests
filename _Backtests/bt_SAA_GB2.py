# %%
import yfinance as yf
import bt
from btpp.strategy import saa_weight_strategy
%matplotlib inline

#########################################
# Code For Static Assets Allocation Strategy(SAA)
# 정적 자산배분 백테스트
# 황금나비(Golden Butterfly, GB) 포트폴리오에 대해 알아보자 !!!
#########################################


# %%

#########################################
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
