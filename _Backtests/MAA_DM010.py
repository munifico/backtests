# %%
import yfinance as yf
import bt
from btpp.strategy import dual_momentum_strategy, saa_weight_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
%matplotlib inline

#########################################
# Code For Dual Momentum Strategy(DM)
#########################################

# %%
#########################################
portfolios = [
    {
        "name": "SPY/TLT",
        "in_market": ["SPY"],
        "out_market": ["TLT"]
    },
    {
        "name": "QQQ/TLT",
        "in_market": ["QQQ"],
        "out_market": ["TLT"]
    },
    {
        "name": "VWO/TLT",
        "in_market": ["VWO"],
        "out_market": ["TLT"]
    },
    {
        "name": "SPY/TIP",
        "in_market": ["SPY"],
        "out_market": ["TIP"]
    },
    {
        "name": "QQQ/TIP",
        "in_market": ["QQQ"],
        "out_market": ["TIP"]
    },
    {
        "name": "VWO/TIP",
        "in_market": ["VWO"],
        "out_market": ["TIP"]
    },
    {
        "name": "SPY+T/BIL",
        "in_market": ["SPY", "TLT"],
        "out_market": ["BIL"]
    },
    {
        "name": "QQQ+T/BIL",
        "in_market": ["QQQ", "TLT"],
        "out_market": ["BIL"]
    },
    {
        "name": "VWO+T/BIL",
        "in_market": ["VWO", "TLT"],
        "out_market": ["BIL"]
    },
    {
        "name": "S+Q+V/TLT",
        "in_market": ["SPY", "QQQ", "VWO"],
        "out_market": ["TLT"]
    },
    {
        "name": "S+Q+V+T/BIL",
        "in_market": ["SPY", "QQQ", "VWO", "TLT"],
        "out_market": ["BIL"]
    },
]

benchmarks = [
    {
        "name": "SPY",
        "weight": {"SPY": 1}
    },
    {
        "name": "QQQ",
        "weight": {"QQQ": 1}
    },
    {
        "name": "VWO",
        "weight": {"VWO": 1}
    },
]

lookbacks = [1, 3, 6]  # Month
lookback_weights = [1, 1, 1]  # Ratio

start_trading_date = "2000-01-01"
end_trading_date = "2021-12-12"
#########################################

# %%
tickers_in_market = sum([p["in_market"] for p in portfolios], [])
tickers_out_market = sum([p["out_market"] for p in portfolios], [])
tickers_benchmark = sum([list(it["weight"].keys()) for it in benchmarks], [])

tickers_all = list(
    set(tickers_in_market + tickers_out_market + tickers_benchmark))
print("# All Tickers:")
print(tickers_all)

# %%
# Momentum ????????? ?????? 6?????? ??? ??????????????? ?????????
month_offset = max(lookbacks)
start_date_off = get_start_date_off(
    start_trading_date, month_offset=month_offset)
print(start_date_off)

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'??? ???????????? ?????? ??????
_d = yf.download(tickers_all, start=start_date_off, end=end_trading_date)
d = _d['Adj Close'].dropna()
print(d.head())

# %%
# ???????????? ????????? ????????? ?????? 6?????? ???????????? ???????????????, ??????????????? ????????? ???????????? ?????????
first_date_of_data = d.index[0].date().isoformat()
real_start_trading_date = get_real_start_trading_date(
    first_date_of_data, month_offset=month_offset)
print("# Firtst Date of Data: ", end="")
print(first_date_of_data)
print("# Real Start Trading Date: ", end="")
print(real_start_trading_date)


# %%

benchmark_strategys = [saa_weight_strategy(pf["name"], assets_with_weight=pf["weight"],
                                           run_term="monthly", start_trading_date=real_start_trading_date) for pf in benchmarks]
benchmark_tests = [bt.Backtest(s, d) for s in benchmark_strategys]
# %%
# ????????? ??????????????? ?????? ????????? ?????????
strategys = [
    dual_momentum_strategy(
        pf["name"],
        n=1,
        alternative_n=1,
        lookbacks=lookbacks,
        lookback_weights=lookback_weights,
        assets=pf["in_market"],
        alternative_assets=pf["out_market"],
        all_or_none=False,
        start_trading_date=real_start_trading_date
    ) for pf in portfolios
]

tests = [bt.Backtest(s, d) for s in strategys]

# %%
# res = bt.run(*benchmark_tests, *tests)
res = bt.run(*benchmark_tests, *tests)

# %%
res.display()

# %%
res.plot()

# %%
# res.prices

# %%
# res.stats
