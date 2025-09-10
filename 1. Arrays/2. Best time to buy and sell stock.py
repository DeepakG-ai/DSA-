"""LeetCode Problem 121: Best Time to Buy and Sell Stock
Method: One-pass scan (track min price and max profit)
Category: Arrays
Time Complexity: O(n)
Space Complexity: O(1)
Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

-----------------------------------
Constraints:
• 1 <= prices.length <= 10^5
• 0 <= prices[i] <= 10^4
• You must buy before you sell
• You can only do one transaction

-----------------------------------
Examples:

Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5

Example 2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: No transactions done as buying then selling would lead to a loss
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


# Test cases
def test_max_profit():
    # Test case 1
    prices1 = [7,1,5,3,6,4]
    assert max_profit(prices1) == 5, "Test case 1 failed"
    
    # Test case 2
    prices2 = [7,6,4,3,1]
    assert max_profit(prices2) == 0, "Test case 2 failed"
    
    # Test case 3 (Additional edge case)
    prices3 = [2,4,1]
    assert max_profit(prices3) == 2, "Test case 3 failed"
    
    print("All test cases passed!")

if __name__ == "__main__":
    test_max_profit()

# Example usage
print(max_profit([7, 1, 5, 3, 6, 4]))  # Output: 5
