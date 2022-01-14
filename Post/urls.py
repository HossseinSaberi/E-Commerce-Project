from django.urls import path
from .views import showPostDetails_rest,  showAllCatrgoty_rest, showComments_rest, showSingleComments_rest, getAllPostByCategory , filter_by_tag_id , delete_post , AddPostView , edit_category , edit_post 
from .views import showAllPosts, postDetails,  contactUs, category, filter_By_category_id, showAllPosts_rest , tag , showUsersPost , AddTagView , delete_tag , edit_tag , delete_category , add_category
from django.views.generic import TemplateView

urlpatterns = [
    path("", showAllPosts , name='index'),
    path("usersPosts/", showUsersPost , name='Usersindex'),
    path("post_Details/<slug:slug>", postDetails , name='post_details'),
    path("category_Archive/", category , name='category_Archive'),
    path("category_Archive/<int:cat_id>", filter_By_category_id),
    path('tag_Archive/<int:tag_id>', filter_by_tag_id , name='filter_tag'),
    path('tag_Archive/' , tag , name='filter_tag'),
#     path("AddComment/<int:post_id>", add_comment, name="AddNewComment"),
    path("AddNewTag/", AddTagView.as_view(), name="AddNewTag"),
    path("EditNewTag/<int:tag_id>", edit_tag, name="EditNewTag"),
    path("DelTag/<int:tag_id>", delete_tag, name="DeleteTag"),
    path("AddNewPost/", AddPostView.as_view(), name="AddNewPost"),
    path("EditPost/<slug:slug>", edit_post, name="EditPost"),
    path("DelPost/<slug:slug>", delete_post, name="DeletePost"),
    path("EditCategory/<int:cat_id>" , edit_category , name='EditCategory'),
    path("AddCategory/" , add_category , name='AddCategory'),
    path("DeleteCategory/<int:cat_id>" , delete_category , name='DeleteCategory'),
    path('aboutUs/', TemplateView.as_view(template_name="AboutTemplate/About.html"), name='about'),
    path('contactUs/', contactUs.as_view()),
    path('api/', showAllPosts_rest, name='GetAllPostRest'),
    path('api/<slug:slug>', showPostDetails_rest, name='GetPostDetailsRest'),
    path('api/GetComment/', showComments_rest, name='GetCommentsRest'),
    path('api/GetComment/<int:id>', showSingleComments_rest,
         name='GetSingleCommentsRest'),
    path('api/AllCategory/', showAllCatrgoty_rest, name='GetAllCategoryRest'),
    path('api/PostByCategory/<str:title>',
         getAllPostByCategory, name='GetAllPostByCategoryRest'),
]
