import pytest

from load_scores import load_scores


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert isinstance(kept, list)
    assert isinstance(skipped, list)
    assert len(kept) > 0


def test_빈_줄은_건너뛴다(tmp_path):
    file = tmp_path / "빈줄.csv"
    file.write_text("name,score\n김하나,88\n\n이두리,75\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("김하나", 88), ("이두리", 75)]
    assert skipped == []
  
  
def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    file = tmp_path / "쉼표.csv"
    file.write_text('name,score\n"최,네번",77\n', encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("최,네번", 77)]
    assert skipped == []


def test_없는_파일이면_오류가_난다(tmp_path):
    file = tmp_path / "없는파일.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(file)


 
def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")

    assert kept == []
    assert skipped == []
   

def test_0점은_정상이다(tmp_path):
    file = tmp_path / "0점.csv"
    file.write_text("name,score\n김하나,0\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("김하나", 0)]
    assert skipped == []


def test_100점은_정상이다(tmp_path):
    file = tmp_path / "100점.csv"
    file.write_text("name,score\n김하나,100\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("김하나", 100)]
    assert skipped == []


def test_101점은_제외한다(tmp_path):
    file = tmp_path / "101점.csv"
    file.write_text("name,score\n김하나,101\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][0] == 2

  
def test_이름이_비어_있으면_제외한다(tmp_path):
    file = tmp_path / "빈이름.csv"
    file.write_text("name,score\n,80\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][0] == 2
    assert skipped[0][2] == "이름이 비어 있음"
  
  