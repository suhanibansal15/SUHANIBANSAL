from django.contrib import admin
from django.urls import path , include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name="home"),
    path('login/', views.loginuser,name='login'),
    path('logout/', views.logoutuser,name='logout'),
    path('generatepass/', views.generatepass,name='generatepass'),
    path('visitorreport/', views.visitorreport,name='visitorreprot'),
    path('vms/', views.vms,name='vms'),
    path('visitorreport/pdf/', views.download_pdf, name='visitorreport_pdf'),
    path('generate_pass/<int:visitor_id>/', views.generate_pass_pdf, name='generate_pass'),
    path('punchout/<int:visitor_id>/', views.punch_out_visitor, name='punch_out_visitor'),

    
    
   
   
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
