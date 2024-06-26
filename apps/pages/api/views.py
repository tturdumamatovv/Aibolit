from rest_framework import generics
from rest_framework.response import Response

from apps.pages.api.serializers import StaticPageSerializer
from apps.pages.models import StaticPage


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

