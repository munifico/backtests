# %%
import pandas as pd
import yfinance as yf
import bt
%matplotlib inline

# %%
s_layer = [
    bt.algos.RunMonthly(),
    bt.algos.SelectAll(),
    bt.algos.WeighEqually(),
    bt.algos.Rebalance()
]

s = bt.Strategy('s1', s_layer)

# %%
# d = bt.get(["spy", "agg"], start="2010-01-01")
d = bt.get(["spy", "qqq", "gld", "tlt", "shy"],
           start="2010-01-01",
           end="2019-12-12")
print(d.head())

# %%
test = bt.Backtest(s, d)
res = bt.run(test)

# %%
res.display()

# %%
res.plot()

# %%
dir(res)
