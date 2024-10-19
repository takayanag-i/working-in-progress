import pandas as pd

from pkgs.sample.sample_model import SampleModel

def display_result_by_homeroom(model: SampleModel, h: str) -> pd.DataFrame:
    """
    学級を指定して結果を表示する

    Arguments:
        h -- 学級名
    """

    result_df = pd.DataFrame(columns = [i for i in range(1,8)], index = model.dto.day_of_week)

    # 時間割結果を表示する
    for d in model.dto.day_of_week:
        for p in model.dto.schedule[h][d]:
            # 複数の講座を一時的に保持するリスト
            courses_in_period = []
            for block in model.dto.curriculum_dict[h]:
                for lane in block:
                    for c in lane:
                        if model.x[h, d, p, c].value() == 1:
                            courses_in_period.append(c)
            # 複数の講座がある場合、カンマ区切りで結合してDataFrameに格納
            if courses_in_period:
                result_df.at[d, p] = '/'.join(courses_in_period)

    return result_df