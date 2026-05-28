"""Self-created dummy snippets used by the prototype."""

SAMPLE_SNIPPETS = {
    "Python pricing calculation": {
        "language": "Python",
        "code": '''def calculate_price(distance, minutes, city):
    price = 5
    if city == "dubai":
        price = price + distance * 2.7
    else:
        price = price + distance * 2.2

    if minutes > 30:
        price = price + 12

    if distance > 25:
        price = price + 18

    return round(price, 2)
''',
    },
    "Python user registration": {
        "language": "Python",
        "code": '''def register_user(name, email, password):
    user = {}
    user["name"] = name
    user["email"] = email
    user["password"] = password
    user["status"] = "active"
    send_welcome_email(email)
    return user
''',
    },
    "JavaScript API fetch": {
        "language": "JavaScript",
        "code": """async function loadTrips(userId) {
  const response = await fetch('/api/trips?user=' + userId);
  const data = await response.json();
  return data.items.map(item => ({
    id: item.id,
    city: item.city,
    price: item.total
  }));
}
""",
    },
    "SQL broad trip query": {
        "language": "SQL",
        "code": """SELECT *
FROM trips t
JOIN users u ON u.id = t.user_id
ORDER BY t.created_at DESC;
""",
    },
    "Java service method": {
        "language": "Java",
        "code": """public Receipt completeRide(Ride ride, User user, PaymentCard card) {
    if (ride == null) {
        throw new IllegalArgumentException("ride missing");
    }
    if (user == null) {
        throw new IllegalArgumentException("user missing");
    }
    double total = 5.0;
    if (ride.getDistanceKm() > 20) {
        total += 15.0;
    }
    if ("AIRPORT".equals(ride.getPickupType())) {
        total += 25.0;
    }
    paymentGateway.charge(card, total);
    notificationService.sendReceipt(user.getEmail(), total);
    analytics.track("ride_completed", user.getId());
    return new Receipt(ride.getId(), total, "PAID");
}
""",
    },
}


def get_sample_names(language: str | None = None) -> list[str]:
    if language is None:
        return list(SAMPLE_SNIPPETS.keys())
    return [name for name, sample in SAMPLE_SNIPPETS.items() if sample["language"] == language]


def get_sample_code(sample_name: str) -> str:
    return SAMPLE_SNIPPETS[sample_name]["code"]
