from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('create_student/',views.Create_student_htmx.as_view(),name = 'create_student'),
    #path('create_student_htmx/',views.create_student_htmx,name = 'create_student_htmx'),
    path('create_group/',views.Create_group_htmx.as_view(),name = 'create_group'),
    path('create_group_htmx/',views.create_group_htmx,name = 'create_group_htmx'),
    # path('upload_photo/<int:id>',views.upload_image,name = 'upload_image'),
    path('<slug:hash>',views.user_registration,name = "inviteplus"),
    path('add_student/',views.add_student_to_group,name = "add_student"),
    path('student/<int:id>',views.student_card_htmx,name='student_htmx'),
    path('student/<int:id>/edit/',views.Student_card_edit.as_view(),name='student_edit')
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# urlpatterns+=[
#     re_path(r'(?P<hash>.+)$',views.user_registration,name = "inviteplus"),
# ]