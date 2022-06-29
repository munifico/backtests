# %%
import yfinance as yf
import bt
from btpp.strategy import relative_momentum_strategy, saa_equal_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
%matplotlib inline

#########################################
# Code For Relative Momentum Strategy(RM)
# 상대 모멘텀을 이용한 종목선택 및 백테스트
# 모멘텀 함수를 검토해 보자.
#########################################

# %%
#########################################

tickers = ["SPY", "QQQ", "VWO", "TLT"]
start_date = "2006-01-01"
end_date = "2021-12-12"

porfolios = [
    {
        "name": 'm6:2:1',
        "lookbacks": [1, 3, 6],
        "lookback_weights": [6, 2, 1]
    },
    {
        "name": 'm5:3:2',
        "lookbacks": [1, 3, 6],
        "lookback_weights": [5, 3, 2]
    },
    {
        "name": 'm1:1:1',
        "lookbacks": [1, 3, 6],
        "lookback_weights": [1, 1, 1]
    },
    {
        "name": 'm2:3:5',
        "lookbacks": [1, 3, 6],
        "lookback_weights": [2, 3, 5]
    },
    {
        "name": 'm1:2:6',
        "lookbacks": [1, 3, 6],
        "lookback_weights": [1, 2, 6]
    },
    {
        "name": 'm3:5:2',
        "lookbacks": [1, 3, 6],
        "lookback_weights": [3, 5, 2]
    },
    {
        "name": 'm2:6:1',
        "lookbacks": [1, 3, 6],
        "lookback_weights": [2, 6, 1]
    },
    {
        "name": 'm12:4:2:1',
        "lookbacks": [1, 3, 6, 12],
        "lookback_weights": [12, 4, 2, 1]
    }
]

start_trading_date = "2000-01-01"
end_trading_date = "2021-12-12"

month_offset = 12
#########################################

# %%
start_date_off = get_start_date_off(
    start_trading_date, month_offset=month_offset)
print(start_date_off)

# %%

# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'를 이용하여 가격 조정
_d = yf.download(tickers, start=start_date_off, end=end_trading_date)
d = _d['Adj Close'].dropna()
print(d.head())


# %%
first_date_of_data = d.index[0].date().isoformat()
real_start_trading_date = get_real_start_trading_date(
    first_date_of_data, month_offset=month_offset)
print("# Firtst Date of Data: ", end="")
print(first_date_of_data)
print("# Real Start Trading Date: ", end="")
print(real_start_trading_date)

# %%
# Benchmark
benchmark = bt.Backtest(saa_equal_strategy('Benchmark', assets=tickers,
                        run_term="monthly", start_trading_date=real_start_trading_date), d)

# %%

# 모멘텀 가중치를 바꾸어가며 테스트
tests = [bt.Backtest(relative_momentum_strategy(pf["name"], lookbacks=pf["lookbacks"],
                     lookback_weights=pf["lookback_weights"], assets=tickers, start_trading_date=real_start_trading_date), d) for pf in porfolios]

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
