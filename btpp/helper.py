from datetime import datetime, date, timedelta


def get_start_date_off(data_start_date, month_offset=6):
    month_offset = month_offset
    _start_date = date.fromisoformat(data_start_date)
    _start_date_off = _start_date - timedelta(days=month_offset * 31)
    start_date_off = _start_date_off.isoformat()
    return start_date_off


def get_real_start_trading_date(first_date_of_data, month_offset=6):
    _first_date_of_data = date.fromisoformat(first_date_of_data)
    start_trading_date = _first_date_of_data + \
        timedelta(days=month_offset * 31)
    return start_trading_date.isoformat()
