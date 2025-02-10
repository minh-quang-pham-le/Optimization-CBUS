#### IT3052E - Fundamentals of Optimization

# **Mini Project - CBUS**

There are n passengers 1, 2, … , 𝑛. The passenger 𝑖 want to travel from
point 𝑖 to point 𝑖 + 𝑛 (𝑖 = 1,2, … , 𝑛). There is a bus located at point
0 and has 𝑘 places for transporting the passengers (it means at any
time, there are at most 𝑘 passengers on the bus). You are given the
distance matrix c in which 𝑐(𝑖, 𝑗) is the traveling distance from point 𝑖
to point 𝑗 (𝑖, 𝑗 = 0,1, … , 2𝑛). Compute the shortest route for the
bus, serving n passengers and coming back to point 0.

• Input
• Line 1 contains n and 𝑘 (1 ≤ 𝑛 ≤ 1000,1 ≤ 𝑘 ≤ 50)
• Line 𝑖 + 1 (𝑖 = 1,2, … , 2𝑛 + 1) contains the 𝑖 − 1 𝑡ℎline of the matrix 𝑐
(rows and columns are indexed from 0,1,2, . . , 2𝑛).
• Output
• Line 1: write the value 𝑛
• Line 2: Write the sequence of points (pickup and drop-off) of passengers
(separated by a SPACE character)

• Example
• Input
5 3
0 5 8 11 12 8 3 3 7 5 5
5 0 3 5 7 5 3 4 2 2 2
8 3 0 7 8 8 5 7 1 6 5
11 5 7 0 1 5 9 8 6 5 6
12 7 8 1 0 6 10 10 7 7 7
8 5 8 5 6 0 8 5 7 3 4
3 3 5 9 10 8 0 3 4 5 4
3 4 7 8 10 5 3 0 6 2 2
7 2 1 6 7 7 4 6 0 5 4
5 2 6 5 7 3 5 2 5 0 1
5 2 5 6 7 4 4 2 4 1 0
• Output
5
1 2 6 7 5 10 3 4 8 9
