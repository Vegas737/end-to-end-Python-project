import pandas as pd
import pytest

def check_unique(df):
    return not df.duplicated(subset=['date', 'name']).any()

def check_not_null(df, col):
    return df[col].notna().all()


def test_unique_positive():
    df = pd.DataFrame({'date': ['2025-01-01', '2025-01-02'], 'name': ['A', 'B']})
    assert check_unique(df) == True

def test_unique_negative():
    df = pd.DataFrame({'date': ['2025-01-01', '2025-01-01'], 'name': ['A', 'A']})
    assert check_unique(df) == False

def test_null_negative():
    df = pd.DataFrame({'date': ['2025-01-01', None]})
    assert check_not_null(df, 'date') == False