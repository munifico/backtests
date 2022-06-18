# %%
import pandas as pd
import numpy as np
import bt

# Lib For Relative Momentum Strategy
# %%
# https: // pmorissette.github.io/bt/_modules/bt/algos.html#StatTotalReturn


class StatMomentumReturn(bt.Algo):

    def __init__(
        self,
        lookbacks=[
            pd.DateOffset(months=1),
            pd.DateOffset(months=3),
            pd.DateOffset(months=6),
            pd.DateOffset(months=12)
        ],
        lookback_weights=[0.3, 0.3, 0.3, 0],
        lag=pd.DateOffset(days=0),
        out_market_asset=None
    ):

        super(StatMomentumReturn, self).__init__()
        self.lookbacks = lookbacks
        self.lookback_weights = lookback_weights
        self.lag = lag
        self.out_market_asset = out_market_asset

    def __call__(self, target):

        selected = target.temp["selected"]

        for i, lookback in enumerate(self.lookbacks):
            t0 = target.now - self.lag
            prc = target.universe.loc[(t0 - lookback): t0, selected]
            stat = prc.calc_total_return() * self.lookback_weights[i]

            if "stat" in target.temp:
                target.temp["stat"] = target.temp["stat"] + stat
            else:
                target.temp["stat"] = stat

        if (self.out_market_asset is not None) and (not target.temp["stat"].isnull().values.any()):
            target.temp["stat"][self.out_market_asset] = 0

        # print(target.temp)

        return True

# %%
# https://pmorissette.github.io/bt/_modules/bt/algos.html#SelectMomentum


class SelectRelativeMomentum(bt.AlgoStack):

    def __init__(
        self,
        n=1,
        lookbacks=[
            pd.DateOffset(months=1),
            pd.DateOffset(months=3),
            pd.DateOffset(months=6),
            pd.DateOffset(months=12)
        ],
        lookback_weights=[0.3, 0.3, 0.3, 0],
        lag=pd.DateOffset(days=0),
        # out_market_asset=None,
        sort_descending=True,
        all_or_none=False
    ):
        super(SelectRelativeMomentum, self).__init__(
            StatMomentumReturn(
                lookbacks=lookbacks,
                lookback_weights=lookback_weights,
                lag=lag,
                out_market_asset=None
            ),
            bt.algos.SelectN(
                n=n,
                sort_descending=sort_descending,
                all_or_none=all_or_none
            ),
        )

# %%


class SelectDualMomentum(bt.AlgoStack):

    def __init__(
        self,
        n=1,
        lookbacks=[
            pd.DateOffset(months=1),
            pd.DateOffset(months=3),
            pd.DateOffset(months=6),
            pd.DateOffset(months=12)
        ],
        lookback_weights=[0.3, 0.3, 0.3, 0],
        lag=pd.DateOffset(days=0),
        out_market_asset=None,
        sort_descending=True,
        all_or_none=False
    ):
        super(SelectDualMomentum, self).__init__(
            StatMomentumReturn(
                lookbacks=lookbacks,
                lookback_weights=lookback_weights,
                lag=lag,
                out_market_asset=out_market_asset
            ),
            bt.algos.SelectN(
                n=n,
                sort_descending=sort_descending,
                all_or_none=all_or_none
            ),
        )
