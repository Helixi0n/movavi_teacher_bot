from data.course_teachers_data import course_teachers_data
from data.teachers_data import teachers_data


class Teacher:
    def __init__(self, name: str, bio: str, photo: str | None = None):
        self.name = name
        self.bio = bio
        self.photo = photo or (name + ".jpg")


teachers = [Teacher(**teacher) for teacher in teachers_data]


def find_teachers(names: list[str]) -> list[Teacher]:
    return [teacher for teacher in teachers if teacher.name in names]


course_teachers = {
    course_name: find_teachers(teacher_names)
    for course_name, teacher_names in course_teachers_data.items()
}
