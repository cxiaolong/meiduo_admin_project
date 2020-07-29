from haystack import indexes

from goods.models import SKU


class SKUIndex(indexes.Indexable, indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return SKU

    def index_queryset(self, using=None):
        '''指定查询集'''
        return self.get_model().objects.filter(is_launched=True)