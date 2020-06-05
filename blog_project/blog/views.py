from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail
from blog.forms import EmailShareForm,CommentForm,SignUp
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect



# Create your views here.


def post_list_view(request,tag_slug = None):

    post_list = Post.objects.filter(status='published')

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag,slug = tag_slug)
        post_list = Post.objects.filter(status='published',tags__in=[tag])



    paginator = Paginator(post_list,4)

    page_number=request.GET.get('page')

    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)


    form=SignUp()
    if request.method=='POST':
        form=SignUp(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


    return render(request,'blog/post_list.html',context = {'post_list':post_list,'tag':tag,'share_form':form })


@login_required
def post_detail_view(request,year,post,pk):
    post = get_object_or_404(Post,
                            slug=post,
                            status='published',
                            publish__year=year,
                            id = pk)

    comment_submit = False
    email_sent = False
    comment_form = CommentForm()

    if (request.method == 'POST'):
        if request.POST.get('share','') == 'share':
            form = EmailShareForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                subject = 'Read, {}'.format(post.title)
                post_url = request.build_absolute_uri(post.get_absolute_url())
                message = 'Hi {},\nPlease Read Post At :\n{}\nRegards,\nMorty Smith'.format(data['name'],post_url)
                send_mail(subject,message,'blog@rickandmorty.com',[data['to']])
                email_sent = True

        elif request.POST.get('comment','') == 'comment':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.name = request.user.get_full_name()
                new_comment.save(True)
                comment_submit = True



    form = EmailShareForm()
    comments = post.comments.filter(active=True)
    context_dict = {'post':post,
                    'form':form,
                    'comment_form':comment_form,
                    'comment_submit':comment_submit,
                    'comments':comments,
                    'email_sent':email_sent}



    return render(request,'blog/post_detail.html',context_dict)
