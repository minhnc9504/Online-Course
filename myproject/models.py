import sys
from django.utils import timezone
from django.db import models
from django.conf import settings

# Lớp Course (Đã có sẵn trong base project)
class Course(models.Model):
    name = models.CharField(null=False, max_length=100, default='online course')
    image = models.ImageField(upload_data='course_images/')
    description = models.CharField(max_length=500)
    pub_date = models.DateField(null=True)
    is_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# Lớp Lesson (Đã có sẵn trong base project)
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "Title: " + self.title

# --- TASK 1: THÊM CÁC MODEL CHO ASSESSMENT ---

# 1. Model Question (Câu hỏi)
class Question(models.Model):
    # Liên kết nhiều câu hỏi với một khóa học (Course)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Nội dung câu hỏi
    question_text = models.CharField(max_length=200)
    # Điểm cho câu hỏi này
    grade = models.IntegerField(default=1)

    # Hàm tính toán xem người dùng có chọn đúng tất cả các Choice đúng không
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        return False

    def __str__(self):
        return "Question: " + self.question_text


# 2. Model Choice (Lựa chọn trả lời)
class Choice(models.Model):
    # Liên kết với Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Nội dung lựa chọn
    choice_text = models.CharField(max_length=200)
    # Đánh dấu đây có phải đáp án đúng không
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "Choice: " + self.choice_text


# 3. Model Submission (Kết quả nộp bài của học viên)
class Submission(models.Model):
    # Liên kết với User (Học viên)
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    # Liên kết với các Choice đã chọn
    choices = models.ManyToManyField(Choice)
    # Ngày nộp bài
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Submission at " + str(self.date_submitted)

# Model Enrollment (Liên kết User và Course)
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=timezone.now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)
class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username

class Learner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist')
    ]
    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT)
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + self.occupation
