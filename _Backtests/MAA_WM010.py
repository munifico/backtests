# %%
import yfinance as yf
import bt
from btpp.strategy import saa_weight_strategy, momentum_weight_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
%matplotlib inline

#########################################
# Code For Weight Momentum Strategy(WM)
# 모멘텀이 0 이상인 자산만 골라, 모멘텀 비율대로 투자 비중 조정하기
#########################################

# %%
#########################################
portfolios = [
    {
        "name": "S031",
        "in_market": ["QQQ", "VWO", "TLT"],
        "out_market": ["BIL"]
    },
    {
        "name": "S032",
        "in_market": ["QQQ", "VWO", "TBF"],
        "out_market": ["BIL"]
    },
    {
        "name": "S041",
        "in_market": ["QQQ", "VWO", "TLT", "TBF"],
        "out_market": ["BIL"]
    },
    {
        "name": "S042",
        "in_market": ["QQQ", "VWO", "VNQ", "TLT"],
        "out_market": ["BIL"]
    },
    {
        "name": "S043",
        "in_market": ["SPY", "QQQ", "VWO", "TLT"],
        "out_market": ["BIL"]
    },
    {
        "name": "S051",
        "in_market": ["SPY", "QQQ", "VWO", "TLT", "TBF"],
        "out_market": ["BIL"]
    },
    {
        "name": "S052",
        "in_market": ["SPY", "IWM", "EFA", "EEM", "VNQ"],
        "out_market": ["BIL"]
    },
    {
        "name": "S061",
        "in_market": ["SPY", "QQQ", "VEA", "VWO", "TLT", "TIP"],
        "out_market": ["BIL"]
    },
    {
        "name": "S09",
        "in_market": ["VT", "SPY", "IWM", "EFA", "EEM", "VNQ", "TLT", "TIP", "BIL"],
        "out_market": ["BIL"]
    },
    {
        "name": "S10",
        "in_market": ["VT", "SPY", "QQQ", "IWM", "EVA", "VWO", "EFA", "EEM", "VNQ", "TLT"],
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
        "name": "VWO",
        "weight": {"VWO": 1}
    },
    {
        "name": "SPY+QQQ+VWO",
        "weight": {"SPY": 0.34, "QQQ": 0.33, "VWO": 0.33}
    }
]

lookbacks = [1, 3, 6]  # Month
lookback_weights = [5, 3, 2]  # Ratio

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


def weight_from_momentum(target):
    # momentum
    stat = target.temp['stat'].copy()
    stat[stat < 0] = 0
    s = stat.sum()
    if s == 0:
        return {}
    else:
        weights = (stat / s).to_dict()
        return weights


strategys = [
    momentum_weight_strategy(
        pf["name"],
        weight_from_momentum,
        # n=1,
        # alternative_n=1,
        lookbacks=lookbacks,
        lookback_weights=lookback_weights,
        assets=pf["in_market"],
        # alternative_assets=pf["out_market"],
        # all_or_none=False,
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
