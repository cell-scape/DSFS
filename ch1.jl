#=
Translate Data Science from Scratch into idiomatic Julia
=#

using StatsBase, DataStructures

number_of_friends(user, friendships) = length(friendships[user[:id]])

users = [Dict(:id => 0, :name => "Hero"),
         Dict(:id => 1, :name => "Dunn"),
         Dict(:id => 2, :name => "Sue"),
         Dict(:id => 3, :name => "Chi"),
         Dict(:id => 4, :name => "Thor"),
         Dict(:id => 5, :name => "Clive"),
         Dict(:id => 6, :name => "Hicks"),
         Dict(:id => 7, :name => "Devin"),
         Dict(:id => 8, :name => "Kate"),
         Dict(:id => 9, :name => "Klein")]

friend_pairs = [(0, 1), (0, 2), (1, 2),
                (1, 3), (2, 3), (3, 4),
                (4, 5), (5, 6), (5, 7),
                (6, 8), (7, 8), (8, 9)]

friendships = Dict(user[:id] => [] for user in users)

for (i, j) in friend_pairs
    push!(friendships[i], j)
    push!(friendships[j], i)
end

total_connections = sum(number_of_friends(user, friendships)
                        for user in users)
avg_connections = total_connections / length(users)

println("Average connections per user: $(avg_connections)")

n_friends_by_id = [(user[:id], number_of_friends(user, friendships))
                   for user in users]
n_friends_sorted = sort(n_friends_by_id,
                        lt=isless,
                        by=x->x[2],
                        rev=true)
println("Most connected: $(n_friends_sorted)")

# Counter object in Julia?
# StatsBase countmap
# or DataStructures counter
# Functions that return a populated dictionary?

"Counts friends of friends, depends on StatsBase: countmap"
function friends_of_friends(user, friendships)
    user_id = user[:id]
    countmap(
        foaf_id for friend_id in friendships[user_id]
            for foaf_id in friendships[friend_id]
                if foaf_id != user_id
                    && !(foaf_id in friendships[user_id])
                    )
end


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


"List all user_ids if interested in <interest>"
function mutual_interests(interest, interests)
    [user_id for (user_id, user_interest) in interests
         if user_interest == interest]
end


# Function is inefficient; searches entire list every time.
# build an index from interests to users.

user_ids_by_interest = DefaultDict{String, Vector{Int64}}(() -> Int64[])

for (user_id, interest) in interests
    push!(user_ids_by_interest[interest], user_id)
end   

# And build an index from users to interests

interests_by_user_id = DefaultDict{Int64, Vector{String}}(() -> String[])

for (user_id, interest) in interests
    push!(interests_by_user_id[user_id], interest)
end

# Now iterate over a users interests
# For each interest, iterate over other users with it
# Keep count of how often we see each other user

function most_common_interests_with(user, uid_interest, interest_uid)
    counter(
        interested for interest in interest_uid[user[:id]]
        for interested in uid_interest[interest]
            if interested != user[:id]
                )
end


# SALARIES AND EXPERIENCE

salaries_and_tenures = [(83000, 8.7), (88000, 8.1),
                        (48000, 0.7), (76000, 6),
                        (69000, 6.5), (76000, 7.5),
                        (60000, 2.5), (83000, 10),
                        (48000, 1.9), (63000, 4.2)]

# Plotting the data, it looks clear that people with more experience
# tend to earn more. How do we turn that into a fun fact?

# Keys are by years, values are lists of the salaries for each tenure
salary_by_tenure = DefaultDict{Float64, Vector{Int64}}(() -> Int64[])

# Taking a simple average like in the first example won't work because
# none of the tenures are the same. We should bin them.


function tenure_bin(tenure)
    if tenure < 2
        return "less than 2"
    elseif tenure < 5
        return "between two and five"
    else
        return "more than five"
    end
end

# We can group the salaries by each bucket
salary_by_tenure_bin = DefaultDict{String, Vector{Int64}}(() -> Int64[])
for (s, t) in salaries_and_tenures
    bin = tenure_bin(t)
    push!(salary_by_tenure_bin[bin], s)
end

# Then compute the average for each group
avg_salary_by_bin = Dict(bin => mean(salaries)
                         for (bin, salaries) in salary_by_tenure_bin)


# PAID ACCOUNTS

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

function predict_paid(tenure)
    if tenure < 3.0
        return "paid"
    elseif tenure < 8.5
        return "unpaid"
    else
        return "paid"
    end
end

# TOPICS OF INTEREST

# lower, split, count

words_and_counts = countmap(word
                            for (user, interest) in interests
                                for word in split(lowercase(interest)))

for (word, count) in words_and_counts
    if count > 1
        println("$word: $count")
    end
end
