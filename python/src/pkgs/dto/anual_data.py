class AnualData:
    def __init__(self):
        # 学級リスト
        self.homeroom_list = None

        # 曜日リスト
        self.day_of_week = None

        # 日課表
        self.schedule = None

        # 講座リスト
        self.course_list = None

        # 教員リスト
        self.teacher_list = None

        # {学級: カリキュラム}辞書
        self.curriculum_dict = None

        # {講座: 教員リスト}辞書
        self.course_teacher_dict = None