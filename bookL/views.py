from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

#메인페이지
def index(request):
    context=None
    if request.user.is_authenticated:
        context={'logineduser':request.user}
    return render(request,'index.html',context)
'''
메인페이지에 로그인했는지 여부를 나누어 메인페이지 상단탭에 로그인/회원가입<->로그아웃 표시 나오게
'''

#로그인
def login(request):
    if request.method=="POST":#로그인 요청이 들어옴
        useremail=request.POST.get('useremail',None)#사용자 아이디
        password=request.POST.get('password',None)
        remember=request.POST.get('remember',False)
        user=auth.authenticate(username=useremail,password=password)
    #로그인 성공
        if user is not None:
            auth.login(request,user)
            if not remember:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60*60*24*14)
            return redirect('main:index')
        else:#로그인 실패
            print("에러")
            return render(request,'login_resist_form.html',{'error':'사용자 아이디 또는 패스워드가 틀립니다.'})
    else:
        return render(request,'login_resist_form.html')

#로그아웃
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('main:index')

#회원가입

'''
account 테이블의 
username=유저아이디(이메일)
last_name= 유저닉네임
password=비번
'''
def register(request):
    res_data=None
    if request.method == "POST":
        useremail=request.POST.get('useremail')
        password=request.POST.get('password')
        re_password=request.POST.get('re-password')
        nickname=request.POST.get('nickname')
        res_data={}
        if User.objects.filter(username=useremail):
            res_data['error']='이미 가입된 아이디(이메일)입니다.'
        elif User.objects.filter(last_name=nickname):
            res_data['error']='이미 존재하는 닉네임 입니다.'
        elif password!=re_password:
            res_data['error']='비밀번호가 다릅니다.'
        else:
            user=User.objects.create_user(username=useremail,last_name=nickname,
                                          password=password)
            auth.login(request,user)
            print("여기까지?")
            return redirect('main:index')
    return render(request,'login_resist_form.html',res_data)

#마이페이지
def mypage(request):
    context=None
    if request.user.is_authenticated:
        context={'user':request.user}
    return render(request,'mypage.html',context)
#html- 마이페이지

#------------------------------------------
