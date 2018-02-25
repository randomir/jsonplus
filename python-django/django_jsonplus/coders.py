"""Additional django-specific encoders and decoders."""

import jsonplus


try:
    from djmoney.money import Money as DjangoMoney
    
    # TODO: add to jsonplus a way to hook encoder/decoder with a priority
    # TODO: add to jsonplus unregister function
    # NOTE: the line below is an abomination; used for test/prototype only
    del jsonplus._encode_handlers['exact']['classname']['Money']
    
    @jsonplus.encoder('DjangoMoney', lambda obj: isinstance(obj, DjangoMoney))
    def _django_money_dumps(obj):
        return jsonplus.getattrs(obj, attrs=['amount', 'currency'])
    
    @jsonplus.decoder('DjangoMoney')
    def _django_money_loads(val):
        return DjangoMoney(**val)

except:
    pass
