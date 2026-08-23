def productExceptSelf(nums):
    output = []

    for i in range(len(nums)):
        product = 1

        for j in range(len(nums)):
            if j != i:
                product *= nums[j]

        output.append(product)

    return output

nums = [1, 2, 4, 6]
print(productExceptSelf(nums))