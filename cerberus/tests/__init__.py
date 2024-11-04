from decimal import Decimal
from random import randint

from model_bakery import baker

baker.generators.add("djmoney.models.fields.MoneyField", lambda: Decimal(randint(100, 9999) / 100))
baker.generators.add("django_sqids.field.SqidsField", lambda: None)
baker.generators.add("cerberus.fields.SqidsModelField", lambda: None)
