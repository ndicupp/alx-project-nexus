from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

pagination_class = ProductPagination


/api/products/?search=phone&min_price=100&ordering=price
/api/products/?category=electronics&page=2&page_size=5

git add .
git commit -m "feat: implement advanced product filtering, search, ordering, and pagination"
git push
