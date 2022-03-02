from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from bookL.models import Post, Reply
from django.core.paginator import Paginator
from django.utils import timezone

#게시글(쇼핑목록) 페이지
def board_list(request):
    all_boards = Post.objects.all().order_by('-id') #Board는 게시글 작성 함수 이름임, 최신게시글이 맨 위에
    page = int(request.GET.get('p', 1)) # 현재 페이지를 나타냄
    paginator = Paginator(all_boards, 6) # 한 페이지에 게시물 6개 보임
    boards = paginator.get_page(page) # 해당 페이지 번호를 리턴받아 현재 페이지를 나타냄
    return render(request, 'board_list.html', {'boards':boards}) # 게시판 html이 board_list.html

#게시글 누른후 페이지
'''
보내는 정보:
post자체의 정보(모델클래스)
'''
def shopping2(request,pk):
     post=Post.objects.get(pk=pk)
     context={"post":post}
     return render(request,'누른후페이지',context)

#검색-제목(기능)
'''
보내는 정보:
제목 필터에 맞는 내용들을 paginator처리해서 list로 보냄
'''
def search(request, title):
    page = request.GET.get('page', 1)
    plist=Post.objects.filter(title=title)
    paginator=Paginator(plist,10)
    plistpage=paginator.get_page(page)
    context={'plist':plistpage}
    return render(request,'쇼핑목록페이지',context)

#게시글 작성(판매하기 게시판)
def p_create(request):
    nickname=request.POST['username']
    title=request.POST['title']
    price=request.POST['price']
    photo=request.FILES('photo',None)
    content=request.POST['content']
    pdata=Post(username=nickname,content=content,price=price,title=title,photo=photo)
    pdata.save()
    return redirect('쇼핑목록페이지')

#게시글 삭제(기능)
'''
html 에서 쿼리로 pk정보 받아와야함
'''
def delete(request):
    pk=request.GET['pk']
    post=Post.objects.get(pk=pk)
    post.delete()
    return redirect("쇼핑목록페이지")

#댓글 작성
def reply_create(request):
    content = request.GET['content']
    pk = request.GET['pk']
    post = Post.objects.get(pk=pk)  # pk=pk, id=pk
    rdata = Reply(content=content, post_id=post)
    rdata.save()
    comment = Reply()
    comment.user = request.user # request.user는 현재 접속한 유저의 정보
    #위 정보가 필요한가?
    return redirect("페이지")

#판매완료(기능)
def sold_out(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        post.title = request.POST['title'] +'[판매완료]'
        post.save()
        return redirect('쇼핑목록페이지')

    else:
        return render(request, 'update.html')

#게시글 정렬(기능)

#html- 게시글페이지, 게시글 누른후 페이지, 게시글 작성페이지