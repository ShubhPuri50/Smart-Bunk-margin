def classify_risk(current, required):
    if current < required:
        return "BELOW TARGET"
    if current < required + 5:
        return "WATCH"
    return "SAFE"


risk_label = classify_risk
