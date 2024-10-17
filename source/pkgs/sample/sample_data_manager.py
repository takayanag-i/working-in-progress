import pandas as pd

from pkgs.const.constants import TimetableConstants

class SampleDataManager:
    """
    Excelファイルからテストデータを読み込み，
    必要な構造を生成するクラス
    """

    def __init__(self, xls_path):
        """
        コンストラクタ

        Arguments:
            xls_path -- Excelファイルへのパス
        """

        # エクセルファイルの読み込み
        xls = pd.ExcelFile(xls_path)

        # 学級エンティティ
        self.homeroom_df = pd.read_excel(xls, 'クラス', usecols=['クラス'])

        # 科目エンティティ
        self.subject_df = pd.read_excel(xls, '科目', usecols=['科目ID', '学年', '科目名', '単位数'])

        # 講座エンティティ
        self.course_df = pd.read_excel(xls, '講座', usecols=['講座ID', '講座名', '科目ID'])

        # ブロックエンティティ
        self.block_df = pd.read_excel(xls, 'ブロック', usecols=['ブロックID', 'ブロック名'])

        # クラス-ブロックエンティティ
        self.class_block_df = pd.read_excel(xls, 'クラスブロック', usecols=['クラス', 'ブロックID'])

        # ブロック-レーンエンティティ
        self.block_lane_df = pd.read_excel(xls, 'ブロックレーン', usecols=['ブロックID', 'レーンID', 'レーン番号'])

        # レーン-講座エンティティ
        self.lane_course_df = pd.read_excel(xls, 'レーン講座', usecols=['レーンID', '講座ID'])

        # 教員エンティティ
        self.teacher_df = pd.read_excel(xls, '教員', usecols=['教員ID', '教員名'])

        # 講座-教員・教室エンティティ
        self.course_teacher_room_df = pd.read_excel(xls, '講座担当・教室', usecols=['講座ID', '教員ID', '教室ID'])

    def get_homeroom_list(self):
        """
        学級リストを取得する

        Returns:
            class_list -- 学級名のリスト
        """
        class_list = self.homeroom_df['クラス'].tolist()

        return class_list

    def get_day_of_week_list(self):
        """
        曜日リストを取得する

        Returns:
            曜日のリスト
        """

        return TimetableConstants.WEEKDAYS


    def get_schedule_dict(self):
        """
        日課表を表す辞書構造を生成する

        Returns:
            schedule_dict -- 学級名をキーとし，値として{曜日 -> 時限リスト}辞書を持つ辞書
        """

        # 普通　月7・火6・水6・木6・金6
        standard_76666 = {
                "Mon": { i for i in range(1,8)},
                "Tue": { i for i in range(1,7)},
                "Wed": { i for i in range(1,7)},
                "Thu": { i for i in range(1,7)},
                "Fri": { i for i in range(1,7)},
        }

        # 類型　月7・火7・水6・木6・金6
        feature_77666 = {
                "Mon": { i for i in range(1,8)},
                "Tue": { i for i in range(1,8)},
                "Wed": { i for i in range(1,7)},
                "Thu": { i for i in range(1,7)},
                "Fri": { i for i in range(1,7)},
        }

        return {
        "1-1": standard_76666,
        "1-2": standard_76666,
        "1-3": standard_76666,
        "1-4": standard_76666,
        "1-5": standard_76666,
        "1-6": standard_76666,
        "1-7": feature_77666,
        "2-1": standard_76666,
        "2-2": standard_76666,
        "2-3": standard_76666,
        "2-4": standard_76666,
        "2-5": standard_76666,
        "2-6": standard_76666,
        "2-7": feature_77666,
        "3-1": standard_76666,
        "3-2": standard_76666,
        "3-3": standard_76666,
        "3-4文": standard_76666,
        "3-4理": standard_76666,
        "3-5": standard_76666,
        "3-6": feature_77666
    }

    def get_course_list(self):
        """
        講座リストを取得する

        Returns:
            course_list -- 講座名のリスト
        """
        course_list = self.course_df['講座名'].tolist()

        return course_list

    def get_teacher_list(self):
        """
        教員リストを取得する

        Returns:
            teacher_list -- 教員名のリスト
        """
        teacher_list = self.teacher_df['教員名'].tolist()

        return teacher_list


    def get_curriculum_dict(self):
        """
        カリキュラムを表す辞書構造を生成する

        Returns:
            class_group_dict -- クラス名をキーとし、値としてブロック、レーン、講座の階層構造を持つ辞書
        """
        # 1. レーン-講座エンティティに講座エンティティを結合
        lane_course_df = self.lane_course_df.merge(self.course_df, left_on='講座ID', right_on='講座ID', how='left')

        # 2. ブロック-レーンエンティティにレーン-講座エンティティを結合
        block_lane_course_df = lane_course_df.merge(self.block_lane_df, left_on='レーンID', right_on='レーンID', how='left')

        # 3. クラス-ブロックエンティティにブロック-レーンエンティティを結合
        class_block_lane_course_df = block_lane_course_df.merge(self.class_block_df, left_on='ブロックID', right_on='ブロックID', how='left')

        # いったんレーンごとに講座名をリスト化
        lane_group = class_block_lane_course_df.groupby(['クラス', 'ブロックID', 'レーンID'])['講座名'].agg(list).reset_index()

        # さらにブロックごとにリストをリスト化
        block_group = lane_group.groupby(['クラス', 'ブロックID'])['講座名'].agg(list).reset_index()

        # 最終的にクラスごとにリスト化して辞書に変換
        class_group_dict = block_group.groupby('クラス')['講座名'].agg(list).to_dict()

        return class_group_dict

    def get_course_teacher_dict(self):
        """講座担当教員の辞書を生成する

        Returns:
            course_teacher_dict -- 講座名をキーとし，値として教員名のリスト持つ辞書
        """
        course_teacher_room_df  = pd.merge(self.course_teacher_room_df, self.teacher_df, on='教員ID', how='left')
        course_teacher_room_df = course_teacher_room_df.merge(self.course_df, on='講座ID', how='left')

        # 辞書を作成
        course_teacher_dict = course_teacher_room_df.groupby('講座名')['教員名'].agg(list).to_dict()

        return course_teacher_dict