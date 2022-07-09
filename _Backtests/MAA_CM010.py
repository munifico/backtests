# %%
import yfinance as yf
import bt
import pandas as pd
from btpp.algos import WeighFunctionally
from btpp.strategy import saa_weight_strategy, saa_with_momentum_weight_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
# %matplotlib inline

#########################################
# Code For Custom Momentum Strategy(CM)
# 여러가지 대표 종목 선정 ( 약 12가지 )
# * 지난 1, 2,  3 ...  12개월 수익률 최대 종목 각각 1개씩(총 12개)
# * 이들 각 종목에 투자금 1/12 씩 투자.  (중복 포함)
# * 단, 수익률 0 이하인 경우 대신 현금 보유
# * 매월 리벨런싱
#########################################

# %%
#########################################
portfolios = [
    {
        "name": "S01",
        "in_market": ["SPY", "QQQ", "VEA", "VWO", "VSS", "AGG", "TLT", "SHY", "TIP", "IEF"],
        "out_market": ["BIL"]
    },
    {
        "name": "S02",
        "in_market": ["SPY", "QQQ", "VEA", "VWO"],
        "out_market": ["BIL"]
    }
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
        "name": "GB",
        "weight": {"SPY": 0.2, "QQQ": 0.2, "GLD": 0.2, "TLT": 0.2, "SHY": 0.2},
    }
]

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
month_offset = 13
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


def custom_strategy(
    name,
    weight_fn,
    assets=[],
    alternative_assets=[],
    start_trading_date=None,
    verbose=True
):
    layer = []
    if start_trading_date is not None:
        layer.append(bt.algos.RunAfterDate(start_trading_date))

    # if verbose is True:
    #     layer.append(bt.algos.PrintDate())

    layer = layer + [
        bt.algos.RunMonthly(),
        bt.algos.SelectThese(list(set(assets+alternative_assets))),
        WeighFunctionally(weight_fn),
        bt.algos.Rebalance(),
    ]

    if verbose is True:
        layer.append(bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ))
        layer.append(bt.algos.PrintTempData())

    return bt.Strategy(name, layer)


def weight_from_momentum(assets, alternative_assets):
    def inner_func(target):
        # momentum
        in_market = assets
        out_market = alternative_assets[0]
        weights = {out_market: 0}
        for it in in_market:
            weights[it] = 0

        t0 = target.now
        for i in range(1, 13):
            lookback = pd.DateOffset(months=i)
            prc = target.universe.loc[(t0 - lookback):t0, in_market]
            _return = prc.calc_total_return()
            maxidx = _return.idxmax()
            maxval = _return.loc[maxidx]
            if maxval > 0:
                weights[maxidx] = weights[maxidx] + 1/12
            else:
                weights[out_market] + 1/12

        return weights

    return inner_func


strategys = [
    custom_strategy(
        pf["name"],
        weight_from_momentum(pf["in_market"], pf["out_market"]),
        assets=pf["in_market"],
        alternative_assets=pf["out_market"],
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
