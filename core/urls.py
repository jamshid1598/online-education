from django.urls import path

from .views import (
    MainView,
    SubjectDetail,
    ModelDetailView,
    AllLesson,
    PaymentView,
    FreeLessonListView,
    download_counter,

    downloads,

    DiscuntView,

    AboutUsView,
    Contact,
    save_model,
    go_to_email,
    abcd,

    search_query,
    like_lesson,
)
from cart.views import (
    CartDetailView,
    add_to_cart_view,
    model_checkbox,
)


app_name='Core'

urlpatterns = [
    path('', MainView.as_view(), name = "main-view"),
    path('lesson/<slug:slug>/', SubjectDetail.as_view(), name='lesson-view'),
    path('lesson/<slug:slug>/<slug:l_slug>/', SubjectDetail.as_view(), name='lesson-view'),

    path('model/<slug:slug>/', ModelDetailView.as_view(), name='model-detail-view'),

    path('free/lessons/', FreeLessonListView.as_view(), name='free-lessons'),
    path('ajax/download_counter/', download_counter, name='download_counter'),

    path('all-lessons/', AllLesson.as_view(), name='all-lessons'),

    path('ajax/downloads/', downloads, name='downloads'),

    path('payment/', PaymentView.as_view(), name='payment-view'),
    path('payment/<int:pk>/', PaymentView.as_view(), name='payment-view'),

    path('card/', CartDetailView.as_view(), name='card-view'),
    path('ajax/cart/detail/', add_to_cart_view, name='add_to_cart_view'),
    path('ajax/model/checkbox/', model_checkbox, name='model_checkbox'),

    path('contact/', Contact.as_view(), name='contact-view'),
    
    path('discount/', DiscuntView.as_view(), name='aksiya-view'),

    
    path('about/', AboutUsView.as_view(), name='about-view'),

    path('ajax/search_query/', search_query, name='search_query'),
    path('ajax/like/lesson/', like_lesson, name='likes'), 

    path('save_model/', save_model, name='save_model'),

    path('go_to_email/', go_to_email, name='go_to_email'),
    path('abcd/', abcd)
]
