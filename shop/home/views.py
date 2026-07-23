from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Comment, Status
from .forms import CommentReplyForm, CommentCreateForm, ProductSearchForm
from django.contrib import messages


class HomeView(View):
    form_class = ProductSearchForm

    def get(self, request):
        products = Product.objects.filter(available=True)
        search_query = request.GET.get('search')

        if search_query is not None and search_query.strip() == '':
            products = Product.objects.none()

        elif search_query:
            products = products.filter(name__contains=search_query)

        return render(request, 'home/home.html', {
            'products': products,
            'search_query': search_query, })


class ProductDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(
            Product, pk=kwargs['product_id'], slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.product_instance.pcomments.filter(
            is_reply=False, status=Status.APPROVED)
        return render(request, "home/detail.html", {
            "product": self.product_instance,
            "comments": comments,
            "form": self.form_class,
            "reply_form": self.form_class_reply
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            new_comment = form.save(commit=False)
            new_comment.Status = Status.PENDING
            new_comment.user = request.user
            new_comment.product = self.product_instance
            new_comment.save()
            messages.success(
                request, "کامنت شما با موفقیت ارسال شد و در حال بررسی می باشد.", "success")
            return redirect("home:product_detail", self.product_instance.id, self.product_instance.slug)

        comments = self.product_instance.pcomments.filter(
            is_reply=False, status=Status.APPROVED)

        messages.error(request, "فرم نامعتبر است", "danger")
        return render(request, "home/detail.html", {
            "product": self.product_instance,
            "comments": comments,
            "form": form,
            "form_reply": self.form_class_reply()
        })


class ProductAddReplyView(View):
    form_class = CommentReplyForm

    def post(self, request, product_id, comment_id):
        product = get_object_or_404(Product, id=product_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.Status = Status.PENDING
            reply.user = request.user
            reply.product = product
            reply.reply = comment
            reply.is_reply = True
            reply.save()

            messages.success(
                request, "کامنت شما با موفقیت ارسال شد و در حال بررسی است", "success")

        return redirect("home:product_detail", product.id, product.slug)


# Create your views here.
