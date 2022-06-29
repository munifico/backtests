import pandas as pd
import bt
from btpp.algos import StatMomentumReturn, SelectRelativeMomentum, SelectDualMomentum, WeighFunctionally

RUN_TERM = {
    "daily": bt.algos.RunDaily,
    "monthly": bt.algos.RunMonthly,
    "quarterly": bt.algos.RunQuarterly,
    "yearly": bt.algos.RunYearly
}

# 정적 자산 배분 - 투자 비중을 동일하게 투자하기


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

    layer.append(RUN_TERM.get(run_term)())

    if len(assets) > 0:
        layer.append(bt.algos.SelectThese(assets))
    else:
        layer.append(bt.algos.SelectAll())

    layer = layer + [
        bt.algos.WeighEqually(),
        bt.algos.Rebalance()
    ]

    if verbose is True:
        layer.append(bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ))
        layer.append(bt.algos.PrintTempData())

    return bt.Strategy(name, layer)

# 정적 자산 배분 - 주어진 가중치대로 투자 비중을 조절하여 투자하자


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

# 특정 일자를 기준으로 모멘텀을 도출하고, 도출된 모멘텀이 가장 큰 자산에 투자하자.


def simple_momentum_strategy(
    name,
    n=1,
    run_term="monthly",
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
        RUN_TERM.get(run_term)(),
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

# 모멘텀이 가장 큰 자산에 투자하자


def relative_momentum_strategy(
    name,
    n=1,
    run_term="monthly",
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
        RUN_TERM.get(run_term)(),
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

# 모멘텀이 가장 크고 0보다 큰 자산에 투자하자.
# 0보자 작을 때는 대안 자산에 투자하자


def dual_momentum_strategy(
    name,
    n=1,
    alternative_n=1,
    run_term="monthly",
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
        RUN_TERM.get(run_term)(),
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


# 모멘텀에 따라 투자 비중을 조절하자.
# 우선, 모멘텀을 구하고, 0 이상인 자산만을 선택한 뒤, 모멘텀 비중에 따라 투자 비중(weight)을 조정하여 적용하자.
# 모든 자산의 모멘텀이 0보자 작다면 대안 자산에 투자하자.

def weight_momentum_strategy(
    name,
    # n=1,
    # alternative_n=1,
    run_term="monthly",
    lookbacks=[1, 3, 6],
    lookback_weights=[5, 3, 2],
    assets=[],
    # alternative_assets=[],
    # all_or_none=False,
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
        StatMomentumReturn(
            lookbacks=[pd.DateOffset(months=e) for e in lookbacks],
            lookback_weights=lookback_weights
        ),
        WeighFunctionally(weight_from_momentum),
        bt.algos.Rebalance(),
    ]

    if verbose is True:
        layer.append(bt.algos.PrintInfo(
            '{name}:{now}. Value:{_value:0.0f}, Price:{_price:0.4f}'
        ))
        layer.append(bt.algos.PrintTempData())

    return bt.Strategy(name, layer)

###################################################################################


def weight_from_momentum(target):
    # momentum
    stat = target.temp['stat']
    good_stat = stat[stat > 0]
    s = good_stat.sum()
    stat_ratio = good_stat / s
    weight = stat_ratio.to_dict()
    return weight
