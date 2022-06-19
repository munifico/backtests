import pandas as pd
import bt
from btpp.algos import SelectRelativeMomentum, SelectDualMomentum


def relative_momentum_strategy(
    name,
    n=1,
    lookbacks=[1, 3, 6],
    lookback_weights=[5, 3, 2],
    assets=[],
    start_trading_date=""
):

    layer = [
        bt.algos.RunAfterDate(start_trading_date),
        bt.algos.PrintDate(),
        bt.algos.RunMonthly(),
        bt.algos.SelectAll(),
        SelectRelativeMomentum(
            n=n,
            lookbacks=[pd.DateOffset(months=e) for e in lookbacks],
            lookback_weights=lookback_weights
        ),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance(),
        bt.algos.PrintTempData()
    ]

    all_assets = assets
    return bt.Strategy(name, layer, all_assets)


def dual_momentum_strategy(
    name,
    n=1,
    alternative_n=1,
    lookbacks=[1, 3, 6],
    lookback_weights=[5, 3, 2],
    assets=[],
    alternative_assets=[],
    all_or_none=False,
    start_trading_date=""
):

    layer = [
        bt.algos.RunAfterDate(start_trading_date),
        bt.algos.PrintDate(),
        bt.algos.RunMonthly(),
        bt.algos.SelectAll(),
        SelectDualMomentum(
            n=n,
            alternative_n=alternative_n,
            lookbacks=[pd.DateOffset(months=e) for e in lookbacks],
            lookback_weights=lookback_weights,
            assets=assets,
            alternative_assets=alternative_assets,
            all_or_none=all_or_none
        ),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance(),
        bt.algos.PrintTempData()
    ]

    all_assets = list(set(assets + alternative_assets))
    return bt.Strategy(name, layer, all_assets)
