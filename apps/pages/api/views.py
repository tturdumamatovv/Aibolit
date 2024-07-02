from rest_framework import generics
from rest_framework.response import Response

from apps.pages.api.serializers import (
    StaticPageSerializer,
    BannerSerializer,
    PartnerSerializer,
    DiscountInfoSerializer
)
from apps.pages.models import (
    StaticPage,
    Banner,
    Partner,
    DiscountInfo
)


class StaticPageDetailView(generics.RetrieveAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        instance = None

        try:
            instance = StaticPage.objects.get(slug=slug)
        except StaticPage.DoesNotExist:
            if slug == 'about-us':
                instance = StaticPage.objects.create(
                    title='',


                    content='',

                    slug="about-us"
                )

        return instance

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class PartnerListView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class DiscountInfoView(generics.RetrieveAPIView):
    queryset = DiscountInfo.objects.all()
    serializer_class = DiscountInfoSerializer

    def get_object(self):
        return self.queryset.first()
