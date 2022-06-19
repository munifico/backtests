# %%
import pandas as pd
import yfinance as yf
import bt
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

# REF : https://medium.com/@richardhwlin/flexible-backtesting-with-bt-7295c0dde5dd

# %%
tickers = {
    'equity': ['ITOT', 'IVV', 'IJH', 'IJR', 'IUSG', 'IUSV', 'IJK', 'IJJ', 'IJS', 'IJT', 'OEF', 'IWC'],
    'bond': ['AGG', 'LQD', 'GOVT', 'MBB', 'MUB', 'TIP', 'SHY', 'IEF', 'TLT', 'HYG', 'FLOT', 'CMBS'],
}
prices = bt.data.get(tickers['equity'] + tickers['bond'], clean_tickers=False)

# %%

# # display Equity ETFs
prices[tickers['equity']].rebase().plot()
plt.title('Equity ETF Prices', {'fontsize': 16})
plt.legend(ncol=3)
plt.show()

# %%
# performance stats for backtests
mtest = prices[tickers['equity']].asfreq(
    'm', method='ffill').pct_change().dropna()
pd.DataFrame.from_dict({'annualized monthly return': mtest.mean()*12*100,
                        'annualized monthly volatility': mtest.std()*np.sqrt(12)*100,
                        'annualized monthly sharpe': mtest.mean() / mtest.std() * np.sqrt(12),
                        }).T.round(2)

# %%
pd.DataFrame.from_dict(
    {k: v.stats for k, v in bt.ffn.calc_stats(prices).items()}
)

# %%
# Display Bond ETFs
prices[tickers['bond']].rebase().plot()
plt.title('Bond ETF Prices', {'fontsize': 16})
plt.legend(ncol=3)
plt.show()

# %%
# performance stats for backtests
mtest = prices[tickers['bond']].asfreq(
    'm', method='ffill').pct_change().dropna()
pd.DataFrame.from_dict({'annualized monthly return': mtest.mean()*12*100,
                        'annualized monthly volatility': mtest.std()*np.sqrt(12)*100,
                        'annualized monthly sharpe': mtest.mean() / mtest.std() * np.sqrt(12),
                        }).T.round(2)

# %%
pd.DataFrame.from_dict(
    {k: v.stats for k, v in bt.ffn.calc_stats(prices).items()}
)
