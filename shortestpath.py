# from queue import PriorityQueue
# from math import sqrt
# import pymysql
#
#
# def getgraph(filename):
#     graph = []
#     with open(filename) as f:
#         x = 0
#         for line in f.readlines():
#             newline = []
#             y = 0
#             for word in line.strip().split(" "):
#                 if word == "s":
#                     src = (x, y)
#                     newline.append(0)
#                 elif word == "t":
#                     dst = (x, y)
#                     newline.append(0)
#                 else:
#                     newline.append(int(word))
#                 y += 1
#             x += 1
#
#             graph.append(newline)
#     height = len(graph)
#     width = len(graph[0])
#     return graph, height, width
#
#
# def findpath(graph, height, width, src, dst):
#     print("开始A*算法")
#     best_queue = PriorityQueue()
#     visited = [[0] * width for i in range(height)]
#
#     def hn(dot):
#         return sqrt((dot[0] - dst[0]) ** 2 + (dot[1] - dst[1]) ** 2)
#
#     best_queue.put((0, 0, src, [src]))
#     ci = 0
#     endpath = []
#     while True:
#         ci += 1
#         # if ci > 50:
#         #     break
#         f, g, now, path = best_queue.get()
#         # print(path)
#         x, y = now
#
#         # 终止条件
#         if now == dst:
#             print(path)
#             print(g)
#             print(ci)
#             endpath = path
#             break
#
#         # 是否访问过
#
#         for i in range(x - 1, x + 2):
#             for j in range(y - 1, y + 2):
#                 if 0 <= i < height and 0 <= j < width and (i != x or j != y) and graph[i][j] >= 0:
#                     # print((i, j), newh)
#                     if i == x or j == y:
#                         newg = g + 1 + graph[i][j]
#                         # if visited[i][j]:
#                         #     continue
#                         # visited[i][j] = 1
#                         # newh = hn((i, j))
#                         if visited[i][j]:
#                             if newg > visited[i][j][0]:
#                                 continue
#                             newh = visited[i][j][1]
#                             visited[i][j][0] = newg
#                         else:
#                             newh = hn((i, j))
#                             visited[i][j] = [newg, newh]
#                         newpath = path + [(i, j)]
#                         best_queue.put((newg + newh, newg, (i, j), newpath))
#                     else:
#                         newg = g + sqrt(2) + graph[i][j]
#                         # if visited[i][j]:
#                         #     continue
#                         # visited[i][j] = 1
#                         # newh = hn((i, j))
#                         if visited[i][j]:
#                             if newg > visited[i][j][0]:
#                                 continue
#                             newh = visited[i][j][1]
#                             visited[i][j][0] = newg
#                         else:
#                             newh = hn((i, j))
#                             visited[i][j] = [newg, newh]
#                         newpath = path + [(i, j)]
#                         best_queue.put((newg + newh, newg, (i, j), newpath))
#
#     for dot in endpath:
#         graph[dot[0]][dot[1]] = "x"
#
#     for i in range(height):
#         for j in range(width):
#             print(graph[i][j], end=" ")
#
#     return endpath
#
#
# def generateGraph(s_x, s_y, e_x, e_y):
#     conn = pymysql.connect(host="cdb-518aglpe.bj.tencentcdb.com", port=10101, user="root", password="zyx1999zyx",
#                            database="service")
#     cursor = conn.cursor()
#     sql = 'select * from place'
#     cursor.execute(sql)
#     map = cursor.fetchall()
#
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#     graph = [[0] * 4300 for i in range(4300)]
#     for i, j, k in map:
#         graph[j][k] = 50
#
#     graph[s_x][s_y] = 's'
#     graph[e_x][e_y] = 't'
#
#     with open("static/graphs/graph.txt", "w") as f:
#         for line in graph:
#             for w in line:
#                 f.write(str(w) + " ")
#             f.write("\n")
#
#
# if __name__ == '__main__':
#     generateGraph(3044,1539,2259,2876)
#     a,b,c = getgraph("static/graphs/graph.txt")
a = [[1,2],[2,3],[4,5]]
b = [0,1]
c = [6,7]

d = []
d.append(b)
for i in range(len(a)):
    d.append(a[i])
d.append(c)
size = len(d)
print(size)
for i in range(size):
    print(d[i])
