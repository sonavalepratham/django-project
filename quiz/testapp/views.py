from django.shortcuts import render, HttpResponse,redirect
from django.db import connection
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import datetime,timedelta
# Create your views here.
def index(request):
    return render(request,'index.html')

def HandleLogin(request): 
    if request.user.username=='admin@elesa.co.in':
         return render(request,'adminprofile.html')
    if request.user.is_authenticated:
        return redirect('/Profile')
 
    if request.method=="POST":
      usrnm=request.POST['usrnm']
      passwrd= request.POST['pass']
      user= authenticate(username=usrnm,password=passwrd)
      if user is not None:
          login(request, user)
          messages.success(request,"Successful")
          if request.user.username=='admin@elesa.co.in':
                 return render(request,'adminprofile.html')
          return redirect('Profile')
      else:
          return HttpResponse("invalid credentials")     
    else:
        messages.error(request,"Error")
        return render(request,'index.html')

def HandleLogout(request):
    logout(request)
    return render(request,'index.html')

def Profile(request):
    if request.user.is_authenticated:
        query="SELECT * FROM quizinfo WHERE id=1"
        cursor= connection.cursor()
        cursor.execute(query)
        result=cursor.fetchall()

        query="SELECT * FROM auth_user WHERE id="+str(request.user.id)
        cursor.execute(query)
        s_result=cursor.fetchall()
        
        query="SELECT * FROM s_marks WHERE s_id="+str(request.user.id)
        res=cursor.execute(query)
        res_f=cursor.fetchall()
        query="SELECT * FROM quizinfo WHERE id=1"
        cursor.execute(query)
        res_q=cursor.fetchall()
        if res_q[0][1]<=datetime.now():
            attempt=""
            review="disabled"
            
            try:
                if res_f[0][3]==1:
                    attempt="disabled"
                    review=""
                else:
                    attempt=""
                    review="disabled"
            except :
                pass
        else:
            attempt="disabled"
            review="disabled"
        print(review)
        return render(request,'Profile.html',{'quizinfo':result,'s_info':s_result,'attempt':attempt,'review':review})
    else:
        return render(request,'index.html')

def Createquiz(request):
    if request.method=="GET" and request.GET.get('question'):
        q=request.GET.get('question')
        o1=request.GET.get('o1')
        o2=request.GET.get('o2')
        o3=request.GET.get('o3')
        o4=request.GET.get('o4')
        co=int(request.GET.get('co'))
        cursor= connection.cursor()
        cursor.execute('''INSERT INTO qna
        (question,o1,o2,o3,o4,co)
        VALUES (%s,%s,%s,%s,%s,%s)''',
        [q,o1,o2,o3,o4,co])
        return render(request,'createquiz.html')
    if request.user.username=='admin@elesa.co.in':
         return render(request,'createquiz.html')
    else:
         return render(request,'index.html')
def viewQuestions(request):
    if request.user.username=='admin@elesa.co.in':
        cursor= connection.cursor()
        cursor.execute("SELECT * FROM qna")
        result=cursor.fetchall()
        return render(request,'viewquestions.html',{'qna':result})
    else:
        return render(request,'index.html')


def UpdateQuestion(request,pk=None):
    if request.user.username=="admin@elesa.co.in":
        cursor= connection.cursor()
        cursor.execute("SELECT * FROM qna WHERE id="+pk)
        result=cursor.fetchall()
        return render(request,'updateq.html',{'qna':result})
    return render(request,'index.html')
def ConfirmUpdate(request):
    if request.user.username=="admin@elesa.co.in":
        if request.method=="GET" and request.GET.get('pk'):
            pk=request.GET.get('pk')
            q=request.GET.get('question')
            o1=request.GET.get('o1')
            o2=request.GET.get('o2')
            o3=request.GET.get('o3')
            o4=request.GET.get('o4')
            co=request.GET.get('co')
            cursor= connection.cursor()
            cursor.execute("UPDATE qna SET question="+"'"+q+"'"+", o1="+"'"+o1+"'"+", o2="+"'"+o2+"'"+", o3="+"'"+o3+"'"+", o4="+"'"+o4+"'"+", co="+"'"+co+"'"+" WHERE id="+pk)
            return HttpResponse("Updated Successfully")
    return render(request,'index.html')        
    
def DeleteQuestion(request,pk=None):
    if request.user.username=="admin@elesa.co.in":
        cursor= connection.cursor()
        cursor.execute("DELETE FROM qna WHERE id="+pk)
        return HttpResponse("Deleted Successfully")
    else:
        return render(request,'index.html')


def Settime(request):
    if request.user.username=="admin@elesa.co.in":
        if request.method=="GET" and request.GET.get('duration'):
            datetime=request.GET.get('date')+" "+request.GET.get('time')
            duration=request.GET.get('duration')
            name=request.GET.get('name')
            query="UPDATE quizinfo SET datetime ="+"'"+datetime+"'"+", duration="+"'"+duration+"'"+", name="+"'"+name+"'"+" WHERE id=1"
            cursor= connection.cursor()
            cursor.execute(query)
            return HttpResponse("Updated Successfully")
        query="SELECT * FROM quizinfo WHERE id=1"
        cursor= connection.cursor()
        cursor.execute(query)
        result=cursor.fetchall()
        return render(request,'Quiztime.html',{'quizinfo':result})
    return render(request,'index.html')

def attempt(request,s_pk):
    if request.user.is_authenticated:
        query="SELECT * FROM quizinfo WHERE id=1"
        cursor= connection.cursor()
        cursor.execute(query)
        res_q=cursor.fetchall()

        query="SELECT * FROM s_marks WHERE s_id="+str(request.user.id)
        res=cursor.execute(query)
        res_f=cursor.fetchall()
        
        if res_q[0][1]<=datetime.now():
            try:
                if res_f[0][3]==1:
                    cursor= connection.cursor()
                    questions=cursor.execute("SELECT * FROM qna")
                    result=cursor.fetchall()
                    query="SELECT * FROM s_marks WHERE s_id="+str(request.user.id)
                    cursor.execute(query)
                    mark=cursor.fetchall()
                    return render(request,'review.html',{'qna':result,'mark':mark,'questions':questions})
                elif res==1 and ((datetime.now()-res_f[0][2]).seconds%3600//60)>=int(res_q[0][2]):
                    cursor.execute("UPDATE s_marks SET flag = '1' WHERE s_id ="+str(request.user.id))
                    return HttpResponse("Time Is Over")
            
            except:
                cursor.execute('''INSERT INTO s_marks
                (s_id,flag)
                VALUES (%s,%s)''',
                [str(request.user.id),0]) 
            cursor.execute("SELECT * FROM qna")
            qna=cursor.fetchall()
            try:
                res=res_f[0][2]+timedelta(minutes=res_q[0][2])
            except:
                res=datetime.now()+timedelta(minutes=res_q[0][2])
            print("it should return")
            return render(request,'attempt.html',{'qna':qna,'datetime':res.strftime("%Y-%m-%d %H:%M:%S.%f")})
        else:
            return redirect('Profile')

def Submit(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            query="SELECT * FROM s_marks WHERE s_id="+str(request.user.id)
            cursor= connection.cursor()
            cursor.execute(query)
            res=cursor.fetchall()
            cursor.execute("SELECT * FROM qna")
            qna=cursor.fetchall()
            count=0
            if res[0][3]!=1:
                for q in qna:
                    var=str(q[0])
                    if int(request.POST.get(var))==int(q[6]):
                        count=count+1
                cursor.execute("UPDATE s_marks SET flag=1,marks="+str(count)+" WHERE s_id="+str(request.user.id))
                return HttpResponse("Submitted")