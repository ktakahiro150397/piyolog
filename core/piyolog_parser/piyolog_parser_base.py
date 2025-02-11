class PiyoLogParserBase:
    """ぴよログファイルパーサーの基底クラス"""

    def __init__(self):
        pass

    def parse_file(self, file_path: str):
        # Implement this method in the subclass
        raise NotImplementedError()
