import pandas as pd

class TestDataManager:
    """
    Excelファイルからテストデータを読み込み，
    辞書を生成するクラス
    """

    def __init__(self, excel_path):
        """
        TestDataManagerを初期化する

        Arguments:
            excel_path -- Excelデータファイルへのパス
        """
        self.excel_path = excel_path

    def getSampleDict(self):
        """
        指定されたExcelファイルからデータを読み込み、クラスカリキュラムを表現する
        ネストされた辞書構造を生成する

        Returns:
            dict -- クラス名をキーとし、ブロック、レーン、講座の構造を持つ辞書
        """
        # エクセルファイルの読み込み
        xls = pd.ExcelFile(self.excel_path)

        class_df = pd.read_excel(xls, 'クラス', usecols=['クラス'])
        subject_df = pd.read_excel(xls, '科目', usecols=['科目ID', '学年', '科目名', '単位数'])
        lecture_df = pd.read_excel(xls, '講座', usecols=['講座ID', '講座名'])
        block_df = pd.read_excel(xls, 'ブロック', usecols=['ブロックID', 'ブロック名'])
        block_lane_df = pd.read_excel(xls, 'ブロックレーン', usecols=['ブロックID', 'レーンID', 'レーン番号'])
        lane_lecture_df = pd.read_excel(xls, 'レーン講座', usecols=['レーンID', '講座ID'])
        class_block_df = pd.read_excel(xls, 'クラスブロック', usecols=['クラス', 'ブロックID'])

        # 1. レーン-講座に講座を結合
        lane_lecture_df = lane_lecture_df.merge(lecture_df, left_on='講座ID', right_on='講座ID', how='left')

        # 2. ブロック-レーンにレーン-講座を結合
        block_lane_lecture_df = lane_lecture_df.merge(block_lane_df, left_on='レーンID', right_on='レーンID', how='left')

        # 3. クラス-ブロックにブロック-レーンを結合
        final_df = block_lane_lecture_df.merge(class_block_df, left_on='ブロックID', right_on='ブロックID', how='left')

        # 講座名をリスト化
        lane_group = final_df.groupby(['クラス', 'ブロックID', 'レーンID'])['講座名'].agg(list).reset_index()

        # レーンごとにリスト化
        block_group = lane_group.groupby(['クラス', 'ブロックID'])['講座名'].agg(list).reset_index()

        # ブロックごとにリスト化
        final_result = block_group.groupby('クラス')['講座名'].agg(list).to_dict()

        return final_result
