def generate_recommendation(features, difficulty):

    recommendations = []

    if difficulty > 0.8:
        recommendations.append("Reduce enemy count")

    if difficulty > 0.6:
        recommendations.append("Add more checkpoints")

    if difficulty < 0.3:
        recommendations.append("Increase enemy count")

    if difficulty < 0.4:
        recommendations.append("Reduce rewards")

    return recommendations