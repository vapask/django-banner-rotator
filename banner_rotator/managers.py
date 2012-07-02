#-*- coding:utf-8 -*-

from datetime import datetime
from decimal import Decimal
from random import random

from django.db import models


def pick(bias_list):
    """
    Takes a list similar to [(item1, item1_weight), (item2, item2_weight),]
        and item(n)_weight as the probability when calculating an item to choose
    """

    # Django ORM returns floats as Decimals,
    #   so we'll convert floats to decimals here to co-operate
    number = Decimal("%.18f" % random())
    current = Decimal(0)

    # With help from
    #   @link http://fr.w3support.net/index.php?db=so&id=479236
    for choice, bias in bias_list:
        current += bias
        if number <= current:
            return choice


class BannerManager(models.Manager):
    def biased_choice(self, place):
        now = datetime.now()

        # проверка условий:
        # - активен и находится привязан к нужному месту
        # - если задано время начало показа баннера
        # - если задано время окончания показа баннера
        # - если задано ограничение на количество показов
        # - если задано ограничение на количество кликов
        queryset = self.filter(is_active=True, places=place).\
                    filter(models.Q(start_at__isnull=True) | models.Q(start_at__lte=now)).\
                    filter(models.Q(finish_at__isnull=True) | models.Q(finish_at__gte=now)).\
                    filter(models.Q(max_views=0) | models.Q(max_views__gt=models.F('views'))).\
                    filter(models.Q(max_clicks=0) | models.Q(max_clicks__gt=models.F('clicks')))

        if not queryset.count():
            raise self.model.DoesNotExist

        calculations = queryset.aggregate(weight_sum=models.Sum('weight'))

        banners = queryset.extra(select={'bias': 'weight/%f' % calculations['weight_sum']})

        return pick([(b, b.bias) for b in banners])
