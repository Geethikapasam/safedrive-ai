import random

#  Updated speed range (0–180)
speeds = list(range(0, 181, 10))
weather_list = ["clear", "rain"]
time_list = ["day", "night"]

actions = ["slow_down", "maintain", "speed_up"]

Q = {}

learning_rate = 0.1
discount_factor = 0.9

#  Reward function
def get_reward(speed, weather, time):
    if speed >= 120:
        return -100
    elif speed > 80 and weather == "rain":
        return -80
    elif speed > 60 and time == "night":
        return -50
    elif speed <= 60 and weather == "clear":
        return 30
    else:
        return 10

#  Training
for episode in range(5000):
    speed = random.choice(speeds)
    w = random.choice(weather_list)
    t = random.choice(time_list)

    state = (speed, w, t)

    if state not in Q:
        Q[state] = {a: 0 for a in actions}

    action = random.choice(actions)
    reward = get_reward(speed, w, t)

    next_max = max(Q[state].values())

    Q[state][action] = Q[state][action] + learning_rate * (
        reward + discount_factor * next_max - Q[state][action]
    )

#  Decision logic
def get_best_action(state):
    speed, weather, time = state

    #  Strong rules
    if speed >= 120:
        return "slow_down"
    elif speed > 80 and weather == "rain":
        return "slow_down"
    elif speed > 60 and time == "night":
        return "slow_down"
    elif speed <= 60 and weather == "clear":
        return "speed_up"

    #  RL fallback
    if state in Q:
        return max(Q[state], key=Q[state].get)

    return "maintain"

#  Risk calculation
def get_risk_score(speed, weather, time, zone):
    risk = 0

    #  Speed risk (STRONG)
    if speed >= 120:
        risk += 60
    elif speed >= 100:
        risk += 50
    elif speed >= 80:
        risk += 35
    elif speed >= 60:
        risk += 20
    else:
        risk += 10

    #  Weather
    if weather == "rain":
        risk += 25

    #  Time
    if time == "night":
        risk += 15

    #  Zone
    if zone == "accident_prone":
        risk += 20

    return min(risk, 100)