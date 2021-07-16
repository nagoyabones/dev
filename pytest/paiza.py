n, m, k = list(map(int, input().split(" ")))
sugoroku_map = [[0, 0]]
players = [[0 for x in range(2)] for y in range(m)]
arrival_rank = []

for _ in range(n - 2):
    move, coin = list(map(int, input().split(" ")))
    sugoroku_map.append([move, coin])
sugoroku_map.append([0, 0])

for i in range(k):

    move = list(map(int, input().split(" ")))

    for i in range(m):
        if (i in arrival_rank) is False:

            p_position = players[i][0]
            p_coin = players[i][1]

            p_position = min(n - 1, max(0, p_position + move[i]))

            if p_position < n - 1:
                players[i][0] = p_position
                map_data = sugoroku_map[p_position]
                command_move = map_data[0]
                get_coin = map_data[1]

                players[i][1] = max(0, p_coin + get_coin)

                p_position = min(n - 1, max(0, p_position + command_move))
                players[i][0] = p_position

                if p_position >= n - 1:
                    arrival_rank.append(i)

            elif p_position >= n - 1:
                arrival_rank.append(i)

        else:
            if arrival_rank.index(i) == 0:
                players[i][1] = players[i][1] + move[i] * 3
            elif arrival_rank == 1:
                players[i][1] = players[i][1] + move[i] * 2
            elif arrival_rank == 2:
                players[i][1] = players[i][1] + move[i] * 1

rank = []
for data in players:
    rank.append(data[1])

max_coin = max(rank)
player = rank.index(max_coin) + 1

print(player, max_coin)
