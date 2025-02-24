import pulp
import math

from python.src.lp.lp_model import LpModel

def add_homeroom_constraints(model: LpModel) -> LpModel:
    """
    学級制約を追加する

    任意の学級の任意の曜日・時限に対して、その学級のカリキュラムに含まれる講座の開講変数xの総和は1以上である。

    Arguments:
        model (SampleModel) -- モデル

    Returns:
        SampleModel -- 制約を追加したモデル
    """
    for h in model.dto.homeroom_list:
        for d in model.dto.day_of_week:
            for p in model.dto.schedule[h][d]:
                    model.prob += pulp.lpSum([model.x[h,d,p,c] for block in model.dto.curriculum_dict[h] for lane in block for c in lane]) >= 1
    return model

def add_course_credit_constraints(
    model: LpModel, course_credit_dict: dict
) -> LpModel:
    """
    単位数制約を追加する

    任意の学級の任意の講座に対して、講座の開講変数xの曜日・時限に関する総和は、科目の単位数に等しい。

    Arguments:
        model (SampleModel) -- モデル

    Returns:
        SampleModel -- 制約を追加したモデル
    """
    for h in model.dto.homeroom_list:
        for block in model.dto.curriculum_dict[h]:
            for lane in block:
                for c in lane:
                    credit = course_credit_dict.get(c, 0)  # 単位数を取得、見つからなければ0
                    model.prob += pulp.lpSum(
                        [model.x[h, d, p, c] for d in model.dto.day_of_week for p in model.dto.schedule[h][d]]
                    ) == credit
    return model


def add_block_constraints(model: LpModel) -> LpModel:
    """
    ブロック制約を追加する

    任意の学級について、任意の曜日・時限で、任意のブロックに対して、レーンに含まれる講座の開講変数xの総和はすべて等しい。

    Arguments:
        model (SampleModel) -- モデル

    Returns:
        SampleModel -- 制約を追加したモデル
    """
    for h in model.dto.homeroom_list:
        for d in model.dto.day_of_week:
            for p in model.dto.schedule[h][d]:
                for block in model.dto.curriculum_dict[h]:
                    if len(block) > 1:  # 複数レーンのあるブロックのみ
                        sums_of_x_in_lanes = [pulp.lpSum([model.x[h,d,p,c] for c in lane]) for lane in block]
                        for i in range(1, len(sums_of_x_in_lanes)): # lem(block) > 1 を満たすlaneの数だけ
                            model.prob += sums_of_x_in_lanes[0] == sums_of_x_in_lanes[i]
    return model

def add_teacher_constraints(model: LpModel) -> LpModel:
    """
    教員制約を追加する

    任意の曜日・時限で、任意の教員に対して、教員の授業実施変数yは1以下である。

    Arguments:
        model (SampleModel) -- モデル

    Returns:
        SampleModel -- 制約を追加したモデル
    """
    for d in model.dto.day_of_week:
        for p in range(1, 8):
            for t in model.dto.teacher_list:
                model.prob += model.y[d,p,t] <= 1
    return model

def add_course_constraints(model: LpModel) -> LpModel:
    """
    講座制約を追加する

    任意の講座について、任意の曜日・時限で、講座の開講変数xはその講座を受講する学級どうしで互いに等しい。

    Arguments:
        model (SampleModel) -- モデル

    Returns:
        SampleModel -- 制約を追加したモデル
    """
    for c in model.dto.course_list:
        for d in model.dto.day_of_week:
            for p in range(1, 8):  # 各時限で
                # 講座cに関連するすべての学級の開講変数が一致するよう制約を追加
                related_classes = [
                    h for h in model.dto.homeroom_list
                    if (h, d, p, c) in model.x  # 変数が定義されている学級のみ対象
                ]

                # すべての関連する学級の開講変数が等しいことを制約
                if len(related_classes) > 1:
                    first_class = related_classes[0]
                    for h in related_classes[1:]:
                        model.prob += (
                            model.x[first_class, d, p, c] == model.x[h, d, p, c]
                        )
    return model

def add_consective_period_constraints(model: LpModel, course: str, credit: int) -> LpModel:
    """
    2コマ連続制約を追加する

    Arguments:
        model (SampleModel) -- モデル
        course (str) -- 講座名
        credit (int) -- 単位数

    Returns:
        SampleModel -- 制約を追加したモデル
    """

    for h in model.dto.homeroom_list:
        consective_list = []  # 2コマ連続の補助変数を保存する

        for d in model.dto.day_of_week:
            periods = sorted(model.dto.schedule[h][d])  # 時限を取得・ソート

            # 2コマ連続の補助変数を定義
            for i in range(len(periods) - 1):
                p1, p2 = periods[i], periods[i + 1]

                if (h, d, p1, course) in model.x and (h, d, p2, course) in model.x:

                    consective = pulp.LpVariable(f"consecutive_{h}_{d}_{p1}_{p2}_{course}", cat="Binary")
                    consective_list.append(consective)

                    # consective := min(x[h, d, p1, course], x[h, d, p2, course])
                    model.prob += consective <= model.x[h, d, p1, course]
                    model.prob += consective <= model.x[h, d, p2, course]
                    model.prob += model.x[h, d, p1, course] + model.x[h, d, p2, course] - 1 <= consective

            for i in range(len(periods) - 2):
                p1, p2, p3 = periods[i], periods[i + 1], periods[i + 2]

                if (h, d, p1, course) in model.x and (h, d, p2, course) in model.x and (h, d, p3, course) in model.x:
                    # 3コマ連続は無効
                    model.prob += model.x[h, d, p1, course] + model.x[h, d, p2, course] + model.x[h, d, p3, course] <= 2

        if consective_list:
            # 可能な限り2コマ連続にする
            model.prob += pulp.lpSum(consective_list) == math.floor(credit / 2)

    return model

def add_courses_per_day_constraints(model: LpModel, twice_course_list: list) -> LpModel:
    """
    同じ講座は1日に1コマまでしか開講しない制約を追加する

    Arguments:
        model (LpModel) -- モデル
        twice_course_list (list) -- 2コマ開講の講座リスト

    Returns:
        LpModel -- 制約を追加したモデル
    """
    for h in model.dto.homeroom_list:
        for c in model.dto.course_list:
            max = 2 if c in twice_course_list else 1  # 最大開講数を設定
            for d in model.dto.day_of_week:
                valid_x = [
                    model.x[h, d, p, c] for p in model.dto.schedule[h][d] if (h, d, p, c) in model.x
                ]
                if valid_x:  # valid_x が空でない場合のみ制約を追加
                    model.prob += pulp.lpSum(valid_x) <= max
    return model
