from datetime import date, timedelta
from core.piyolog_parser.piyolog_parser_day import PiyoLogParserDay
from core.piyolog_parser.piyolog_parser_month import PiyoLogParserMonth

UNITTEST_ASSERT_STR_MEMO_DAILY = """----------
2025/2/8(土)
あかさん (4か月13日)

10:05   起きる (10時間35分)  
10:25   ミルク 200ml  
11:55   おしっこ  
12:40   寝る  
13:35   起きる (0時間55分)  
13:50   ミルク 200ml  
14:15   さんぽ  30分ほど
14:45   おしっこ  
15:15   メモ  ネスペの教科書読み聞かせたらめちゃくちゃ泣かれた

笑ってしまった笑　まだ早かったか　by彩花
16:00   寝る  
16:50   起きる (0時間50分)  
17:05   ミルク 200ml  
19:30   お風呂  
19:40   くすり  
19:40   保湿  
20:00   ミルク 200ml  
21:00   おしっこ  
21:00   うんち (多め/黄色)  
21:25   寝る  

母乳合計 左 0分 / 右 0分
ミルク合計 4回 800ml
睡眠合計 14時間25分
おしっこ合計 3回
うんち合計 1回

【家事】
☑︎洗濯回す🧺(大人)
☑︎洗面台の排水溝の蓋ダイソーで買えたら、変える
☑︎洗い物適宜
☑︎智也のベビーバス洗う🧼

未達
クイックルワイパー(毛の掃除🧹)

"""


def test_parse_record_contains_daily_memo():
    # Arrange
    parser = PiyoLogParserMonth()

    # Act
    record = parser.parse_str(UNITTEST_ASSERT_STR_MEMO_DAILY)

    # Assert
    assert (
        record[0].daily_memo
        == """【家事】
☑︎洗濯回す🧺(大人)
☑︎洗面台の排水溝の蓋ダイソーで買えたら、変える
☑︎洗い物適宜
☑︎智也のベビーバス洗う🧼

未達
クイックルワイパー(毛の掃除🧹)"""
    )
