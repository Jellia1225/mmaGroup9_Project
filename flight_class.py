# Creating Flight Class
class Flight:

    def __init__(
        self,
        flight_id,
        origin,
        destination,
        departure_date,
        base_fare,
        seats_remaining,
        capacity,
        route_demand,
        season,
        is_weekend
    ):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.base_fare = float(base_fare)
        self.seats_remaining = int(seats_remaining)
        self.capacity = int(capacity)
        self.route_demand = float(route_demand)
        self.season = season
        self.is_weekend = is_weekend