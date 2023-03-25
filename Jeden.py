# 144166703
# 144826098
import requests
from bs4 import BeautifulSoup

errorLoop = "Y"
while errorLoop == "Y":
    product_id = input("Podaj kod produktu:\n")
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"

    # Getting html
    site = requests.get(url)
    errorLoop = ""
    if (not site.status_code == requests.codes.ok):
        print(f"Error {site.status_code}")
        errorLoop = input("Czy chcesz podać inny kod produktu? (Y/N)")

    else:
        soup = BeautifulSoup(site.content, 'html.parser')

        # user-post user-post__card js_product-review
        # user-post js_comment-from-user
        reviews = soup.select('div.js_product-review')
        if (not len(reviews) > 0):
            print("Nie ma opini")
            errorLoop = input("Czy chcesz podać inny kod produktu? (Y/N)")
        else:
            print("Są opinie")
            reviewList = []
            for review in reviews:
                pros = review.select("div.review-feature__title.review-feature__title--positives")[0].parent.contents if len(review.select("div.review-feature__title.review-feature__title--positives")) > 0 else []
                cons = review.select("div.review-feature__title.review-feature__title--negatives")[0].parent.contents if (len(review.select("div.review-feature__title.review-feature__title--negatives")) > 0) else []
                
                
                myReview = {
                    "id": review.get("data-entry-id"),
                    'author': review.select("div.user-post__content > span.user-post__author-name")[0].text,
                    "recomendation": review.select("div.user-post__content > span.user-post__author-recomendation > em")[0].text if len(review.select("div.user-post__content > span.user-post__author-recomendation > em")) > 0 else -1,
                    "stars": review.select("div.user-post__content > span.user-post__score > span.user-post__score-count")[0].text,
                    "trustedReview": True if (len(review.select("div.user-post__info > div.review-pz")) > 0) else False,
                    "date": review.select("div.user-post__content > span.user-post__score > span.user-post__published > time:nth-child(1)")[0].get('datetime'),
                    "purchasedDate": review.select("div.user-post__content > span.user-post__score > span.user-post__published > time:nth-child(2)")[0].get('datetime'),
                    "usefull": review.select("div.user-post__info > div.js_product-review-usefulness.vote > button.vote-yes.js_product-review-vote.js_vote-yes")[0].text,
                    "notUsefull": review.select("div.user-post__info > div.js_product-review-usefulness.vote > button.vote-no.js_product-review-vote.js_vote-no")[0].text,
                    "content": review.select("div.user-post__content > div.user-post__text")[0].text,
                    "prosCount": len(list(filter(lambda pro: pro != "\n", pros))) - 1 if len(pros) > 0 else -1,
                    "consCount": len(list(filter(lambda con: con != "\n", cons))) - 1 if len(cons) > 0 else -1
                }
                print(review)
