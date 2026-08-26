def twoSum(numbers, target):
        left, right = 0, len(numbers) - 1

        while left < right:
            s = numbers[left] + numbers[right]

            if s == target:
                return [left + 1, right + 1]  # 1-based index
            elif s < target:
                left += 1
            else:
                right -= 1

numbers = [2,7,11,15]
target = 9
print(twoSum(numbers, target))