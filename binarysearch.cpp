// DESCRIPTION:Problem: Search in Rotated Sorted Array
// You are given a rotated sorted array nums of n elements, which is originally sorted in ascending order. 
// The array has been rotated at some unknown pivot point. Your task is to search for a target value in the array
//  and return its index. If the target is not found, return -1.
// testcase 1:
// Input: nums = [4,5,6,7,0,1,2], target = 0
// Output: 4
// testcase 2:
// Input: nums = [4,5,6,7,0,1,2], target = 3
// Output: -1
//  testcase 3:
// Input: nums = [1], target = 0
// Output: -1

#include <iostream>
#include <vector>

using namespace std;

int search(vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size() - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (nums[mid] == target) {
            return mid; // Target found
        }

        // Determine which side is sorted
        if (nums[left] <= nums[mid]) { // Left side is sorted
            if (nums[left] <= target && target < nums[mid]) {
                right = mid - 1; // Target is in the left side
            } else {
                left = mid + 1; // Target is in the right side
            }
        } else { // Right side is sorted
            if (nums[mid] < target && target <= nums[right]) {
                left = mid + 1; // Target is in the right side
            } else {
                right = mid - 1; // Target is in the left side
            }
        }
    }

    return -1; // Target not found
}

int main() {
    vector<int> nums = {4, 5, 6, 7, 0, 1, 2};
    int target = 0;

    int result = search(nums, target);
    cout << "Target index: " << result << endl; // Output: 4

    return 0;
}
// Explanation of the Solution
// 1.Initialization: Start with two pointers, left and right, representing the boundaries of the search space.
// 2.While Loop: Continue searching while left is less than or equal to right.
// 3.Finding the Middle: Calculate the middle index mid and check if the target is found.
// 4.Identifying Sorted Half: Determine whether the left half or the right half is sorted:
// *If the left half is sorted (nums[left] <= nums[mid]), check if the target lies within this range.
// *If the target is within the sorted left half, adjust the right pointer. Otherwise, adjust the left pointer.
// *If the right half is sorted, apply similar logic to adjust left and right pointers.
// 5.Return Result: If the target is not found, return -1.
// Complexity Analysis
// Time Complexity: O(log n) because we are dividing the search space in half at each iteration.
// Space Complexity: O(1) since no additional space is used except for a few variables.