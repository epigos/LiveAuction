#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from LiveAuction.models import Auction
from LiveAuction.forms import LoginForm, RegisterForm, AddAuctionForm
import django

from django.core.paginator import Paginator, EmptyPage, InvalidPage


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
    context = {'auction': auction}

    return render_to_response('Auctions/SingleAuction.html', context,
                              context_instance=RequestContext(request))


def add_auction_view(request):
    message = ''

    if request.method == 'POST':
        form = AddAuctionForm(request.POST, request.FILES)

        if form.is_valid():
            add = form.save(commit=False)
            add.status = True
            add.save()
            message = 'Saved successfully.'

            return HttpResponseRedirect('/auction/%s' % add.id)
    else:
        form = AddAuctionForm()

    context = {'form': form, 'message': message}

    return render_to_response('Auctions/addAuction.html', context,
                              context_instance=RequestContext(request))
