import psycopg2
from settings import connection_string, screenshot_interval, start_time, end_time

start, end = (start_time, end_time)


def get_timings():
    conn = psycopg2.connect(host=connection_string['host'],
                            database=connection_string['database'],
                            user=connection_string['user'],
                            password=connection_string['password'])

    cur = conn.cursor()

    query = """
                SELECT * 
                FROM screenshots
                WHERE screen_time >= %s AND screen_time <= %s
                ORDER BY screen_time;
            """

    cur.execute(query, (start, end))

    screenshot_timings = cur.fetchall()

    cur.close()
    conn.close()

    return screenshot_timings


timings = get_timings()
print('TIMINGS: ', timings)


def get_unique_users(timings):
    users_set = set()
    for user_id, _ in timings:
        users_set.add(user_id)
    return list(users_set)


print(get_unique_users(timings))


def generate_group_name(i):
    return f"group_{i}"


def analyse_groups(timings):
    groups = {}
    current_group = []
    group_index = 1

    for i in range(len(timings)):
        current_time = timings[i][1]

        if i == 0 or current_time - timings[i - 1][1] > screenshot_interval:
            # Начинаем новую группу
            group_name = generate_group_name(group_index)
            groups[group_name] = {}
            current_group = groups[group_name]
            group_index += 1

        user_id, time = timings[i]
        current_group[user_id] = time

    return groups


groups = analyse_groups(timings)
print(groups)


def calculate_delays(groups):
    delays = {}
    for group_name, group_data in groups.items():
        delays[group_name] = {}
        first_user, first_time = next(iter(group_data.items()))

        if len(group_data) > 1:
            for user, time in group_data.items():
                delay = time - first_time
                delays[group_name][user] = delay

    return delays


delays = calculate_delays(groups)
print(delays)
