from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator

#게시글(쇼핑목록) 페이지
def board_list(request):
    all_boards = Board.objects.all().order_by('-id') #Board는 게시글 작성 함수 이름임, 최신게시글이 맨 위에
    page = int(request.GET.get('p', 1)) # 현재 페이지를 나타냄
    paginator = Paginator(all_boards, 6) # 한 페이지에 게시물 6개 보임
    boards = paginator.get_page(page) # 해당 페이지 번호를 리턴받아 현재 페이지를 나타냄
    return render(request, 'board_list.html', {'boards':boards}) # 게시판 html이 board_list.html

#게시글 누른후 페이지

#검색-제목(기능)

#게시글 작성(판매하기 게시판)

#게시글 삭제(기능)

#댓글 작성
@login_required(login_url='common:login')
def comment_create_question(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

#판매완료(기능)

#게시글 정렬(기능)

#html- 게시글페이지, 게시글 누른후 페이지, 게시글 작성페이지