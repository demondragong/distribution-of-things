from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView
from .models import Post

from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID

class PostListView(ListView):
    model = Post
    ordering = ['-updated_on']


# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "pending",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))

def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        subscribe(email)
        messages.success(request, "Email received. thank You! ") # message

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def post_detail(request, slug=None):
    if slug is None:
        try:
            post = Post.objects.filter(created_on__isnull=False).latest('created_on')
        except Post.DoesNotExist:
            raise Http404("Post does not exist")
    else:
        post = get_object_or_404(Post, slug=slug)

    try:
        next_post = post.get_next_by_created_on()
    except Post.DoesNotExist:
        next_post = None

    try:
        previous_post = post.get_previous_by_created_on()
    except Post.DoesNotExist:
        previous_post = None

    return render(request, 'blog/index.html', {
        'post': post,
        'next_post': next_post,
        'previous_post': previous_post
    })


def about(request):
    return render(request, 'blog/about.html')
