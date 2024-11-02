"""
В этом файле определяются классы данных (модели)
"""
import json
from collections import defaultdict

from data.course_teachers_data import course_teacher_mapping
from data.teachers_data import teachers_list


class Teacher:
    def __init__(self, name: str, bio: str, photo: str | None = None):
        self.name = name
        self.bio = bio
        self.photo = photo or (name + ".jpg")


class TeacherList:
    def __init__(self, initial_data: list[dict]):
        self.teachers = [Teacher(**teacher) for teacher in initial_data]

    def get_teachers(self, names: list[str]) -> list[Teacher]:
        return [teacher for teacher in self.teachers if teacher.name in names]


class UserVote:
    def __init__(self, user_id: str, teacher: str, vote_value: int):
        self.user_id = user_id
        self.teacher = teacher
        self.vote_value = vote_value


class VotesList:
    EXPORT_FILE_NAME = "votes.json"

    def __init__(self):
        self.votes: list[UserVote] = []
        self.load()

    def load(self):
        try:
            with open(VotesList.EXPORT_FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.votes = [UserVote(**vote_dict) for vote_dict in data]
        except Exception:
            self.votes = []

    def get_user_votes(self, user_id: str) -> list[tuple[str, int]]:
        return [(v.teacher, v.vote_value) for v in self.votes if v.user_id == user_id]

    def get_teachers_votes(self):
        res = defaultdict(int)
        for vote in self.votes:
            res[vote.teacher] += vote.vote_value
        return res

    def add_vote(self, user_id: str, teacher: str, vote_value: int):
        self.votes = [vote for vote in self.votes if not (user_id == vote.user_id and teacher == vote.teacher)]
        if vote_value:
            self.votes.append(UserVote(user_id, teacher, vote_value))
        self.save()

    def save(self):
        with open(VotesList.EXPORT_FILE_NAME, "w", encoding="utf-8") as file:
            export = [d.__dict__ for d in self.votes]
            json.dump(export, file)


def get_rating():
    teacher_votes = user_votes.get_teachers_votes()
    rating = [
        (teacher.name, teacher_votes[teacher.name])
        for teacher in teachers.teachers
    ]
    rating.sort(key=lambda x: -x[1])
    return rating[:10]


teachers = TeacherList(teachers_list)
user_votes = VotesList()

course_to_teachers = {
    course_name: teachers.get_teachers(teacher_names)
    for course_name, teacher_names in course_teacher_mapping.items()
}
