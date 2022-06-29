# %%
import pandas as pd
import yfinance as yf
import bt
from btpp.strategy import simple_momentum_strategy, saa_equal_strategy
from btpp.helper import get_start_date_off, get_real_start_trading_date
%matplotlib inline

#########################################
# Code For Simple Momentum Strategy(SM)
# 단순 모멘텀 기간에 따른 백테스트
#########################################

# %%
#########################################

tickers = ["SPY", "QQQ", "VWO", "TLT", "SHY"]
start_trading_date = "2000-01-01"
end_trading_date = "2021-12-12"
month_offset = 6
#########################################

# %%
start_date_off = get_start_date_off(
    start_trading_date, month_offset=month_offset)
print(start_date_off)

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
# 'Adj Close'를 이용하여 가격 조정
d = yf.download(tickers,
                start=start_date_off,
                end=end_trading_date)['Adj Close'].dropna()
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
# 1개월 수익률 최대 종목을 선택할 경우
test1 = bt.Backtest(
    simple_momentum_strategy(
        'm1',
        lookback_month=1,
        start_trading_date=real_start_trading_date),
    d)
# 3개월 수익률 최대 종목을 선택할 경우
test3 = bt.Backtest(
    simple_momentum_strategy(
        'm3',
        lookback_month=3,
        start_trading_date=real_start_trading_date),
    d)
# 6개월 수익률 최대 종목을 선택할 경우
test6 = bt.Backtest(
    simple_momentum_strategy(
        'm6',
        lookback_month=6,
        start_trading_date=real_start_trading_date),
    d)

res = bt.run(benchmark, test1, test3, test6)

# %%
res.display()

# %%
res.plot()

# %%
