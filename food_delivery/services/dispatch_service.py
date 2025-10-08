from datetime import datetime
from food_delivery.repositories.order_repository import OrderRepository
from food_delivery.repositories.courier_repository import CourierRepository
from food_delivery.services.event_bus import EventBus
from food_delivery.services.route_estimator import RouteEstimator
from food_delivery.models.service_area import ServiceArea
from datetime import timedelta


class DispatchService:
    def __init__(
        self,
        orders: OrderRepository,
        couriers: CourierRepository,
        route_estimator: RouteEstimator,
        bus: EventBus,
    ):
        self.orders, self.couriers, self.route_estimator, self.bus = (
            orders,
            couriers,
            route_estimator,
            bus,
        )

    def assign_best_courier(self, order_id: str, service_area: ServiceArea) -> None:
        order = self.orders.get(order_id)
        candidates = self.couriers.find_available_in_area(service_area)

        assert candidates, "No available couriers"

        # Choose best by ETA to restaurant
        best = min(
            candidates,
            key=lambda c: self.route_estimator.estimate_eta(
                c.location, service_area.restaurant_location
            ),
        )
        # Eta from courier to restaurant + restaurant to customer
        eta = (
            self.route_estimator.estimate_eta(
                best.location, service_area.restaurant_location
            )
            + self.route_estimator.estimate_eta(
                service_area.restaurant_location, order.address.geo
            )
            + timedelta(minutes=2)
        )  # 2 min buffer for pickup

        assert order.can_dispatch(eta), "Would miss SLA"

        best.take_order(order.id, eta)

        evt = order.dispatch(courier_id=best.id)

        self.orders.save(order)
        self.bus.publish(evt)
