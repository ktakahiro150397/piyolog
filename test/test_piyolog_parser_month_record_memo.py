from datetime import date, timedelta
from core.piyolog_parser.piyolog_parser_day import PiyoLogParserDay
from core.piyolog_parser.piyolog_parser_month import PiyoLogParserMonth

UNITTEST_ASSERT_STR_MEMO_FINAL = """----------
2024/12/1(日)
あかさん (0歳2か月5日)

01:45   起きる (2時間5分)   
01:50   ミルク 120ml   
02:00   寝る   
04:45   起きる (2時間45分)   
04:50   ミルク 140ml   
22:05   起きる (0時間15分)   
23:00   寝る   22:40 ちょこちょこ起きるなぁ。
「ひぁあっ！！」って、思い出したように男梅になるのやめておくれ。もうお風呂入るよ。深い睡眠に移行するんだ智也💩

母乳合計　　   左 0分 / 右 0分
ミルク合計　   5回 700ml
睡眠合計　　   9時間50分
おしっこ合計   5回
うんち合計　   1回

E赤ちゃんにしてから、ミルクの吐き戻しが少なくなった気がする。

"""

UNITTEST_ASSERT_STR_MEMO_MIDDLE = """----------
2024/12/1(日)
あかさん (0歳2か月5日)

01:45   起きる (2時間5分)   
01:50   ミルク 120ml   
02:00   寝る   
04:45   起きる (2時間45分)   
04:50   ミルク 140ml   
22:05   起きる (0時間15分)   
23:00   寝る   22:40 ちょこちょこ起きるなぁ。
「ひぁあっ！！」って、思い出したように男梅になるのやめておくれ。もうお風呂入るよ。深い睡眠に移行するんだ智也💩
04:50   ミルク 140ml   

母乳合計　　   左 0分 / 右 0分
ミルク合計　   5回 700ml
睡眠合計　　   9時間50分
おしっこ合計   5回
うんち合計　   1回

E赤ちゃんにしてから、ミルクの吐き戻しが少なくなった気がする。

"""

UNITTEST_ASSERT_STR_MEMO_MULTILINE = """----------
2024/12/1(日)
あかさん (0歳2か月5日)

06:50   ミルク 160ml   
11:35   くすり   腕:ゴワゴワ感は残る
背中,お腹:綺麗
足:ちょっと赤みと湿疹があり

まだ薬塗らんと赤みと湿疹がぶり返してくる感がある。プロペトだけやと、ちょっと不安。
13:00   寝る   

母乳合計　　   左 0分 / 右 0分
ミルク合計　   5回 700ml
睡眠合計　　   9時間50分
おしっこ合計   5回
うんち合計　   1回

E赤ちゃんにしてから、ミルクの吐き戻しが少なくなった気がする。

"""

UNITTEST_ASSERT_STR_MEMO_HHMM = """----------
2025/1/2(木)
あかさん (0歳3か月7日)

07:45   起きる (10時間15分)   
07:55   ミルク 180ml   
20:20   遊ぶ   ドラえもん見る。
20:35 腹減ってきて泣いてる。
みよこでも腹減りは誤魔化せないのか…
20:35   ミルク 160ml   
21:30   寝る   たまに「ふぇえぇ😭」って言うてるけど、たぶん寝てる。

母乳合計　　   左 0分 / 右 0分
ミルク合計　   5回 800ml
睡眠合計　　   10時間30分
おしっこ合計   2回
うんち合計　   3回

だんだん授乳回数が5回になってきている？
ここ2〜3日、夜間起きひんからやな。
今日はめっちゃうんこしたな💩

"""

def test_parse_record_contains_date_memo_final():
    # Arrange
    parser = PiyoLogParserMonth()

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR_MEMO_FINAL)

    # Assert
    assert len(record[0].records) == 7
    assert record[0].records[6].record_memo == """22:40 ちょこちょこ起きるなぁ。
「ひぁあっ！！」って、思い出したように男梅になるのやめておくれ。もうお風呂入るよ。深い睡眠に移行するんだ智也💩"""

def test_parse_record_contains_date_memo_middle():
    # Arrange
    parser = PiyoLogParserMonth()

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR_MEMO_MIDDLE)

    # Assert
    assert len(record[0].records) == 8
    assert record[0].records[6].record_memo == """22:40 ちょこちょこ起きるなぁ。
「ひぁあっ！！」って、思い出したように男梅になるのやめておくれ。もうお風呂入るよ。深い睡眠に移行するんだ智也💩"""

def test_parse_record_contains_multiline():
    # Arrange
    parser = PiyoLogParserMonth()

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR_MEMO_MULTILINE)

    # Assert
    assert len(record[0].records) == 3
    assert record[0].records[1].record_memo == """腕:ゴワゴワ感は残る
背中,お腹:綺麗
足:ちょっと赤みと湿疹があり

まだ薬塗らんと赤みと湿疹がぶり返してくる感がある。プロペトだけやと、ちょっと不安。"""

def test_parse_record_contains_hhmm():
    # Arrange
    parser = PiyoLogParserMonth()

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR_MEMO_HHMM)

    # Assert
    assert len(record[0].records) == 5
    assert record[0].records[2].record_memo == """ドラえもん見る。
20:35 腹減ってきて泣いてる。
みよこでも腹減りは誤魔化せないのか…"""
