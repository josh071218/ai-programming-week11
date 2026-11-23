import pandas as pd
from analysis import 정제


def test_정제하면_100행이_남는다():
    df = 정제(pd.read_csv("scores_2026.csv"))
    assert len(df) == 100


def test_반은_두_종류만_남는다():
    df = 정제(pd.read_csv("scores_2026.csv"))
    assert sorted(df["반"].unique()) == ["1반", "2반"]


def test_그룹합이_전체합과_같다():
    df = 정제(pd.read_csv("scores_2026.csv"))
    assert df.groupby("반")["점수"].sum().sum() == df["점수"].sum()


def test_손계산과_일치한다():
    mini = 정제(pd.read_csv("mini.csv"))
    평균 = mini.groupby("반")["점수"].mean()
    assert len(mini) == 7
    assert 평균["1반"] == 80.0
    assert 평균["2반"] == 70.0