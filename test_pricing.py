from datetime import date, timedelta
from unittest.mock import patch

from pricing import calculate_prices
from validation import validate_final_fare


# Fix the pricing date to make tests repeatable.
PRICING_DATE = date(2027, 2, 1)


class FixedDate(date):
    @classmethod
    def today(cls):
        return PRICING_DATE


def make_flight(
    days=10,
    base_fare=300,
    seats_remaining=50,
    capacity=100,
    route_demand=0.5,
    season="Regular",
    is_weekend=False
):
    departure = PRICING_DATE + timedelta(days=days)

    # Match the column order expected by calculate_prices().
    return (
        "TEST01",
        "Montreal",
        "Toronto",
        departure.isoformat(),
        base_fare,
        seats_remaining,
        capacity,
        route_demand,
        season,
        is_weekend
    )


def check_price(name, expected, **inputs):
    flight = make_flight(**inputs)
    result = calculate_prices([flight])

    assert len(result) == 1, "Expected one priced flight"
    assert result[0][:4] == flight[:4], "Flight information changed"

    actual = result[0][4]

    validate_final_fare(actual, min_fare=200, max_fare=800)

    assert abs(actual - expected) < 0.005, (
        f"Expected ${expected:.2f}, got ${actual:.2f}"
    )

    print(
        f"EXPECTED PRICE CONFIRMED: {name} — "
        f"expected ${expected:.2f}, actual ${actual:.2f}"
    )


def run_tests():
    cases = [
        # Normal fare: 300 × 1.18 × 1 × 1 × 1 × 1
        ("Normal flight", 354.00, {}),

        # Time-factor boundaries
        ("Same-day departure", 435.00, {"days": 0}),
        ("1 day before departure", 375.00, {"days": 1}),
        ("7 days before departure", 375.00, {"days": 7}),
        ("8 days before departure", 354.00, {"days": 8}),
        ("14 days before departure", 354.00, {"days": 14}),
        ("15 days before departure", 324.00, {"days": 15}),
        ("30 days before departure", 324.00, {"days": 30}),
        ("31 days before departure", 285.00, {"days": 31}),

        # Demand-factor boundaries
        ("Demand = 0", 318.60, {"route_demand": 0}),
        ("Demand below 0.40", 318.60, {"route_demand": 0.399}),
        ("Demand = 0.40", 354.00, {"route_demand": 0.40}),
        ("Demand = 0.70", 354.00, {"route_demand": 0.70}),
        ("Demand above 0.70", 424.80, {"route_demand": 0.701}),
        ("Demand = 1", 424.80, {"route_demand": 1}),

        # Occupancy-factor boundaries
        ("49% occupancy", 318.60, {"seats_remaining": 51}),
        ("50% occupancy", 354.00, {"seats_remaining": 50}),
        ("79% occupancy", 354.00, {"seats_remaining": 21}),
        ("80% occupancy", 407.10, {"seats_remaining": 20}),
        ("89% occupancy", 407.10, {"seats_remaining": 11}),
        ("90% occupancy", 460.20, {"seats_remaining": 10}),
        ("No seats remaining", 460.20, {"seats_remaining": 0}),
        ("All seats available", 318.60, {"seats_remaining": 100}),

        # Season and weekend adjustments
        ("Vacation season", 407.10, {"season": "Vacation"}),
        ("Weekend flight", 389.40, {"is_weekend": True}),
        ("SQLite weekday value", 354.00, {"is_weekend": 0}),
        ("SQLite weekend value", 389.40, {"is_weekend": 1}),

        # Lower bound: 153.90 becomes 200
        ("Minimum fare applied", 200.00, {
            "base_fare": 200,
            "days": 31,
            "route_demand": 0,
            "seats_remaining": 100
        }),

        # Upper bound: 1716.858 becomes 800
        ("Maximum fare applied", 800.00, {
            "base_fare": 600,
            "days": 0,
            "route_demand": 1,
            "seats_remaining": 0,
            "season": "Vacation",
            "is_weekend": True
        }),

        # Extreme but valid positive base fares
        ("Very low base fare", 200.00, {"base_fare": 1}),
        ("Very high base fare", 800.00, {"base_fare": 10000})
    ]

    successful = 0
    failed = 0

    with patch("pricing.date", FixedDate):
        for name, expected, inputs in cases:
            try:
                check_price(name, expected, **inputs)

            except AssertionError as error:
                failed += 1
                print(f"TEST FAILED: {name} — {error}")

            except Exception as error:
                failed += 1
                print(
                    f"TEST FAILED: {name} — "
                    f"unexpected {type(error).__name__}: {error}"
                )

            else:
                successful += 1

        # Empty results are expected to return an empty list.
        try:
            result = calculate_prices([])
            assert result == [], (
                f"Expected an empty list, got {result!r}"
            )

        except Exception as error:
            failed += 1
            print(
                "TEST FAILED: Empty flight list — "
                f"{type(error).__name__}: {error}"
            )

        else:
            successful += 1
            print(
                "EXPECTED RESULT CONFIRMED: "
                "Empty flight list — returned []"
            )

    total = successful + failed

    print("\nTEST SUMMARY")
    print(f"Checks matching the expected outcome: {successful}/{total}")
    print(f"Failed tests: {failed}")

    assert failed == 0, "Some pricing tests failed"


if __name__ == "__main__":
    run_tests()