
from unittest import result
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import datetime
import base64
from django.core.files.base import ContentFile
import os




from home.models import Visitor

# Create your views here.
def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("/login")
    total_passes = Visitor.objects.count()
    todays_visitors = Visitor.objects.filter(visit_time__date=now().date()).count()

    total_visitors = Visitor.objects.count()

    return render(request, 'index.html', {
        'total_passes': total_passes,
        'todays_visitors': todays_visitors,
        'total_visitors': total_visitors,
    })
    
    
def loginuser(request):
    if request.method=="POST":
        userid= request.POST.get('userid')
        password=request.POST.get('password')
        print(userid,password)
        #check if user entered correct credentials
        user = authenticate (username=userid, password=password)
        if user is not None:
            login(request, user)
            # A backend authenticated the credentials
            return redirect('/')
        else:
            return render(request,'login.html',{'error': "Invalid credentials"})
            
            
    # No backend authenticated the credentials
    return render(request,'login.html')
def logoutuser(request):
    logout(request)
    return redirect('/login')
from django.core.files.base import ContentFile
import base64
from .models import Visitor

def generatepass(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        country = request.POST.get('country')
        state = request.POST.get('state')
        office_designation = request.POST.get('officedesignation')
        office_name = request.POST.get('officcename')
        visiting_purpose = request.POST.get('visitingpurpose')
        captured_image_data = request.POST.get('captured_image')
        


        image_file = None
        if captured_image_data:
            try:
                format, imgstr = captured_image_data.split(';base64,')
                ext = format.split('/')[-1]
                image_file = ContentFile(base64.b64decode(imgstr), name=f'visitor_{first_name}_{last_name}.{ext}')
            except Exception as e:
                print("Image processing error:", e)

        # Create and save visitor
        visitor = Visitor(
            first_name=first_name,
            last_name=last_name,
            address=address,
            country=country,
            state=state,
            mobile=mobile,
            office_designation=office_designation,
            office_name=office_name,
            visiting_purpose=visiting_purpose
            
        )

        if image_file:
            visitor.photo = image_file

        visitor.save()

        return redirect('vms')

    return render(request, 'generatepass.html')

def link_callback(uri, rel):
    if uri is None:
        return ''
    if uri.startswith(settings.MEDIA_URL):
        return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        return os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    return uri

def visitorreport(request):
    visitors = []
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        visitors = Visitor.objects.filter(
            visit_time__date__gte=parse_date(from_date),
            visit_time__date__lte=parse_date(to_date)
        ).order_by('-visit_time')
    
    return render(request, 'visitorreport.html', {
        'visitors': visitors,
        'from_date': from_date,
        'to_date': to_date,
    })
def vms(request):
    today = datetime.date.today()
    visitors = Visitor.objects.filter(visit_time__date=today)
    return render(request, 'vms.html', {'visitors': visitors})
def download_pdf(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    visitors = []

    if from_date and to_date:
        visitors = Visitor.objects.filter(
            visit_time__date__gte=parse_date(from_date),
            visit_time__date__lte=parse_date(to_date)
        ).order_by('-visit_time')

    template = get_template('visitorreport_pdf.html')
    html = template.render({'visitors': visitors, 'from_date': from_date, 'to_date': to_date})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="visitor_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation failed', status=500)
    return response
def generate_pass_pdf(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)

    # Prepare the photo URL
    visitor.photo_url = visitor.photo.url if visitor.photo else settings.STATIC_URL + 'images/default_photo.png'

    template = get_template('visitor_pass_pdf.html')
    html = template.render({'visitor': visitor})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pass_{visitor.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse("PDF generation failed")
    return response
def punch_out_visitor(request, visitor_id):
    if request.method == 'POST':
        visitor = get_object_or_404(Visitor, id=visitor_id)
        if not visitor.punch_out_time:  # Only punch out if not already done
            visitor.punch_out_time = now()
            visitor.save()
    return redirect('vms') 

