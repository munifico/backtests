import pandas as pd
import numpy as np
import bt

# Lib For Relative Momentum Strategy
# https: // pmorissette.github.io/bt/_modules/bt/algos.html#StatTotalReturn

DEFAULT = {
    'lookbacks': [
        pd.DateOffset(months=1),
        pd.DateOffset(months=3),
        pd.DateOffset(months=6),
        pd.DateOffset(months=12)
    ],
    "lookback_weights": [5, 3, 2, 0],
    "lag": pd.DateOffset(days=0),
}

###########################################
# Class for tmep["stat"]
###########################################


class StatMomentumReturn(bt.Algo):

    def __init__(
        self,
        lookbacks=DEFAULT.get("lookbacks"),
        lookback_weights=DEFAULT.get("lookback_weights"),
        lag=DEFAULT.get("lag")
    ):
        super(StatMomentumReturn, self).__init__()
        self.lookbacks = lookbacks
        self.lookback_weights = lookback_weights
        self.lag = lag

    def __call__(self, target):

        selected = target.temp["selected"]
        # init stat
        stat = target.universe.loc[target.now, selected] * 0

        for i, lookback in enumerate(self.lookbacks):
            t0 = target.now - self.lag
            prc = target.universe.loc[(t0 - lookback): t0, selected]
            _stat = prc.calc_total_return() * self.lookback_weights[i]
            stat = stat + _stat

        target.temp["stat"] = stat / sum(self.lookback_weights)

        return True

###########################################
# Class for tmep["selected"]
###########################################


class SelectAssets(bt.Algo):

    def __init__(
        self,
        n,
        alternative_n=1,
        assets=[],
        alternative_assets=[],
        sort_descending=True,
        # True 일때 : 하나의 자산이라도 모멘텀이 0보다 작으면 대체자산으로 이동
        all_or_none=False
    ):
        super(SelectAssets, self).__init__()
        if n < 0:
            raise ValueError("n cannot be negative")
        self.n = n
        self.alternative_n = alternative_n
        self.assets = assets
        self.alternative_assets = alternative_assets
        self.ascending = not sort_descending
        self.all_or_none = all_or_none

    def __call__(self, target):
        stat = target.temp["stat"].dropna()

        core_assets = self.assets
        alter_assets = self.alternative_assets

        core_stat = stat.loc[core_assets].sort_values(
            ascending=self.ascending)

        alter_stat = stat.loc[alter_assets].sort_values(
            ascending=self.ascending)

        # print("# core_stat")
        # print(core_stat)

        # handle percent n
        keep_n = self.n
        if self.n < 1:
            keep_n = int(self.n * len(core_stat))

        alter_n = self.alternative_n
        if self.alternative_n < 1:
            alter_n = int(self.alternative_n * len(alter_stat))

        core_stat_gt0 = core_stat[core_stat > 0]

        # print("core_stat_gt0")
        # print(core_stat_gt0)

        if self.all_or_none:
            if core_stat_gt0.size > keep_n:
                # 모두 0보다 크면 자산 상위 n개 선택
                sel = list(core_stat[:keep_n].index)
            else:
                # 모두 0보다 크지 않으면 대안 자산으로 이동
                sel = list(alter_stat[:alter_n].index)
        else:
            if core_stat_gt0.size > 0:
                # 0 보다 큰 것이 하나라도 있으면 n개 선택
                sel = list(core_stat_gt0[:keep_n].index)
            else:
                # 0보다 큰 것이 없으면 대안 자산으로 이동
                sel = list(alter_stat[:alter_n].index)

        target.temp["selected"] = sel
        return True

# REF: https://pmorissette.github.io/bt/_modules/bt/algos.html#SelectN
# temp["stat"]이 0보다 큰 경우만 고름


class SelectCondition(bt.Algo):
    def __init__(
        self,
        n,
        condition="{} > 0",
        sort_descending=True,
        all_or_none=False,
        filter_selected=False
    ):
        super(SelectCondition, self).__init__()
        if n < 0:
            raise ValueError("n cannot be negative")
        self.n = n
        self.ascending = not sort_descending
        self.filter_selected = filter_selected

    def __call__(self, target):
        stat = target.temp["stat"].dropna()
        if self.filter_selected and "selected" in target.temp:
            stat = stat.loc[stat.index.intersection(target.temp["selected"])]
        stat.sort_values(ascending=self.ascending, inplace=True)

        n_val = self.condition.count("{}")
        vals = ["stat"] * n_val
        cond_str = self.condition.format(*vals)
        stat = stat.loc[eval(cond_str)]

        # handle percent n
        keep_n = self.n
        if self.n < 1:
            keep_n = int(self.n * len(stat))

        sel = list(stat[:keep_n].index)

        if self.all_or_none and len(sel) < keep_n:
            sel = []

        target.temp["selected"] = sel

        return True

###########################################
# Class for tmep["selected"] ( Stack Class )
###########################################

# https://pmorissette.github.io/bt/_modules/bt/algos.html#SelectMomentum


class SelectRelativeMomentum(bt.AlgoStack):

    def __init__(
        self,
        n,
        lookbacks=DEFAULT.get("lookbacks"),
        lookback_weights=DEFAULT.get("lookback_weights"),
        lag=DEFAULT.get("lag"),
        # out_market_asset=None,
        sort_descending=True,
        all_or_none=False,
        filter_selected=False
    ):
        super(SelectRelativeMomentum, self).__init__(
            StatMomentumReturn(
                lookbacks=lookbacks,
                lookback_weights=lookback_weights,
                lag=lag
            ),
            bt.algos.SelectN(
                n=n,
                sort_descending=sort_descending,
                all_or_none=all_or_none,
                filter_selected=filter_selected
            ),
        )


class SelectAbsoluteMomentum(bt.AlgoStack):
    def __init__(
        self,
        n,
        lookbacks=DEFAULT.get("lookbacks"),
        lookback_weights=DEFAULT.get("lookback_weights"),
        lag=DEFAULT.get("lag"),
        condition="{} > 0",
        sort_descending=True,
        all_or_none=False,
        filter_selected=False
    ):
        super(SelectAbsoluteMomentum, self).__init__(
            StatMomentumReturn(
                lookbacks=lookbacks,
                lookback_weights=lookback_weights,
                lag=lag
            ),
            SelectCondition(
                n=n,
                condition=condition,
                sort_descending=sort_descending,
                all_or_none=all_or_none,
                filter_selected=filter_selected
            ),
        )


class SelectDualMomentum(bt.AlgoStack):
    def __init__(
        self,
        n,
        alternative_n=1,
        lookbacks=DEFAULT.get("lookbacks"),
        lookback_weights=DEFAULT.get("lookback_weights"),
        lag=DEFAULT.get("lag"),
        assets=[],
        alternative_assets=[],
        sort_descending=True,
        all_or_none=False,
    ):
        super(SelectDualMomentum, self).__init__(
            StatMomentumReturn(
                lookbacks=lookbacks,
                lookback_weights=lookback_weights,
                lag=lag
            ),
            SelectAssets(
                n=n,
                alternative_n=alternative_n,
                assets=assets,
                alternative_assets=alternative_assets,
                sort_descending=sort_descending,
                all_or_none=all_or_none
            ),
        )


class WeighFunctionally(bt.Algo):

    def __init__(self, fn):
        super(WeighFunctionally, self).__init__()
        self.fn = fn

    def __call__(self, target):
        target.temp["weights"] = self.fn(target)
        return True


#########################################################
# Weights
#########################################################

class WeighFunctionally(bt.Algo):

    def __init__(self, fn):
        super(WeighFunctionally, self).__init__()
        self.fn = fn

    def __call__(self, target):
        target.temp["weights"] = self.fn(target)
        return True


class WeighSpecifiedMonthly(bt.Algo):

    weights_with_months = [
        {
            "weights": {},
            "months": [11, 12, 1, 2, 3, 4]
        },
        {
            "weights": {},
            "months": [5, 6, 7, 8, 9, 10]
        },
    ]

    def __init__(self, weights_with_months):
        super(WeighSpecifiedMonthly, self).__init__()
        self.wm = weights_with_months

    def __call__(self, target):
        for it in self.wm:
            if target.now.month in it["months"]:
                target.temp["weights"] = it["weights"].copy()

        return True
