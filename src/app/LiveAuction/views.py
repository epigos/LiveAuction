#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.views.generic import  DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from LiveAuction.models import Auction, Bid
from LiveAuction.forms import LoginForm, RegisterForm, AddAuctionForm
from django.db.models import Max
from django.utils.log import getLogger
import django
import json

from django.core.paginator import Paginator, EmptyPage, InvalidPage

logger = getLogger('app')

def index_view(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))


def about_view(request):
    return render_to_response('about.html',
                              context_instance=RequestContext(request))


def login_view(request):
    message = ''

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username,
                                    password=password)

                if user is not None and user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    message = \
                        'The username or password you entered is incorrect.'

        form = LoginForm()
        context = {'form': form, 'message': message}

        return render_to_response('login.html', context,
                                  context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password_one = form.cleaned_data['password_one']
            password_two = form.cleaned_data['password_two']

            user = User.objects.create_user(username=username,
                    email=email, password=password_one)

            user.save()

            return render_to_response('thanks_register.html',
                    context_instance=RequestContext(request))
        else:
            context = {'form': form}

            return render_to_response('register.html', context,
                    context_instance=RequestContext(request))

    context = {'form': form}

    return render_to_response('register.html', context,
                              context_instance=RequestContext(request))


def auction_index_view(request, pagina):
    auction_list = Auction.objects.all()
    paginator = Paginator(auction_list, 5)

    try:
        page = int(pagina)
    except:
        page = 1
    try:
        auctions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        auctions = paginator.page(paginator.num_pages)

    context = {'auctions': auctions}

    return render_to_response('Auctions/index.html', context,
                              context_instance=RequestContext(request))


def singleAuction_view(request, id_auction):
    auction = Auction.objects.get(Id=id_auction)
    higherBid = Bid.objects.filter(Id=id_auction).values('Id').annotate(Max('Amount'))

    bid = Bid.objects.get(Id=higherBid[0]["Id"])
    logger.debug(bid)

    context = {'auction': auction, 'bid': bid}

    return render_to_response('Auctions/SingleAuction.html', context,
                              context_instance=RequestContext(request))


def add_auction_view(request):
    message = ''

    if request.method == 'POST':
        form = AddAuctionForm(request.POST)

        if form.is_valid():
            add = form.save(commit=False)
            add.status = True
            add.save()
            message = 'Saved successfully.'

            return HttpResponseRedirect('/auction/%s' % add.Id)
    else:
        form = AddAuctionForm()

    context = {'form': form, 'message': message}

    return render_to_response('Auctions/addAuction.html', context,
                              context_instance=RequestContext(request))


def edit_auction_view(request,id_auction):
    info = "Loading..."
    auction = Auction.objects.get(Id=id_auction)

    if request.method == "POST":
        form = AddAuctionForm(request.POST,instance=auction)
        if form.is_valid():
            edit_auction = form.save(commit=False)
            edit_auction.status = True
            edit_auction.save()
            info = "Edited successfully."
            return HttpResponseRedirect('/auction/%s/' % edit_auction.Id)
    else:
        form = AddAuctionForm(instance=auction)
    context = {'form':form,'informacion':info}
    return render_to_response('Auctions/editAuction.html',context,context_instance=RequestContext(request))


class delete_auction_view(DeleteView):
    model = Auction
    template_name = "employees_confirm_delete.html"
    success_url = "/"

    # allow delete only logged in user by appling decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # maybe do some checks here for permissions ...

        resp = super(delete_auction_view, self).dispatch(*args, **kwargs)

        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                content_type="application/json")
        else:
            return resp

@csrf_exempt
def node_api(request):
    try:
        #Get User from sessionid
        session = Session.objects.get(session_key=request.POST.get("sessionId"))
        user_id = session.get_decoded().get("_auth_user_id")
        user = User.objects.get(id=user_id)

        auction = Auction.objects.get(Id=request.POST.get("auctionId"))
        amount = request.POST.get("amount")
        time = datetime.now()
        
        logger.debug(request.POST.get("auctionId"))

        #Add Bid
        Bid.objects.create(Auction=auction, User=user, Amount=amount, Hour=time)
        data = json.dumps({ "success": True, "message": "", "auctionId":auction.Id, "amount":amount, "time":time }, cls=DjangoJSONEncoder)
        
        return HttpResponse(data, content_type="application/json")
        #return HttpResponse("Everything worked :)")
    except Exception, e:
        return HttpResponseServerError(json.dumps({ "success": False, "message": str(e) }), content_type="application/json")
        #return HttpResponse(str(e))

