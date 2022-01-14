from django import forms
from django.contrib import messages
from django.db.models.fields import SlugField
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls.base import reverse
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseNotFound, request
from django.views.generic.base import TemplateView, View
from rest_framework import serializers
from .models import Post, Category, Comment, Tag
from .forms import AddCategoryForm, CommentForm, AddTagForm, DeleteCategoryForm, DeleteTagForm, EditPostForm, EditTagForm, DeletePostForm, CreatePostForm, EditCategoryForm
from rest_framework.decorators import api_view
from .serializers import AllPostSerializer, CommentSerializer, PostDetailsSerializer, CategorySerializer
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

User = get_user_model()
################################## Function Base #############################


def showAllPosts(request):

    if request.method == 'GET':
        if request.GET.get('search_box'):
            search_query = request.GET.get('search_box')
            if(search_query[0] == '@'):
                username = search_query[1:]
                try:
                    user = User.objects.get(username = username)
                    users_post = Post.objects.filter(writer=user.id)
                except:
                    username = 'Mr NoBody'
                    users_post = None
                context = {
                    'Posts': users_post,
                    'cat_or_tag': username
                }
                return render(request, 'PostTemplate/AllPosts.html', context=context)
            else:
                posts = Post.objects.filter(
                    Q(title__icontains=search_query))
                return render(request, 'PostTemplate/AllPosts.html', {'Posts': posts, 'cat_or_tag': 'Serached'})
        allPost = Post.objects.all().order_by('-create_at')
        return render(request, 'PostTemplate/AllPosts.html', {'Posts': allPost, 'cat_or_tag': "All"})


def showUsersPost(request):
    users_post = Post.objects.filter(writer_id=request.user.id)
    context = {
        'Posts': users_post,
        'cat_or_tag': request.user.username
    }
    return render(request, 'PostTemplate/AllPosts.html', context=context)


def postDetails(request, slug):

    if request.GET.get('q'):
        q = request.GET['q']
        specific_post = get_object_or_404(Post, title=q)
    else:
        specific_post = get_object_or_404(Post, slug=slug)
    category = specific_post.category.all()
    tags = specific_post.tag.all()
    comments = Comment.objects.filter(post_id=specific_post.id)

    if request.method == 'POST':
        comments_form = CommentForm(data=request.POST)
        if comments_form.is_valid():
            form = comments_form.save(commit=False)
            form.post = specific_post
            form.save()

            return redirect(reverse('post_details', args=[str(specific_post.slug)]))

    else:
        comments_form = CommentForm()
    return render(request, 'PostDetails/DetailsOfPost.html', {'PostDetails': specific_post, 'category': category, 'comments': comments, 'tags': tags, 'forms': comments_form})


def category(request):
    all_category = Category.objects.all()
    parrent_categury = Category.objects.filter(parent=None)
    return render(request, 'CategoryTemplate/Category.html', {'Categories': all_category, 'parrent_categury': parrent_categury})


def tag(request):
    all_tag = Tag.objects.all()
    return render(request, 'TagTemplate/Tag.html', {'tags': all_tag})


def filter_By_category_id(request, cat_id):
    category_filter = Post.objects.filter(category__id=cat_id)
    cat = Category.objects.get(id=cat_id).title
    return render(request, 'PostTemplate/AllPosts.html', {'Posts': list(category_filter), 'cat_or_tag': cat})


def filter_by_tag_id(request, tag_id):
    tag_filter = Post.objects.filter(tag__id=tag_id)
    tag_title = Tag.objects.get(id=tag_id).title
    return render(request, 'PostTemplate/AllPosts.html', {'Posts': tag_filter, 'cat_or_tag': '#' + str(tag_title)})


class AddTagView(LoginRequiredMixin, View):
    form = AddTagForm

    def get(self, request, *args, **kwargs):
        return render(request, 'TagTemplate/AddTag.html', {'form': self.form})

    def post(self, request, *args, **kwargs):
        post_form = self.form(request.POST)
        if post_form.is_valid():
            post_form.save()
            messages.info(request, 'The Tag is Adding to Tags')
            return redirect('filter_tag')


@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    form = DeleteTagForm(tag)
    if request.method == 'POST':
        tag.delete()
        return redirect(reverse('filter_tag'))

    return render(request, 'TagTemplate/ConfrimDelete.html', {'form': form, 'tag': tag})


@login_required
def edit_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    form = EditTagForm(instance=tag)
    if request.method == 'POST':
        form = EditTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect(reverse('filter_tag'))

    return render(request, 'TagTemplate/EditTag.html', {'form': form, 'tag': tag})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        if request.user == post.writer:
            DeletePostForm(post)
            post.delete()
            return redirect(reverse('Usersindex'))
        else:
            messages.error(
                request, f"Dear {request.user.username} , this post does not belong to you !", extra_tags='danger')

    return render(request, 'PostDetails/ConfrimDelete.html', {'post': post})


@login_required
def edit_post(request, slug):
    specific_post = get_object_or_404(Post, slug=slug)

    form = EditPostForm(instance=specific_post)
    if request.method == 'POST':
        if request.user == specific_post.writer:
            form = EditPostForm(request.POST, instance=specific_post)
            if form.is_valid():
                form.save()
                return redirect(reverse('post_details', args=[str(specific_post.slug)]))
        else:
            messages.error(
                request, f"Dear {request.user.username} , this post does not belong to you !", extra_tags='danger')

    return render(request, 'PostDetails/EditPost.html', {'form': form, 'post': specific_post})


class AddPostView(LoginRequiredMixin, View):
    form = CreatePostForm
    print(form)

    def get(self, request, *args, **kwargs):
        return render(request, 'PostDetails/AddPost.html', {'form': self.form})

    def post(self, request, *args, **kwargs):

        post_form = self.form(request.POST, request.FILES)
        if post_form.is_valid():
            category_selected = post_form.cleaned_data['category']
            tag_selected = post_form.cleaned_data['tag']

            category_set = Category.objects.filter(title__in=category_selected)
            tag_set = Tag.objects.filter(title__in=tag_selected)

            created_post = Post.objects.create(
                title=post_form.cleaned_data['title'], shortDescription=post_form.cleaned_data['shortDescription'], writer=request.user,  Text=post_form.cleaned_data['Text'], image=post_form.cleaned_data['image'], slug=post_form.cleaned_data['slug'])

            print(category_selected)
            for cat_item in category_selected:
                created_post.category.add(cat_item.id)
            for tag_item in tag_selected:
                created_post.tag.add(tag_item)

            messages.info(request, 'The Post is Adding to Posts')
        return redirect('Usersindex')


@login_required
def delete_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)

    form = DeleteCategoryForm(category)
    if request.method == 'POST':
        category.delete()
        return redirect(reverse('category_Archive'))

    return render(request, 'CategoryTemplate/ConfrimDelete.html', {'form': form, 'category': category})


@login_required
def edit_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    form = EditCategoryForm(instance=category)
    if request.method == 'POST':
        form = EditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(reverse('category_Archive'))
    return render(request, 'CategoryTemplate/EditCategory.html', {'form': form, 'category': category})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('category_Archive'))
    form = AddCategoryForm()
    return render(request, 'CategoryTemplate/AddCategory.html', {'form': form})

############################# Class Base ###################################################


class contactUs(TemplateView):
    template_name = 'ContactUsTemplate/ContactUs.html'


class aboutUs (TemplateView):
    template_name = 'AboutTemplate/About.html'

# class showUsersPosts (ListView):
#     template_name =  'PostTemplate/AllPosts.html'
#     users_post = Post.objects.filter(writer__id = request.user.id)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["users_post"] = self.users_post
#         return context


################################# DRF View #####################################

@api_view(['GET'])
def showAllPosts_rest(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        post_serializers = AllPostSerializer(posts, many=True)
        return Response(data=post_serializers.data, status=200)

    elif request.method == 'POST':
        pass


@api_view(['GET'])
def showPostDetails_rest(request, slug):
    if request.method == 'GET':
        post_details = get_object_or_404(Post, slug=slug)
        post_details_serializer = PostDetailsSerializer(post_details)

        return Response(data=post_details_serializer.data, status=200)


@api_view(['GET'])
def showAllCatrgoty_rest(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)
        return Response(data=categories_serializer.data, status=200)

    elif request.method == 'POST':
        pass


@api_view(['GET'])
def showComments_rest(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        comments_serializer = CommentSerializer(comments, many=True)

        return Response(data=comments_serializer.data, status=200)


@api_view(['GET'])
def showSingleComments_rest(request, id):
    if request.method == 'GET':
        comments = Comment.objects.get(id=id)
        comments_serializer = CommentSerializer(comments)

        return Response(data=comments_serializer.data, status=200)


@api_view(['GET'])
def getAllPostByCategory(request, title):
    if request.method == 'GET':
        posts = Post.objects.filter(category__title=title)
        postsSerializer = AllPostSerializer(posts, many=True)

        return Response(data=postsSerializer.data, status=200)

############################### Forms ##########################################
