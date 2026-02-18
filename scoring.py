def calculate_credit_score(features):
    score = 300  # base

    # Total credit volume (max +150)
    if features["total_credit"] > 10000:
        score += 150
    elif features["total_credit"] > 5000:
        score += 120
    elif features["total_credit"] > 2000:
        score += 70

    # Cashflow stability — inflows vs outflows (max +150)
    stability = features["cashflow_stability"]
    if stability >= 1.5:
        score += 150
    elif stability >= 1.0:
        score += 120
    elif stability >= 0.8:
        score += 60

    # Average ticket size — business health (max +150)
    avg = features["avg_ticket_size"]
    if avg > 800:
        score += 150
    elif avg > 400:
        score += 100
    elif avg > 200:
        score += 60

    # Inflow count — transaction frequency (max +80)
    inflow = features["inflow_count"]
    if inflow >= 8:
        score += 80
    elif inflow >= 5:
        score += 50
    elif inflow >= 3:
        score += 25

    # Penalty: more outflows than inflows
    if features["outflow_count"] > features["inflow_count"]:
        score -= 100

    # Penalty: very low credit
    if features["total_credit"] < 500:
        score -= 60

    score = max(300, min(score, 900))
    return score


def risk_category(score):
    if score >= 720:
        return "Low Risk"
    elif score >= 580:
        return "Moderate Risk"
    else:
        return "High Risk"
