from django.shortcuts import redirect, render,HttpResponse
from cargapp.models import User,UserActivity
from django.contrib import messages
from pandas import read_excel
from datetime import datetime
# Create your views here.
def index(request):
    return render(request,"cargapp/index.html")
def loginpage(request):
    if request.method=='POST':
        sid=request.POST.get('SID')
        pword=request.POST.get('password')
        try:
            user=User.objects.get(SID=sid,password=pword)
            intime=datetime.now()
            if pword=='welcome123#': return redirect('changepassword')
            request.session['user']=sid
            try:
                record=UserActivity.objects.get(SID=sid)
                record=UserActivity.objects.get(id=record.id)
                record.lastlogin=intime
                record.lastlogout=intime
                record.count+=1
            except:
                record=UserActivity(SID=user.SID,fullname=user.fullname,lastlogin=intime,lastlogout=intime,count=1)
            record.save()
            s=f'{user.SID} logged in successfully'
            return render(request,'cargapp/'+user.type+'.html',{'user':s})
        except : 
            s='<h1>login credentials are wrong</h1>'
        return HttpResponse(s)
    return render(request,"cargapp/loginpage.html")

def logout(request):
    outime=datetime.now()
    sid=request.session.get('user')
    record=UserActivity.objects.get(SID=sid)
    record=UserActivity.objects.get(id=record.id)
    record.lastlogout=outime
    record.save()
    request.session.flush()
    return redirect('loginpage')


def register(request):
    if request.method=='POST':
        sid=request.POST.get('SID')
        fname=request.POST.get('fullname')
        email=request.POST.get('email')
        type=request.POST.get('type')
        pword=request.POST.get('password')
        cpword=request.POST.get('confirm password')
        if pword==cpword:
            try:
                User.objects.get(SID=sid)
                s=f'<h1>{sid} roll number already exits</h1>'
            except:
                User(SID=sid,fullname=fname,email=email,password=pword,type=type).save() 
                s='<h1>you are regsitered successfully</h1>'
            return HttpResponse(s)
        return HttpResponse("<h1> please enter correct details</h1>")
    return render(request,'cargapp/register.html',{'registration':True})


def bulkregister(request):
    if request.method=='POST':
        excelfile=request.FILES['file']
        if not excelfile.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request,'cargapp/register.html',{'registration':False})
        data=read_excel(excelfile)#dataframe
        data=data.values.tolist()#to convert dataframe to list
        print(data[0])
        for person in data:
            record=User(SID=person[0],fullname=person[1],email=person[2],password=person[3],type=person[4])
            record.save()
        return HttpResponse('<h1> BULK REGISTRATION COMPLETED SUCCESSFULLY</h1>')
    return render(request,'cargapp/register.html',{'registration':False})


def changepassword(request):
    if request.method=='POST':
        sid=request.POST.get('SID')
        opword=request.POST.get('old password')
        pword=request.POST.get('password')
        cpword=request.POST.get('confirm password')
        try:
            user=User.objects.get(SID=sid,password=opword)
            if pword=='welcome123#':
                return redirect('changepassword')
            if not pword==cpword: s='<h1> new and confrim password must be same</h1>'
            else:
                user.password=pword
                user.save()
                s='<h1>your password is changed successfully</h1>'
        except: s="<h1>please enter existed SID and  old password</h1>"
        return HttpResponse(s)
    return render(request,'cargapp/changepassword.html',{'message':'please change your password as it should not be welcome123#'})


