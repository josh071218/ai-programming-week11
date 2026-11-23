import pandas as pd


def 정제(df):
    df = df.copy()
    df["점수"] = pd.to_numeric(df["점수"], errors="coerce")

    df = df.dropna(subset=["점수"])
    print(f"점수 결측 행 삭제 후: {len(df)}행")

    df = df.drop_duplicates()
    print(f"중복 행 삭제 후: {len(df)}행")

    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print(f"공백 제거 후: {len(df)}행")

    df = df[df["점수"].isin(range(101))]
    print(f"유효하지 않은 점수 행 삭제 후: {len(df)}행")

    return df

if __name__ == "__main__":
    df = pd.read_csv("scores_2026.csv")
    df = 정제(df)

    수학 = df[df["과목"] == "수학"]
    print("수학 과목 행 수:", len(수학))

    반별_점수_평균 = df.groupby("반")["점수"].mean()
    print("\n반별 점수 평균:")
    print(반별_점수_평균)

    과목_반별_점수_평균 = df.groupby(["과목", "반"])["점수"].mean()
    print("\n과목·반별 점수 평균:")
    print(과목_반별_점수_평균)

    반별_점수_통계 = (
        df.groupby("반")["점수"]
        .agg(["count", "mean", "median", "max"])
        .rename(columns={
            "count": "개수",
            "mean": "평균",
            "median": "중앙값",
            "max": "최댓값",
        })
        .round(2)
    )

    print("\n반별 점수 통계:")
    print(반별_점수_통계)
    print("\n[합계 검증]")
    print("반별 합계의 합:", df.groupby("반")["점수"].sum().sum())
    print("전체 점수 합계:", df["점수"].sum())

    print("\n[개수 검증]")
    print("반별 개수의 합:", df.groupby("반")["점수"].count().sum())
    print("전체 데이터 개수:", len(df))
    print("\n[스팟 체크: 1반 수학]")
    점수목록 = df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"]

    print("점수 목록:", 점수목록.tolist())
    print("점수 개수:", len(점수목록))
    print("점수 합계:", 점수목록.sum())
    print("점수 평균:", 점수목록.mean())
    print("\n[mini.csv 손계산 검증]")
    미니 = pd.read_csv("mini.csv")
    미니 = 정제(미니)

    print("정제 후 행 수:", len(미니))
    print("1반 평균:", 미니[미니["반"] == "1반"]["점수"].mean())
    print("2반 평균:", 미니[미니["반"] == "2반"]["점수"].mean())