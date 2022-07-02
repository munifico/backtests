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

portfolios = [   # 8 : 0 전략 검토
    {
        "name": "4040/0000",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.40, "SPY": 0.40, "SHY": 0.00, "TLT": 0.00},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.00, "SPY": 0.00, "SHY": 0.40, "TLT": 0.40},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "6020/0000a",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.60, "SPY": 0.20, "SHY": 0.00, "TLT": 0.00},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.00, "SPY": 0.00, "SHY": 0.20, "TLT": 0.60},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "6020/0000b",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.60, "SPY": 0.20, "SHY": 0.00, "TLT": 0.00},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.00, "SPY": 0.00, "SHY": 0.60, "TLT": 0.20},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "2060/0000a",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.20, "SPY": 0.60, "SHY": 0.00, "TLT": 0.00},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.00, "SPY": 0.00, "SHY": 0.20, "TLT": 0.60},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },
    {
        "name": "2060/0000b",
        "weights_with_months": [
            {
                "weights": {"GLD": 0.2, "QQQ": 0.20, "SPY": 0.60, "SHY": 0.00, "TLT": 0.00},
                "months": [11, 12, 1, 2, 3, 4]
            },
            {
                "weights": {"GLD": 0.2, "QQQ": 0.00, "SPY": 0.00, "SHY": 0.60, "TLT": 0.20},
                "months": [5, 6, 7, 8, 9, 10]
            },
        ]
    },

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
