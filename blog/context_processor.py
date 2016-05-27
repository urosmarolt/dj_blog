from blog .models import  Review


def insert_reviews(request):
    reviews_page = request.GET.get("review_page", 0)
    reviews = Review.get_review(reviews_page)
    return {"reviews": reviews, "reviews_page": reviews_page}
