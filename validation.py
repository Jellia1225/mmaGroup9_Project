import math
from datetime import date


# ============================================================
# 1. FLIGHT INPUT VALIDATION
# ============================================================

def validate_flight(
    flight_id,
    origin,
    destination,
    departure_date,
    base_fare,
    seats_remaining,
    capacity,
    route_demand,
    season,
    is_weekend,
    pricing_date
):
    # Flight ID and route
    for name, value in [
        ("flight_id", flight_id),
        ("origin", origin),
        ("destination", destination)
    ]:
        assert isinstance(value, str), f"{name} must be a string"
        assert value.strip() != "", f"{name} cannot be empty"

    assert origin.strip().lower() != destination.strip().lower(), (
        "Origin and destination must be different"
    )

    # Dates: accept date objects or YYYY-MM-DD strings
    if isinstance(departure_date, str):
        try:
            departure_date = date.fromisoformat(departure_date)
        except ValueError:
            raise AssertionError(
                "Departure date must be a valid YYYY-MM-DD date"
            ) from None

    assert type(departure_date) is date, (
        "Departure date must be a date or YYYY-MM-DD string"
    )
    assert type(pricing_date) is date, "Pricing date must be a date"

    assert departure_date >= pricing_date, (
        "Departure date cannot be before the pricing date"
    )

    # Capacity and seats
    assert type(capacity) is int, "Capacity must be an integer"
    assert capacity > 0, "Capacity must be greater than 0"

    assert type(seats_remaining) is int, (
        "Seats remaining must be an integer"
    )
    assert 0 <= seats_remaining <= capacity, (
        "Seats remaining must be between 0 and capacity"
    )

    # Base fare
    assert type(base_fare) in (int, float), (
        "Base fare must be numeric"
    )
    assert math.isfinite(base_fare), "Base fare must be finite"
    assert base_fare > 0, "Base fare must be greater than 0"

    # Route demand
    assert type(route_demand) in (int, float), (
        "Route demand must be numeric"
    )
    assert math.isfinite(route_demand), (
        "Route demand must be finite"
    )
    assert 0 <= route_demand <= 1, (
        "Route demand must be between 0 and 1"
    )

    # Season and weekend
    assert season in ("Regular", "Vacation"), (
        "Season must be Regular or Vacation"
    )
    assert type(is_weekend) is bool, (
        "is_weekend must be True or False"
    )


# ============================================================
# 2. FINAL FARE VALIDATION
# ============================================================

def validate_final_fare(final_fare, min_fare=200, max_fare=800):
    for name, value in [
        ("Minimum fare", min_fare),
        ("Maximum fare", max_fare),
        ("Final fare", final_fare)
    ]:
        assert type(value) in (int, float), (
            f"{name} must be numeric"
        )
        assert math.isfinite(value), f"{name} must be finite"

    assert 0 < min_fare <= max_fare, "Invalid fare bounds"

    assert min_fare <= final_fare <= max_fare, (
        f"Final fare must be between ${min_fare} and ${max_fare}"
    )


# ============================================================
# 3. BOOKING INPUT VALIDATION
# ============================================================

def validate_booking(ticket_number, seats_remaining):
    assert type(seats_remaining) is int, (
        "Seats remaining must be an integer"
    )
    assert seats_remaining >= 0, (
        "Seats remaining cannot be negative"
    )

    assert type(ticket_number) is int, (
        "Ticket number must be an integer"
    )
    assert ticket_number > 0, (
        "Ticket number must be greater than 0"
    )
    assert ticket_number <= seats_remaining, (
        "Not enough seats available"
    )


# ============================================================
# 4. TEST HELPER
# ============================================================

def check_case(name, function, arguments, should_pass):
    """
    Return True when the result matches the expectation.

    Valid input should be accepted.
    Invalid input should raise an AssertionError.
    """
    try:
        function(**arguments)

    except AssertionError as error:
        if should_pass:
            print(
                f"TEST FAILED: {name} — "
                f"valid input was rejected: {error}"
            )
            return False

        print(f"EXPECTED ERROR CAUGHT: {name} — {error}")
        return True

    except Exception as error:
        # An unexpected crash does not count as successful validation.
        print(
            f"TEST FAILED: {name} — "
            f"unexpected {type(error).__name__}: {error}"
        )
        return False

    else:
        if should_pass:
            print(f"VALID INPUT ACCEPTED: {name}")
            return True

        print(
            f"TEST FAILED: {name} — "
            "invalid input was accepted"
        )
        return False


# ============================================================
# 5. VALIDATION TESTS AND EDGE-CASE DEMONSTRATION
# ============================================================

if __name__ == "__main__":
    # Fixed dates make the tests repeatable.
    normal_flight = {
        "flight_id": "TEST01",
        "origin": "Montreal",
        "destination": "Toronto",
        "departure_date": "2027-02-15",
        "base_fare": 300.0,
        "seats_remaining": 50,
        "capacity": 100,
        "route_demand": 0.5,
        "season": "Regular",
        "is_weekend": False,
        "pricing_date": date(2027, 2, 1)
    }

    results = []

    # True means the input should be accepted.
    # False means an assertion error should be caught.
    flight_cases = [
        ("Normal flight", {}, True),
        ("Zero remaining seats", {"seats_remaining": 0}, True),
        ("All seats available", {"seats_remaining": 100}, True),
        ("Minimum demand", {"route_demand": 0}, True),
        ("Maximum demand", {"route_demand": 1}, True),
        (
            "Same-day departure",
            {"departure_date": "2027-02-01"},
            True
        ),

        ("Zero capacity", {"capacity": 0}, False),
        ("Negative capacity", {"capacity": -100}, False),
        ("Decimal capacity", {"capacity": 100.5}, False),
        ("Negative seats", {"seats_remaining": -1}, False),
        ("Seats exceed capacity", {"seats_remaining": 101}, False),
        ("Decimal seats", {"seats_remaining": 1.5}, False),

        ("Zero base fare", {"base_fare": 0}, False),
        ("Negative base fare", {"base_fare": -100}, False),
        (
            "Infinite base fare",
            {"base_fare": float("inf")},
            False
        ),
        ("Missing base fare", {"base_fare": None}, False),
        ("NaN base fare", {"base_fare": float("nan")}, False),

        ("Demand below zero", {"route_demand": -0.01}, False),
        ("Demand above one", {"route_demand": 1.01}, False),
        ("Invalid season", {"season": "Unknown"}, False),
        (
            "Weekend stored as text",
            {"is_weekend": "False"},
            False
        ),
        ("Empty flight ID", {"flight_id": ""}, False),
        ("Identical cities", {"destination": "Montreal"}, False),
        (
            "Invalid date",
            {"departure_date": "2027-02-30"},
            False
        ),
        (
            "Past departure",
            {"departure_date": "2027-01-31"},
            False
        )
    ]

    print("\nFLIGHT INPUT CHECKS")

    for name, changes, should_pass in flight_cases:
        test_flight = normal_flight.copy()
        test_flight.update(changes)

        results.append(
            check_case(
                name,
                validate_flight,
                test_flight,
                should_pass
            )
        )

    print("\nFINAL FARE CHECKS")

    for value, should_pass in [
        (200, True),
        (500, True),
        (800, True),
        (199.99, False),
        (800.01, False),
        (float("inf"), False),
        (float("nan"), False)
    ]:
        results.append(
            check_case(
                f"Final fare: {value}",
                validate_final_fare,
                {"final_fare": value},
                should_pass
            )
        )

    print("\nBOOKING INPUT CHECKS")

    for name, tickets, seats, should_pass in [
        ("Normal booking", 1, 5, True),
        ("Book all remaining seats", 5, 5, True),
        ("Zero tickets", 0, 5, False),
        ("Negative tickets", -1, 5, False),
        ("Decimal tickets", 1.5, 5, False),
        ("Tickets exceed availability", 6, 5, False),
        ("Sold-out flight", 1, 0, False)
    ]:
        results.append(
            check_case(
                name,
                validate_booking,
                {
                    "ticket_number": tickets,
                    "seats_remaining": seats
                },
                should_pass
            )
        )

    successful = sum(results)
    total = len(results)
    failed = total - successful

    print("\nTEST SUMMARY")
    print(f"Checks matching the expected outcome: {successful}/{total}")
    print(f"Failed tests: {failed}")

    assert all(results), "Some validation tests failed"