from django.db.models import Q

from apps.flowers.models import Flower


def get_distinct_product_attributes():
    distinct_plantation = set()
    distinct_head_outer_diameter = set()
    distinct_volume = set()
    distinct_stem_height = set()

    flowers = Flower.objects.all()

    for flower in flowers:
        if flower.plantation:
            distinct_plantation.add(flower.plantation)
        if flower.head_outer_diameter:
            distinct_head_outer_diameter.add(flower.head_outer_diameter)
        if flower.volume:
            distinct_volume.add(flower.volume)
        if flower.stem_height:
            distinct_stem_height.add(flower.stem_height)

    return {
        'plantation': list(distinct_plantation),
        'head_outer_diameter': list(distinct_head_outer_diameter),
        'volume': list(distinct_volume),
        'stem_height': list(distinct_stem_height),
    }