# %%
import pandas as pd
import yfinance as yf
import bt
from datetime import datetime, date, timedelta
from lib.maa import SelectDualMomentum
%matplotlib inline

#########################################
# Code For Dual Momentum Strategy(DM)
#########################################

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'를 이용하여 가격 조정
portfolios = [
    {
        "name": "SPY",
        "in_market": ["SPY"],
        "out_market": "TLT"
    },
    {
        "name": "QQQ",
        "in_market": ["QQQ"],
        "out_market": "TLT"
    },
    {
        "name": "SPY+VWO",
        "in_market": ["SPY", "VWO"],
        "out_market": "TLT"
    },
    {
        "name": "SPY+QQQ",
        "in_market": ["SPY", "QQQ"],
        "out_market": "TLT"
    },
    {
        "name": "SPY+IWS",
        "in_market": ["SPY", "IWS"],
        "out_market": "TLT"
    },
    {
        "name": "SPY+VWO+QQQ",
        "in_market": ["SPY", "VWO", "QQQ"],
        "out_market": "TLT"
    },
    {
        "name": "SPY+VWO+IWS",
        "in_market": ["SPY", "VWO", "IWS"],
        "out_market": "TLT"
    },
    {
        "name": "SPY+QQQ+VWO+IWS",
        "in_market": ["SPY", "QQQ", "VWO", "IWS"],
        "out_market": "TLT"
    },
    {
        "name": "SPY+QQQ+VWO+TIP",
        "in_market": ["SPY", "QQQ", "VWO", "TIP"],
        "out_market": "TLT"
    },
    {
        "name": "SPY+QQQ+VWO+IWP+IJH",
        "in_market": ["SPY", "QQQ", "VWO", "IWP", "IJH"],
        "out_market": "TLT"
    }
]
lookbacks = [1, 3, 6]  # Month
lookback_weights = [5, 3, 2]  # Ratio

data_start_date = "2006-01-01"
data_end_date = "2019-12-12"
#########################################

# %%
in_market = sum([p["in_market"] for p in portfolios], [])
out_market = [p["out_market"] for p in portfolios]
tickers = list(set(in_market + out_market))
print("# All Tickers:")
print(tickers)

# %%
# Momentum 계산을 위해ㅔ 6개월 전 데이터부터 가져옴
month_offset = max(lookbacks)
_start_date = date.fromisoformat(data_start_date)
_start_date_off = _start_date - timedelta(days=month_offset * 31)
start_date_off = _start_date_off.isoformat()
print(start_date_off)

# %%
_d = yf.download(tickers, start=start_date_off, end=data_end_date)
d = _d['Adj Close'].dropna()
print(d.head())

# %%
# 데이터는 모멘텀 계산을 위해 6개월 이전부터 가져왔지만, 백테스트는 지정한 일자부터 시작함
first_date_of_data = d.index[0].to_pydatetime().date()
_new_start_date = first_date_of_data if _start_date < first_date_of_data else _start_date
new_start_date = _new_start_date.isoformat()
print(first_date_of_data)
print(_new_start_date)
print(new_start_date)

d = d[d.index >= new_start_date]

# %%


def get_dualmomentum_strategy(name, lookbacks, lookback_weights, in_market_asset, out_market_asset):
    layer = [
        bt.algos.RunMonthly(),
        bt.algos.SelectThese(in_market_asset),
        SelectDualMomentum(
            lookbacks=[pd.DateOffset(months=e) for e in lookbacks],
            lookback_weights=lookback_weights,
            out_market_asset=out_market_asset
        ),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance(),
        bt.algos.PrintTempData()
    ]
    return bt.Strategy(name, layer)


# %%
# Benchmark
bm_layer = [
    bt.algos.RunMonthly(),
    bt.algos.SelectAll(),
    bt.algos.WeighEqually(),
    bt.algos.Rebalance()
]
bm_st = bt.Strategy('Benchmark', bm_layer)
benchmark = bt.Backtest(bm_st, d)

# %%

# 종목을 바꾸어가며 듀얼 모멘텀 테스트

# name, lookbacks, lookback_weights, in_market_asset, out_market_asset

strategys = [
    get_dualmomentum_strategy(pf["name"], lookbacks, lookback_weights, pf["in_market"], pf["out_market"]) for pf in portfolios
]
tests = [bt.Backtest(s, d) for s in strategys]

# %%
res = bt.run(benchmark, *tests)

# %%
res.display()

# %%
res.plot()

# %%
# res.prices

# %%
# res.stats
