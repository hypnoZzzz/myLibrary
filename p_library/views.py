from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect
from django.template import loader
from p_library.models import Book, Publisher, Author, Friend
from p_library.forms import AuthorForm, BookForm


class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:authors_list')
    template_name = 'author_edit.html'


class AuthorList(ListView):
    model = Author
    template_name = 'base/authors_list.html'


class PublisherList(ListView):
    model = Publisher
    template_name = 'base/publishers.html'


def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/')
            book.copy_count += 1
            book.save()
        return redirect('/')
    else:
        return redirect('/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/')
    else:
        return redirect('/')


def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)


def publishers(request):
    template = loader.get_template('base/publishers.html')
    publishers = Publisher.objects.all()
    publisher_data = {
        'publishers': publishers
    }
    return HttpResponse(template.render(publisher_data, request))


def friends(request):
    template = loader.get_template('base/friends.html')
    friend = Friend.objects.all()
    friends_data = {
        'friends': friend
    }
    return HttpResponse(template.render(friends_data, request))


def index(request):
    template = loader.get_template('base/index.html')
    books = Book.objects.all()
    bible_data = {
        "books": books,
    }
    return HttpResponse(template.render(bible_data, request))


def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
    return render(request, 'manage_authors.html', {'author_formset': author_formset})


def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
        request,
        'manage_books_authors.html',
        {
            'author_formset': author_formset,
            'book_formset': book_formset,
        }
    )