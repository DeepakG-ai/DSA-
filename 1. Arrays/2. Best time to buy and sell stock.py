"""
LeetCode Problem: 121. Best Time to Buy and Sell Stock
Method: One-pass scan (track min price and max profit)
Category: Arrays
Time Complexity: O(n)
Space Complexity: O(1)
Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
"""

def max_profit(prices):
    min_price = prices[0]
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price  # update buying day
        else:
            max_profit = max(max_profit, price - min_price)  # update selling day

    return max_profit

# Example usage
print(max_profit([7, 1, 5, 3, 6, 4]))  # Output: 5
