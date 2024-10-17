import pandas as pd
import pulp

from pkgs.sample.sample_data_manager import SampleDataManager
from pkgs.const.constants import TimetableConstants

class SampleSolver:
    """
    与えられたサンプルデータで問題を解くクラス
    """

    def __init__(self, sm: SampleDataManager):
        """
        イニシャライザ

        Arguments:
            xls_path -- Excelファイルへのパス
        """

        # 学級リスト
        self.homeroom_list = sm.get_homeroom_list()

        # 曜日リスト
        self.day_of_week = sm.get_day_of_week_list()

        # 日課表
        self.schedule = sm.get_schedule_dict()

        # 講座リスト
        self.course_list = sm.get_course_list()

        # 教員リスト
        self.teacher_list = sm.get_teacher_list()

        # {学級: カリキュラム}辞書
        self.curriculum_dict = sm.get_curriculum_dict()

        # {講座: 教員リスト}辞書
        self.course_teacher_dict = sm.get_course_teacher_dict()

        # LPモデル
        self.model = pulp.LpProblem("sample", pulp.LpMinimize)

        # x_{学級, 曜日, 時限, 講座}
        self.x = {}

        # y_{曜日, 時限, 教員}
        self.y = {}

        self.define_variables() # 変数の定義

    def define_variables(self) -> None:
        """
        変数を定義する
        """

        # xの定義
        for h in self.homeroom_list:
            for d in self.day_of_week:
                for p in self.schedule[h][d]:
                    for block in self.curriculum_dict[h]:
                        for lane in block:
                            for c in lane:
                                self.x[h,d,p,c] = pulp.LpVariable(name=f"x_{h}_{d}_{p}_{c}", cat="Binary")
        # yの定義
        for d in self.day_of_week:
            for p in range(1,8):
                for t in self.teacher_list:
                    self.y[d,p,t] = pulp.LpVariable(name=f"y_{d}_{p}_{t}", cat="Binary")

        # yをxの関数として表す
        for t in self.teacher_list:
            first_hcs = []
            for h in self.homeroom_list:
                for block in self.curriculum_dict[h]:
                    for lane in block:
                        for c in lane:
                            if t in self.course_teacher_dict[c] and c not in [hc[1] for hc in first_hcs]:
                                first_hcs.append((h, c))
            for d in self.day_of_week:
                for p in range(1, 8):
                    self.y[d, p, t] = pulp.lpSum([self.x[h, d, p, c] for (h, c) in first_hcs if (h, d, p, c) in self.x])

    def display_result_by_homeroom(self, h: str) -> pd.DataFrame:
        """
        学級を指定して結果を表示する

        Arguments:
            h -- 学級名
        """

        result_df = pd.DataFrame(columns=[i for i in range(1,8)], index=self.day_of_week)

        # 時間割結果を表示する
        for d in self.day_of_week:
            for p in self.schedule[h][d]:
                # 複数の講座を一時的に保持するリスト
                courses_in_period = []
                for block in self.curriculum_dict[h]:
                    for lane in block:
                        for c in lane:
                            if self.x[h, d, p, c].value() == 1:
                                courses_in_period.append(c)
                # 複数の講座がある場合、カンマ区切りで結合してDataFrameに格納
                if courses_in_period:
                    result_df.at[d, p] = '/'.join(courses_in_period)

        return result_df