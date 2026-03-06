def implied_probability(odds):

    return round(1 / odds, 4)


def calculate_value_edge(model_prob, odds):

    market_prob = implied_probability(odds)

    value_edge = model_prob - market_prob

    return round(value_edge * 100, 2)

def generate_signal(ai_prob, odds):

    value = calculate_value_edge(ai_prob, odds)

    confidence = ai_prob * 100

    if confidence > 65 and value > 15:

        return {
            "signal": "HIGH",
            "confidence": round(confidence,2),
            "value_edge": value
        }

    elif confidence > 55:

        return {
            "signal": "MEDIUM",
            "confidence": round(confidence,2),
            "value_edge": value
        }

    return {
        "signal": "LOW",
        "confidence": round(confidence,2),
        "value_edge": value
    }
    
def is_good_signal(confidence, value_edge):

    if confidence > 65 and value_edge > 15:
        return True

    return False