def calculate_credit_score(features):
    score = 300  # base score

    if features["total_credit"] > 2000:
        score += 100

    if features["cashflow_stability"] > 1:
        score += 100

    if features["avg_ticket_size"] > 300:
        score += 100

    if features["outflow_count"] > features["inflow_count"]:
        score -= 50

    score = max(300, min(score, 900))
    return score


def risk_category(score):
    if score >= 750:
        return "Low Risk"
    elif score >= 600:
        return "Medium Risk"
    else:
        return "High Risk"