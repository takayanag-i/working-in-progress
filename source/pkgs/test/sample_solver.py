import pandas as pd
import pulp
from collections import defaultdict

from pkgs.test.sample_data_manager import SampleDataManager

class SampleSolver:
    """
    テストデータを用いて問題を解くクラス
    """

    def __init__(self, excel_path):
        """
        コンストラクタ

        Arguments:
            excel_path -- xlsファイルへのパス
        """
        self.sm = SampleDataManager(excel_path)
        self.homeroom_list = self.sm.get_homeroom_list()
        self.schedule = self.sm.get_schedule()
        self.course_list = self.sm.get_course_list()
        self.teacher_list = self.sm.get_teacher_list()
        self.day_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        self.curriculum_dict = self.sm.get_curriculum_dict()
        self.course_teacher_dict = self.sm.get_course_teacher_dict()
        self.teacher_course_dict = self.reverse_dict(self.course_teacher_dict)

        self.model = pulp.LpProblem("sample", pulp.LpMinimize)

        self.define_variables()

    def define_variables(self):
        """
        変数を定義する
        """

        self.x = {}
        self.y = {}
        self.z = {}

        # x_HR_曜日_時限_講座
        for h in self.homeroom_list:
            for d in self.day_of_week:
                for p in self.schedule[h][d]:
                    for block in self.curriculum_dict[h]:
                        for lane in block:
                            for c in lane:
                                self.x[h,d,p,c] = pulp.LpVariable(name=f"x_{h}_{d}_{p}_{c}", cat="Binary")
        # y_曜日_時限_教員
        for d in self.day_of_week:
            for p in range(1,8):
                for t in self.teacher_list:
                    self.y[d,p,t] = pulp.LpVariable(name=f"y_{d}_{p}_{t}", cat="Binary")

        # yをxの関数として定義
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

    def display_result(self, h: str):
        """
        結果を表示する
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

    def reverse_dict(self, d):
        """
        辞書のキーと値を逆にする
        """
        reversed_dict = defaultdict(list)

        for k, vs in d.items():
            for v in vs:
                reversed_dict[v].append(k)

        # 結果を辞書に変換（defaultdictから通常のdictへ）

        return dict(reversed_dict)