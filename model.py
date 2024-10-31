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
    def __init__(self):
        self.votes: list[UserVote] = []

    def get_user_votes(self, user_id: str, teacher: str = None):
        pass

    def get_teachers_votes(self):
        res = defaultdict(int)
        for vote in self.votes:
            res[vote.teacher] += vote.vote_value
        return res

    def add_vote(self, user_id: str, teacher: str, vote_value: int):
        self.votes = [vote for vote in self.votes if not (user_id == vote.user_id and teacher == vote.teacher)]
        self.votes.append(UserVote(user_id, teacher, vote_value))

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
