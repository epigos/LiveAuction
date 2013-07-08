from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from LiveAuction.models import Auction
from LiveAuction.forms import LoginForm, RegisterForm
import django

from django.core.paginator import Paginator,EmptyPage,InvalidPage

def index_view(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o password incorrecto"
		form = LoginForm()
		ctx = {'form':form,'mensaje':mensaje}
		return render_to_response('login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username = usuario, email = email, password = password_one)
			u.save() # Guardar el objeto
			return render_to_response('thanks_register.html', context_instance = RequestContext(request))
		else:
			ctx = {'form':form}
			return 	render_to_response('register.html',ctx,context_instance = RequestContext(request))
	ctx = {'form':form}
	return render_to_response('register.html', ctx, context_instance = RequestContext(request))

def auction_index_view(request, pagina):

	auction_list = Auction.objects.all()
	paginator = Paginator(auction_list, 5)

	try:
		page = int(pagina)
	except:
		page = 1
	try:
		auctions = paginator.page(page)
	except (EmptyPage,InvalidPage):
		auctions = paginator.page(paginator.num_pages)

	ctx = {'auctions':auctions}
	
	return render_to_response('Auctions/index.html', ctx, context_instance = RequestContext(request))

def singleAuction_view(request, id_auction):
	auction = Auction.objects.get(Id=id_auction) 
	ctx = { 'auction': auction }
	return render_to_response('Auctions/SingleAuction.html', ctx, context_instance = RequestContext(request))
