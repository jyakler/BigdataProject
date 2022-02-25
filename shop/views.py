from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from bookL.models import Post,Reply
from django.core.paginator import Paginator


#게시글(쇼핑목록) 페이지

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
def delete(request):
    pk=request.GET['pk']
    post=Post.objects.get(pk=pk)
    post.delete()
    return redirect("쇼핑목록페이지")
#댓글 작성

#판매완료(기능)

#게시글 정렬(기능)

#html- 게시글페이지, 게시글 누른후 페이지, 게시글 작성페이지