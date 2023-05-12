# 144166703
# 144826098
# 58835954
import requests
from bs4 import BeautifulSoup
import json
import os.path


def getFromSelector(ancestor, selector=None, attribute=None, return_list=False):
    try:
        if return_list:
            return [tag.get_text().strip() for tag in ancestor.select(selector)]
        if not selector and attribute:
            return ancestor[attribute].strip()
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None


mySelectors = {
    "opinion_id": (None, "data-entry-id"),
    "author": ("span.user-post__author-name",),
    "recommendation": ("span.user-post__author-recomendation > em",),
    "stars": ("span.user-post__score-count",),
    "purchased": ("div.review-pz",),
    "opinion_date": ("span.user-post__published > time:nth-child(1)", "datetime"),
    "purchase_date": ("span.user-post__published > time:nth-child(2)", "datetime"),
    "usefull_count": ("button.vote-yes", "data-total-vote"),
    "unusefull_count": ("button.vote-no", "data-total-vote"),
    "content": ("div.user-post__text",),
    "pros": ("div.review-feature__title--positives ~ div.review-feature__item", None, True),
    "cons": ("div.review-feature__title--negatives ~ div.review-feature__item", None, True)
}

errorLoop = "Y"
while errorLoop == "Y":
    errorLoop = ""

    # product_id = input("Podaj kod produktu:\n")
    product_id = 58835954
    nrStrony = 1
    nextStrona = True

    reviewList = []
    while nextStrona:
        # Getting html
        url = f"https://www.ceneo.pl/{product_id}/opinie-{nrStrony}"
        site = requests.get(url)
        if (not site.status_code == requests.codes.ok):
            print(f"Error {site.status_code}")
            errorLoop = input("Czy chcesz podać inny kod produktu? (Y/N)")

        else:
            soup = BeautifulSoup(site.content, 'html.parser')

            reviews = soup.select('div.js_product-review')
            if (not len(reviews) > 0):
                print("Nie ma opini")
                errorLoop = input("Czy chcesz podać inny kod produktu? (Y/N)")
            else:
                for review in reviews:
                    myReview = {}
                    for key, value in mySelectors.items():
                        myReview[key] = getFromSelector(review, *value)
                    reviewList.append(myReview)
        nextStrona = True if len(soup.select(
            'a.pagination__next')) > 0 else False
        nrStrony += 1

    json_object = json.dumps(reviewList, indent=4, ensure_ascii=False)
    if (not os.path.exists('Opinions')):
        os.mkdir('Opinions')
    with open(f"Opinions/{product_id}.json", "w", encoding='utf-8') as outfile:
        outfile.write(json_object)
