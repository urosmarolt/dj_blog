from django.shortcuts import render, get_object_or_404, render_to_response
#from django.template import RequestContext
from .models import Post, Comment, Review, Game
from django.db.models import Count
from .forms import EmailPostForm, CommentForm, SearchForm
#from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from taggit.models import Tag
from haystack.query import SearchQuerySet
from django.views.generic.base import RedirectView


class ReviewListView(ListView):
    queryset = Review.published.all()
    context_object_name = 'reviews'
    paginate_by = 6
    template_name = 'blog/review/toplist.html'


def review_list(request):
    page = request.GET.get("page")
    reviews = Review.get_review(page)
    return render(request,
                  'blog/review/toplist.html',
                  {'page': page,
                   'reviews': reviews,
                   "meta": reviews.as_meta(request)
                   })

def _get_featured_review():
    return get_object_or_404(Review, featured=True)

def _get_slider_data():
    return Review.published.filter(slider__gt=0).order_by('slider')

class GameListView(ListView):
    queryset = Game.published.all()
    context_object_name = 'games'
    paginate_by = 6
    template_name = 'blog/games/toplist.html'

def _get_game(game_page):
    object_list = Game.published.all()
    paginator = Paginator(object_list, 6)  #
    try:
        games = paginator.page(game_page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        games = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        games = paginator.page(paginator.num_pages)
    return games

def game_list(request):
    page = request.GET.get("page")
    games = _get_game(page)
    return render(request,
                  'blog/games/list.html',
                  {'page': page,
                   'games': games,
                   "meta": games.as_meta(request)
                   })

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all().filter(post_type='post')
    tag = None
    featured_review = _get_featured_review()

    games_page = request.GET.get("game_page")
    games = _get_game(games_page)


    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag,
                   'games': games,
                   'games_page': games_page,
                   'featured_review': featured_review,
                   'slider_reviews': _get_slider_data(),
                   })

def review_detail(request, review):
    review = get_object_or_404(Review, slug=review,
                             status='published')
    return render(request,
                  'blog/review/detail.html',
                  {'review': review})

def game_detail(request, game):
    game = get_object_or_404(Game, slug=game,
                             status='published')
    #
    # reviews_page = request.GET.get("review_page")
    # reviews = _get_review(reviews_page)

    return render(request,
                  'blog/games/detail.html',
                  {'game': game,
                   })


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post)

    # List of active comments for this post
    comments = post.comments.filter(active=True).order_by('-created')

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                   "meta": post.as_meta(request),
                   })

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                          post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

def post_search(request):
    form = SearchForm()
    cd = {}
    results = {}
    total_results = {}
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            #print (form.errors)
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post)\
                          .filter(content=cd['query']).load_all()

            # count total results
            total_results = results.count()
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'cd': cd,
                   'results': results,
                   'total_results': total_results})

class RedirectPlay(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'play_redirect'

    def get_redirect_url(self, review):
        review = get_object_or_404(Review, slug=review)
        return review.tracking_link