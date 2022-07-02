# %%
import yfinance as yf
import bt
from btpp.algos import WeighSpecifiedMonthly
from btpp.strategy import saa_weight_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
%matplotlib inline

#########################################
# Code For Mixture Strategy (M)
# GB + HW(할로윈) 전략을 결합했을 때
#########################################

# %%

gb = {"GLD": 0.2, "QQQ": 0.2, "SPY": 0.2, "SHY": 0.2, "TLT": 0.2}

portfolios = [
    {
        "name": "2020/2020",
        "weights_with_months": [
            {
                "weights": gb,
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": gb,
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "2525/1515",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.25, "SPY": 0.25, "SHY": 0.15, "TLT": 0.15},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.15, "SPY": 0.15, "SHY": 0.25, "TLT": 0.25},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "1515/2525",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.15, "SPY": 0.15, "SHY": 0.25, "TLT": 0.25},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights":  {"GLD": 0.2, "QQQ": 0.25, "SPY": 0.25, "SHY": 0.15, "TLT": 0.15},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "3030/1010",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.3, "SPY": 0.3, "SHY": 0.1, "TLT": 0.1},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.1, "SPY": 0.1, "SHY": 0.3, "TLT": 0.3},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "1010/3030",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.1, "SPY": 0.1, "SHY": 0.3, "TLT": 0.3},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.3, "SPY": 0.3, "SHY": 0.1, "TLT": 0.1},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "4040/0000a",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.4, "SPY": 0.4, "SHY": 0.0, "TLT": 0.0},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.0, "SPY": 0.0, "SHY": 0.4, "TLT": 0.4},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "4040/0000b",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.4, "SPY": 0.4, "SHY": 0.0, "TLT": 0.0},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.0, "SPY": 0.0, "SHY": 0.8, "TLT": 0.0},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "4040/0000c",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.4, "SPY": 0.4, "SHY": 0.0, "TLT": 0.0},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.0, "SPY": 0.0, "SHY": 0.0, "TLT": 0.8},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },

    # {
    #     "name": "4040/0000d",
    #     "weights_with_months": [
    #         {
    #             "weights": {"GLD": 0.2, "QQQ": 0.4, "SPY": 0.4, "SHY": 0.0, "TLT": 0.0},
    #             "months": [11, 12, 1, 2, 3, 4]
    #         },
    #         {
    #             "weights": {"GLD": 0.2, "BIL": 0.8},
    #             "months": [5, 6, 7, 8, 9, 10]
    #         },
    #     ]
    # }

]

# Golden Butterfly
benchmarks = [
    {
        "name": "Benchmark",
        "weight": gb
    },
]

start_trading_date = "2000-01-01"
end_trading_date = "2019-12-12"
# 코로나 기간 제외
#########################################

# %%
tickers_in_weights = []

for p in portfolios:
    for it in p["weights_with_months"]:
        tickers_in_weights = tickers_in_weights + list(it["weights"].keys())

tickers_benchmark = sum([list(it["weight"].keys()) for it in benchmarks], [])

tickers_all = list(set(tickers_in_weights + tickers_benchmark))
print("# All Tickers:")
print(tickers_all)

# %%
# Momentum 계산을 위해 6개월 전 데이터부터 가져옴
start_date_off = start_trading_date
real_start_trading_date = start_date_off
print(start_date_off)

# %%
# 'Adj Close'를 이용하여 가격 조정
_d = yf.download(tickers_all, start=start_date_off, end=end_trading_date)
d = _d['Adj Close'].dropna()
print(d.head())


# %%
benchmark_strategys = [
    saa_weight_strategy(
        pf["name"],
        assets_with_weight=pf["weight"],
        run_term="monthly",
        start_trading_date=real_start_trading_date
    ) for pf in benchmarks
]
benchmark_tests = [bt.Backtest(s, d) for s in benchmark_strategys]
# %%
# 종목을 바꾸어가며 듀얼 모멘텀 테스트

strategys = []

for pf in portfolios:

    layer = [
        bt.algos.RunMonthly(),
        bt.algos.SelectAll(),
        WeighSpecifiedMonthly(pf["weights_with_months"]),
        bt.algos.Rebalance(),
        bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ),
        bt.algos.PrintTempData()
    ]

    parent_st = bt.Strategy(pf["name"], layer)
    strategys.append(parent_st)

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
