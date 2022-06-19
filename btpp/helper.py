from datetime import datetime, date, timedelta


def get_start_date_off(data_start_date, month_offset=6):
    month_offset = month_offset
    _start_date = date.fromisoformat(data_start_date)
    _start_date_off = _start_date - timedelta(days=month_offset * 31)
    start_date_off = _start_date_off.isoformat()
    return start_date_off


def get_real_start_trading_date(user_start_date, first_date_of_data):
    _user_start_date = date.fromisoformat(user_start_date)
    _first_date_of_data = date.fromisoformat(first_date_of_data)
    start_trading_date = _first_date_of_data if _user_start_date < _first_date_of_data else _user_start_date
    return start_trading_date.isoformat()
