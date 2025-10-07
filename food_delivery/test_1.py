from datetime import datetime, timedelta
from food_delivery.models.order import Order
from food_delivery.models.address import Address
from food_delivery.models.geo_point import GeoPoint

now = datetime.now()
o = Order(
    "o1", "r1", [], Address("x", GeoPoint(0, 0)), "Placed", now + timedelta(minutes=45)
)
ok = o.can_dispatch(timedelta(minutes=30))
late = o.can_dispatch(timedelta(minutes=60))

assert ok is True and late is False
