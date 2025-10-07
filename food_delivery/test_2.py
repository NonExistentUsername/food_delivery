from datetime import datetime, timedelta
from food_delivery.models.order import Order
from food_delivery.models.address import Address
from food_delivery.models.geo_point import GeoPoint
from food_delivery.services.dispatch_service import DispatchService
from food_delivery.services.event_bus import SimpleEventBus
from food_delivery.repositories.order_repository import InMemoryOrderRepository
from food_delivery.repositories.courier_repository import InMemoryCourierRepository
from food_delivery.services.route_estimator import RouteEstimator
from food_delivery.models.courier import Courier
from food_delivery.models.service_area import ServiceArea

o = Order(
    "o1",
    "r1",
    [],
    Address("x", GeoPoint(0, 0)),
    "Placed",
    datetime.now() + timedelta(minutes=45),
)
bus = SimpleEventBus()
order_repo = InMemoryOrderRepository()
courier_repo = InMemoryCourierRepository()
routes = RouteEstimator()
svc = DispatchService(order_repo, courier_repo, routes, bus)

order_repo.save(o)
courier_repo.save(Courier("c1", GeoPoint(0, 0), "Available"))

assert ServiceArea(99, center=GeoPoint(0, 0)).contains(GeoPoint(0, 0)) is True

svc.assign_best_courier("o1", ServiceArea(99, center=GeoPoint(0, 0)))

assert (
    o.state == "Dispatched"
    and type(bus.published_events[0]).__name__ == "CourierAssigned"
)
