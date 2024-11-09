import pandas as pd

from pkgs.optmdl.lp_model import LpModel

def display_result_by_homeroom(model: LpModel, h: str) -> pd.DataFrame:
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

def display_result_all_homerooms(model: LpModel) -> pd.DataFrame:
    """
    すべての学級の結果を表示する

    Arguments:
        model(SampleModel) -- 解が求められたモデル
    """

    # 月曜日から金曜日の1時間目から7時間目までのカラムを作成
    periods = [f'{d} {p}' for d in model.dto.day_of_week for p in range(1, 8)]

    # 学級名をインデックスに設定
    index = list(model.dto.homeroom_list)

    # 空のデータフレームを作成
    timetable_df = pd.DataFrame(index=index, columns=periods)

    # 各学級の時間割をデータフレームに挿入
    for h in index:
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
                    timetable_df.at[h, f'{d} {p}'] = '/'.join(courses_in_period)

    return timetable_df

def display_result_all_teachers(model: LpModel) -> pd.DataFrame:
    """
    すべての教員の結果を表示する

    Arguments:
        model(SampleModel) -- 解が求められたモデル
    """

    # 月曜日から金曜日の1時間目から7時間目までのカラムを作成
    periods = [f'{d} {p}' for d in model.dto.day_of_week for p in range(1, 8)]

    # 教員名をインデックスに設定
    index = list(model.dto.teacher_list)

    # 空のデータフレームを作成
    timetable_df = pd.DataFrame(index=index, columns=periods)

    # 各教員の時間割をデータフレームに挿入
    for h in model.dto.homeroom_list:
        for d in model.dto.day_of_week:
            for p in model.dto.schedule[h][d]:
                for block in model.dto.curriculum_dict[h]:
                    for lane in block:
                        for c in lane:
                            for t in model.dto.course_teacher_dict[c]:
                                if model.x[h, d, p, c].value() == 1:
                                        timetable_df.at[t, f'{d} {p}'] = c

    return timetable_df