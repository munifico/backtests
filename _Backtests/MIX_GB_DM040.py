# %%
import yfinance as yf
import bt
from btpp.strategy import dual_momentum_strategy, saa_weight_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
%matplotlib inline

#########################################
# Code For Mixture Strategy (M)
# GB + DM 전략을 결합했을 때
#########################################

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'를 이용하여 가격 조정

gb = {"GLD": 0.2, "QQQ": 0.2, "SPY": 0.2, "SHY": 0.2, "TLT": 0.2}

portfolios = [
    {
        "name": "M100",
        "weight": {"SAA": 1.0, "MAA1": 0.0, "MAA2": 0.0},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M010",
        "weight": {"SAA": 0.0, "MAA1": 1.0, "MAA2": 0.0},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M001",
        "weight": {"SAA": 0.0, "MAA1": 0.0, "MAA2": 1.0},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M442",
        "weight": {"SAA": 0.4, "MAA1": 0.4, "MAA2": 0.2},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M333",
        "weight": {"SAA": 0.34, "MAA1": 0.33, "MAA2": 0.33},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M244",
        "weight": {"SAA": 0.2, "MAA1": 0.4, "MAA2": 0.4},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M550",
        "weight": {"SAA": 0.5, "MAA1": 0.5, "MAA2": 0.0},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M505",
        "weight": {"SAA": 0.5, "MAA1": 0.0, "MAA2": 0.5},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M055",
        "weight": {"SAA": 0.0, "MAA1": 0.5, "MAA2": 0.5},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    },
    {
        "name": "M021",
        "weight": {"SAA": 0.0, "MAA1": 0.66, "MAA2": 0.34},
        "SAA": {
            "weight": gb
        },
        "MAA1": {
            "in_market": ["SPY", "QQQ", "VWO"],
            "out_market": ["TLT"]
        },
        "MAA2": {
            "in_market": ["TLT", "SHY", "IEF", "TIP"],
            "out_market": ["BIL"]
        }
    }
]

# Golden Butterfly
benchmarks = [
    {
        "name": "Benchmark",
        "weight": {"GLD": 0.2, "QQQ": 0.2, "SPY": 0.2, "SHY": 0.2, "TLT": 0.2}
    },
]

lookbacks = [1, 3, 6]  # Month
lookback_weights = [5, 3, 1]  # Ratio
# lookback_weights = [1, 1, 1]  # Ratio

start_trading_date = "1980-01-01"
end_trading_date = "2021-12-12"
#########################################

# %%
tickers_in_market1 = sum([p["MAA1"]["in_market"] for p in portfolios], [])
tickers_out_market1 = sum([p["MAA1"]["out_market"] for p in portfolios], [])
tickers_in_market2 = sum([p["MAA2"]["in_market"] for p in portfolios], [])
tickers_out_market2 = sum([p["MAA2"]["out_market"] for p in portfolios], [])
tickers_in_market = tickers_in_market1 + tickers_in_market2
tickers_out_market = tickers_out_market1 + tickers_out_market2
tickers_benchmark = sum([list(it["weight"].keys())
                        for it in benchmarks], [])

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
    first_date_of_data, month_offset=month_offset)
print("# Firtst Date of Data: ", end="")
print(first_date_of_data)
print("# Real Start Trading Date: ", end="")
print(real_start_trading_date)


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

    parent_layer = [
        bt.algos.RunMonthly(),
        bt.algos.SelectAll(),
        # bt.algos.SelectThese(["SAA", "MAA1", "MAA2"]),
        bt.algos.WeighSpecified(**pf["weight"]),
        bt.algos.Rebalance(),
        bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ),
        bt.algos.PrintTempData()
    ]

    saa_st = saa_weight_strategy(
        "SAA",
        assets_with_weight=pf["SAA"]["weight"],
        run_term="monthly",
        start_trading_date=real_start_trading_date
    )

    maa1_st = dual_momentum_strategy(
        "MAA1",
        n=1,
        alternative_n=1,
        lookbacks=lookbacks,
        lookback_weights=lookback_weights,
        assets=pf["MAA1"]["in_market"],
        alternative_assets=pf["MAA1"]["out_market"],
        all_or_none=False,
        start_trading_date=real_start_trading_date
    )

    maa2_st = dual_momentum_strategy(
        "MAA2",
        n=1,
        alternative_n=1,
        lookbacks=lookbacks,
        lookback_weights=lookback_weights,
        assets=pf["MAA2"]["in_market"],
        alternative_assets=pf["MAA2"]["out_market"],
        all_or_none=False,
        start_trading_date=real_start_trading_date
    )

    parent_st = bt.Strategy(pf["name"], parent_layer, [
                            saa_st, maa1_st, maa2_st])

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
