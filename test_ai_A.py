import pytest

from load_scores import load_scores


def write_csv(tmp_path, content, *, encoding="utf-8"):
    path = tmp_path / "test_scores.csv"
    path.write_text(content, encoding=encoding)
    return path


def test_유효한_성적을_읽는다(tmp_path):
    path = write_csv(tmp_path, "name,score\n김하나,88\n이두리,75\n")

    kept, skipped = load_scores(path)

    assert kept == [("김하나", 88), ("이두리", 75)]
    assert skipped == []


def test_빈_줄은_기록하지_않고_건너뛴다(tmp_path):
    path = write_csv(tmp_path, "name,score\n\n김하나,88\n\n이두리,75\n")

    kept, skipped = load_scores(path)

    assert kept == [("김하나", 88), ("이두리", 75)]
    assert skipped == []


def test_쉼표가_포함된_이름을_읽는다(tmp_path):
    path = write_csv(tmp_path, 'name,score\n"최,네번",77\n')

    kept, skipped = load_scores(path)

    assert kept == [("최,네번", 77)]
    assert skipped == []


def test_같은_이름의_행을_모두_남긴다(tmp_path):
    path = write_csv(tmp_path, "name,score\n김하나,88\n김하나,91\n")

    kept, skipped = load_scores(path)

    assert kept == [("김하나", 88), ("김하나", 91)]
    assert skipped == []


def test_utf8_bom이_있는_파일을_읽는다(tmp_path):
    path = write_csv(
        tmp_path,
        "name,score\n김하나,88\n",
        encoding="utf-8-sig",
    )

    kept, skipped = load_scores(path)

    assert kept == [("김하나", 88)]
    assert skipped == []


def test_파일이_없으면_FileNotFoundError를_발생시킨다(tmp_path):
    path = tmp_path / "없는파일.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(path)


def test_헤더만_있으면_빈_결과를_반환한다(tmp_path):
    path = write_csv(tmp_path, "name,score\n")

    assert load_scores(path) == ([], [])


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("김하나", "열 개수가 2가 아님"),
        ("김하나,80,비고", "열 개수가 2가 아님"),
        (",80", "이름이 비어 있음"),
        ("김하나,", "점수가 비어 있음"),
        ("김하나,결석", "점수가 정수가 아님"),
        ("김하나,-1", "점수가 0~100 밖"),
        ("김하나,101", "점수가 0~100 밖"),
    ],
)
def test_잘못된_행을_사유와_함께_기록한다(tmp_path, row, reason):
    path = write_csv(tmp_path, f"name,score\n{row}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [(2, row, reason)]


@pytest.mark.parametrize("score", [0, 100])
def test_점수_경계값은_정상으로_포함한다(tmp_path, score):
    path = write_csv(tmp_path, f"name,score\n김하나,{score}\n")

    kept, skipped = load_scores(path)

    assert kept == [("김하나", score)]
    assert skipped == []