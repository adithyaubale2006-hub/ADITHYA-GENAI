#Brute force sol
def Buy_sell(nums):
    n = len(nums)
    max_profit = 0
    for i in range(0, n):
        for j in range(i+1, n):
            p = nums[i]-nums[j]
            max_profit = max(max_profit, p)
    return max_profit

nums = [7,2,1,5,6,4,8]
print(Buy_sell(nums))

#Optimal sol
def Buy_sell(prices):
    n = len(prices)
    max_profit = 0
    min_profit = float("inf")

    for i in range(0, n):
        min_profit = min(min_profit, prices[i])
        max_profit = max(max_profit, prices[i]-min_profit)
        
    return max_profit

prices = [7,6,4,3,1]
print(Buy_sell(prices))