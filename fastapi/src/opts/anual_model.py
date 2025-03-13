import os
import pulp

from dotenv import load_dotenv

from opts.anual_data import AnualData

load_dotenv()
cbc_path = os.getenv("CBC_PATH")


class AnualModel:
    """年間時間割の最適化モデルを管理するクラス。

    Attributes:
        data (AnualData): 時間割の元データ。
        problem (pulp.LpProblem): 線形最適化問題の定義。
        x (Dict[Tuple[str, str, int, str], pulp.LpVariable]): 学級・曜日・時限・講座ごとの変数。
        y (Dict[Tuple[str, str, int], pulp.LpAffineExpression]): 教員ごとの授業数を表す式。
    """

    def __init__(self, data: AnualData):
        self.data = data
        self.problem = pulp.LpProblem("sample", pulp.LpMinimize)
        self.x = {}
        self.y = {}

        self.problem.setSolver(pulp.COIN_CMD(path=cbc_path, msg=True))
        self.define_variables()

    def define_variables(self) -> None:
        """変数ｘとｙを定義する。

        - x[h, d, p, c]
        - y[d, p, i]
        """
        # xの定義
        self.x = {
            (h, d, p, c): pulp.LpVariable(name=f"x_{h}_{d}_{p}_{c}", cat=pulp.LpBinary)
            # 任意のh, d, p, dに対して
            for h in self.data.H
            for d in self.data.D
            for p in self.data.periods[h][d]
            for block in self.data.curriculums[h]
            for lane in block
            for c in lane
        }

        # yの定義
        self.y = {
            (d, p, i): pulp.lpSum(
                self.x[h, d, p, c]
                # cに関して和をとる
                for c in self.data.C
                if (h := min(  # 講座cを開講する学級hを1つ選ぶ
                    (h for h in self.data.H  # すべての学級 h の中から
                     if any(c in lane       # cを履修する学級を検索
                            for block in self.data.curriculums[h]
                            for lane in block))
                )) is not None
                # ただし、和をとるのはcの担当教員にiが含まれているとき
                and i in self.data.course_details[c]
                and (h, d, p, c) in self.x  # pによっては存在しない場合があるため
            )

            # 任意のd, p, iに対して
            for d in self.data.D
            for p in range(1, self.data.max_periods + 1)
            for i in self.data.I
        }
