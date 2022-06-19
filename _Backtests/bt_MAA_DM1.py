# %%
import pandas as pd
import yfinance as yf
import bt
from datetime import datetime, date, timedelta
from btpp.strategy import dual_momentum_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
%matplotlib inline

#########################################
# Code For Dual Momentum Strategy(DM)
#########################################

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'를 이용하여 가격 조정
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
lookback_weights = [5, 3, 2]  # Ratio

start_trading_date = "2010-01-01"
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
# Momentum 계산을 위해 6개월 전 데이터부터 가져옴
month_offset = max(lookbacks)
start_date_off = get_start_date_off(
    start_trading_date, month_offset=month_offset)
print(start_date_off)

# %%
_d = yf.download(tickers_all, start=start_date_off, end=end_trading_date)
d = _d['Adj Close'].dropna()
print(d.head())

# %%
# 데이터는 모멘텀 계산을 위해 6개월 이전부터 가져왔지만, 백테스트는 지정한 일자부터 시작함
first_date_of_data = d.index[0].date().isoformat()
real_start_trading_date = get_real_start_trading_date(
    start_trading_date, first_date_of_data)
print("# Firtst Date of Data: ", end="")
print(first_date_of_data)
print("# Real Start Trading Date: ", end="")
print(real_start_trading_date)


# %%
# Benchmark
def benchmark_strategy(name, weight, start_trading_date):
    tickers = list(weight.keys())
    layer = [
        bt.algos.RunAfterDate(start_trading_date),
        bt.algos.RunMonthly(),
        bt.algos.SelectAll(),
        bt.algos.WeighSpecified(**weight),
        bt.algos.Rebalance()
    ]
    return bt.Strategy(name, layer, tickers)


# %%
benchmark_strategys = [benchmark_strategy(
    pf["name"], pf["weight"], real_start_trading_date) for pf in benchmarks]
benchmark_tests = [bt.Backtest(s, d) for s in benchmark_strategys]
# %%
# 종목을 바꾸어가며 듀얼 모멘텀 테스트
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
