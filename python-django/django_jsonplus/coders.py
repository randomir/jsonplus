"""Additional django-specific encoders and decoders."""

import jsonplus


try:
    from djmoney.money import Money as DjangoMoney

    @jsonplus.encoder('DjangoMoney', lambda obj: isinstance(obj, DjangoMoney))
    def _django_money_dumps(obj):
        return jsonplus.getattrs(obj, attrs=['amount', 'currency'])

    @jsonplus.decoder('DjangoMoney')
    def _django_money_loads(val):
        return DjangoMoney(**val)

except:
    pass
