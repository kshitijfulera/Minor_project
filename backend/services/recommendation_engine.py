def generate_recommendation(features, difficulty):

    recommendations = []

    if difficulty > 0.8:
        recommendations.append("Reduce enemy count significantly")
        recommendations.append("Increase checkpoints")

    elif difficulty > 0.6:
        recommendations.append("Add more checkpoints")
        recommendations.append("Reduce enemy density slightly")

    elif difficulty >= 0.4:
        recommendations.append("Level is balanced, consider minor tweaks")

    elif difficulty > 0.2:
        recommendations.append("Increase enemy count slightly")
        recommendations.append("Reduce rewards")

    else:
        recommendations.append("Increase difficulty: add enemies and reduce checkpoints")

    return recommendations