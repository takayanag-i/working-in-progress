import pulp

from pkgs.optmdl.sample_model import SampleModel

def add_homeroom_constraints(model: SampleModel) -> SampleModel:
    """
    学級制約を追加する

    任意の学級の任意の曜日・時限に対して，その学級のカリキュラムに含まれる講座の開講変数xの総和は1以上である。

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
    model: SampleModel, course_credit_dict: dict
) -> SampleModel:
    """
    単位数制約を追加する

    任意の学級の任意の講座に対して，講座の開講変数xの曜日・時限に関する総和は，科目の単位数に等しい。

    Arguments:
        model (SampleModel) -- モデル

    Returns:
        SampleModel -- 制約を追加したモデル
    """
    for h in model.dto.homeroom_list:
        for block in model.dto.curriculum_dict[h]:
            for lane in block:
                for c in lane:
                    credit = course_credit_dict.get(c, 0)  # 単位数を取得，見つからなければ0
                    model.prob += pulp.lpSum(
                        [model.x[h, d, p, c] for d in model.dto.day_of_week for p in model.dto.schedule[h][d]]
                    ) == credit
    return model


def add_block_constraints(model: SampleModel) -> SampleModel:
    """
    ブロック制約を追加する

    任意の学級について，任意の曜日・時限で，任意のブロックに対して，レーンに含まれる講座の開講変数xの総和はすべて等しい。

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

def add_teacher_constraints(model: SampleModel) -> SampleModel:
    """
    教員制約を追加する

    任意の曜日・時限で，任意の教員に対して，教員の授業実施変数yは1以下である。

    Arguments:
        model (SampleModel) -- モデル

    Returns:
        SampleModel -- 制約を追加したモデル
    """
    for d in model.dto.day_of_week:
        for p in [i for i in range(1,8)]:
            for t in model.dto.teacher_list:
                model.prob += model.y[d,p,t] <= 1
    return model
