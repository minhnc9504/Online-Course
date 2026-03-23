from django.shortcuts import render, get_object_ some_shortcut, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment
from django.contrib.auth.models import User

# ... Các hàm ListView và DetailView đã có sẵn ...

# --- NHIỆM VỤ 5: TRIỂN KHAI HÀM SUBMIT VÀ SHOW_EXAM_RESULT ---

def submit(request, course_id):
    """
    Hàm này xử lý yêu cầu POST khi người dùng nộp bài thi.
    Nó thu thập các Choice đã chọn, tạo một bản ghi Submission và tính điểm.
    """
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # 1. Lấy danh sách các ID lựa chọn mà người dùng đã tích vào
        selected_ids = [int(value) for key, value in request.POST.items() if 'choice_' in key]
        
        # 2. Kiểm tra xem người dùng đã đăng ký khóa học chưa (Enrollment)
        # Giả định user đã login, nếu chưa cần xử lý login_required
        enrollment = Enrollment.objects.get(user=request.user, course=course)
        
        # 3. Tạo một bản ghi Submission mới
        submission = Submission(enrollment=enrollment)
        submission.save()
        
        # 4. Lưu các lựa chọn đã chọn vào Submission (Many-to-Many)
        for choice_id in selected_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
        submission.save()

        # 5. Chuyển hướng đến trang hiển thị kết quả
        return redirect('onlinecourse:show_exam_result', submission_id=submission.id)
    
    return redirect('onlinecourse:course_details', pk=course_id)


def show_exam_result(request, submission_id):
    """
    Hàm này tính toán tổng điểm dựa trên Submission và hiển thị trang kết quả.
    """
    # 1. Lấy bản ghi Submission và các thông tin liên quan
    submission = get_object_or_404(Submission, pk=submission_id)
    course = submission.enrollment.course
    course_questions = Question.objects.filter(course=course)
    
    # 2. Lấy danh sách các Choice mà người dùng đã chọn trong lần nộp này
    selected_choice_ids = [choice.id for choice in submission.choices.all()]
    
    total_score = 0
    results = []

    # 3. Duyệt qua từng câu hỏi trong khóa học để tính điểm
    for question in course_questions:
        # Sử dụng hàm is_get_score đã viết trong models.py (Task 1)
        is_correct = question.is_get_score(selected_choice_ids)
        if is_correct:
            total_score += question.grade
        
        results.append({
            'question': question,
            'is_correct': is_correct
        })

    # 4. Render template hiển thị kết quả (Thường là exam_result_bootstrap.html)
    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'results': results,
    }
    def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    course = submission.enrollment.course
    questions = Question.objects.filter(course=course)
    
    # Lấy danh sách ID đã chọn
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    total_score = 0
    for question in questions:
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    # Tính tổng điểm tối đa có thể đạt được (possible)
    possible_score = sum([q.grade for q in questions])

    context = {
        'course': course,
        'total_score': total_score,
        'selected_ids': selected_ids, # BẮT BUỘC CÓ
        'possible': possible_score,   # BẮT BUỘC CÓ
        'submission': submission
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
