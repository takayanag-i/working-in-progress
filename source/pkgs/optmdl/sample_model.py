import pandas as pd
import pulp

from pkgs.optmdl.sample_data_manager import SampleDataManager
from pkgs.dto.anual_data import AnualData

class SampleModel:
    """
    与えられたサンプルデータで問題を解くクラス
    """

    def __init__(self, dto: AnualData):
        """
        イニシャライザ

        Arguments:
            xls_path -- Excelファイルへのパス
        """

        # 年間データ
        self.dto = dto

        # LP
        self.prob = pulp.LpProblem("sample", pulp.LpMinimize)

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
        for h in self.dto.homeroom_list:
            for d in self.dto.day_of_week:
                for p in self.dto.schedule[h][d]:
                    for block in self.dto.curriculum_dict[h]:
                        for lane in block:
                            for c in lane:
                                self.x[h,d,p,c] = pulp.LpVariable(name=f"x_{h}_{d}_{p}_{c}", cat="Binary")
        # yの定義
        for d in self.dto.day_of_week:
            for p in range(1,8):
                for t in self.dto.teacher_list:
                    self.y[d,p,t] = pulp.LpVariable(name=f"y_{d}_{p}_{t}", cat="Binary")

        # yをxの関数として表す
        for t in self.dto.teacher_list:
            first_hcs = []
            for h in self.dto.homeroom_list:
                for block in self.dto.curriculum_dict[h]:
                    for lane in block:
                        for c in lane:
                            if t in self.dto.course_teacher_dict[c] and c not in [hc[1] for hc in first_hcs]:
                                first_hcs.append((h, c))
            for d in self.dto.day_of_week:
                for p in range(1, 8):
                    self.y[d, p, t] = pulp.lpSum([self.x[h, d, p, c] for (h, c) in first_hcs if (h, d, p, c) in self.x])

    def solve(self) -> None:
        """
        問題を解く
        """
        self.prob.solve()
