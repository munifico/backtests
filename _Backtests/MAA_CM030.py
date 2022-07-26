# %%
import yfinance as yf
import bt
import pandas as pd
from btpp.algos import WeighFunctionally
from btpp.strategy import dual_momentum_strategy, saa_weight_strategy, saa_with_momentum_weight_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
# %matplotlib inline

#########################################
# Code For Custom Momentum Strategy(CM)
# 여러가지 대표 종목 선정
# * 자산군으로 묶음 ( 주식 40%, 채권 40%, 원자재 20% )
# * 각 자산군에서 모멘텀이 가장 높은 종목에 투자.
# * 단, 모멘텀이 0 이하인 경우 대신 현금(혹은 단기채권) 보유
# * 매월 리벨런싱
#########################################

# %%
#########################################
portfolios = [
    {
        "name": "주식A",
        "in_market": ["SPY", "VEA", "VWO"],  # "SH"],
        "out_market": ["BIL"],
        "lookback_weights": [1.0, 0, 0]
    },
    {
        "name": "주식B",
        # "XLC", "XLU", "XLE",  "VNQ"],  # ],
        "in_market": ["QQQ", "XLV"],  # "PSQ"],
        "out_market": ["BIL"],
        "lookback_weights": [1.0, 0, 0]
    },
    {
        "name": "채권",
        # "AGG", ],  # ],
        "in_market": ["TLT", "SHY", "TIP", "IEF"],  # "TBF", "TBX"],
        "out_market": ["BIL"],
        "lookback_weights": [1.0, 0, 0]
    },
    {
        "name": "원자재",
        "in_market": ["GLD", "DBC", "USO"],  # "DBA", "DGZ"],
        "out_market": ["BIL"],
        "lookback_weights": [1.0, 0, 0]
    }
]

benchmarks = [
    # {
    #     "name": "SPY",
    #     "weight": {"SPY": 1}
    # },
    # {
    #     "name": "QQQ",
    #     "weight": {"QQQ": 1}
    # },
    {
        "name": "GB",
        "weight": {"SPY": 0.2, "QQQ": 0.2, "GLD": 0.2, "TLT": 0.2, "SHY": 0.2},
    }
]

lookbacks = [1, 3, 6]  # Month

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
# Momentum 계산을 위해 6개월 전 데이터부터 가져옴
month_offset = max(lookbacks)
start_date_off = get_start_date_off(
    start_trading_date, month_offset=month_offset)
print(start_date_off)

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'를 이용하여 가격 조정
_d = yf.download(tickers_all, start=start_date_off, end=end_trading_date)
d = _d['Adj Close'].dropna()
print(d.head())

# %%
# 데이터는 모멘텀 계산을 위해 6개월 이전부터 가져왔지만, 백테스트는 지정한 일자부터 시작함
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
# 종목을 바꾸어가며 듀얼 모멘텀 테스트

strategys = [
    dual_momentum_strategy(
        pf["name"],
        n=1,
        alternative_n=1,
        lookbacks=lookbacks,
        lookback_weights=pf['lookback_weights'],
        assets=pf["in_market"],
        alternative_assets=pf["out_market"],
        all_or_none=False,
        start_trading_date=real_start_trading_date
    ) for pf in portfolios
]

# %%
chidren_weights = {"주식A": 0.2, "주식B": 0.2, "채권": 0.4, "원자재": 0.2}
chidren_tickers = list(chidren_weights.keys())
parents_s = bt.Strategy('parent', [
    bt.algos.RunAfterDate(real_start_trading_date),
    bt.algos.RunMonthly(),
    bt.algos.SelectAll(),
    bt.algos.WeighSpecified(**chidren_weights),
    # bt.algos.WeighEqually(),
    bt.algos.Rebalance(),
    bt.algos.PrintInfo(
        '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
    ),
    bt.algos.PrintTempData()
], strategys)


tests = bt.Backtest(parents_s, d)

# %%
# res = bt.run(tests)
res = bt.run(*benchmark_tests, tests)

# %%
res.display()

# %%
res.plot()

# %%
# res.prices

# %%
# res.stats
