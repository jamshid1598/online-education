from cart.forms import PayForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse, BadHeaderError
from django.core import serializers
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder
from django.template import defaultfilters
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
from django.db.models import Case, Value, When, Q, F
import json

from product.models import *
from product.forms import ModelSearchForm
from cart.models import *
from core.models import *

from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)
# from .forms import SearchForm
from product.filters import LessonFilter
from download.views import create_verify


class MainView(ListView):
	model = Category
	template_name = "index.html"
	paginate_by = 5


class SubjectDetail(DetailView):
	template_name = "lesson.html"
	model = Subject

	slug_field = 'slug'
	slug_url_kwarg = 'slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["category"] = self.object.category
		try: 
			l_slug = self.kwargs.get('l_slug')
			c_lesson = Lesson.objects.get(slug=l_slug, subject=self.object)
			context["c_lesson"] = c_lesson
			try:
				context["n_lesson"] = Lesson.objects.get(lesson_series=c_lesson.lesson_series+1, subject=self.object)
			except:
				context["n_lesson"] = None
		except:
			c_lesson = Lesson.objects.filter(subject=self.object).order_by("lesson_series").first()
			context["c_lesson"] = c_lesson
			try:
				context["n_lesson"] = Lesson.objects.get(lesson_series=c_lesson.lesson_series+1, subject=self.object)
				print("hello")
			except:
				context["n_lesson"] = None
				print("hello")

		return context
	


class ModelDetailView(DetailView):
	template_name = 'Mahsulot.html'
	model = Lesson

	slug_field = 'slug'
	slug_url_kwarg = 'slug'

	# def get_context_data(self, **kwargs):
	#     context = super().get_context_data(**kwargs)

	#     # images related to 3d model object
	#     md = Lesson.objects.get(slug=self.kwargs['slug'])
		# context['image_list'] = md.product_images.all()

	#     return context


class AllLesson(ListView):
	template_name='all-lesson.html'
	model = Subject

class FreeLessonListView(ListView):
	template_name = "free.html"
	model = Subject
	paginate_by = 24

	def get_queryset(self):
		queryset = super().get_queryset()
		try:
			return queryset.filter(free=True)
		except:
			return queryset


class DiscuntView(ListView):
	template_name = "discount.html"
	model = Subject
	paginate_by = 24

	def get_queryset(self):
		queryset = super().get_queryset()
		discount_list = []
		try:
			for sub in queryset.filter(free=False):
				if sub.discount:
					discount_list.appand(sub)
			queryset = discount_list
		except:
			queryset = discount_list
		return queryset


class PaymentView(LoginRequiredMixin, View):
	template_name = "To'lov.forma.html"
	# context       = {}
	total_price = 0

	def get(self, request, pk=None, *args, **kwargs):
		payform = PayForm()  # Payment Form
		# send_download_page(request, request.user.customer)
		return render(
			request,
			self.template_name,
			{'payform': payform},
		)

	def post(self, request, pk=None, *args, **kwargs):
		model = None
		if request.user.is_authenticated and pk == None:
			customer = self.request.user.customer
			order, created = Order.objects.get_or_create(customer=customer, complete=False)
			print("Order: ", order, '\n', "Created: ", created)
			items = order.orderitem_set.all()
		elif request.user.is_authenticated and pk != None:
			model = Lesson.objects.get(pk=pk)
			items = []
		else:
			items = []

		if len(items) > 0:
			for item in items:
				if item.cart_field and item.model.discount:
					self.total_price += item.model.discount
				elif item.cart_field:
					self.total_price += item.model.price
		elif model:
			if model.discount:
				self.total_price += model.discount
			else:
				self.total_price += model.price

		print("total price: ", self.total_price)
		# get selected models' total proce in cart page

		payform = PayForm(request.POST)
		if payform.is_valid():
			number = payform.cleaned_data['number']
			exp_date = payform.cleaned_data['exp_date']
			r = create_verify(request, number, exp_date, self.total_price)
			if 'error' not in r:
				return render(request, "card_verify.html", {
					'token': r['token'],
					'amount': self.total_price,
					'blogid': pk,
				})
		print("Error")
		return redirect('Core:payment-view')


@login_required
def like_lesson(request):
	data = json.loads(request.body)
	slug = data['slug']
	print('slug', slug)
	try:
		obj = SubCategory.objects.get(slug=slug)
	except Exception as e:
		obj=None
	if obj and obj.like.filter(id=request.user.id).exists():
		obj.like.remove(request.user)
		print("unliked")
		return JsonResponse({"success":"Unliked"}, safe=False, status=200)
	elif obj and not obj.like.filter(id=request.user.id).exists():
		obj.like.add(request.user)
		print("liked")
		return JsonResponse({"success":"Liked"}, safe=False, status=200)
	return JsonResponse({"success":"Something went wrong :("}, safe=False, status=200)


def download_counter(request):
	slug = request.GET.get('request_data')
	Lesson.objects.filter(slug=slug).update(downloaded=F('downloaded') + 1)
	return HttpResponse(
		json.dumps('Increased'),
		content_type="application/json"
	)


def downloads(request, *args, **kwargs):
	# print("Customer, ", request.user.customer.user.first_name)
	# print("Curront url: ", request.path)
	# print(request.build_absolute_uri)

	models = Lesson.objects.all()
	downloads = 0
	if models:
		downloads = sum([product.downloaded for product in models])
		try:
			return JsonResponse({"instance": downloads, }, safe=False, status=200)
		except Exception as e:
			print("Error occured: ", e)
	return Http404


# other changes
def save_model(request):
	quantity = request.GET.get('model_quantity')
	single_price = request.GET.get('single_price')
	total_price = request.GET.get('total_price')
	# print(quantity, single_price, request.user.id)
	customer = Customer.objects.get(user=request.user.id)
	ordereditem = OrderedItem.objects.create(
		model_quantity=quantity,
		single_price=single_price,
		total_price=total_price,
		completed=False,
		customer_id=customer.id
	)
	print(ordereditem)
	ordereditem.save()
	return redirect('/')


# end other changes
class AboutUsView(View):
	template_name = "about.html"
	context = {}

	def get(self, request, *args, **kwargs):
		self.context["object_list"] = AboutUs.objects.all()
		return render(
			request,
			self.template_name,
			self.context
		)


from users.forms import FeedbackForm


class Contact(View):
	template_name = 'Aloqa.html'
	context = {}

	def get(self, request, *args, **kwargs):
		form = FeedbackForm()
		self.context['form'] = form

		return render(
			request,
			self.template_name,
			self.context
		)

	def post(self, request, *args, **kwargs):
		if request.method == "POST":
			form = FeedbackForm(request.POST)
			if form.is_valid():
				first_name = form.cleaned_data['first_name']
				last_name = form.cleaned_data['last_name']
				phone_number = form.cleaned_data['phone_number']
				text = form.cleaned_data['text']

				try:
					subject = "Subject"
					thoughts = f"{first_name} {last_name}dan yangi xabar: \n\n{text}\nTel: {phone_number}"
					sender = settings.EMAIL_HOST_USER
					recipients = ['ruslanovrahmet@gmail.com']

					send_mail(subject, thoughts, sender, recipients, fail_silently=False)

					messages.success(request, f"{first_name} xabaringiz muvofaqiyatli yuborildi.")
				except BadHeaderError:
					return HttpResponse('Invalid header')
				return redirect('Core:contact-view')
			else:
				for msg in form.errors:
					messages.error(request, f"{msg}")
				return redirect('Core:contact-view')
		form = FeedbackForm()
		self.context = {
			'form': form
		}

		return render(
			request,
			self.template_name,
			self.context
		)


from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal


class LazyEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			return str(obj)
		return super().default(obj)


def search_query(request, *args, **kwargs):
	query = ''
	images_url = {}

	# data = json.loads(request.body)
	# query = data['query']
	query = request.GET.get('query')
	print(query)

	object_list = None
	if (len(query) > 0) and (query != "" or query != " "):
		print("length: ", len(query))
		object_list = Lesson.objects.filter(
			Q(name__icontains=query) | Q(slug__icontains=query) | Q(short_info__icontains=query) | Q(
				description__icontains=query)
		)
	if object_list.count() > 0:
		for obj in object_list:
			if obj.imageURL:
				images_url[obj.pk] = obj.imageURL
		print(images_url)
		try:
			object_list_json = serializers.serialize('json', object_list, cls=LazyEncoder, ensure_ascii=True)
		# images_url_json =  json.dumps([images_url,])#serializers.serialize('json', [images_url, ])
		except Exception as e:
			print("Error occured: ", e)
		return JsonResponse({"instance": object_list_json, "images_url": images_url}, safe=False, status=200)
	else:
		object_list_json = "nothing"
		return JsonResponse(object_list_json, safe=False, status=200)
	return Http404


def go_to_email(request):
	return render(request, "go_to_email.html")


def abcd(request):
	return render(request, "email.html")