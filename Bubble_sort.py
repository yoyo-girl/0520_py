'''氣泡排序法'''
unsorted = [54, 22, 86, 61, 15]
print('原始資料為', unsorted)
tmp = unsorted.copy()
p = 0

while True:
    p += 1
    n = len(tmp)
    for i in range(n-1):
        if tmp[i] > tmp[i+1]:
            tmp[i], tmp[i+1] = tmp[i+1], tmp[i]
    print('這是第',p,'次','排序完的資料', tmp)

#跳出無限迴圈
    if tmp[n - 1] > tmp[n - 2] > tmp[n - 3] > tmp[n - 4] > tmp[n - 5]:
        break