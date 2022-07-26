# %%
import pandas as pd
import yfinance as yf
import bt
from datetime import datetime, date, timedelta
from btpp.strategy import dual_momentum_strategy, saa_weight_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
%matplotlib inline

#########################################
# Code For Dual Momentum Strategy(DM)
# 채권을 위주로 했을 때
#########################################
# 결과
# * 하이일드채권("HYG")의 유무가 수익률에 크게 작용함
# * 1:3:6월을 0:0:1로 했을 때 수익률 좋았음
# portfoliovisualizer 결과와 차이가 있음
# * 1:3:6월을 5:3:2로 했을 때 수익률 좋았음
# * https://www.portfoliovisualizer.com/test-market-timing-model?s=y&coreSatellite=false&timingModel=6&timePeriod=4&startYear=1985&firstMonth=1&endYear=2022&lastMonth=12&calendarAligned=true&includeYTD=false&initialAmount=10000&periodicAdjustment=0&adjustmentAmount=0&inflationAdjusted=true&adjustmentPercentage=0.0&adjustmentFrequency=4&symbols=TLT+SHY+IEF+TIP+HYG&singleAbsoluteMomentum=false&volatilityTarget=9.0&downsideVolatility=false&outOfMarketStartMonth=5&outOfMarketEndMonth=10&outOfMarketAssetType=1&movingAverageSignal=1&movingAverageType=1&multipleTimingPeriods=true&periodWeighting=2&windowSize=10&windowSizeInDays=105&movingAverageType2=1&windowSize2=10&windowSizeInDays2=105&excludePreviousMonth=false&normalizeReturns=false&volatilityWindowSize=0&volatilityWindowSizeInDays=0&assetsToHold=1&allocationWeights=1&riskControlType=0&riskWindowSize=10&riskWindowSizeInDays=0&stopLossMode=0&stopLossThreshold=2.0&stopLossAssetType=1&rebalancePeriod=1&separateSignalAsset=false&tradeExecution=0&leverageType=0&leverageRatio=0.0&debtAmount=0&debtInterest=0.0&maintenanceMargin=25.0&leveragedBenchmark=false&comparedAllocation=0&benchmark=-1&benchmarkSymbol=SPY&timingPeriods%5B0%5D=1&timingUnits%5B0%5D=2&timingWeights%5B0%5D=50&timingPeriods%5B1%5D=3&timingUnits%5B1%5D=2&timingWeights%5B1%5D=30&timingPeriods%5B2%5D=6&timingUnits%5B2%5D=2&timingWeights%5B2%5D=20&timingUnits%5B3%5D=2&timingWeights%5B3%5D=0&timingUnits%5B4%5D=2&timingWeights%5B4%5D=0&volatilityPeriodUnit=2&volatilityPeriodWeight=0
#########################################

# %%
#########################################

portfolios = [
    {
        "name": "B1",
        "in_market": ["TLT"],
        "out_market": ["BIL"]
    },
    {
        "name": "B2",
        "in_market": ["TLT", "SHY"],
        "out_market": ["BIL"]
    },
    {
        "name": "B3",
        "in_market": ["TLT", "SHY", "IEF"],
        "out_market": ["BIL"]
    },
    {
        "name": "B4",
        "in_market": ["TLT", "SHY", "IEF", "TIP"],
        "out_market": ["BIL"]
    },
    {
        "name": "B5",
        "in_market": ["TLT", "SHY", "IEF", "TIP", "LQD"],
        "out_market": ["BIL"]
    },
    {
        "name": "B6",
        "in_market": ["TLT", "SHY", "IEF", "TIP", "HYG"],
        "out_market": ["BIL"]
    },
    {
        "name": "B7",
        "in_market": ["TLT", "SHY", "IEF", "TIP", "LQD", "HYG"],
        "out_market": ["BIL"]
    },
    {
        "name": "B8",
        "in_market": ["TLT", "SHY", "IEF", "TIP", "LQD", "HYG", "BWX", "EMB"],
        "out_market": ["BIL"]
    }
]

benchmarks = [
    {
        "name": "SPY+QQQ+T",
        "weight": {"SPY": 0.34, "QQQ": 0.33, "TLT": 0.33}
    },
]

lookbacks = [1, 3, 6]  # Month
lookback_weights = [0.5, 0.3, 0.2]  # Ratio

start_trading_date = "1980-01-01"
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
    first_date_of_data, month_offset=month_offset)
print("# Firtst Date of Data: ", end="")
print(first_date_of_data)
print("# Real Start Trading Date: ", end="")
print(real_start_trading_date)


# %%
# Benchmark
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
