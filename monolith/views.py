from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views import View
from .forms import *
from django.contrib.auth import logout
# Create your views here.
from .models import *
from django.contrib.auth.models import User

def get_user_data(request:HttpRequest) ->tuple:
  user = User.objects.get(id = request.user.id)
  light = LightUser.objects.get(user = user)
  guild = light.guild
  return user,light,guild  

def index(request):
    if request.user.is_authenticated:
      return main_panel(request)
    else:
      context= {}
      # Page from the theme 
      return render(request, 'pages/custom-index.html',context)

def main_panel(request:HttpRequest):
  user,light,guild = get_user_data(request)
  if light.role == "OWN":
    return admin_panel(request,user,light,guild)
  elif light.role == "TEA":
    return teacher_panel(request,user,light,guild)
  else:
    return student_panel(request,user,light,guild)

# Различные страницы для разных ролей, но все сидят на одной ссылке
def admin_panel(request:HttpRequest,user:User,light:LightUser,guild:Guild):
  students = Student.objects.filter(light__guild = guild)
  student_data = [{
    'student':s,
    'invite':Invite.objects.get(light_user = s.light)
  } for s in students]
  groups = Group.objects.filter(guild = guild)
  student_form = StudentCreationForm()
  group_form = GroupCreationForm()
  context = {
    'user':user,
    'light':light,
    'guild':guild,
    'student_data':student_data,
    'groups':groups,
    'student_form':student_form,
    'group_form':group_form
  }
  return render(request, 'pages/main_panel_final.html',context)  

def teacher_panel(request:HttpRequest,user:User,light:LightUser,guild:Guild):
  context = {
    'user':user,
    'light':light,
    'guild':guild
  }
  return render(request, 'pages/main_panel.html',context)  

def student_panel(request:HttpRequest,user:User,light:LightUser,guild:Guild):
  context = {
    'user':user,
    'light':light,
    'guild':guild
  }
  return render(request, 'pages/main_panel.html',context) 

def create_invite(request:HttpRequest,role:str):
  #depritiated
  user,light,guild = get_user_data(request)
  new_light = LightUser(role = role,guild = guild)
  new_light.save()
  new_invite = Invite(light_user = new_light)
  new_invite.save()
  return redirect('index')


#diffrent registration modes
def user_registration(request:HttpRequest,hash:str):
  invite = Invite.objects.get(url_hash = hash)
  if invite.active:
    if invite.light_user.role == "TEA":
      return TeacherRegister(request,hash)
    elif invite.light_user.role == "STU":
      return StudentRegister(request,hash)

def StudentRegister(request:HttpRequest,hash:str):
  invite = Invite.objects.get(url_hash = hash)
  if request.method == 'POST':
    form = SimpleRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      light = invite.light_user
      light.user = user
      light.save()
      invite.active = False
      invite.save()

    return redirect('login')
  else:
    form = SimpleRegistrationForm()
    context = { 'form': form ,
               'light':invite.light_user}
    return render(request, 'pages/sign-up student.html', context)  

def TeacherRegister(request:HttpRequest,hash:str):
  invite = Invite.objects.get(url_hash = hash)
  if request.method == 'POST':
    form = SimpleRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      light = invite.light_user
      light.user = user
      light.save()
      invite.active = False
      invite.save()

    return redirect('login')
  else:
    form = SimpleRegistrationForm()
    context = { 'form': form ,
               'light':invite.light_user}
    return render(request, 'pages/sign-up teacher.html', context)

class Create_student_htmx(View):

  def get(self,request:HttpRequest):
    form = StudentCreationForm()
    context = {
      'form':form
    }
    return render(request,'htmx/student_card_create.html',context)
  
  def post(self,request:HttpRequest):
    user,light,guild = get_user_data(request)
    form = StudentCreationForm(request.POST,request.FILES)
    if form.is_valid():
      student = form.save() #create student
      light = LightUser(role = 'STU',guild=guild) # create lightuser and link them
      light.save()
      student.light=light
      student.save()
      #create invite for student
      new_invite = Invite(light_user = light)
      new_invite.save()    
    return serve_student_list(request)

def serve_student_list(request:HttpRequest):
  user,light,guild = get_user_data(request)
  students = Student.objects.filter(light__guild = guild)
  student_data = [{
    'student':s,
    'invite':Invite.objects.get(light_user = s.light)
  } for s in students]
  context = {
    "student_data":student_data
  }
  return render(request,'htmx/student_list_htmx.html',context)

def student_card_htmx(request:HttpRequest,id:int):
  #print(id,id//10)
  student = Student.objects.get(id=id)
  context = {
    'student':student
  }
  return render(request,'htmx/student_card_htmx.html',context)

class Student_card_edit(View):
  def get(self,request:HttpRequest,id:int):
    student = Student.objects.get(id=id)
    student_data={
      'name':student.name,
      'gender':student.gender,
      'photo':student.photo
    }
    form = StudentCreationForm(initial=student_data)
    context={
      'student':student,
      'form':form
    }
    return render(request,'htmx/student_card_edit.html',context)
  def post(self,request:HttpRequest,id:int):
    pass


class Create_group_htmx(View):
  def get(self,request:HttpRequest):
    form = GroupCreationForm(request.POST)
    context={"form":form}
    return render(request,"htmx/group_create_htmx.html",context)
  
  def post(self,request:HttpRequest):
    user,light,guild = get_user_data(request)
    form = GroupCreationForm(request.POST)
    if form.is_valid():
      group = form.save(commit=False)
      group.guild = guild
      group.save()

    return serve_group_list_htmx(request)

def serve_group_list_htmx(request:HttpRequest):
  user,light,guild = get_user_data(request)
  groups = Group.objects.filter(guild = guild)
  context = {
    'groups':groups,
  }    
  return render(request,'htmx/group_list_htmx.html',context)

def create_group(request:HttpRequest):
  user,light,guild = get_user_data(request)
  if request.method == 'POST':
    form = GroupCreationForm(request.POST)
    if form.is_valid():
      group = form.save(commit=False)
      group.guild = guild
      group.save()

  return redirect('index')

def create_group_htmx(request:HttpRequest):
  user,light,guild = get_user_data(request)
  if request.method == 'POST':
    form = GroupCreationForm(request.POST)
    if form.is_valid():
      group = form.save(commit=False)
      group.guild = guild
      group.save()

  return serve_group_list_htmx(request)

def add_student_to_group(request:HttpRequest):
  student_id = int(request.POST['studentId'])
  group_id = int(request.POST['groupId'])
  group = Group.objects.get(id = group_id)
  student = Student.objects.get(id = student_id)
  user,light,guild = get_user_data(request)
  #check if user from the same guild as request user and group
  if student.light.guild == group.guild == guild:
    group.student.add(student)
    group.save()
  return serve_group_list_htmx(request)
# Authentication
class UserLoginView(LoginView):
  template_name = 'pages/sign-in.html'
  form_class = UserLoginForm

def logout_view(request):
  logout(request)
  return redirect('index')

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()

      guild_name = form.cleaned_data['guild_name']
      guild = Guild(name = guild_name)
      guild.save()

      light = LightUser(user = user,role = "OWN",guild = guild)
      light.save()
      
      print("Account created successfully!")
      return redirect('login')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'pages/sign-up.html', context)