from datetime import datetime, timedelta
from logger_factory import LoggerFactory


logger = LoggerFactory.getLogger(__name__)


class DayLogType:

    def get_type_name(type: int) -> str:

        if type == 0:
            return "その他"
        if type == 1:
            # left_time
            # right_time
            return "母乳"
        if type == 2:
            # amount
            return "ミルク"
        if type == 3:
            # amount
            return "搾母乳"
        if type == 4:
            return "寝る"
        if type == 5:
            return "起きる"
        if type == 6:
            return "おしっこ"
        if type == 7:
            return "うんち"
        if type == 8:
            # value
            return "体温"
        if type == 9:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 10:
            return "身長"
        if type == 11:
            return "体重"
        if type == 12:
            return "せき"
        if type == 13:
            return "吐く"
        if type == 14:
            return "発疹"
        if type == 15:
            return "けが"
        if type == 16:
            return "お風呂"
        if type == 17:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 18:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 19:
            # amount
            return "のみもの"
        if type == 20:
            return "くすり"
        if type == 21:
            return "病院"
        if type == 22:
            # value:さんぽ時間（秒）
            return "さんぽ"
        if type == 23:
            # amount
            return "搾乳"
        if type == 24:
            return "?お着替え"
        if type == 25:
            return "?保湿"
        if type == 26:
            return "?爪切り"
        if type == 27:
            return "家事"
        if type == 28:
            return "遊ぶ"
        if type == 29:
            # meta : 予防接種の詳細な内容
            return "予防接種"
        if type == 30:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 31:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 32:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 33:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 34:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 35:
            return "できた"
        if type == 36:
            # value
            return "頭囲"
        if type == 37:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 38:
            return "メモ"

        raise NotImplementedError(f"{type} is not valid.")

    def get_type_additional_memo(api_data: dict) -> str:
        type = api_data["type"]

        if type == 0:
            return ""
        if type == 1:
            # left_time
            # right_time
            return f"左 {int(api_data["left_time"]/60)}分 右 {int(api_data["right_time"]/60)}分"
        if type == 2:
            # amount
            return f"{api_data["amount"]}ml"
        if type == 3:
            # amount
            return f"{api_data["amount"]}ml"
        if type == 4:
            return ""
        if type == 5:
            return ""
        if type == 6:
            # TODO : 確認
            return ""
        if type == 7:
            # TODO : 確認
            # left_time
            # amount
            # value
            # が設定値？
            return ""
        if type == 8:
            # value
            return f"{api_data['value']}℃"
        if type == 9:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 10:
            return f"{api_data["value"]}cm"
        if type == 11:
            return f"{int(api_data["value"] * 1000)}g"
        if type == 12:
            return ""
        if type == 13:
            return ""
        if type == 14:
            return ""
        if type == 15:
            return ""
        if type == 16:
            return ""
        if type == 17:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 18:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 19:
            # amount
            return f"{api_data['amount']}ml"
        if type == 20:
            return ""
        if type == 21:
            return ""
        if type == 22:
            # value:さんぽ時間（秒）
            duration = timedelta(seconds=api_data["value"])
            return f"{duration.seconds//3600}時間{duration.seconds//60%60}分"
        if type == 23:
            # amount
            return f"{api_data['amount']}ml"
        if type == 24:
            return ""
        if type == 25:
            return ""
        if type == 26:
            return ""
        if type == 27:
            return ""
        if type == 28:
            return ""
        if type == 29:
            # meta : 予防接種の詳細な内容
            return ""
        if type == 30:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 31:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 32:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 33:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 34:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 35:
            return ""
        if type == 36:
            # value
            return f"{api_data['value']}cm"
        if type == 37:
            logger.warning("%s is unknown type.", type)
            return f"N/A({type})"
        if type == 38:
            return ""
