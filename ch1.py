#! /usr/bin/env python
# -*- coding: utf-8 -*-


from collections import Counter, defaultdict


# What's the average number of connections?
def number_of_friends(user: dict, friendships: dict) -> int:
    """How many friends does user have?"""
    user_id = user["id"]
    friend_ids = friendships[user_id]
    return len(friend_ids)


users = [
    {"id": 0, "name": "Hero"},
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"},
]

friendship_pairs = [
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (5, 7),
    (6, 8),
    (7, 8),
    (8, 9),
]

friendships = {user["id"]: [] for user in users}

for i, j in friendship_pairs:
    friendships[i].append(j)
    friendships[j].append(i)


# Begin with simple questions:
# What is the average number of connections per node (user)?
    
# Total connections
total_connections = sum(number_of_friends(user, friendships)
                        for user in users)

# Total number of users
num_users = len(users)

# Average connections per user
avg_connections = total_connections / num_users

print(f"Average connections per user: {avg_connections}")

# Who are the most connected users?
# Simply sort them by most friends -> least friends
# Small data set, not many other metrics

num_friends_by_id = [(user["id"], number_of_friends(user, friendships))
                     for user in users]
nfriends_by_id_sorted = sorted(num_friends_by_id,
                               key=lambda id_friends: id_friends[1],
                               reverse=True)
print(f"Most connected users: {nfriends_by_id_sorted}")

# Data Scientists you may know:
# Friend of a Friend


# Produces duplicates - let's keep a count of mutual friends
def foaf_ids_bad(user, friendships):
    """friend of a friend"""
    return [foaf_id
            for friend_id in friendships[user["id"]]
            for foaf_id in friendships[friend_id]]


def friends_of_friends(user, friendships):
    user_id = user["id"]
    return Counter(
        foaf_id
        for friend_id in friendships[user_id]
        for foaf_id in friendships[friend_id]
        if foaf_id != user_id
        and foaf_id not in friendships[user_id]
    )


# Mutual Interests

interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]


def data_scientists_who_like(interest, interests):
    """Find User IDs of all users who like interest"""
    return [user_id for user_id, user_interest in interests
            if user_interest == interest]

# This is not efficient
# Searches the list every time.
# We should build an index FROM interests TO users
# Use a defaultdict initialized to empty lists


user_ids_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)
    

# And build an index FROM users TO interests

interests_by_user_id = defaultdict(list)

for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)


# Now it's easy to find most common interests between users
# Iterate over a user's interests
# For each interest, iterate over the other users with it
# Keep count of how many times we see each other user


def most_common_interests_with(user, uid_interests, interest_uids):
    return Counter(
        interested for interest in interest_uids[user["id"]]
        for interested in uid_interests[interest]
        if interested != user["id"]
    )
    
    
# SALARY AND EXPERIENCE

salaries_and_tenures = [(83000, 8.7), (88000, 8.1),
                        (48000, 0.7), (76000, 6),
                        (69000, 6.5), (76000, 7.5),
                        (60000, 2.5), (83000, 10),
                        (48000, 1.9), (63000, 4.2)]


def tenure_bucket(t):
    if t < 2:
        return "less than 2"
    elif t < 5:
        return "between 2 and 5"
    else:
        return "more than 5"


salary_by_tenure_bucket = defaultdict(list)
for s, t in salaries_and_tenures:
    bucket = tenure_bucket(t)
    salary_by_tenure_bucket[bucket].append(s)

avg_salary_by_tenure = {bucket: sum(salary) / len(salary)
                        for bucket, salary in
                        salary_by_tenure_bucket.items()}


# PAID ACCOUNTS

# Make a simple model based on an observation,
# then test it against data

paid_accounts = [(0.7, "paid"),
                 (1.9, "paid"),
                 (2.5, "paid"),
                 (4.2, "unpaid"),
                 (6.0, "unpaid"),
                 (6.5, "unpaid"),
                 (7.5, "unpaid"),
                 (8.1, "unpaid"),
                 (8.7, "paid"),
                 (10, "paid")]

# There seems to be a correspondence between experience and
# paid accounts. Very few and very many years = paid
# Make a very simple model.


def predict_paid(tenure):
    if tenure < 3.0:
        return "paid"
    elif tenure < 8.5:
        return "unpaid"
    else:
        return "paid"


# TOPICS OF INTEREST
# Count the words
# Lower case them, split, count

words_and_counts = Counter(word
                           for user, interest in interests
                           for word in interest.lower().split())

