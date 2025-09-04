def search(number: int) -> bool:
    arr = [1, 2, 3, 45, 356, 569, 600, 705, 923]
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == number:
            return True
        elif arr[mid] < number:
            left = mid + 1
        else:
            right = mid -1
    return False



print(search(45))
print(search(46))
print(search(923))
print(search(0))