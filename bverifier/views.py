from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template 
from django.template import RequestContext
from businesssearch import fsearch
from bverifier.models import Brands
# Create your views here.
def index(request):
    result = {}
    if request.session.get('result',{}):
       
       result = request.session.get('result')
       print(result);
       del request.session['result'] 
       return render(request,"index.html",result) 
    template = get_template('index.html')
    return render(request,"index.html")


def search(request):
    if request.method == "POST":
        #Handling Instagram
        if str(request.POST["method"]) == "instagram":
            user_name = request.POST["username"]
            brands = Brands.objects.filter(search_key__icontains=user_name,search_via='instagram')
            #check in db first
            if not brands:
                # if not found, Run the process find on instagram
                result = {}
                result["search_status"] = "failure"
                result["search_message"] = "Business is not registered with us!"
                request.session['result'] = result
                return HttpResponseRedirect('/')
            else:
                # Run the loop and find verified status in db
                flag = 0
                for brand in brands:
                    if brand.search_verified == '1' :
                        flag = 1
                # if found return response
                if flag == 1:
                    result = {}
                    result["search_status"] = "success"
                    result["search_message"] = "Business verified successfully"
                    request.session['result'] = result
                    return HttpResponseRedirect('/')     
                # if not found search on instagram
                else:     
                    # if not found return the response as unverified
                    result = {}
                    result["search_status"] = "failure"
                    result["search_message"] = "Business is not verified!"
                    request.session['result'] = result
                    return HttpResponseRedirect('/')
        # Handling WebURL
        if str(request.POST["method"]) == "weburl":
            weburl = request.POST["weburl"]
            brands = Brands.objects.filter(search_key__icontains=weburl,search_via='weburl')
            if not brands:
                result = {}
                result["search_status"] = "failure"
                result["search_message"] = "Business is not registered with us verified!"
                request.session['result'] = result
                return HttpResponseRedirect('/')
            else:
                flag = 0
                for brand in brands:
                    if brand.search_verified == '1' :
                        flag = 1
                if flag == 1:
                    result = {}
                    result["search_status"] = "success"
                    result["search_message"] = "Business verified successfully"
                    request.session['result'] = result
                    return HttpResponseRedirect('/')     
                else:     
                    result = {}
                    result["search_status"] = "failure"
                    result["search_message"] = "Business could not verified!"
                    request.session['result'] = result
                    return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def register(request):
    if request.method == "POST":
        form = request.POST;
        if form["method"] == 'weburl':
            brands = Brands(
            search_key      = form["weburl"],
            search_via      = form["method"],
            search_cr       = form["cr_number"],
            search_cr_url   = form["weburlcr"],
            )
            brands.search_verified = fsearch.website_cr_verification(form["weburlcr"],form["cr_number"])
            brands.save()   
            if(brands.search_verified==1):
                result = {}
                result["register_status"] = "success"
                result["register_message"] = "Brand Added successfully with Verification" 
                request.session['result'] = result
            else:
                result = {}
                result["register_status"] = "success"
                result["register_message"] = "Brand Added successfully <b>without verification</b>" 
                request.session['result'] = result
            return HttpResponseRedirect('/')
        else:
            brands = Brands(
                search_key      = form["weburl"],
                search_via      = form["method"],
                search_cr       = form["cr_number"],
                search_cr_url   = '#',
            )
            brands.search_verified = fsearch.instagram_check(form["weburl"], form['cr_number'])
            # if found return the response and save it in db
            brands.save()   
            if(brands.search_verified==1):
                result = {}
                result["register_status"] = "success"
                result["register_message"] = "Brand Added successfully with Verification" 
                request.session['result'] = result
            else:
                result = {}
                result["register_status"] = "success"
                result["register_message"] = "Brand Added successfully without verification" 
                request.session['result'] = result
            return HttpResponseRedirect('/')

    return render(request,"index.html")
