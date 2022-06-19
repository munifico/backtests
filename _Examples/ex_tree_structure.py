# %%
import bt

# Example Tree Structure
# https://pmorissette.github.io/bt/tree.html

# %%
tickers = ["spy", "eem", "qqq", "agg"]
data_start_date = "2010-01-01"
data_end_date = "2021-12-12"

# %%
_d = bt.data.get(tickers, start=data_start_date, end=data_end_date)
data = _d.dropna()
print(data.head())

# %%
# create the momentum strategy - we will specify the children (3rd argument)
# to limit the universe the strategy can choose from
mom_s = bt.Strategy('mom_s', [
    bt.algos.RunMonthly(),
    bt.algos.SelectAll(),
    bt.algos.SelectMomentum(1),
    bt.algos.WeighEqually(),
    bt.algos.Rebalance(),
    bt.algos.PrintTempData()
], ['spy', 'qqq', 'eem'])

# %%
# create the parent strategy - this is the top-most node in the tree
# Once again, we are also specifying  the children. In this case, one of the
# children is a Security and the other is a Strategy.
parent = bt.Strategy('parent', [
    bt.algos.RunMonthly(),
    bt.algos.SelectAll(),
    bt.algos.WeighEqually(),
    bt.algos.Rebalance(),
    bt.algos.PrintTempData()
], [mom_s, 'agg'])

# %%
# create the backtest and run it
t = bt.Backtest(parent, data)
r = bt.run(t)

# %%
r.display()
