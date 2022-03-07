from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from bookL.models import Post, Reply
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Q

#게시글(쇼핑목록) 페이지
def board_list(request):
    all_boards = Post.objects.all().order_by('-created_at') #Board는 게시글 작성 함수 이름임, 최신게시글이 맨 위에
    page = int(request.GET.get('p', 1)) # 현재 페이지를 나타냄
    paginator = Paginator(all_boards, 6) # 한 페이지에 게시물 6개 보임
    boards = paginator.get_page(page) # 해당 페이지 번호를 리턴받아 현재 페이지를 나타냄
    return render(request, 'result.html', {'plist':boards}) # 게시판 html이 board_list.html

#게시글 누른후 페이지
'''
보내는 정보:
post자체의 정보(모델클래스)
'''
def shopping2(request,pk):
     post=Post.objects.get(pk=pk)
     replylist = []
     try:
        replylist=Reply.objects.filter(post_id=pk)
     except:
        print("null")
     for a in replylist:
         print(a.content)
     context={"post":post, "reply":replylist}
     return render(request,'detail.html',context)

#검색-제목(기능)
'''
보내는 정보:
제목 필터에 맞는 내용들을 paginator처리해서 list로 보냄
'''
def search(request):
    page = request.GET.get('page', 1)
    title=request.GET.get('title')
    plist=Post.objects.filter(Q(title__icontains=title) | Q(content__icontains=title))
    paginator=Paginator(plist,10)
    plistpage=paginator.get_page(page)
    context={'plist':plistpage}
    return render(request,'result.html',context)

#게시글 작성(판매하기 게시판)
def p_create(request):
    if request.user.is_authenticated:#로그인 상태면
        if request.method=="POST":
            print(request.user)
            id=request.user
            title=request.POST['title']
            price=request.POST['price']
            photo=request.FILES['photo']
            content=request.POST['content']
            print(id,title,price,content)
            pdata=Post(title=title,username=id,price=price,content=content,photo=photo)
            pdata.save()
            return redirect('result')
        return render(request,"deal.html")
    else:
        redirect("main:index")

#게시글 수정(기능)
def p_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        post.title = request.GET['title']
        post.price = request.POST['price']
        post.photo = request.FILE['photo']
        post.content = request.GET['content']
        post.save()
        return redirect('main:index')   # 작성 후에 메인페이지로 이동

    else:
        return render(request,'deal.html',{'post':post}) # 수정버튼 누르면 작성게시글 불러오기

#게시글 삭제(기능)
'''
html 에서 쿼리로 pk정보 받아와야함
'''
def delete(request):
    pk=request.GET['pk']
    post=Post.objects.get(pk=pk)
    post.delete()
    return redirect("main:index")

#댓글 작성
def reply_create(request):
    pk = request.GET['pk']
    content = request.POST['content']
    post = Post.objects.get(pk=pk)  # pk=pk, id=pk
    rdata = Reply(content=content, post_id=post, username=request.user)
    rdata.save()
    comment = Reply()
    comment.user = request.user # request.user는 현재 접속한 유저의 정보
    #위 정보가 필요한가?
    return shopping2(request,pk)

#댓글 수정
def reply_edit(request, post_id):
    post = get_object_or_404(Reply, pk=post_id)
    if request.method == "POST":
        post = get_object_or_404(Reply, pk=post_id)
        post.content = request.GET['content']
        post.save()
        return redirect('main:index')   # 작성 후에 메인페이지로 이동

    else:
        return render(request,'deal.html',{'post':post}) # 수정버튼 누르면 작성게시글 불러오기

#댓글 삭제
def reply_delete(request):
    pk=request.GET['pk']
    reply=Reply.objects.get(pk=pk)
    reply.delete()
    return redirect("main:index")

#판매완료(기능)
def sold_out(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        post.title = request.POST['title'] +'[판매완료]'
        post.save()
        return redirect('쇼핑목록페이지')

    else:
        return render(request, 'update.html')

#게시글 정렬(기능) - 최신순, 가격순
def page_array(request):
    sort = request.GET.get('sort', '')
    if sort == 'price':
        post_list = Post.objects.all().order_by('-price', 'created_at') # 가격 순으로 정렬
    else:
        post_list = Post.objects.all().order_by('created_at') # 날짜 순으로 정렬

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)

    return render(request, 'result.html', {'plist': posts, 'page': page, 'sort': sort})

@require_POST
def likes(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Post, pk=article_pk)

        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect('쇼핑목록페이지') # 좋아요 누르면 새로고침
    return render(request, 'login_resist_form.html') # 로그인 안되 있으면 로그인 창으로 이동

#html- 게시글페이지, 게시글 누른후 페이지