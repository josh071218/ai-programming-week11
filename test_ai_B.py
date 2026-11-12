import pytest

from load_scores import load_scores


def test_정상_파일을_읽는다(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n김하나,88\n이두리,75\n", encoding="utf-8")

    assert load_scores(file) == [("김하나", 88), ("이두리", 75)]


def test_빈_파일은_빈_목록을_반환한다(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(file) == []


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    file = tmp_path / "comma.csv"
    file.write_text('name,score\n"최,네번",77\n', encoding="utf-8")

    assert load_scores(file) == [("최,네번", 77)]


@pytest.mark.parametrize(
    "row",
    [
        "김하나",             # 열 부족
        "김하나,80,비고",     # 열 초과
        ",80",                # 이름 없음
        "김하나,",            # 점수 없음
        "김하나,결석",        # 숫자가 아닌 점수
        "김하나,-1",          # 최솟값 미만
        "김하나,101",         # 최댓값 초과
    ],
)
def test_잘못된_행은_건너뛴다(tmp_path, row):
    file = tmp_path / "invalid.csv"
    file.write_text(f"name,score\n{row}\n", encoding="utf-8")

    assert load_scores(file) == []


def test_유효한_행만_반환하고_빈_줄은_무시한다(tmp_path):
    file = tmp_path / "mixed.csv"
    file.write_text(
        "name,score\n김하나,88\n\n,80\n이두리,75\n",
        encoding="utf-8",
    )

    assert load_scores(file) == [("김하나", 88), ("이두리", 75)]


@pytest.mark.parametrize("score", [0, 100])
def test_점수_범위의_양끝은_유효하다(tmp_path, score):
    file = tmp_path / "boundary.csv"
    file.write_text(f"name,score\n김하나,{score}\n", encoding="utf-8")

    assert load_scores(file) == [("김하나", score)]


def test_없는_파일이면_FileNotFoundError가_발생한다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_읽을_수_없으면_PermissionError가_발생한다(tmp_path, monkeypatch):
    file = tmp_path / "unreadable.csv"

    def deny_open(*args, **kwargs):
        raise PermissionError("읽기 권한이 없습니다")

    monkeypatch.setattr("builtins.open", deny_open)

    with pytest.raises(PermissionError):
        load_scores(file)