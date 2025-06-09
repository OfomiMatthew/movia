from django.shortcuts import render,get_object_or_404,redirect
import requests 
from .models import Movie,Genre,Rating,Review,Likes,Comment
from actor.models import Actor
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from account.models import Profile
from django.contrib import messages
from .forms import RateForm,CommentForm
from django.db.models import Avg
from django.contrib.auth.models import User
from django.db import transaction


def index(request):
    # Check if there's a search query
    query = request.GET.get('q')
    
    # If no query, show landing page
    if not query:
        return render(request, 'landing.html')
    
    # If there's a query, process search
    url = f"http://www.omdbapi.com/?apikey=89553bad&s={query}"
    
    try:
        res = requests.get(url)
        res.raise_for_status()  
        movie_data = res.json()
        
        if movie_data.get('Response') == 'False':
            context = {
                'query': query, 
                'error': movie_data.get('Error', 'No results found')
            }
        else:
            context = {
                'query': query, 
                'movie_data': movie_data,
                'page_number': 1
            }
            
        return render(request, 'home.html', context)
        
    except requests.exceptions.RequestException as e:
        context = {
            'query': query, 
            'error': str(e)
        }
        return render(request, 'home.html', context)



def pagination(request,query,page_number):
    url = "http://www.omdbapi.com/?apikey=89553bad&s=" + query + "&page=" + str(page_number) 
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) +1
    context ={
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number
    }
    return render(request,'home.html',context)



@login_required               
def movieDetails(request, imdb_id):
    try:
        movie_obj = get_object_or_404(Movie,imdbID=imdb_id)
        reviews = Review.objects.filter(movie=movie_obj)
        reviews_avg = reviews.aggregate(Avg('rate'))
        reviews_count = reviews.count()
        our_db = True
    except Movie.DoesNotExist:
        url = f"http://www.omdbapi.com/?apikey=89553bad&i={imdb_id}"
        response = requests.get(url)
        movie_data = response.json()

        rating_objects = []
        genre_objects = []
        actor_objects = []

        actor_list = [x.strip() for x in movie_data.get('Actors', '').split(',')]
        for actor in actor_list:
            if not actor:
                continue
            actor_obj, _ = Actor.objects.get_or_create(name=actor)
            actor_objects.append(actor_obj)

        genre_list = [x.strip() for x in movie_data.get('Genre', '').split(',')]
        for genre in genre_list:
            genre_slug = slugify(genre)
            genre_obj, _ = Genre.objects.get_or_create(title=genre, slug=genre_slug)
            genre_objects.append(genre_obj)

        for rate in movie_data.get('Ratings', []):
            rating_obj, _ = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
            rating_objects.append(rating_obj)

        movie_obj, _ = Movie.objects.get_or_create(
            title=movie_data.get('Title'),
            year=movie_data.get('Year'),
            rated=movie_data.get('Rated'),
            released=movie_data.get('Released'),
            runtime=movie_data.get('Runtime'),
            director=movie_data.get('Director'),
            writer=movie_data.get('Writer'),
            plot=movie_data.get('Plot'),
            language=movie_data.get('Language'),
            country=movie_data.get('Country'),
            awards=movie_data.get('Awards'),
            poster_url=movie_data.get('Poster'),
            metascore=movie_data.get('Metascore'),
            imdbRating=movie_data.get('imdbRating'),
            imdbVotes=movie_data.get('imdbVotes'),
            imdbID=movie_data.get('imdbID'),
            type=movie_data.get('Type'),
            dvd=movie_data.get('DVD'),
            boxOffice=movie_data.get('BoxOffice'),
            production=movie_data.get('Production'),
            website=movie_data.get('Website'),
            totalSeasons=movie_data.get('totalSeasons') if movie_data.get('Type') == 'series' else None,
        )

        movie_obj.genre.set(genre_objects)
        movie_obj.ratings.set(rating_objects)
        movie_obj.actors.set(actor_objects)

        for actor in actor_objects:
            actor.movies.add(movie_obj)
            actor.save()

        movie_obj.save()
        our_db = False

    context = {
        'movie_data': movie_obj,  # now always a Movie model instance
        'our_db': our_db,
        'reviews':reviews,
        'reviews_avg':reviews_avg,
        'reviews_count':reviews_count
    }
    return render(request, 'movie_details.html', context)
      
            
        
def genres(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug) 
    movie_list = Movie.objects.filter(genre=genre)  # Changed variable name to be more accurate
    paginator = Paginator(movie_list, 10)  # Changed to 10 items per page as requested
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'genre.html', {
        'page_obj': page_obj,
        'genre': genre
    })
    
    

def watchlist(request):
    profile = get_object_or_404(Profile, user=request.user)
    movies_to_watch = profile.to_watch.all()
    paginator = Paginator(movies_to_watch, 10)  # Changed to 10 items per page as requested
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist.html', {'movies': movies_to_watch,'page_obj':page_obj})

def watched_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    watched_movies = profile.watched.all()
    return render(request, 'watched.html', {'movies': watched_movies})

def add_movies_to_watch(request, imdb_id):
    movie = get_object_or_404(Movie, imdbID=imdb_id)
    profile = Profile.objects.get(user=request.user)
    profile.to_watch.add(movie)
    messages.success(request, f'"{movie.title}" added to your watchlist!')
    return redirect('movie_details', imdb_id=movie.imdbID)

def add_movies_watched(request, imdb_id):
    movie = get_object_or_404(Movie, imdbID=imdb_id)
    profile = Profile.objects.get(user=request.user)
    
    # Remove from watchlist if it's there
    profile.to_watch.remove(movie)
    profile.watched.add(movie)
    messages.success(request, f'"{movie.title}" added to your watched list!')
    return redirect('movie_details', imdb_id=movie.imdbID)
    
    
def Rate(request, imdb_id):
    user = request.user
    movie = get_object_or_404(Movie,imdbID=imdb_id)
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user 
            rate.movie = movie 
            rate.save()
            return redirect('movie_details', imdb_id=movie.imdbID)
    else:
        form = RateForm()
    return render(request,'rate.html',{'form':form,'movie':movie})



    
@transaction.atomic
def like(request, username, imdb_id):
    try:
        user_liking = request.user
        user_review = get_object_or_404(User, username=username)
        movie = get_object_or_404(Movie, imdbID=imdb_id)
        review = get_object_or_404(Review, user=user_review, movie=movie)
        
        # Check if user already unliked (type_like=1)
        existing_unlike = Likes.objects.filter(user=user_liking, review=review, type_like=1).first()
        
        if existing_unlike:
            # Remove the unlike first
            existing_unlike.delete()
            review.unlikes -= 1
        
        # Check if already liked
        existing_like = Likes.objects.filter(user=user_liking, review=review, type_like=2).first()
        
        if existing_like:
            existing_like.delete()
            review.likes -= 1
            messages.info(request, "Like removed")
        else:
            Likes.objects.create(user=user_liking, review=review, type_like=2)
            review.likes += 1
            messages.success(request, "Review liked!")
        
        review.save()
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    
    return redirect('movie_details', imdb_id=movie.imdbID)

@transaction.atomic
def unlike(request, username, imdb_id):
    try:
        user_unliking = request.user
        user_review = get_object_or_404(User, username=username)
        movie = get_object_or_404(Movie, imdbID=imdb_id)
        review = get_object_or_404(Review, user=user_review, movie=movie)
        
        # Check if user already liked (type_like=2)
        existing_like = Likes.objects.filter(user=user_unliking, review=review, type_like=2).first()
        
        if existing_like:
            # Remove the like first
            existing_like.delete()
            review.likes -= 1
        
        # Check if already unliked
        existing_unlike = Likes.objects.filter(user=user_unliking, review=review, type_like=1).first()
        
        if existing_unlike:
            existing_unlike.delete()
            review.unlikes -= 1
            messages.info(request, "Unlike removed")
        else:
            Likes.objects.create(user=user_unliking, review=review, type_like=1)
            review.unlikes += 1
            messages.warning(request, "Review unliked")
        
        review.save()
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    
    return redirect('movie_details', imdb_id=movie.imdbID)  





def add_comment(request, username, imdb_id):
    # Get the review being commented on
    review_user = get_object_or_404(User, username=username)
    movie = get_object_or_404(Movie, imdbID=imdb_id)
    review = get_object_or_404(Review, user=review_user, movie=movie)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('movie_details', imdb_id=imdb_id)
    
    return redirect('movie_details', imdb_id=imdb_id)


# def add_comment(request, imdb_id):
#     if request.method == 'POST':
#         review_id = request.POST.get('review_id')
#         body = request.POST.get('body')
        
#         try:
#             review = Review.objects.get(id=review_id, movie__imdbID=imdb_id)
#             Comment.objects.create(
#                 review=review,
#                 user=request.user,
#                 body=body
#             )
#             messages.success(request, 'Comment added successfully!')
#         except Review.DoesNotExist:
#             messages.error(request, 'Review not found')
            
#     return redirect('movie_detail', imdb_id=imdb_id)
            