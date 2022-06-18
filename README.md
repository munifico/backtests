# Try BackTest  !!!

## 준비물

### Project Manager : [Poetry](https://python-poetry.org/docs/cli/)

Excute Scripts

```bash
poetry run python my_script.py
```

### VSCode 

[VSCode Python Interactive window](https://code.visualstudio.com/docs/python/jupyter-support-py)

### Packages

* jupyter (for VSCode Python Interactive window)
* [bt - Flexible Backtesting for Python](https://pmorissette.github.io/bt/)
* yfinance

```bash
poetry add jupyter bt yfinance
```

## 구성

* bt_SAA.py : backtest static asset allocation
* bt_SAA_BG.py : backtest static asset allocation ( golden butterfly )
* bt_MAA.py : backtest momentum asset allocation
* bt_MAA_RM.py : backtest momentum asset allocation ( relative momentum )

## 실습자료

* [Flexible Backtesting for Python 1](https://beok.tistory.com/51)
* [Flexible Backtesting with BT](https://medium.com/@richardhwlin/flexible-backtesting-with-bt-7295c0dde5dd)
* [Advanced Backtesting with BT. Introduction | by Richard L | Medium](https://medium.com/@richardhwlin/advanced-backtesting-with-bt-635ed441cb60)