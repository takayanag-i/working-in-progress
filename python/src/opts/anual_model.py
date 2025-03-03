import pulp

from pydantic import BaseModel
from typing import List, Dict, Optional


class AnualData(BaseModel):
    H: Optional[List[str]] = None
    D: Optional[List[str]] = None
    C: Optional[List[str]] = None
    I: Optional[List[str]] = None
    periods: Optional[Dict[str, List[int]]] = None
    curriculums: Optional[Dict[str, List[List[List[str]]]]] = None
    course_details: Optional[Dict[str, List[str]]] = None


class AnualModel:
    def __init__(self, dto: AnualData):
        # 年間データ
        self.dto = dto

        # LP
        self.problem = pulp.LpProblem("sample", pulp.LpMinimize)

        # x_{学級, 曜日, 時限, 講座}
        self.x = {}

        # y_{曜日, 時限, 教員}
        self.y = {}

        self.define_variables()  # 変数の定義

    def define_variables(self) -> None:
        """変数を定義する"""

        # xの定義
        self.x = {
            (h, d, p, c): pulp.LpVariable(name=f"x_{h}_{d}_{p}_{c}", cat="Binary")
            # 任意のh, d, p, dに対して
            for h in self.dto.H
            for d in self.dto.D
            for p in self.dto.periods[h][d]
            for block in self.dto.curriculums[h]
            for lane in block
            for c in lane
        }

        self.y = {
            (d, p, i): pulp.lpSum(
                self.x[h, d, p, c]
                # cに関して和をとる
                for c in self.dto.C
                if (h := min(  # 講座cを開講する学級hを1つ選ぶ
                    (h for h in self.dto.H  # すべての学級 h の中から
                     if any(c in lane       # cを履修する学級を検索
                            for block in self.dto.curriculums[h]
                            for lane in block))
                )) is not None
                # ただし、和をとるのはcの担当教員にiが含まれているとき
                and i in self.dto.course_details[c]
                and (h, d, p, c) in self.x  # pによっては存在しない場合があるため
            )

            # 任意のd, p, iに対して
            for d in self.dto.D
            for p in range(1, 8)
            for i in self.dto.I
        }
