from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from p_library import views
from p_library.views import AuthorEdit, AuthorList, author_create_many, books_authors_create_many

app_name = 'p_library'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('publishers/', views.publishers),
    path('friends/', views.friends),
    path('index/book_increment/', views.book_increment),
    path('index/book_decrement/', views.book_decrement),
    path('author/create', AuthorEdit.as_view(), name='author_create'),
    path('authors', AuthorList.as_view(), name='author_list'),
    path('author/create_many', author_create_many, name='author_create_many'),
    path('author_book/create_many', books_authors_create_many, name='author_book_create_many'),
    path('', include('common.urls', namespace='common')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
