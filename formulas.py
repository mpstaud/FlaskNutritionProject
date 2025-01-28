

def basal_metabolic_rate(height, weight, age, sex):
    if sex == 'male':
        return 66 + (6.23 * weight) + (12.7 * height) - (6.8 * age)
    elif sex == 'female':
        return 655 + (4.35 * weight) + (4.7 * weight) - (4.7 * age)

def harris_benedict_calculation(activity_level, bmr):
    # calculates recommended caloric intake using the harris benedict equation
    if activity_level == 'inactive':
        return int(bmr * 1.2)
    elif activity_level == 'somewhat_active':
        return int(bmr * 1.375)
    elif activity_level == 'active':
        return int(bmr * 1.55)
    elif activity_level == 'athlete':
        return int(bmr * 1.725)
    else:
        return print("error: enter a valid return type")
