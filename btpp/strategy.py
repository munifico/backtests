import pandas as pd
import bt
from btpp.algos import SelectRelativeMomentum, SelectDualMomentum

RUN_TERM = {
    "daily": bt.algos.RunDaily,
    "monthly": bt.algos.RunMonthly,
    "quarterly": bt.algos.RunQuarterly,
    "yearly": bt.algos.RunYearly
}


def saa_equal_strategy(
    name,
    assets=[],
    run_term="yearly",
    start_trading_date=None,
    verbose=True
):

    layer = []
    if start_trading_date is not None:
        layer.append(bt.algos.RunAfterDate(start_trading_date))

    # if verbose is True:
    #     layer.append(bt.algos.PrintDate())

    layer = layer + [
        RUN_TERM.get(run_term)(),
        bt.algos.SelectThese(assets),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance()
    ]

    if verbose is True:
        layer.append(bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ))
        layer.append(bt.algos.PrintTempData())

    return bt.Strategy(name, layer)


def saa_weight_strategy(
    name,
    assets_with_weight={},
    run_term="yearly",
    start_trading_date=None,
    verbose=True
):

    layer = []
    if start_trading_date is not None:
        layer.append(bt.algos.RunAfterDate(start_trading_date))

    # if verbose is True:
    #     layer.append(bt.algos.PrintDate())

    layer = layer + [
        RUN_TERM.get(run_term)(),
        bt.algos.SelectAll(),
        bt.algos.WeighSpecified(**assets_with_weight),
        bt.algos.Rebalance()
    ]

    if verbose is True:
        layer.append(bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ))
        layer.append(bt.algos.PrintTempData())

    return bt.Strategy(name, layer)


def simple_momentum_strategy(
    name,
    n=1,
    lookback_month=1,
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
        bt.algos.SelectAll(),
        bt.algos.SelectMomentum(
            n=n,
            lookback=pd.DateOffset(months=lookback_month),
            lag=pd.DateOffset(days=0)),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance(),
    ]

    if verbose is True:
        layer.append(bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ))
        layer.append(bt.algos.PrintTempData())

    return bt.Strategy(name, layer)


def relative_momentum_strategy(
    name,
    n=1,
    lookbacks=[1, 3, 6],
    lookback_weights=[5, 3, 2],
    assets=[],
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
        bt.algos.SelectAll(),
        SelectRelativeMomentum(
            n=n,
            lookbacks=[pd.DateOffset(months=e) for e in lookbacks],
            lookback_weights=lookback_weights
        ),
        bt.algos.WeighEqually(),
        bt.algos.Rebalance(),
    ]

    if verbose is True:
        layer.append(bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ))
        layer.append(bt.algos.PrintTempData())

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
    ]

    if verbose is True:
        layer.append(bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ))
        layer.append(bt.algos.PrintTempData())

    all_assets = list(set(assets + alternative_assets))
    return bt.Strategy(name, layer, all_assets)
