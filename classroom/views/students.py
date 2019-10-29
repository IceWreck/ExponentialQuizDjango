from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm
from ..models import Quiz, Student, TakenQuiz, User, Answer


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():

                # This execs after every answer submission.

                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save() 

                # Random Info Needed
                print(student_answer.answer)

                #print("Question ID is "+ str(question.id))
                #print("Student's Answer is " + str(student_answer.answer_id))
                correct_answer = Answer.objects.get(question=question.id, is_correct=True)
                #print("Correct answer is " + str(correct_answer.id))

                # New Session var name unique to each quiz in case there are multiple
                temp_score_name = 'temp_score_' + str(quiz.id)
                score_factor_name = 'score_factor_' + str(quiz.id)

                # Create session if doesn't exist
                
                # Score Session 
                temp_score = request.session.get(temp_score_name, 0) #default val 0
                request.session[temp_score_name] = temp_score
                # Exponent Session
                score_factor = request.session.get(score_factor_name, 1)
                request.session[temp_score_name] = temp_score

                # Handle scoring on basis of answer

                '''

                Score system
                * Questions will appear one by one.
                * The participant will have the choice of either skipping the question or answering it.
                * If they answer it corectly they'll get 2^1 points.
                * If they answer another question correctly after that theyll get 2^2 points.
                * And so on 
                * If they skip a question, next questions points will again start from 2^1.
                * If they answer the question incorrectly 2 marks will be deducted.
                * If they answer another question incorrectly 4 marks will be deducted and so on.

                '''
                if str(student_answer.answer) == 'Skip':
                    # set score factor to default
                    request.session[score_factor_name] = 1
                    messages.success(request, 'Question Skipped. Points are: ' + str(request.session[temp_score_name]))
                elif student_answer.answer_id == correct_answer.id:
                    print("Correct")
                    
                    if score_factor >= 0:
                        pass
                    else:
                        score_factor = 1
                    
                    # Add to Score
                    request.session[temp_score_name] = temp_score + abs(score_factor * 2)
                    messages.success(request, 'Correct. Points are: ' + str(request.session[temp_score_name]))
                    # Change score factor for next question
                    request.session[score_factor_name] = abs(score_factor * 2)

                else:
                    # Give -ve marking 

                    if score_factor >= 0:
                        # Decrease Score
                        request.session[temp_score_name] = temp_score - 2
                        # Set score factor to negative
                        request.session[score_factor_name] = -2
                    else:
                        # Score factor is already -ve
                        request.session[temp_score_name] = temp_score + (score_factor * 2)
                        # Change score factor for the next question
                        request.session[score_factor_name] = score_factor * 2

                    messages.error(request, 'Wrong. Points are: ' + str(request.session[temp_score_name]))

                # Number of correct answers till now
                number_correct = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                print("Total Correct Till Now are:" + str(number_correct))


                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    # If all questions have been answered, open the student interface.
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    
                    # Percentage of Questions Right
                    percentage_correct = round((correct_answers / total_questions) * 100.0, 2)
                    # Exponential Scoring
                    score = request.session[temp_score_name]
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if percentage_correct < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s points. You got %s percent questions correct.' % (quiz.name, score, percentage_correct))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points. You got %s percent questions correct.' % (quiz.name, score, percentage_correct))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })
