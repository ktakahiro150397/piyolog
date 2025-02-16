PIYOLOG_EXPORT_FILE_DELIMITER = "   "
"""ぴよログファイルのエクスポートファイルのデリミタ。
iOS版とAndroid版で異なる。

iOS: 
HH:MM/種類/メモ がすべてこのデリミタで区切られている。

Android: 
HH:MM/種類 はこのデリミタで区切られている。
種類/メモ はPIYOLOG_EXPORT_FILE_ANDROID_MEMO_DELIMITERで区切られている。
"""

PIYOLOG_EXPORT_FILE_ANDROID_MEMO_DELIMITER = "  "
"""Android出力ファイルのメモ部分のデリミタ。"""
