from collections import defaultdict

class CollectionUtils:
    """
    コレクションに関するユーティリティクラス
    """

    def reverse_dict(self, target_dict: dict) -> dict:
        """
        辞書のキーと値（リスト型）を逆にする
        """
        reversed_default_dict = defaultdict(list)

        for key, list in target_dict.items():
            for element in list:
                reversed_default_dict[element].append(key)

        return dict(reversed_default_dict)  # 通常の辞書で返却