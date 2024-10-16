import pandas as pd

class SampleDataManager:
    """
    Excelファイルからテストデータを読み込み，
    必要な構造を生成するクラス
    """

    def __init__(self, excel_path):
        """
        コンストラクタ

        Arguments:
            excel_path -- xlsファイルへのパス
        """
        self.excel_path = excel_path

        # エクセルファイルの読み込み
        xls = pd.ExcelFile(self.excel_path)

        self.class_df = pd.read_excel(xls, 'クラス', usecols=['クラス'])
        self.subject_df = pd.read_excel(xls, '科目', usecols=['科目ID', '学年', '科目名', '単位数'])
        self.course_df = pd.read_excel(xls, '講座', usecols=['講座ID', '講座名', '科目ID'])
        self.block_df = pd.read_excel(xls, 'ブロック', usecols=['ブロックID', 'ブロック名'])
        self.block_lane_df = pd.read_excel(xls, 'ブロックレーン', usecols=['ブロックID', 'レーンID', 'レーン番号'])
        self.lane_course_df = pd.read_excel(xls, 'レーン講座', usecols=['レーンID', '講座ID'])
        self.class_block_df = pd.read_excel(xls, 'クラスブロック', usecols=['クラス', 'ブロックID'])
        self.teacher_df = pd.read_excel(xls, '教員', usecols=['教員ID', '教員名'])
        self.course_teacher_room_df = pd.read_excel(xls, '講座担当・教室', usecols=['講座ID', '教員ID', '教室ID'])

    def get_homeroom_list(self):
        """
        クラスリストを取得する

        Returns:
            class_list -- クラス名のリスト
        """
        class_list = self.class_df['クラス'].tolist()

        return class_list

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
            class_group_dict -- クラス名をキーとし、ブロック、レーン、講座の階層構造を持つ辞書
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
            course_teacher_dict -- 講座名をキーとし、教員名のリストを持つ辞書
        """
        course_teacher_room_df  = pd.merge(self.course_teacher_room_df, self.teacher_df, on='教員ID', how='left')
        course_teacher_room_df = course_teacher_room_df.merge(self.course_df, on='講座ID', how='left')

        # 辞書を作成
        course_teacher_dict = course_teacher_room_df.groupby('講座名')['教員名'].agg(list).to_dict()

        return course_teacher_dict

    def get_schedule(self):
        return {
        "1-1": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "1-2": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "1-3": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "1-4": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "1-5": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "1-6": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "1-7": {
            "Mon": { i for i in range(1,8)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "2-1": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "2-2": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "2-3": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "2-4": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "2-5": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "2-6": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "2-7": {
            "Mon": { i for i in range(1,8)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "3-1": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "3-2": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "3-3": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "3-4文": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "3-4理": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "3-5": {
            "Mon": { i for i in range(1,7)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        },
        "3-6": {
            "Mon": { i for i in range(1,8)},
            "Tue": { i for i in range(1,8)},
            "Wed": { i for i in range(1,7)},
            "Thu": { i for i in range(1,7)},
            "Fri": { i for i in range(1,7)},
        }
    }