---
title: 'LeetCode Java 刷题笔记'
description: '按题型分类整理 LeetCode Hot 100 与剑指 Offer 题解，每类包含解题模板，覆盖哈希、双指针、滑动窗口、动态规划等核心算法。'
pubDate: '2026-05-03'
category: '算法'
tags: ['LeetCode Hot 100', '剑指 Offer', 'Java', '哈希', '双指针', '滑动窗口', '动态规划', '回溯', '二分查找', '链表', '二叉树']
---

## 前言

这份笔记按题型分类整理了 LeetCode Hot 100 和剑指 Offer 的经典题目，每个类型的题目顺序是 Hot 100 在前、剑指 Offer 在后，类型末尾附有解题模板便于快速回顾。

题目解法参考了 [doocs/leetcode](https://github.com/doocs/leetcode) 开源题解项目，代码均为 Java 实现。

---

## 一、哈希

**来源：LeetCode Hot 100**

<a id="p-1"></a>
## 1. 两数之和

- 难度：简单
- 标签：数组、哈希表
- 跳转：[官方题目](https://leetcode.cn/problems/two-sum/) | [参考题解](https://leetcode.doocs.org/lc/1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0001.Two%20Sum/README.md)

### 题目要求
给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出 和为目标值 `target` 的那 两个 整数，并返回它们的数组下标。 你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。 你可以按任意顺序返回答案。

### 样例数据
样例 1:
```text
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

样例 2:
```text
输入：nums = [3,2,4], target = 6
输出：[1,2]
```

### 核心思路
`方法一：哈希表`

我们可以使用一个哈希表 d 来存储每个元素及其对应的索引。 遍历数组 nums，对于当前元素 nums[i]，我们首先判断 target - nums[i] 是否在哈希表 d 中，如果在 d 中，说明 target 值已经找到，返回 target - nums[i] 的索引和 i 即可。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)，其中 n 为数组 nums 的长度。

### Java 代码
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> d = new HashMap<>();
        for (int i = 0;; ++i) {
            int x = nums[i];
            int y = target - x;
            if (d.containsKey(y)) {
                return new int[] {d.get(y), i};
            }
            d.put(x, i);
        }
    }
}
```

---

<a id="p-49"></a>
## 49. 字母异位词分组

- 难度：中等
- 标签：数组、哈希表、字符串、排序
- 跳转：[官方题目](https://leetcode.cn/problems/group-anagrams/) | [参考题解](https://leetcode.doocs.org/lc/49/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0049.Group%20Anagrams/README.md)

### 题目要求
给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。

### 样例数据
样例 1:
```text
输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
解释：
- 在 strs 中没有字符串可以通过重新排列来形成 `"bat"`。
- 字符串 `"nat"` 和 `"tan"` 是字母异位词，因为它们可以重新排列以形成彼此。
- 字符串 `"ate"` ，`"eat"` 和 `"tea"` 是字母异位词，因为它们可以重新排列以形成彼此。
```

样例 2:
```text
输入: strs = [""]
输出: [[""]]
```

### 核心思路
`方法一：哈希表`

1. 遍历字符串，对每个字符串按照**字符字典序**排序，得到一个新的字符串。 2. 以新字符串为 `key`，`[str]` 为 `value`，存入哈希表当中（`HashMap<String, List<String>>`）。 3. 后续遍历得到相同 `key` 时，将其加入到对应的 `value` 当中即可。 以 `strs = ["eat", "tea", "tan", "ate", "nat", "bat"]` 为例，遍历结束时，哈希表的状况：

| key     | value                   |
| ------- | ----------------------- |
| `"aet"` | `["eat", "tea", "ate"]` |
| `"ant"` | `["tan", "nat"] `       |
| `"abt"` | `["bat"] `              |

最后返回哈希表的 `value` 列表即可。 其中 n 和 k 分别是字符串数组的长度和字符串的最大长度。

### 复杂度
时间复杂度 O(n\times k\times \log k)。

### Java 代码
```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> d = new HashMap<>();
        for (String s : strs) {
            char[] t = s.toCharArray();
            Arrays.sort(t);
            String k = String.valueOf(t);
            d.computeIfAbsent(k, key -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(d.values());
    }
}
```

---

<a id="p-128"></a>
## 128. 最长连续序列

- 难度：中等
- 标签：并查集、数组、哈希表
- 跳转：[官方题目](https://leetcode.cn/problems/longest-consecutive-sequence/) | [参考题解](https://leetcode.doocs.org/lc/128/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0128.Longest%20Consecutive%20Sequence/README.md)

### 题目要求
给定一个未排序的整数数组 `nums` ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。 请你设计并实现时间复杂度为 `O(n)` 的算法解决此问题。

### 样例数据
样例 1:
```text
输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
```

样例 2:
```text
输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9
```

### 核心思路
`方法一：哈希表`

我们可以用一个哈希表 s 存储数组中所有的元素，用一个变量 ans 记录最长连续序列的长度，用一个哈希表 d 记录每个元素 x 所在的连续序列的长度。 接下来，我们遍历数组中每个元素 x，用一个临时变量 y 记录当前连续序列的最大值，初始时 y = x。 然后，我们不断尝试匹配 y+1, y+2, y+3, \dots，直到匹配不到为止，过程中将匹配到的元素从哈希表 s 中移除。 那么，当前元素 x 所在的连续序列的长度即为 d[x] = d[y] + y - x，然后更新答案 ans = \max(ans, d[x])。 遍历结束后，返回答案 ans 即可。 其中 n 是数组 nums 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> s = new HashSet<>();
        for (int x : nums) {
            s.add(x);
        }
        int ans = 0;
        Map<Integer, Integer> d = new HashMap<>();
        for (int x : nums) {
            int y = x;
            while (s.contains(y)) {
                s.remove(y++);
            }
            d.put(x, d.getOrDefault(y, 0) + y - x);
            ans = Math.max(ans, d.get(x));
        }
        return ans;
    }
}
```


**来源：剑指 Offer**

<a id="offer-50"></a>
## 剑指 Offer 50. 第一个只出现一次的字符

- 难度：简单
- 标签：哈希表
- 跳转：[官方题目](https://leetcode.cn/problems/di-yi-ge-zhi-chu-xian-yi-ci-de-zi-fu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/50/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9850.%20%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%8F%AA%E5%87%BA%E7%8E%B0%E4%B8%80%E6%AC%A1%E7%9A%84%E5%AD%97%E7%AC%A6/README.md)

### 题目要求
在字符串 s 中找出第一个只出现一次的字符。如果没有，返回一个单空格。 s 只包含小写字母。

### 样例数据
样例 1:
```text
输入：s = "abaccdeff"
输出：'b'
```

样例 2:
```text
输入：s = ""
输出：' '
```

### 核心思路
`方法一：数组或哈希表`

我们可以使用哈希表或数组 cnt 来统计每个字符出现的次数，然后再遍历一遍字符串，找到第一个出现次数为 1 的字符。 其中 n 为字符串长度；而 C 为字符集大小，本题中 C=26。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(C)。

### Java 代码
```java
class Solution {
    public char firstUniqChar(String s) {
        int[] cnt = new int[26];
        for (int i = 0; i < s.length(); ++i) {
            ++cnt[s.charAt(i) - 'a'];
        }
        for (int i = 0; i < s.length(); ++i) {
            char c = s.charAt(i);
            if (cnt[c - 'a'] == 1) {
                return c;
            }
        }
        return ' ';
    }
}
```

---

<a id="offer-57"></a>
## 剑指 Offer 57. 和为s的两个数字

- 难度：简单
- 标签：哈希表
- 跳转：[官方题目](https://leetcode.cn/problems/he-wei-sde-liang-ge-shu-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/57/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9857.%20%E5%92%8C%E4%B8%BAs%E7%9A%84%E4%B8%A4%E4%B8%AA%E6%95%B0%E5%AD%97/README.md)

### 题目要求
输入一个递增排序的数组和一个数字s，在数组中查找两个数，使得它们的和正好是s。如果有多对数字的和等于s，则输出任意一对即可。

### 样例数据
样例 1:
```text
输入：nums = [2,7,11,15], target = 9
输出：[2,7] 或者 [7,2]
```

样例 2:
```text
输入：nums = [10,26,30,31,47,60], target = 40
输出：[10,30] 或者 [30,10]
```

### 核心思路
`方法一：双指针`

优先按题目所属专题套用对应模板，再处理边界。

### Java 代码
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (true) {
            if (nums[l] + nums[r] == target) {
                return new int[] {nums[l], nums[r]};
            }
            if (nums[l] + nums[r] > target) {
                --r;
            } else {
                ++l;
            }
        }
    }
}
```


### 解题模板

```
// 1. 两数之和型：边遍历边查补
Map<Integer, Integer> map = new HashMap<>();
for (int i = 0; i < nums.length; i++) {
    if (map.containsKey(target - nums[i])) { return ...; }
    map.put(nums[i], i);
}

// 2. 分组型：排序/计数作为 key，原始值作为 value
Map<String, List<String>> map = new HashMap<>();
for (String s : strs) {
    char[] t = s.toCharArray(); Arrays.sort(t);
    map.computeIfAbsent(String.valueOf(t), k -> new ArrayList<>()).add(s);
}

// 3. 去重/计数型：HashSet 判存在，HashMap 计频次
```

**识别信号**：O(n) 内查找、去重、计数、判断"是否存在某值" → 哈希表把双层循环压成单层。

---

## 二、双指针

**来源：LeetCode Hot 100**

<a id="p-283"></a>
## 283. 移动零

- 难度：简单
- 标签：数组、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/move-zeroes/) | [参考题解](https://leetcode.doocs.org/lc/283/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0283.Move%20Zeroes/README.md)

### 题目要求
给定一个数组 `nums`，编写一个函数将所有 `0` 移动到数组的末尾，同时保持非零元素的相对顺序。 请注意 ，必须在不复制数组的情况下原地对数组进行操作。

### 样例数据
样例 1:
```text
输入: nums = `[0,1,0,3,12]`
输出: `[1,3,12,0,0]`
```

样例 2:
```text
输入: nums = `[0]`
输出: `[0]`
```

### 核心思路
`方法一：双指针`

我们用一个指针 k 记录当前待插入的位置，初始时 k = 0。 然后我们遍历数组 nums，每次遇到一个非零数，就将其与 nums[k] 交换，同时将 k 的值加 1。 这样我们就可以保证 nums 的前 k 个元素都是非零的，且它们的相对顺序与原数组一致。

### 复杂度
时间复杂度 O(n)，其中 n 是数组 nums 的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public void moveZeroes(int[] nums) {
        int k = 0, n = nums.length;
        for (int i = 0; i < n; ++i) {
            if (nums[i] != 0) {
                int t = nums[i];
                nums[i] = nums[k];
                nums[k++] = t;
            }
        }
    }
}
```

---

<a id="p-11"></a>
## 11. 盛最多水的容器

- 难度：中等
- 标签：贪心、数组、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/container-with-most-water/) | [参考题解](https://leetcode.doocs.org/lc/11/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0011.Container%20With%20Most%20Water/README.md)

### 题目要求
给定一个长度为 `n` 的整数数组 `height` 。有 `n` 条垂线，第 `i` 条线的两个端点是 `(i, 0)` 和 `(i, height[i])` 。 找出其中的两条线，使得它们与 `x` 轴共同构成的容器可以容纳最多的水。 返回容器可以储存的最大水量。 说明：你不能倾斜容器。

### 样例数据
样例 1:
```text
输入：[1,8,6,2,5,4,8,3,7]
输出：49
解释：图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。
```

样例 2:
```text
输入：height = [1,1]
输出：1
```

### 核心思路
`方法一：双指针`

我们使用两个指针 l 和 r 分别指向数组的左右两端，即 l = 0，而 r = n - 1，其中 n 是数组的长度。 接下来，我们使用变量 ans 记录容器的最大容量，初始化为 0。 然后，我们开始进行循环，每次循环中，我们计算当前容器的容量，即 min(height[l], height[r]) \times (r - l)，并将其与 ans 进行比较，将较大值赋给 ans。 然后，我们判断 height[l] 和 height[r] 的大小，如果 height[l] < height[r]，移动 r 指针不会使得结果变得更好，因为容器的高度由较短的那根垂直线决定，所以我们移动 l 指针。 反之，我们移动 r 指针。 遍历结束后，返回 ans 即可。

### 复杂度
时间复杂度 O(n)，其中 n 是数组 height 的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int maxArea(int[] height) {
        int l = 0, r = height.length - 1;
        int ans = 0;
        while (l < r) {
            int t = Math.min(height[l], height[r]) * (r - l);
            ans = Math.max(ans, t);
            if (height[l] < height[r]) {
                ++l;
            } else {
                --r;
            }
        }
        return ans;
    }
}
```

---

<a id="p-15"></a>
## 15. 三数之和

- 难度：中等
- 标签：数组、双指针、排序
- 跳转：[官方题目](https://leetcode.cn/problems/3sum/) | [参考题解](https://leetcode.doocs.org/lc/15/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0015.3Sum/README.md)

### 题目要求
给你一个整数数组 `nums` ，判断是否存在三元组 `[nums[i], nums[j], nums[k]]` 满足 `i != j`、`i != k` 且 `j != k` ，同时还满足 `nums[i] + nums[j] + nums[k] == 0` 。请你返回所有和为 `0` 且不重复的三元组。 注意：答案中不可以包含重复的三元组。

### 样例数据
样例 1:
```text
输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
解释：
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
注意，输出的顺序和三元组的顺序并不重要。
```

样例 2:
```text
输入：nums = [0,1,1]
输出：[]
解释：唯一可能的三元组和不为 0 。
```

### 核心思路
`方法一：排序 + 双指针`

我们注意到，题目不要求我们按照顺序返回三元组，因此我们不妨先对数组进行排序，这样就可以方便地跳过重复的元素。 接下来，我们枚举三元组的第一个元素 nums[i]，其中 0 \leq i \lt n - 2。 对于每个 i，我们可以通过维护两个指针 j = i + 1 和 k = n - 1，从而找到满足 nums[i] + nums[j] + nums[k] = 0 的 j 和 k。 在枚举的过程中，我们需要跳过重复的元素，以避免出现重复的三元组。 具体判断逻辑如下：

如果 i \gt 0 并且 nums[i] = nums[i - 1]，则说明当前枚举的元素与上一个元素相同，我们可以直接跳过，因为不会产生新的结果。 如果 nums[i] \gt 0，则说明当前枚举的元素大于 0，则三数之和必然无法等于 0，结束枚举。 否则，我们令左指针 j = i + 1，右指针 k = n - 1，当 j \lt k 时，执行循环，计算三数之和 x = nums[i] + nums[j] + nums[k]，并与 0 比较：

- 如果 x \lt 0，则说明 nums[j] 太小，我们需要将 j 右移一位。 - 如果 x \gt 0，则说明 nums[k] 太大，我们需要将 k 左移一位。 - 否则，说明我们找到了一个合法的三元组，将其加入答案，并将 j 右移一位，将 k 左移一位，同时跳过所有重复的元素，继续寻找下一个合法的三元组。 枚举结束后，我们即可得到三元组的答案。 其中 n 为数组的长度。

### 复杂度
时间复杂度 O(n^2)，空间复杂度 O(\log n)。

### Java 代码
```java
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> ans = new ArrayList<>();
        int n = nums.length;
        for (int i = 0; i < n - 2 && nums[i] <= 0; ++i) {
            if (i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }
            int j = i + 1, k = n - 1;
            while (j < k) {
                int x = nums[i] + nums[j] + nums[k];
                if (x < 0) {
                    ++j;
                } else if (x > 0) {
                    --k;
                } else {
                    ans.add(List.of(nums[i], nums[j++], nums[k--]));
                    while (j < k && nums[j] == nums[j - 1]) {
                        ++j;
                    }
                    while (j < k && nums[k] == nums[k + 1]) {
                        --k;
                    }
                }
            }
        }
        return ans;
    }
}
```

---

<a id="p-42"></a>
## 42. 接雨水

- 难度：困难
- 标签：栈、数组、双指针、动态规划、单调栈
- 跳转：[官方题目](https://leetcode.cn/problems/trapping-rain-water/) | [参考题解](https://leetcode.doocs.org/lc/42/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0042.Trapping%20Rain%20Water/README.md)

### 题目要求
给定 `n` 个非负整数表示每个宽度为 `1` 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

### 样例数据
样例 1:
```text
输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。
```

样例 2:
```text
输入：height = [4,2,0,3,2,5]
输出：9
```

### 核心思路
`方法一：动态规划`

我们定义 left[i] 表示下标 i 位置及其左边的最高柱子的高度，定义 right[i] 表示下标 i 位置及其右边的最高柱子的高度。 那么下标 i 位置能接的雨水量为 \min(left[i], right[i]) - height[i]。 我们遍历数组，计算出 left[i] 和 right[i]，最后答案为 \sum_{i=0}^{n-1} \min(left[i], right[i]) - height[i]。 其中 n 为数组的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int trap(int[] height) {
        int n = height.length;
        int[] left = new int[n];
        int[] right = new int[n];
        left[0] = height[0];
        right[n - 1] = height[n - 1];
        for (int i = 1; i < n; ++i) {
            left[i] = Math.max(left[i - 1], height[i]);
            right[n - i - 1] = Math.max(right[n - i], height[n - i - 1]);
        }
        int ans = 0;
        for (int i = 0; i < n; ++i) {
            ans += Math.min(left[i], right[i]) - height[i];
        }
        return ans;
    }
}
```


**来源：剑指 Offer**

<a id="offer-3"></a>
## 剑指 Offer 03. 数组中重复的数字

- 难度：简单
- 标签：双指针
- 跳转：[官方题目](https://leetcode.cn/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/3/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9803.%20%E6%95%B0%E7%BB%84%E4%B8%AD%E9%87%8D%E5%A4%8D%E7%9A%84%E6%95%B0%E5%AD%97/README.md)

### 题目要求
找出数组中重复的数字。 在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。

### 样例数据
样例 1:
```text
输入：
[2, 3, 1, 0, 2, 5, 3]
输出：2 或 3
```

### 核心思路
`方法一：排序`

我们可以先对数组 `nums` 进行排序，然后遍历排序后的数组，判断相邻的两个元素是否相等，如果相等，即找到了一个重复的数字，返回该数字即可。 其中 n 是数组 `nums` 的长度。

### 复杂度
时间复杂度 O(n \times \log n)，空间复杂度 O(\log n)。

### Java 代码
```java
class Solution {
    public int findRepeatNumber(int[] nums) {
        Arrays.sort(nums);
        for (int i = 0;; ++i) {
            if (nums[i] == nums[i + 1]) {
                return nums[i];
            }
        }
    }
}
```

---

<a id="offer-21"></a>
## 剑指 Offer 21. 调整数组顺序使奇数位于偶数前面

- 难度：简单
- 标签：双指针
- 跳转：[官方题目](https://leetcode.cn/problems/diao-zheng-shu-zu-shun-xu-shi-qi-shu-wei-yu-ou-shu-qian-mian-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/21/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9821.%20%E8%B0%83%E6%95%B4%E6%95%B0%E7%BB%84%E9%A1%BA%E5%BA%8F%E4%BD%BF%E5%A5%87%E6%95%B0%E4%BD%8D%E4%BA%8E%E5%81%B6%E6%95%B0%E5%89%8D%E9%9D%A2/README.md)

### 题目要求
输入一个整数数组，实现一个函数来调整该数组中数字的顺序，使得所有奇数在数组的前半部分，所有偶数在数组的后半部分。

### 样例数据
样例 1:
```text
输入：nums = [1,2,3,4]
输出：[1,3,2,4]
注：[3,1,2,4] 也是正确的答案之一。
```

### 核心思路
`方法一：双指针`

我们定义两个指针 i 和 j，其中指针 i 指向当前元素，指针 j 指向当前最后一个奇数的下一个位置。 接下来，我们从左到右遍历数组，当 nums[i] 是奇数时，我们将其与 nums[j] 交换，然后指针 j 向右移动一位。 指针 i 每次向右移动一位，直到遍历完整个数组。 其中 n 是数组的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int[] exchange(int[] nums) {
        int j = 0;
        for (int i = 0; i < nums.length; ++i) {
            if (nums[i] % 2 == 1) {
                int t = nums[i];
                nums[i] = nums[j];
                nums[j++] = t;
            }
        }
        return nums;
    }
}
```

---

<a id="offer-48"></a>
## 剑指 Offer 48. 最长不含重复字符的子字符串

- 难度：中等
- 标签：双指针
- 跳转：[官方题目](https://leetcode.cn/problems/zui-chang-bu-han-zhong-fu-zi-fu-de-zi-zi-fu-chuan-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/48/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9848.%20%E6%9C%80%E9%95%BF%E4%B8%8D%E5%90%AB%E9%87%8D%E5%A4%8D%E5%AD%97%E7%AC%A6%E7%9A%84%E5%AD%90%E5%AD%97%E7%AC%A6%E4%B8%B2/README.md)

### 题目要求
请从字符串中找出一个最长的不包含重复字符的子字符串，计算该最长子字符串的长度。

### 样例数据
样例 1:
```text
输入: "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 `"abc"，所以其`长度为 3。
```

样例 2:
```text
输入: "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 `"b"`，所以其长度为 1。
```

### 核心思路
`方法一：双指针 + 哈希表`

我们用双指针 j 和 i 分别表示子串的左右边界，其中 j 是滑动窗口的左边界，i 是滑动窗口的右边界，用哈希表 vis 记录每个字符是否出现过。 遍历字符串 s，如果此时 s[i] 在哈希表 vis 中存在，说明 s[i] 重复了，我们需要将左边界 j 右移，直到 s[i] 不在哈希表 vis 中为止，然后将 s[i] 加入哈希表 vis 中。 此时，我们更新无重复字符子串的最大长度，即 ans = \max(ans, i - j + 1)。 遍历结束后，我们返回 ans 即可。 其中 n 是字符串 s 的长度；而 C 是字符集的大小。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(C)。

### Java 代码
```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        int ans = 0, j = 0;
        Set<Character> vis = new HashSet<>();
        for (int i = 0; i < s.length(); ++i) {
            while (vis.contains(s.charAt(i))) {
                vis.remove(s.charAt(j++));
            }
            vis.add(s.charAt(i));
            ans = Math.max(ans, i - j + 1);
        }
        return ans;
    }
}
```

---

<a id="offer-57-2"></a>
## 剑指 Offer 57 - II. 和为s的连续正数序列

- 难度：简单
- 标签：双指针
- 跳转：[官方题目](https://leetcode.cn/problems/he-wei-sde-lian-xu-zheng-shu-xu-lie-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/57.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9857%20-%20II.%20%E5%92%8C%E4%B8%BAs%E7%9A%84%E8%BF%9E%E7%BB%AD%E6%AD%A3%E6%95%B0%E5%BA%8F%E5%88%97/README.md)

### 题目要求
输入一个正整数 `target` ，输出所有和为 `target` 的连续正整数序列（至少含有两个数）。 序列内的数字由小到大排列，不同序列按照首个数字从小到大排列。

### 样例数据
样例 1:
```text
输入：target = 9
输出：[[2,3,4],[4,5]]
```

样例 2:
```text
输入：target = 15
输出：[[1,2,3,4,5],[4,5,6],[7,8]]
```

### 核心思路
`方法一：双指针`

我们可以使用双指针的方法，维护一个区间 [l,.. r]，使得区间内的数之和 s 为 target，如果区间内的数之和小于 target，则右指针 l 右移，如果区间内的数之和大于 target，则左指针 l 右移，直到左指针到达 target 的一半为止。

### 复杂度
时间复杂度 O(target)，忽略答案的空间消耗，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int[][] findContinuousSequence(int target) {
        int l = 1, r = 2;
        List<int[]> ans = new ArrayList<>();
        while (l < r) {
            int s = (l + r) * (r - l + 1) / 2;
            if (s == target) {
                int[] t = new int[r - l + 1];
                for (int i = l; i <= r; ++i) {
                    t[i - l] = i;
                }
                ans.add(t);
                ++l;
            } else if (s < target) {
                ++r;
            } else {
                ++l;
            }
        }
        return ans.toArray(new int[0][]);
    }
}
```

---

<a id="offer-58-1"></a>
## 剑指 Offer 58 - I. 翻转单词顺序

- 难度：简单
- 标签：双指针
- 跳转：[官方题目](https://leetcode.cn/problems/fan-zhuan-dan-ci-shun-xu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/58.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9858%20-%20I.%20%E7%BF%BB%E8%BD%AC%E5%8D%95%E8%AF%8D%E9%A1%BA%E5%BA%8F/README.md)

### 题目要求
输入一个英文句子，翻转句子中单词的顺序，但单词内字符的顺序不变。为简单起见，标点符号和普通字母一样处理。例如输入字符串"I am a student. "，则输出"student. a am I"。

### 样例数据
样例 1:
```text
输入: "`the sky is blue`"
输出: "`blue is sky the`"
```

样例 2:
```text
输入: " hello world! "
输出: "world! hello"
解释: 输入字符串可以在前面或者后面包含多余的空格，但是反转后的字符不能包括。
```

### 核心思路
`方法一：双指针`

我们可以使用双指针 i 和 j，每次找到一个单词，将其添加到结果列表中，最后将结果列表反转，再拼接成字符串即可。 其中 n 为字符串的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public String reverseWords(String s) {
        List<String> words = new ArrayList<>();
        int n = s.length();
        for (int i = 0; i < n;) {
            while (i < n && s.charAt(i) == ' ') {
                ++i;
            }
            if (i < n) {
                StringBuilder t = new StringBuilder();
                int j = i;
                while (j < n && s.charAt(j) != ' ') {
                    t.append(s.charAt(j++));
                }
                words.add(t.toString());
                i = j;
            }
        }
        Collections.reverse(words);
        return String.join(" ", words);
    }
}
```


### 解题模板

```
// 1. 快慢指针（原地压缩/去重）
int k = 0;
for (int i = 0; i < n; i++) {
    if (满足条件) { nums[k++] = nums[i]; }
}

// 2. 左右相向指针（容器/回文）
int l = 0, r = n - 1;
while (l < r) {
    // 处理
    if (height[l] < height[r]) l++; else r--;
}

// 3. 排序 + 双指针（N 数之和）
Arrays.sort(nums);
for (int i = 0; i < n - 2; i++) {
    int j = i + 1, k = n - 1;
    while (j < k) {
        int sum = nums[i] + nums[j] + nums[k];
        if (sum < 0) j++; else if (sum > 0) k--; else { 记录; j++; k--; }
    }
}
```

**识别信号**：数组/字符串上原地操作、回文判断、N 数之和 → 双指针。

---

## 三、滑动窗口

**来源：LeetCode Hot 100**

<a id="p-3"></a>
## 3. 无重复字符的最长子串

- 难度：中等
- 标签：哈希表、字符串、滑动窗口
- 跳转：[官方题目](https://leetcode.cn/problems/longest-substring-without-repeating-characters/) | [参考题解](https://leetcode.doocs.org/lc/3/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0003.Longest%20Substring%20Without%20Repeating%20Characters/README.md)

### 题目要求
给定一个字符串 `s` ，请你找出其中不含有重复字符的 最长 子串 的长度。

### 样例数据
样例 1:
```text
输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 `"abc"`，所以其长度为 3。注意 "bca" 和 "cab" 也是正确答案。
```

样例 2:
```text
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 `"b"`，所以其长度为 1。
```

### 核心思路
`方法一：滑动窗口`

我们可以用两个指针 l 和 r 维护一个滑动窗口，使其始终满足窗口内没有重复字符，初始时 l 和 r 都指向字符串的第一个字符。 用一个哈希表或者长度为 128 的数组 cnt 来记录每个字符出现的次数，其中 cnt[c] 表示字符 c 出现的次数。 接下来，我们依次移动右指针 r，每次移动时，将 cnt[s[r]] 的值加 1，然后判断当前窗口 [l, r] 内 cnt[s[r]] 是否大于 1，如果大于 1，说明当前窗口内有重复字符，我们需要移动左指针 l，直到窗口内没有重复字符为止。 然后，我们更新答案 ans = \max(ans, r - l + 1)。 最终，我们返回答案 ans 即可。

### 复杂度
时间复杂度 O(n)，其中 n 为字符串的长度。 空间复杂度 O(|\Sigma|)，其中 \Sigma 表示字符集，这里 \Sigma 的大小为 128。

### Java 代码
```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        int[] cnt = new int[128];
        int ans = 0, n = s.length();
        for (int l = 0, r = 0; r < n; ++r) {
            char c = s.charAt(r);
            ++cnt[c];
            while (cnt[c] > 1) {
                --cnt[s.charAt(l++)];
            }
            ans = Math.max(ans, r - l + 1);
        }
        return ans;
    }
}
```

---

<a id="p-438"></a>
## 438. 找到字符串中所有字母异位词

- 难度：中等
- 标签：哈希表、字符串、滑动窗口
- 跳转：[官方题目](https://leetcode.cn/problems/find-all-anagrams-in-a-string/) | [参考题解](https://leetcode.doocs.org/lc/438/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0400-0499/0438.Find%20All%20Anagrams%20in%20a%20String/README.md)

### 题目要求
给定两个字符串 `s` 和 `p`，找到 `s` 中所有 `p` 的 异位词 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。

### 样例数据
样例 1:
```text
输入: s = "cbaebabacd", p = "abc"
输出: [0,6]
解释:
起始索引等于 0 的子串是 "cba", 它是 "abc" 的异位词。
起始索引等于 6 的子串是 "bac", 它是 "abc" 的异位词。
```

样例 2:
```text
输入: s = "abab", p = "ab"
输出: [0,1,2]
解释:
起始索引等于 0 的子串是 "ab", 它是 "ab" 的异位词。
起始索引等于 1 的子串是 "ba", 它是 "ab" 的异位词。
起始索引等于 2 的子串是 "ab", 它是 "ab" 的异位词。
```

### 核心思路
`方法一：滑动窗口`

我们不妨设字符串 s 的长度为 m，字符串 p 的长度为 n。 如果 m \lt n，那么 s 中不可能存在任何一个子串同 p 为异位词，返回空列表即可。 当 m \ge n 时，我们可以使用一个固定长度为 n 的滑动窗口来维护 s 的子串。 为了判断子串是否为 p 的异位词，我们可以用一个固定长度为 26 的数组 cnt1 记录 p 中每个字母的出现次数，再用另一个数组 cnt2 记录当前滑动窗口中每个字母的出现次数，如果这两个数组相同，那么当前滑动窗口的子串就是 p 的异位词，我们记录下起始位置。 其中 m 是字符串 s 的长度；而 C 是字符集大小，在本题中字符集为所有小写字母，所以 C = 26。

### 复杂度
时间复杂度 O(m \times C)，空间复杂度 O(C)。

### Java 代码
```java
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        int m = s.length(), n = p.length();
        List<Integer> ans = new ArrayList<>();
        if (m < n) {
            return ans;
        }
        int[] cnt1 = new int[26];
        for (int i = 0; i < n; ++i) {
            ++cnt1[p.charAt(i) - 'a'];
        }
        int[] cnt2 = new int[26];
        for (int i = 0; i < n - 1; ++i) {
            ++cnt2[s.charAt(i) - 'a'];
        }
        for (int i = n - 1; i < m; ++i) {
            ++cnt2[s.charAt(i) - 'a'];
            if (Arrays.equals(cnt1, cnt2)) {
                ans.add(i - n + 1);
            }
            --cnt2[s.charAt(i - n + 1) - 'a'];
        }
        return ans;
    }
}
```


### 解题模板

```
// 最长/最短子串型
int[] cnt = new int[128];  // 或 Map
for (int l = 0, r = 0; r < n; r++) {
    cnt[s.charAt(r)]++;
    while (不满足条件) { cnt[s.charAt(l++)]--; }
    ans = Math.max(ans, r - l + 1);  // 或 Math.min
}

// 固定窗口 + 异位词匹配型
int[] cnt1 = new int[26], cnt2 = new int[26];
for (int i = 0; i < n; i++) cnt1[p.charAt(i) - 'a']++;
for (int i = n - 1; i < m; i++) {
    cnt2[s.charAt(i) - 'a']++;
    if (Arrays.equals(cnt1, cnt2)) ans.add(i - n + 1);
    cnt2[s.charAt(i - n + 1) - 'a']--;
}
```

**识别信号**：最长/最短子串、窗口内去重/满足约束 → 滑动窗口（右扩左缩）。

---

## 四、子串 / 前缀和

**来源：LeetCode Hot 100**

<a id="p-560"></a>
## 560. 和为 K 的子数组

- 难度：中等
- 标签：数组、哈希表、前缀和
- 跳转：[官方题目](https://leetcode.cn/problems/subarray-sum-equals-k/) | [参考题解](https://leetcode.doocs.org/lc/560/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0500-0599/0560.Subarray%20Sum%20Equals%20K/README.md)

### 题目要求
给你一个整数数组 `nums` 和一个整数 `k` ，请你统计并返回 该数组中和为 `k` 的子数组的个数 。 子数组是数组中元素的连续非空序列。

### 样例数据
样例 1:
```text
输入：nums = [1,1,1], k = 2
输出：2
```

样例 2:
```text
输入：nums = [1,2,3], k = 3
输出：2
```

### 核心思路
`方法一：哈希表 + 前缀和`

我们定义一个哈希表 cnt，用于存储数组 nums 的前缀和出现的次数。 初始时，我们将 cnt[0] 的值设为 1，表示前缀和 0 出现了一次。 我们遍历数组 nums，计算前缀和 s，然后将 cnt[s - k] 的值累加到答案中，并将 cnt[s] 的值增加 1。 遍历结束后，我们返回答案。 其中 n 为数组 nums 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> cnt = new HashMap<>();
        cnt.put(0, 1);
        int ans = 0, s = 0;
        for (int x : nums) {
            s += x;
            ans += cnt.getOrDefault(s - k, 0);
            cnt.merge(s, 1, Integer::sum);
        }
        return ans;
    }
}
```

---

<a id="p-239"></a>
## 239. 滑动窗口最大值

- 难度：困难
- 标签：队列、数组、滑动窗口、单调队列、堆（优先队列）
- 跳转：[官方题目](https://leetcode.cn/problems/sliding-window-maximum/) | [参考题解](https://leetcode.doocs.org/lc/239/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0239.Sliding%20Window%20Maximum/README.md)

### 题目要求
给你一个整数数组 `nums`，有一个大小为 `k` 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 `k` 个数字。滑动窗口每次只向右移动一位。 返回 滑动窗口中的最大值 。

### 样例数据
样例 1:
```text
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置 最大值
--------------- -----
[1 3 -1] -3 5 3 6 7 3
1 [3 -1 -3] 5 3 6 7 3
1 3 [-1 -3 5] 3 6 7 5
1 3 -1 [-3 5 3] 6 7 5
1 3 -1 -3 [5 3 6] 7 6
1 3 -1 -3 5 [3 6 7] 7
```

样例 2:
```text
输入：nums = [1], k = 1
输出：[1]
```

### 核心思路
`方法一：优先队列（大根堆）`

我们可以使用优先队列（大根堆）来维护滑动窗口中的最大值。 先将前 k-1 个元素加入优先队列，接下来从第 k 个元素开始，将新元素加入优先队列，同时判断堆顶元素是否滑出窗口，如果滑出窗口则将堆顶元素弹出。 然后我们将堆顶元素加入结果数组。 其中 n 为数组长度。

### 复杂度
时间复杂度 O(n \times \log k)，空间复杂度 O(k)。

### Java 代码
```java
class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        PriorityQueue<int[]> q
            = new PriorityQueue<>((a, b) -> a[0] == b[0] ? a[1] - b[1] : b[0] - a[0]);
        int n = nums.length;
        for (int i = 0; i < k - 1; ++i) {
            q.offer(new int[] {nums[i], i});
        }
        int[] ans = new int[n - k + 1];
        for (int i = k - 1, j = 0; i < n; ++i) {
            q.offer(new int[] {nums[i], i});
            while (q.peek()[1] <= i - k) {
                q.poll();
            }
            ans[j++] = q.peek()[0];
        }
        return ans;
    }
}
```

---

<a id="p-76"></a>
## 76. 最小覆盖子串

- 难度：困难
- 标签：哈希表、字符串、滑动窗口
- 跳转：[官方题目](https://leetcode.cn/problems/minimum-window-substring/) | [参考题解](https://leetcode.doocs.org/lc/76/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0076.Minimum%20Window%20Substring/README.md)

### 题目要求
给定两个字符串 `s` 和 `t`，长度分别是 `m` 和 `n`，返回 s 中的 最短窗口 子串，使得该子串包含 `t` 中的每一个字符（包括重复字符）。如果没有这样的子串，返回空字符串 `""`。 测试用例保证答案唯一。

### 样例数据
样例 1:
```text
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最小覆盖子串 "BANC" 包含来自字符串 t 的 'A'、'B' 和 'C'。
```

样例 2:
```text
输入：s = "a", t = "a"
输出："a"
解释：整个字符串 s 是最小覆盖子串。
```

### 核心思路
`方法一：计数 + 双指针`

我们用一个哈希表或数组 need 统计字符串 t 中每个字符出现的次数，用另一个哈希表或数组 window 统计滑动窗口中每个字符出现的次数。 另外，定义两个指针 l 和 r 分别指向窗口的左右边界，变量 cnt 表示窗口中已经包含了 t 中的多少个字符，变量 k 和 mi 分别表示最小覆盖子串的起始位置和长度。 我们从左到右遍历字符串 s，对于当前遍历到的字符 s[r]：

- 我们将其加入窗口中，即 window[s[r]] = window[s[r]] + 1，如果此时 need[s[r]] \geq window[s[r]]，则说明 s[r] 是一个「必要的字符」，我们将 cnt 加一。 - 如果 cnt 等于 t 的长度，说明此时窗口中已经包含了 t 中的所有字符，我们就可以尝试更新最小覆盖子串的起始位置和长度了。 如果 r - l + 1 < mi，说明当前窗口表示的子串更短，我们就更新 mi = r - l + 1 和 k = l。 - 然后，我们尝试移动左边界 l，如果此时 need[s[l]] \geq window[s[l]]，则说明 s[l] 是一个「必要的字符」，移动左边界时会把 s[l] 这个字符从窗口中移除，因此我们需要将 cnt 减一，然后更新 window[s[l]] = window[s[l]] - 1，并将 l 右移一位。 - 如果 cnt 与 t 的长度不相等，说明此时窗口中还没有包含 t 中的所有字符，我们就不需要移动左边界了，直接将 r 右移一位，继续遍历即可。 遍历结束，如果没有找到最小覆盖子串，返回空字符串，否则返回 s[k:k+mi] 即可。 其中 m 和 n 分别是字符串 s 和 t 的长度；而 |\Sigma| 是字符集的大小，本题中 |\Sigma| = 128。

### 复杂度
时间复杂度 O(m + n)，空间复杂度 O(|\Sigma|)。

### Java 代码
```java
class Solution {
    public String minWindow(String s, String t) {
        int[] need = new int[128];
        int[] window = new int[128];
        for (char c : t.toCharArray()) {
            ++need[c];
        }
        int m = s.length(), n = t.length();
        int k = -1, mi = m + 1, cnt = 0;
        for (int l = 0, r = 0; r < m; ++r) {
            char c = s.charAt(r);
            if (++window[c] <= need[c]) {
                ++cnt;
            }
            while (cnt == n) {
                if (r - l + 1 < mi) {
                    mi = r - l + 1;
                    k = l;
                }
                c = s.charAt(l);
                if (window[c] <= need[c]) {
                    --cnt;
                }
                --window[c];
                ++l;
            }
        }
        return k < 0 ? "" : s.substring(k, k + mi);
    }
}
```


### 解题模板

```
// 前缀和 + 哈希表：和为 K 的子数组
Map<Integer, Integer> cnt = new HashMap<>();
cnt.put(0, 1);
int s = 0;
for (int x : nums) {
    s += x;
    ans += cnt.getOrDefault(s - k, 0);
    cnt.merge(s, 1, Integer::sum);
}

// 单调队列：滑动窗口最大值
// 最小覆盖子串：计数 + 双指针
```

**识别信号**：连续子数组和/个数 → 前缀和把区间问题变成两前缀状态之差。

---

## 五、数组

**来源：LeetCode Hot 100**

<a id="p-53"></a>
## 53. 最大子数组和

- 难度：中等
- 标签：数组、分治、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/maximum-subarray/) | [参考题解](https://leetcode.doocs.org/lc/53/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0053.Maximum%20Subarray/README.md)

### 题目要求
给你一个整数数组 `nums` ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。 子数组 是数组中的一个连续部分。

### 样例数据
样例 1:
```text
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
```

样例 2:
```text
输入：nums = [1]
输出：1
```

### 核心思路
`方法一：动态规划`

我们定义 f[i] 表示以元素 nums[i] 为结尾的连续子数组的最大和，初始时 f[0] = nums[0]，那么最终我们要求的答案即为 \max_{0 \leq i < n} f[i]。 考虑 f[i]，其中 i \geq 1，它的状态转移方程为：

$
f[i] = \max(f[i - 1] + nums[i], nums[i])

也即：

f[i] = \max(f[i - 1], 0) + nums[i]

由于 f[i] 只与 f[i - 1] 有关系，因此我们可以只用一个变量 f 来维护对于当前 f[i] 的值是多少，然后进行状态转移即可。 答案为 \max_{0 \leq i < n} f。

### 复杂度
时间复杂度 O(n)，其中 n 为数组 nums 的长度。 空间复杂度 O(1)$。

### Java 代码
```java
class Solution {
    public int maxSubArray(int[] nums) {
        int ans = nums[0];
        for (int i = 1, f = nums[0]; i < nums.length; ++i) {
            f = Math.max(f, 0) + nums[i];
            ans = Math.max(ans, f);
        }
        return ans;
    }
}
```

---

<a id="p-56"></a>
## 56. 合并区间

- 难度：中等
- 标签：数组、排序
- 跳转：[官方题目](https://leetcode.cn/problems/merge-intervals/) | [参考题解](https://leetcode.doocs.org/lc/56/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0056.Merge%20Intervals/README.md)

### 题目要求
以数组 `intervals` 表示若干个区间的集合，其中单个区间为 `intervals[i] = [starti, endi]` 。请你合并所有重叠的区间，并返回 一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间 。

### 样例数据
样例 1:
```text
输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
```

样例 2:
```text
输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。
```

### 核心思路
`方法一：排序 + 一次遍历`

我们可以将区间按照左端点升序排列，然后遍历区间进行合并操作。 具体的合并操作如下。 我们先将第一个区间加入答案，然后依次考虑之后的每个区间：

- 如果答案数组中最后一个区间的右端点小于当前考虑区间的左端点，说明两个区间不会重合，因此我们可以直接将当前区间加入答案数组末尾；
- 否则，说明两个区间重合，我们需要用当前区间的右端点更新答案数组中最后一个区间的右端点，将其置为二者的较大值。 最后，我们返回答案数组即可。 其中 n 为区间个数。

### 复杂度
时间复杂度 O(n \times \log n)，空间复杂度 O(\log n)。

### Java 代码
```java
class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
        int st = intervals[0][0], ed = intervals[0][1];
        List<int[]> ans = new ArrayList<>();
        for (int i = 1; i < intervals.length; ++i) {
            int s = intervals[i][0], e = intervals[i][1];
            if (ed < s) {
                ans.add(new int[] {st, ed});
                st = s;
                ed = e;
            } else {
                ed = Math.max(ed, e);
            }
        }
        ans.add(new int[] {st, ed});
        return ans.toArray(new int[ans.size()][]);
    }
}
```

---

<a id="p-189"></a>
## 189. 轮转数组

- 难度：中等
- 标签：数组、数学、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/rotate-array/) | [参考题解](https://leetcode.doocs.org/lc/189/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0189.Rotate%20Array/README.md)

### 题目要求
给定一个整数数组 `nums`，将数组中的元素向右轮转 `k` 个位置，其中 `k` 是非负数。

### 样例数据
样例 1:
```text
输入: nums = [1,2,3,4,5,6,7], k = 3
输出: `[5,6,7,1,2,3,4]`
解释:
向右轮转 1 步: `[7,1,2,3,4,5,6]`
向右轮转 2 步: `[6,7,1,2,3,4,5]
`向右轮转 3 步: `[5,6,7,1,2,3,4]`
```

样例 2:
```text
输入：nums = [-1,-100,3,99], k = 2
输出：[3,99,-1,-100]
解释:
向右轮转 1 步: [99,-1,-100,3]
向右轮转 2 步: [3,99,-1,-100]
```

### 核心思路
`方法一：三次翻转`

我们不妨记数组长度为 n，然后将 k 对 n 取模，得到实际需要旋转的步数 k。 接下来，我们进行三次翻转，即可得到最终结果：

1. 将整个数组翻转
2. 将前 k 个元素翻转
3. 将后 n - k 个元素翻转

举个例子，对于数组 [1, 2, 3, 4, 5, 6, 7], k = 3, n = 7, k \bmod n = 3。 1. 第一次翻转，将整个数组翻转，得到 [7, 6, 5, 4, 3, 2, 1]。 2. 第二次翻转，将前 k 个元素翻转，得到 [5, 6, 7, 4, 3, 2, 1]。 3. 第三次翻转，将后 n - k 个元素翻转，得到 [5, 6, 7, 1, 2, 3, 4]，即为最终结果。

### 复杂度
时间复杂度 O(n)，其中 n 为数组长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    private int[] nums;

    public void rotate(int[] nums, int k) {
        this.nums = nums;
        int n = nums.length;
        k %= n;
        reverse(0, n - 1);
        reverse(0, k - 1);
        reverse(k, n - 1);
    }

    private void reverse(int i, int j) {
        for (; i < j; ++i, --j) {
            int t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
    }
}
```

---

<a id="p-238"></a>
## 238. 除了自身以外数组的乘积

- 难度：中等
- 标签：数组、前缀和
- 跳转：[官方题目](https://leetcode.cn/problems/product-of-array-except-self/) | [参考题解](https://leetcode.doocs.org/lc/238/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0238.Product%20of%20Array%20Except%20Self/README.md)

### 题目要求
给你一个整数数组 `nums`，返回 数组 `answer` ，其中 `answer[i]` 等于 `nums` 中除了 `nums[i]` 之外其余各元素的乘积 。 题目数据 保证 数组 `nums`之中任意元素的全部前缀元素和后缀的乘积都在 32 位 整数范围内。 请 不要使用除法，且在 `O(n)` 时间复杂度内完成此题。

### 样例数据
样例 1:
```text
输入: nums = `[1,2,3,4]`
输出: `[24,12,8,6]`
```

样例 2:
```text
输入: nums = [-1,1,0,-3,3]
输出: [0,0,9,0,0]
```

### 核心思路
`方法一：两次遍历`

我们定义两个变量 left 和 right，分别表示当前元素左边所有元素的乘积和右边所有元素的乘积。 初始时 left=1, right=1。 定义一个长度为 n 的答案数组 ans。 我们先从左到右遍历数组，对于遍历到的第 i 个元素，我们用 left 更新 ans[i]，然后 left 乘以 nums[i]。 然后，我们从右到左遍历数组，对于遍历到的第 i 个元素，我们更新 ans[i] 为 ans[i] \times right，然后 right 乘以 nums[i]。 遍历结束后，返回答案数组 ans。

### 复杂度
时间复杂度 O(n)，其中 n 是数组 nums 的长度。 忽略答案数组的空间消耗，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] ans = new int[n];
        for (int i = 0, left = 1; i < n; ++i) {
            ans[i] = left;
            left *= nums[i];
        }
        for (int i = n - 1, right = 1; i >= 0; --i) {
            ans[i] *= right;
            right *= nums[i];
        }
        return ans;
    }
}
```

---

<a id="p-41"></a>
## 41. 缺失的第一个正数

- 难度：困难
- 标签：数组、哈希表
- 跳转：[官方题目](https://leetcode.cn/problems/first-missing-positive/) | [参考题解](https://leetcode.doocs.org/lc/41/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0041.First%20Missing%20Positive/README.md)

### 题目要求
给你一个未排序的整数数组 `nums` ，请你找出其中没有出现的最小的正整数。 请你实现时间复杂度为 `O(n)` 并且只使用常数级别额外空间的解决方案。

### 样例数据
样例 1:
```text
输入：nums = [1,2,0]
输出：3
解释：范围 [1,2] 中的数字都在数组中。
```

样例 2:
```text
输入：nums = [3,4,-1,1]
输出：2
解释：1 在数组中，但 2 没有。
```

### 核心思路
`方法一：原地交换`

我们假设数组 nums 长度为 n，那么最小的正整数一定在 [1, .., n + 1] 之间。 我们可以遍历数组，将数组中的每个数 x 交换到它应该在的位置上，即 x 应该在的位置为 x - 1。 如果 x 不在 [1, n + 1] 之间，那么我们就不用管它。 遍历结束后，我们再遍历数组，如果 i+1 不等于 nums[i]，那么 i+1 就是我们要找的最小的正整数。

### 复杂度
时间复杂度 O(n)，其中 n 是数组的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int firstMissingPositive(int[] nums) {
        int n = nums.length;
        for (int i = 0; i < n; ++i) {
            while (nums[i] > 0 && nums[i] <= n && nums[i] != nums[nums[i] - 1]) {
                swap(nums, i, nums[i] - 1);
            }
        }
        for (int i = 0; i < n; ++i) {
            if (nums[i] != i + 1) {
                return i + 1;
            }
        }
        return n + 1;
    }

    private void swap(int[] nums, int i, int j) {
        int t = nums[i];
        nums[i] = nums[j];
        nums[j] = t;
    }
}
```


### 解题模板

```
// Kadane 最大子数组和
int f = 0, ans = Integer.MIN_VALUE;
for (int x : nums) {
    f = Math.max(f, 0) + x;
    ans = Math.max(ans, f);
}

// 合并区间
Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
// 遍历合并重叠区间

// 旋转数组：三次翻转
// 缺失的第一个正数：原地哈希
```

**识别信号**：最大子数组和 → Kadane；区间操作 → 排序+合并；原地要求 → 索引映射。

---

## 六、矩阵

**来源：LeetCode Hot 100**

<a id="p-73"></a>
## 73. 矩阵置零

- 难度：中等
- 标签：数组、哈希表、矩阵
- 跳转：[官方题目](https://leetcode.cn/problems/set-matrix-zeroes/) | [参考题解](https://leetcode.doocs.org/lc/73/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0073.Set%20Matrix%20Zeroes/README.md)

### 题目要求
给定一个 `m x n` 的矩阵，如果一个元素为 0 ，则将其所在行和列的所有元素都设为 0 。请使用 原地 算法。

### 样例数据
样例 1:
```text
输入：matrix = [[1,1,1],[1,0,1],[1,1,1]]
输出：[[1,0,1],[0,0,0],[1,0,1]]
```

样例 2:
```text
输入：matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
输出：[[0,0,0,0],[0,4,5,0],[0,3,1,0]]
```

### 核心思路
`Solution 1: Array Marking`

Let the number of rows and columns of the matrix be m and n, respectively. We use an array rows of length m and an array cols of length n to record which rows and columns need to be set to zero.

First, we traverse the matrix. When we find a zero element in the matrix, we set the corresponding row and column markers to \text{true}. That is, if matrix[i][j] = 0, then rows[i] = cols[j] = \text{true}.

Finally, we traverse the matrix again and use the markers in rows and cols to update the elements in the matrix. When we find that rows[i] or cols[j] is \text{true}, we set matrix[i][j] to zero.

The time complexity is O(m \times n), and the space complexity is O(m + n). Here, m and n are the number of rows and columns of the matrix, respectively.

### Java 代码
```java
class Solution {
    public void setZeroes(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        boolean[] row = new boolean[m];
        boolean[] col = new boolean[n];
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (matrix[i][j] == 0) {
                    row[i] = col[j] = true;
                }
            }
        }
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (row[i] || col[j]) {
                    matrix[i][j] = 0;
                }
            }
        }
    }
}
```

---

<a id="p-54"></a>
## 54. 螺旋矩阵

- 难度：中等
- 标签：数组、矩阵、模拟
- 跳转：[官方题目](https://leetcode.cn/problems/spiral-matrix/) | [参考题解](https://leetcode.doocs.org/lc/54/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0054.Spiral%20Matrix/README.md)

### 题目要求
给你一个 `m` 行 `n` 列的矩阵 `matrix` ，请按照 顺时针螺旋顺序 ，返回矩阵中的所有元素。

### 样例数据
样例 1:
```text
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]
```

样例 2:
```text
输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出：[1,2,3,4,8,12,11,10,9,5,6,7]
```

### 核心思路
`方法一：模拟`

我们可以模拟整个遍历的过程，用 i 和 j 分别表示当前访问到的元素的行和列，用 k 表示当前的方向，用数组或哈希表 vis 记录每个元素是否被访问过。 每次我们访问到一个元素后，将其标记为已访问，然后按照当前的方向前进一步，如果前进一步后发现越界或者已经访问过，则改变方向继续前进，直到遍历完整个矩阵。 其中 m 和 n 分别是矩阵的行数和列数。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int[] dirs = {0, 1, 0, -1, 0};
        int i = 0, j = 0, k = 0;
        List<Integer> ans = new ArrayList<>();
        boolean[][] vis = new boolean[m][n];
        for (int h = m * n; h > 0; --h) {
            ans.add(matrix[i][j]);
            vis[i][j] = true;
            int x = i + dirs[k], y = j + dirs[k + 1];
            if (x < 0 || x >= m || y < 0 || y >= n || vis[x][y]) {
                k = (k + 1) % 4;
            }
            i += dirs[k];
            j += dirs[k + 1];
        }
        return ans;
    }
}
```

---

<a id="p-48"></a>
## 48. 旋转图像

- 难度：中等
- 标签：数组、数学、矩阵
- 跳转：[官方题目](https://leetcode.cn/problems/rotate-image/) | [参考题解](https://leetcode.doocs.org/lc/48/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0048.Rotate%20Image/README.md)

### 题目要求
给定一个 n × n 的二维矩阵 `matrix` 表示一个图像。请你将图像顺时针旋转 90 度。 你必须在 原地 旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要 使用另一个矩阵来旋转图像。

### 样例数据
样例 1:
```text
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]
```

样例 2:
```text
输入：matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
输出：[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
```

### 核心思路
`方法一：原地翻转`

根据题目要求，我们实际上需要将 \text{matrix}[i][j] 旋转至 \text{matrix}[j][n - i - 1]。 我们可以先对矩阵进行上下翻转，即 \text{matrix}[i][j] 和 \text{matrix}[n - i - 1][j] 进行交换，然后再对矩阵进行主对角线翻转，即 \text{matrix}[i][j] 和 \text{matrix}[j][i] 进行交换。 这样就能将 \text{matrix}[i][j] 旋转至 \text{matrix}[j][n - i - 1] 了。

### 复杂度
时间复杂度 O(n^2)，其中 n 是矩阵的边长。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int i = 0; i < n >> 1; ++i) {
            for (int j = 0; j < n; ++j) {
                int t = matrix[i][j];
                matrix[i][j] = matrix[n - i - 1][j];
                matrix[n - i - 1][j] = t;
            }
        }
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                int t = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = t;
            }
        }
    }
}
```

---

<a id="p-240"></a>
## 240. 搜索二维矩阵 II

- 难度：中等
- 标签：数组、二分查找、分治、矩阵
- 跳转：[官方题目](https://leetcode.cn/problems/search-a-2d-matrix-ii/) | [参考题解](https://leetcode.doocs.org/lc/240/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0240.Search%20a%202D%20Matrix%20II/README.md)

### 题目要求
编写一个高效的算法来搜索 `m x n` 矩阵 `matrix` 中的一个目标值 `target` 。该矩阵具有以下特性： - 每行的元素从左到右升序排列。 - 每列的元素从上到下升序排列。 示例 1：

### 样例数据
样例 1:
```text
输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
输出：true
```

样例 2:
```text
输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
输出：false
```

### 核心思路
`方法一：二分查找`

由于每一行的所有元素升序排列，因此，对于每一行，我们可以使用二分查找找到第一个大于等于 target 的元素，然后判断该元素是否等于 target。 如果等于 target，说明找到了目标值，直接返回 \text{true}。 如果不等于 target，说明这一行的所有元素都小于 target，应该继续搜索下一行。 如果所有行都搜索完了，都没有找到目标值，说明目标值不存在，返回 \text{false}。

### 复杂度
时间复杂度 O(m \times \log n)，其中 m 和 n 分别为矩阵的行数和列数。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        for (var row : matrix) {
            int j = Arrays.binarySearch(row, target);
            if (j >= 0) {
                return true;
            }
        }
        return false;
    }
}
```


### 解题模板

```
// 矩阵置零：用第一行/第一列标记
// 螺旋遍历：四边界收缩
// 顺时针旋转：先转置再水平翻转
// 搜索二维矩阵 II：从右上角开始
int i = 0, j = n - 1;
while (i < m && j >= 0) {
    if (matrix[i][j] == target) return true;
    if (matrix[i][j] > target) j--; else i++;
}
```

**识别信号**：矩阵旋转 → 转置+翻转；矩阵搜索 → 从角上出发缩小范围。

---

## 七、链表

**来源：LeetCode Hot 100**

<a id="p-160"></a>
## 160. 相交链表

- 难度：简单
- 标签：哈希表、链表、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/intersection-of-two-linked-lists/) | [参考题解](https://leetcode.doocs.org/lc/160/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0160.Intersection%20of%20Two%20Linked%20Lists/README.md)

### 题目要求
给你两个单链表的头节点 `headA` 和 `headB` ，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回 `null` 。 图示两个链表在节点 `c1` 开始相交： 题目数据 保证 整个链式结构中不存在环。 注意，函数返回结果后，链表必须 保持其原始结构 。 自定义评测： 评测系统 的输入如下（你设计的程序 不适用 此输入）： - `intersectVal` - 相交的起始节点的值。如果不存在相交节点，这一值为 `0` - `listA` - 第一个链表 - `listB` - 第二个链表 - `skipA` - 在 `listA` 中（从头节点开始）跳到交叉节点的节点数 - `skipB` - 在 `listB` 中（从头节点开始）跳到交叉节点的节点数 评测系统将根据这些输入创建链式数据结构，并将两个头节点 `headA` 和 `headB` 传递给你的程序。如果程序能够正确返回相交节点，那么你的解决方案将被 视作正确答案 。

### 样例数据
样例 1:
```text
输入：intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3
输出：Intersected at '8'
解释：相交节点的值为 8 （注意，如果两个链表相交则不能为 0）。
从各自的表头开始算起，链表 A 为 [4,1,8,4,5]，链表 B 为 [5,6,1,8,4,5]。
在 A 中，相交节点前有 2 个节点；在 B 中，相交节点前有 3 个节点。
— 请注意相交节点的值不为 1，因为在链表 A 和链表 B 之中值为 1 的节点 (A 中第二个节点和 B 中第三个节点) 是不同的节点。换句话说，它们在内存中指向两个不同的位置，而链表 A 和链表 B 中值为 8 的节点 (A 中第三个节点，B 中第四个节点) 在内存中指向相同的位置。
```

样例 2:
```text
输入：intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
输出：Intersected at '2'
解释：相交节点的值为 2 （注意，如果两个链表相交则不能为 0）。
从各自的表头开始算起，链表 A 为 [1,9,1,2,4]，链表 B 为 [3,2,4]。
在 A 中，相交节点前有 3 个节点；在 B 中，相交节点前有 1 个节点。
```

### 核心思路
`方法一：双指针`

我们使用两个指针 a, b 分别指向两个链表 headA, headB。 同时遍历链表，当 a 到达链表 headA 的末尾时，重新定位到链表 headB 的头节点；当 b 到达链表 headB 的末尾时，重新定位到链表 headA 的头节点。 若两指针相遇，所指向的结点就是第一个公共节点。 若没相遇，说明两链表无公共节点，此时两个指针都指向 `null`，返回其中一个即可。

### 复杂度
时间复杂度 O(m + n)，其中 m 和 n 分别是链表 headA 和 headB 的长度。 空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode a = headA, b = headB;
        while (a != b) {
            a = a == null ? headB : a.next;
            b = b == null ? headA : b.next;
        }
        return a;
    }
}
```

---

<a id="p-206"></a>
## 206. 反转链表

- 难度：简单
- 标签：递归、链表
- 跳转：[官方题目](https://leetcode.cn/problems/reverse-linked-list/) | [参考题解](https://leetcode.doocs.org/lc/206/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0206.Reverse%20Linked%20List/README.md)

### 题目要求
给你单链表的头节点 `head` ，请你反转链表，并返回反转后的链表。

### 样例数据
样例 1:
```text
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
```

样例 2:
```text
输入：head = [1,2]
输出：[2,1]
```

### 核心思路
`方法一：头插法`

我们创建一个虚拟头节点 dummy，然后遍历链表，将每个节点依次插入 dummy 的下一个节点。 遍历结束，返回 dummy.next。

### 复杂度
时间复杂度 O(n)，其中 n 为链表的长度。 空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode dummy = new ListNode();
        ListNode curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = dummy.next;
            dummy.next = curr;
            curr = next;
        }
        return dummy.next;
    }
}
```

---

<a id="p-234"></a>
## 234. 回文链表

- 难度：简单
- 标签：栈、递归、链表、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/palindrome-linked-list/) | [参考题解](https://leetcode.doocs.org/lc/234/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0234.Palindrome%20Linked%20List/README.md)

### 题目要求
给你一个单链表的头节点 `head` ，请你判断该链表是否为回文链表。如果是，返回 `true` ；否则，返回 `false` 。

### 样例数据
样例 1:
```text
输入：head = [1,2,2,1]
输出：true
```

样例 2:
```text
输入：head = [1,2]
输出：false
```

### 核心思路
`方法一：快慢指针`

我们可以先用快慢指针找到链表的中点，接着反转右半部分的链表。 然后同时遍历前后两段链表，若前后两段链表节点对应的值不等，说明不是回文链表，否则说明是回文链表。

### 复杂度
时间复杂度 O(n)，其中 n 为链表的长度。 空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public boolean isPalindrome(ListNode head) {
        ListNode slow = head;
        ListNode fast = head.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode cur = slow.next;
        slow.next = null;
        ListNode pre = null;
        while (cur != null) {
            ListNode t = cur.next;
            cur.next = pre;
            pre = cur;
            cur = t;
        }
        while (pre != null) {
            if (pre.val != head.val) {
                return false;
            }
            pre = pre.next;
            head = head.next;
        }
        return true;
    }
}
```

---

<a id="p-141"></a>
## 141. 环形链表

- 难度：简单
- 标签：哈希表、链表、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/linked-list-cycle/) | [参考题解](https://leetcode.doocs.org/lc/141/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0141.Linked%20List%20Cycle/README.md)

### 题目要求
给你一个链表的头节点 `head` ，判断链表中是否有环。 如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（索引从 0 开始）。注意：`pos` 不作为参数进行传递 。仅仅是为了标识链表的实际情况。 如果链表中存在环 ，则返回 `true` 。 否则，返回 `false` 。

### 样例数据
样例 1:
```text
输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。
```

样例 2:
```text
输入：head = [1,2], pos = 0
输出：true
解释：链表中有一个环，其尾部连接到第一个节点。
```

### 核心思路
`方法一：哈希表`

我们可以遍历链表，用一个哈希表 s 记录每个节点。 当某个节点二次出现时，则表示存在环，直接返回 `true`。 否则链表遍历结束，返回 `false`。 其中 n 是链表中的节点数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public boolean hasCycle(ListNode head) {
        Set<ListNode> s = new HashSet<>();
        for (; head != null; head = head.next) {
            if (!s.add(head)) {
                return true;
            }
        }
        return false;
    }
}
```

---

<a id="p-142"></a>
## 142. 环形链表 II

- 难度：中等
- 标签：哈希表、链表、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/linked-list-cycle-ii/) | [参考题解](https://leetcode.doocs.org/lc/142/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0142.Linked%20List%20Cycle%20II/README.md)

### 题目要求
给定一个链表的头节点 `head` ，返回链表开始入环的第一个节点。 如果链表无环，则返回 `null`。 如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（索引从 0 开始）。如果 `pos` 是 `-1`，则在该链表中没有环。注意：`pos` 不作为参数进行传递，仅仅是为了标识链表的实际情况。 不允许修改 链表。

### 样例数据
样例 1:
```text
输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点
解释：链表中有一个环，其尾部连接到第二个节点。
```

样例 2:
```text
输入：head = [1,2], pos = 0
输出：返回索引为 0 的链表节点
解释：链表中有一个环，其尾部连接到第一个节点。
```

### 核心思路
`方法一：快慢指针`

我们先利用快慢指针判断链表是否有环，如果有环的话，快慢指针一定会相遇，且相遇的节点一定在环中。 如果没有环，快指针会先到达链表尾部，直接返回 `null` 即可。 如果有环，我们再定义一个答案指针 ans 指向链表头部，然后让 ans 和慢指针一起向前走，每次走一步，直到 ans 和慢指针相遇，相遇的节点即为环的入口节点。 为什么这样能找到环的入口节点呢？

我们不妨假设链表头节点到环入口的距离为 x，环入口到相遇节点的距离为 y，相遇节点到环入口的距离为 z，那么慢指针走过的距离为 x + y，快指针走过的距离为 x + y + k \times (y + z)，其中 k 是快指针在环中绕了 k 圈。 <p><img src="https://fastly.jsdelivr.net/gh/doocs/leetcode@main/solution/0100-0199/0142.Linked%20List%20Cycle%20II/images/linked-list-cycle-ii.png" /></p>

由于快指针速度是慢指针的 2 倍，因此有 2 \times (x + y) = x + y + k \times (y + z)，可以推出 x + y = k \times (y + z)，即 x = (k - 1) \times (y + z) + z。 也即是说，如果我们定义一个答案指针 ans 指向链表头部，然后 ans 和慢指针一起向前走，那么它们一定会在环入口相遇。

### 复杂度
时间复杂度 O(n)，其中 n 是链表中节点的数目。 空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode fast = head, slow = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                ListNode ans = head;
                while (ans != slow) {
                    ans = ans.next;
                    slow = slow.next;
                }
                return ans;
            }
        }
        return null;
    }
}
```

---

<a id="p-21"></a>
## 21. 合并两个有序链表

- 难度：简单
- 标签：递归、链表
- 跳转：[官方题目](https://leetcode.cn/problems/merge-two-sorted-lists/) | [参考题解](https://leetcode.doocs.org/lc/21/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0021.Merge%20Two%20Sorted%20Lists/README.md)

### 题目要求
将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。

### 样例数据
样例 1:
```text
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

样例 2:
```text
输入：l1 = [], l2 = []
输出：[]
```

### 核心思路
`方法一：递归`

我们先判断链表 l_1 和 l_2 是否为空，若其中一个为空，则返回另一个链表。 否则，我们比较 l_1 和 l_2 的头节点：

- 若 l_1 的头节点的值小于等于 l_2 的头节点的值，则递归调用函数 mergeTwoLists(l_1.next, l_2)，并将 l_1 的头节点与返回的链表头节点相连，返回 l_1 的头节点。 - 否则，递归调用函数 mergeTwoLists(l_1, l_2.next)，并将 l_2 的头节点与返回的链表头节点相连，返回 l_2 的头节点。 其中 m 和 n 分别为两个链表的长度。

### 复杂度
时间复杂度 O(m + n)，空间复杂度 O(m + n)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        if (list1 == null) {
            return list2;
        }
        if (list2 == null) {
            return list1;
        }
        if (list1.val <= list2.val) {
            list1.next = mergeTwoLists(list1.next, list2);
            return list1;
        } else {
            list2.next = mergeTwoLists(list1, list2.next);
            return list2;
        }
    }
}
```

---

<a id="p-2"></a>
## 2. 两数相加

- 难度：中等
- 标签：递归、链表、数学
- 跳转：[官方题目](https://leetcode.cn/problems/add-two-numbers/) | [参考题解](https://leetcode.doocs.org/lc/2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0002.Add%20Two%20Numbers/README.md)

### 题目要求
给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。 请你将两个数相加，并以相同形式返回一个表示和的链表。 你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

### 样例数据
样例 1:
```text
输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[7,0,8]
解释：342 + 465 = 807.
```

样例 2:
```text
输入：l1 = [0], l2 = [0]
输出：[0]
```

### 核心思路
`方法一：模拟`

我们同时遍历两个链表 l_1 和 l_2，并使用变量 carry 表示当前是否有进位。 每次遍历时，我们取出对应链表的当前位，计算它们与进位 carry 的和，然后更新进位的值，最后将当前位的值加入答案链表。 如果两个链表都遍历完了，并且进位为 0 时，遍历结束。 最后我们返回答案链表的头节点即可。 我们需要遍历两个链表的全部位置，而处理每个位置只需要 O(1) 的时间。

### 复杂度
时间复杂度 O(\max(m, n))，其中 m 和 n 分别为两个链表的长度。 忽略答案的空间消耗，空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        int carry = 0;
        ListNode cur = dummy;
        while (l1 != null || l2 != null || carry != 0) {
            int s = (l1 == null ? 0 : l1.val) + (l2 == null ? 0 : l2.val) + carry;
            carry = s / 10;
            cur.next = new ListNode(s % 10);
            cur = cur.next;
            l1 = l1 == null ? null : l1.next;
            l2 = l2 == null ? null : l2.next;
        }
        return dummy.next;
    }
}
```

---

<a id="p-19"></a>
## 19. 删除链表的倒数第 N 个结点

- 难度：中等
- 标签：链表、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/) | [参考题解](https://leetcode.doocs.org/lc/19/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0019.Remove%20Nth%20Node%20From%20End%20of%20List/README.md)

### 题目要求
给你一个链表，删除链表的倒数第 `n` 个结点，并且返回链表的头结点。

### 样例数据
样例 1:
```text
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
```

样例 2:
```text
输入：head = [1], n = 1
输出：[]
```

### 核心思路
`方法一：快慢指针`

我们定义两个指针 `fast` 和 `slow`，初始时都指向链表的虚拟头结点 `dummy`。 接着 `fast` 指针先向前移动 n 步，然后 `fast` 和 `slow` 指针同时向前移动，直到 `fast` 指针到达链表的末尾。 此时 `slow.next` 指针指向的结点就是倒数第 `n` 个结点的前驱结点，将其删除即可。

### 复杂度
时间复杂度 O(n)，其中 n 为链表的长度。 空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0, head);
        ListNode fast = dummy, slow = dummy;
        while (n-- > 0) {
            fast = fast.next;
        }
        while (fast.next != null) {
            slow = slow.next;
            fast = fast.next;
        }
        slow.next = slow.next.next;
        return dummy.next;
    }
}
```

---

<a id="p-24"></a>
## 24. 两两交换链表中的节点

- 难度：中等
- 标签：递归、链表
- 跳转：[官方题目](https://leetcode.cn/problems/swap-nodes-in-pairs/) | [参考题解](https://leetcode.doocs.org/lc/24/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0024.Swap%20Nodes%20in%20Pairs/README.md)

### 题目要求
给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）。

### 样例数据
样例 1:
```text
输入：head = [1,2,3,4]
输出：[2,1,4,3]
```

样例 2:
```text
输入：head = []
输出：[]
```

### 核心思路
`方法一：递归`

我们可以通过递归的方式实现两两交换链表中的节点。 递归的终止条件是链表中没有节点，或者链表中只有一个节点，此时无法进行交换，直接返回该节点。 否则，我们递归交换链表 head.next.next，记交换后的头节点为 t，然后我们记 head 的下一个节点为 p，然后令 p 指向 head，而 head 指向 t，最后返回 p。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)，其中 n 是链表的长度。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode swapPairs(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode t = swapPairs(head.next.next);
        ListNode p = head.next;
        p.next = head;
        head.next = t;
        return p;
    }
}
```

---

<a id="p-25"></a>
## 25. K 个一组翻转链表

- 难度：困难
- 标签：递归、链表
- 跳转：[官方题目](https://leetcode.cn/problems/reverse-nodes-in-k-group/) | [参考题解](https://leetcode.doocs.org/lc/25/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0025.Reverse%20Nodes%20in%20k-Group/README.md)

### 题目要求
给你链表的头节点 `head` ，每 `k` 个节点一组进行翻转，请你返回修改后的链表。 `k` 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 `k` 的整数倍，那么请将最后剩余的节点保持原有顺序。 你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。

### 样例数据
样例 1:
```text
输入：head = [1,2,3,4,5], k = 2
输出：[2,1,4,3,5]
```

样例 2:
```text
输入：head = [1,2,3,4,5], k = 3
输出：[3,2,1,4,5]
```

### 核心思路
`方法一：模拟`

我们可以根据题意，模拟整个翻转的过程。 首先，我们定义一个辅助函数 reverse，用于翻转一个链表。 然后，我们定义一个虚拟头结点 dummy，并将其 next 指针指向 head。 接着，我们遍历链表，每次遍历 k 个节点，若剩余节点不足 k 个，则不进行翻转。 否则，我们将 k 个节点取出，然后调用 reverse 函数翻转这 k 个节点。 然后将翻转后的链表与原链表连接起来。 继续遍历下一个 k 个节点，直到遍历完整个链表。

### 复杂度
时间复杂度 O(n)，其中 n 为链表的长度。 空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        ListNode dummy = new ListNode(0, head);
        dummy.next = head;
        ListNode pre = dummy;
        while (pre != null) {
            ListNode cur = pre;
            for (int i = 0; i < k; i++) {
                cur = cur.next;
                if (cur == null) {
                    return dummy.next;
                }
            }
            ListNode node = pre.next;
            ListNode nxt = cur.next;
            cur.next = null;
            pre.next = reverse(node);
            node.next = nxt;
            pre = node;
        }
        return dummy.next;
    }

    private ListNode reverse(ListNode head) {
        ListNode dummy = new ListNode();
        ListNode cur = head;
        while (cur != null) {
            ListNode nxt = cur.next;
            cur.next = dummy.next;
            dummy.next = cur;
            cur = nxt;
        }
        return dummy.next;
    }
}
```

---

<a id="p-138"></a>
## 138. 随机链表的复制

- 难度：中等
- 标签：哈希表、链表
- 跳转：[官方题目](https://leetcode.cn/problems/copy-list-with-random-pointer/) | [参考题解](https://leetcode.doocs.org/lc/138/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0138.Copy%20List%20with%20Random%20Pointer/README.md)

### 题目要求
给你一个长度为 `n` 的链表，每个节点包含一个额外增加的随机指针 `random` ，该指针可以指向链表中的任何节点或空节点。 构造这个链表的 深拷贝。 深拷贝应该正好由 `n` 个 全新 节点组成，其中每个新节点的值都设为其对应的原节点的值。新节点的 `next` 指针和 `random` 指针也都应指向复制链表中的新节点，并使原链表和复制链表中的这些指针能够表示相同的链表状态。复制链表中的指针都不应指向原链表中的节点 。 例如，如果原链表中有 `X` 和 `Y` 两个节点，其中 `X.random --> Y` 。那么在复制链表中对应的两个节点 `x` 和 `y` ，同样有 `x.random --> y` 。 返回复制链表的头节点。 用一个由 `n` 个节点组成的链表来表示输入/输出中的链表。每个节点用一个 `[val, random_index]` 表示： - `val`：一个表示 `Node.val` 的整数。 - `random_index`：随机指针指向的节点索引（范围从 `0` 到 `n-1`）；如果不指向任何节点，则为 `null` 。 你的代码 只 接受原链表的头节点 `head` 作为传入参数。

### 样例数据
样例 1:
```text
输入：head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
输出：[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

样例 2:
```text
输入：head = [[1,1],[2,1]]
输出：[[1,1],[2,1]]
```

### 核心思路
`方法一：哈希表 + 模拟`

我们可以定义一个虚拟头节点 dummy，用一个指针 tail 指向虚拟头节点，然后遍历链表，将链表中的每个节点都复制一份，并将每个节点及其复制节点的对应关系存储在哈希表 d 中，同时连接好复制节点的 next 指针。 接下来再遍历链表，根据哈希表中存储的对应关系，将复制节点的 random 指针连接好。 其中 n 为链表的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/*
// Definition for a Node.
class Node {
    int val;
    Node next;
    Node random;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.random = null;
    }
}
*/

class Solution {
    public Node copyRandomList(Node head) {
        Map<Node, Node> d = new HashMap<>();
        Node dummy = new Node(0);
        Node tail = dummy;
        for (Node cur = head; cur != null; cur = cur.next) {
            Node node = new Node(cur.val);
            tail.next = node;
            tail = node;
            d.put(cur, node);
        }
        for (Node cur = head; cur != null; cur = cur.next) {
            d.get(cur).random = cur.random == null ? null : d.get(cur.random);
        }
        return dummy.next;
    }
}
```

---

<a id="p-148"></a>
## 148. 排序链表

- 难度：中等
- 标签：链表、双指针、分治、排序、归并排序
- 跳转：[官方题目](https://leetcode.cn/problems/sort-list/) | [参考题解](https://leetcode.doocs.org/lc/148/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0148.Sort%20List/README.md)

### 题目要求
给你链表的头结点 `head` ，请将其按 升序 排列并返回 排序后的链表 。

### 样例数据
样例 1:
```text
输入：head = [4,2,1,3]
输出：[1,2,3,4]
```

样例 2:
```text
输入：head = [-1,5,3,4,0]
输出：[-1,0,3,4,5]
```

### 核心思路
`方法一：归并排序`

我们可以用归并排序的思想来解决。 首先，我们利用快慢指针找到链表的中点，将链表从中点处断开，形成两个独立的子链表 l1 和 l2。 然后，我们递归地对 l1 和 l2 进行排序，最后将 l1 和 l2 合并为一个有序链表。 其中 n 是链表的长度。

### 复杂度
时间复杂度 O(n \times \log n)，空间复杂度 O(\log n)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode slow = head, fast = head.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode l1 = head, l2 = slow.next;
        slow.next = null;
        l1 = sortList(l1);
        l2 = sortList(l2);
        ListNode dummy = new ListNode();
        ListNode tail = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                tail.next = l1;
                l1 = l1.next;
            } else {
                tail.next = l2;
                l2 = l2.next;
            }
            tail = tail.next;
        }
        tail.next = l1 != null ? l1 : l2;
        return dummy.next;
    }
}
```

---

<a id="p-23"></a>
## 23. 合并 K 个升序链表

- 难度：困难
- 标签：链表、分治、堆（优先队列）、归并排序
- 跳转：[官方题目](https://leetcode.cn/problems/merge-k-sorted-lists/) | [参考题解](https://leetcode.doocs.org/lc/23/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0023.Merge%20k%20Sorted%20Lists/README.md)

### 题目要求
给你一个链表数组，每个链表都已经按升序排列。 请你将所有链表合并到一个升序链表中，返回合并后的链表。

### 样例数据
样例 1:
```text
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
1->4->5,
1->3->4,
2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6
```

样例 2:
```text
输入：lists = []
输出：[]
```

### 核心思路
`方法一：优先队列（小根堆）`

我们可以创建一个小根堆来 pq 维护所有链表的头节点，每次从小根堆中取出值最小的节点，添加到结果链表的末尾，然后将该节点的下一个节点加入堆中，重复上述步骤直到堆为空。 其中 n 是所有链表节点数目的总和，而 k 是题目给定的链表数目。

### 复杂度
时间复杂度 O(n \times \log k)，空间复杂度 O(k)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
        for (ListNode head : lists) {
            if (head != null) {
                pq.offer(head);
            }
        }
        ListNode dummy = new ListNode();
        ListNode cur = dummy;
        while (!pq.isEmpty()) {
            ListNode node = pq.poll();
            if (node.next != null) {
                pq.offer(node.next);
            }
            cur.next = node;
            cur = cur.next;
        }
        return dummy.next;
    }
}
```

---

<a id="p-146"></a>
## 146. LRU 缓存

- 难度：中等
- 标签：设计、哈希表、链表、双向链表
- 跳转：[官方题目](https://leetcode.cn/problems/lru-cache/) | [参考题解](https://leetcode.doocs.org/lc/146/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0146.LRU%20Cache/README.md)

### 题目要求
请你设计并实现一个满足 LRU (最近最少使用) 缓存 约束的数据结构。 实现 `LRUCache` 类： - `LRUCache(int capacity)` 以 正整数 作为容量 `capacity` 初始化 LRU 缓存 - `int get(int key)` 如果关键字 `key` 存在于缓存中，则返回关键字的值，否则返回 `-1` 。 - `void put(int key, int value)` 如果关键字 `key` 已经存在，则变更其数据值 `value` ；如果不存在，则向缓存中插入该组 `key-value` 。如果插入操作导致关键字数量超过 `capacity` ，则应该 逐出 最久未使用的关键字。 函数 `get` 和 `put` 必须以 `O(1)` 的平均时间复杂度运行。

### 样例数据
样例 1:
```text
输入
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
输出
[null, null, null, 1, null, -1, null, -1, 3, 4]
解释
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // 缓存是 {1=1}
lRUCache.put(2, 2); // 缓存是 {1=1, 2=2}
lRUCache.get(1); // 返回 1
lRUCache.put(3, 3); // 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}
lRUCache.get(2); // 返回 -1 (未找到)
lRUCache.put(4, 4); // 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}
lRUCache.get(1); // 返回 -1 (未找到)
lRUCache.get(3); // 返回 3
lRUCache.get(4); // 返回 4
```

### 核心思路
`方法一：哈希表 + 双向链表`

我们可以用“哈希表”和“双向链表”实现一个 LRU 缓存。 - 哈希表：用于存储 key 和对应的节点位置。 - 双向链表：用于存储节点数据，按照访问时间排序。 当访问一个节点时，如果节点存在，我们将其从原来的位置删除，并重新插入到链表头部。 这样就能保证链表尾部存储的就是最近最久未使用的节点，当节点数量大于缓存最大空间时就淘汰链表尾部的节点。 当插入一个节点时，如果节点存在，我们将其从原来的位置删除，并重新插入到链表头部。 如果不存在，我们首先检查缓存是否已满，如果已满，则删除链表尾部的节点，将新的节点插入链表头部。

### 复杂度
时间复杂度 O(1)，空间复杂度 O(capacity)。

### Java 代码
```java
class Node {
    int key, val;
    Node prev, next;

    Node() {
    }

    Node(int key, int val) {
        this.key = key;
        this.val = val;
    }
}

class LRUCache {
    private int size;
    private int capacity;
    private Node head = new Node();
    private Node tail = new Node();
    private Map<Integer, Node> cache = new HashMap<>();

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!cache.containsKey(key)) {
            return -1;
        }
        Node node = cache.get(key);
        removeNode(node);
        addToHead(node);
        return node.val;
    }

    public void put(int key, int value) {
        if (cache.containsKey(key)) {
            Node node = cache.get(key);
            removeNode(node);
            node.val = value;
            addToHead(node);
        } else {
            Node node = new Node(key, value);
            cache.put(key, node);
            addToHead(node);
            if (++size > capacity) {
                node = tail.prev;
                cache.remove(node.key);
                removeNode(node);
                --size;
            }
        }
    }

    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addToHead(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next = node;
        node.next.prev = node;
    }
}

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache obj = new LRUCache(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */
```


**来源：剑指 Offer**

<a id="offer-6"></a>
## 剑指 Offer 06. 从尾到头打印链表

- 难度：简单
- 标签：链表
- 跳转：[官方题目](https://leetcode.cn/problems/cong-wei-dao-tou-da-yin-lian-biao-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/6/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9806.%20%E4%BB%8E%E5%B0%BE%E5%88%B0%E5%A4%B4%E6%89%93%E5%8D%B0%E9%93%BE%E8%A1%A8/README.md)

### 题目要求
输入一个链表的头节点，从尾到头反过来返回每个节点的值（用数组返回）。

### 样例数据
样例 1:
```text
输入：head = [1,3,2]
输出：[2,3,1]
```

### 核心思路
`方法一：顺序遍历 + 反转`

我们可以顺序遍历链表，将每个节点的值存入数组中，然后将数组反转。 其中 n 为链表的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    public int[] reversePrint(ListNode head) {
        Deque<Integer> stk = new ArrayDeque<>();
        for (; head != null; head = head.next) {
            stk.push(head.val);
        }
        int[] ans = new int[stk.size()];
        for (int i = 0; !stk.isEmpty(); ++i) {
            ans[i] = stk.pop();
        }
        return ans;
    }
}
```

---

<a id="offer-18"></a>
## 剑指 Offer 18. 删除链表的节点

- 难度：简单
- 标签：链表
- 跳转：[官方题目](https://leetcode.cn/problems/shan-chu-lian-biao-de-jie-dian-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/18/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9818.%20%E5%88%A0%E9%99%A4%E9%93%BE%E8%A1%A8%E7%9A%84%E8%8A%82%E7%82%B9/README.md)

### 题目要求
给定单向链表的头指针和一个要删除的节点的值，定义一个函数删除该节点。 返回删除后的链表的头节点。 注意：此题对比原题有改动

### 样例数据
样例 1:
```text
输入: head = [4,5,1,9], val = 5
输出: [4,1,9]
解释: 给定你链表中值为 5 的第二个节点，那么在调用了你的函数之后，该链表应变为 4 -> 1 -> 9.
```

样例 2:
```text
输入: head = [4,5,1,9], val = 1
输出: [4,5,9]
解释: 给定你链表中值为 1 的第三个节点，那么在调用了你的函数之后，该链表应变为 4 -> 5 -> 9.
```

### 核心思路
`方法一：模拟`

我们先创建一个虚拟头节点 `dummy`，令 `dummy.next = head`，然后创建一个指针 `cur` 指向 `dummy`。 遍历链表，当 `cur.next.val == val` 时，将 `cur.next` 指向 `cur.next.next`，然后跳出循环。 最后返回 `dummy.next` 即可。 其中 n 为链表的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    public ListNode deleteNode(ListNode head, int val) {
        ListNode dummy = new ListNode(0, head);
        for (ListNode cur = dummy; cur.next != null; cur = cur.next) {
            if (cur.next.val == val) {
                cur.next = cur.next.next;
                break;
            }
        }
        return dummy.next;
    }
}
```

---

<a id="offer-22"></a>
## 剑指 Offer 22. 链表中倒数第k个节点

- 难度：简单
- 标签：链表
- 跳转：[官方题目](https://leetcode.cn/problems/lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/22/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9822.%20%E9%93%BE%E8%A1%A8%E4%B8%AD%E5%80%92%E6%95%B0%E7%AC%ACk%E4%B8%AA%E8%8A%82%E7%82%B9/README.md)

### 题目要求
输入一个链表，输出该链表中倒数第k个节点。为了符合大多数人的习惯，本题从1开始计数，即链表的尾节点是倒数第1个节点。 例如，一个链表有 `6` 个节点，从头节点开始，它们的值依次是 `1、2、3、4、5、6`。这个链表的倒数第 `3` 个节点是值为 `4` 的节点。

### 样例数据
样例 1:
```text
给定一个链表: 1->2->3->4->5, 和 k = 2.
返回链表 4->5.
```

### 核心思路
`方法一：快慢指针`

我们可以定义快慢指针 `fast` 和 `slow`，初始时均指向 `head`。 然后快指针 `fast` 先向前走 k 步，然后快慢指针同时向前走，直到快指针走到链表尾部，此时慢指针指向的节点就是倒数第 k 个节点。 其中 n 为链表长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    public ListNode getKthFromEnd(ListNode head, int k) {
        ListNode slow = head, fast = head;
        while (k-- > 0) {
            fast = fast.next;
        }
        while (fast != null) {
            slow = slow.next;
            fast = fast.next;
        }
        return slow;
    }
}
```

---

<a id="offer-24"></a>
## 剑指 Offer 24. 反转链表

- 难度：简单
- 标签：链表
- 跳转：[官方题目](https://leetcode.cn/problems/fan-zhuan-lian-biao-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/24/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9824.%20%E5%8F%8D%E8%BD%AC%E9%93%BE%E8%A1%A8/README.md)

### 题目要求
定义一个函数，输入一个链表的头节点，反转该链表并输出反转后链表的头节点。

### 样例数据
样例 1:
```text
输入: 1->2->3->4->5->NULL
输出: 5->4->3->2->1->NULL
```

### 核心思路
`方法一：头插法`

创建虚拟头节点 dummy，遍历链表，将每个节点依次插入 dummy 的下一个节点。 遍历结束，返回 dummy.next。 其中 n 为链表的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode dummy = new ListNode(0);
        ListNode curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = dummy.next;
            dummy.next = curr;
            curr = next;
        }
        return dummy.next;
    }
}
```

---

<a id="offer-25"></a>
## 剑指 Offer 25. 合并两个排序的链表

- 难度：简单
- 标签：链表
- 跳转：[官方题目](https://leetcode.cn/problems/he-bing-liang-ge-pai-xu-de-lian-biao-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/25/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9825.%20%E5%90%88%E5%B9%B6%E4%B8%A4%E4%B8%AA%E6%8E%92%E5%BA%8F%E7%9A%84%E9%93%BE%E8%A1%A8/README.md)

### 题目要求
输入两个递增排序的链表，合并这两个链表并使新链表中的节点仍然是递增排序的。

### 样例数据
样例 1:
```text
输入：1->2->4, 1->3->4
输出：1->1->2->3->4->4
```

### 核心思路
`方法一：迭代`

我们先创建一个虚拟头结点 `dummy`，然后创建一个指针 `cur` 指向 `dummy`。 接下来，循环比较 `l1` 和 `l2` 的值，将较小的值接在 `cur` 后面，然后将指针向后移动一位。 循环结束，将 `cur` 指向 `l1` 或者 `l2` 中剩余的部分。 最后返回 `dummy.next` 即可。 其中 m 和 n 分别为两个链表的长度。

### 复杂度
时间复杂度 O(m + n)，空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode cur = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                cur.next = l1;
                l1 = l1.next;
            } else {
                cur.next = l2;
                l2 = l2.next;
            }
            cur = cur.next;
        }
        cur.next = l1 == null ? l2 : l1;
        return dummy.next;
    }
}
```

---

<a id="offer-35"></a>
## 剑指 Offer 35. 复杂链表的复制

- 难度：中等
- 标签：链表
- 跳转：[官方题目](https://leetcode.cn/problems/fu-za-lian-biao-de-fu-zhi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/35/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9835.%20%E5%A4%8D%E6%9D%82%E9%93%BE%E8%A1%A8%E7%9A%84%E5%A4%8D%E5%88%B6/README.md)

### 题目要求
请实现 `copyRandomList` 函数，复制一个复杂链表。在复杂链表中，每个节点除了有一个 `next` 指针指向下一个节点，还有一个 `random` 指针指向链表中的任意节点或者 `null`。

### 样例数据
样例 1:
```text
输入：head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
输出：[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

样例 2:
```text
输入：head = [[1,1],[2,1]]
输出：[[1,1],[2,1]]
```

### 核心思路
`方法一：哈希表`

遍历链表，将链表中的每个节点都复制一份，然后将原节点和复制节点的对应关系存储在哈希表中，同时连接好复制节点的 next 指针。 接下来再遍历链表，根据哈希表中存储的对应关系，将复制节点的 random 指针连接好。 其中 n 为链表的长度。

### 复杂度
时间复杂度为 O(n)，空间复杂度为 O(n)。

### Java 代码
```java
/*
// Definition for a Node.
class Node {
    int val;
    Node next;
    Node random;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.random = null;
    }
}
*/
class Solution {
    public Node copyRandomList(Node head) {
        Map<Node, Node> d = new HashMap<>();
        Node dummy = new Node(0);
        Node tail = dummy;
        for (Node cur = head; cur != null; cur = cur.next) {
            tail.next = new Node(cur.val);
            tail = tail.next;
            d.put(cur, tail);
        }
        tail = dummy.next;
        for (Node cur = head; cur != null; cur = cur.next) {
            tail.random = d.get(cur.random);
            tail = tail.next;
        }
        return dummy.next;
    }
}
```

---

<a id="offer-36"></a>
## 剑指 Offer 36. 二叉搜索树与双向链表

- 难度：中等
- 标签：链表
- 跳转：[官方题目](https://leetcode.cn/problems/er-cha-sou-suo-shu-yu-shuang-xiang-lian-biao-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/36/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9836.%20%E4%BA%8C%E5%8F%89%E6%90%9C%E7%B4%A2%E6%A0%91%E4%B8%8E%E5%8F%8C%E5%90%91%E9%93%BE%E8%A1%A8/README.md)

### 题目要求
输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的循环双向链表。要求不能创建任何新的节点，只能调整树中节点指针的指向。 为了让您更好地理解问题，以下面的二叉搜索树为例： 我们希望将这个二叉搜索树转化为双向循环链表。链表中的每个节点都有一个前驱和后继指针。对于双向循环链表，第一个节点的前驱是最后一个节点，最后一个节点的后继是第一个节点。 下图展示了上面的二叉搜索树转化成的链表。“head” 表示指向链表中有最小元素的节点。 特别地，我们希望可以就地完成转换操作。当转化完成以后，树中节点的左指针需要指向前驱，树中节点的右指针需要指向后继。还需要返回链表中的第一个节点的指针。 注意：本题与主站 426 题相同：https://leetcode.cn/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/ 注意：此题对比原题有改动。

### 样例数据
样例 1:
```text
输入：root = [4,2,5,1,3]
输出：[1,2,3,4,5]
解释：下图显示了转化后的二叉搜索树，实线表示后继关系，虚线表示前驱关系。
```

样例 2:
```text
输入：root = [2,1,3]
输出：[1,2,3]
```

### 核心思路
`方法一：中序遍历`

二叉搜索树的中序遍历是有序序列，因此可以通过中序遍历得到有序序列，过程中构建双向链表。 遍历结束，将头节点和尾节点相连，返回头节点。 其中 n 为二叉搜索树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/*
// Definition for a Node.
class Node {
    public int val;
    public Node left;
    public Node right;

    public Node() {}

    public Node(int _val) {
        val = _val;
    }

    public Node(int _val,Node _left,Node _right) {
        val = _val;
        left = _left;
        right = _right;
    }
};
*/
class Solution {
    private Node head;
    private Node pre;

    public Node treeToDoublyList(Node root) {
        if (root == null) {
            return null;
        }
        dfs(root);
        head.left = pre;
        pre.right = head;
        return head;
    }

    private void dfs(Node root) {
        if (root == null) {
            return;
        }
        dfs(root.left);
        if (pre != null) {
            pre.right = root;
        } else {
            head = root;
        }
        root.left = pre;
        pre = root;
        dfs(root.right);
    }
}
```

---

<a id="offer-52"></a>
## 剑指 Offer 52. 两个链表的第一个公共节点

- 难度：简单
- 标签：链表
- 跳转：[官方题目](https://leetcode.cn/problems/liang-ge-lian-biao-de-di-yi-ge-gong-gong-jie-dian-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/52/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9852.%20%E4%B8%A4%E4%B8%AA%E9%93%BE%E8%A1%A8%E7%9A%84%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%85%AC%E5%85%B1%E8%8A%82%E7%82%B9/README.md)

### 题目要求
输入两个链表，找出它们的第一个公共节点。 如下面的两个链表： 在节点 c1 开始相交。

### 样例数据
样例 1:
```text
输入：intersectVal = 8, listA = [4,1,8,4,5], listB = [5,0,1,8,4,5], skipA = 2, skipB = 3
输出：Reference of the node with value = 8
输入解释：相交节点的值为 8 （注意，如果两个列表相交则不能为 0）。从各自的表头开始算起，链表 A 为 [4,1,8,4,5]，链表 B 为 [5,0,1,8,4,5]。在 A 中，相交节点前有 2 个节点；在 B 中，相交节点前有 3 个节点。
```

样例 2:
```text
输入：intersectVal = 2, listA = [0,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
输出：Reference of the node with value = 2
输入解释：相交节点的值为 2 （注意，如果两个列表相交则不能为 0）。从各自的表头开始算起，链表 A 为 [0,9,1,2,4]，链表 B 为 [3,2,4]。在 A 中，相交节点前有 3 个节点；在 B 中，相交节点前有 1 个节点。
```

### 核心思路
`方法一：双指针`

我们可以用两个指针 a 和 b 分别指向两个链表的头节点，然后同时分别向后遍历，当 a 到达链表 A 的末尾时，令 a 指向链表 B 的头节点；当 b 到达链表 B 的末尾时，令 b 指向链表 A 的头节点。 这样，当它们相遇时，所指向的节点就是第一个公共节点。

### 复杂度
时间复杂度 O(m + n)，其中 m 和 n 分别为两个链表的长度。 空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
class Solution {
    ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode a = headA, b = headB;
        while (a != b) {
            a = a == null ? headB : a.next;
            b = b == null ? headA : b.next;
        }
        return a;
    }
}
```


### 解题模板

```
// 反转链表
ListNode prev = null, curr = head;
while (curr != null) {
    ListNode next = curr.next;
    curr.next = prev;
    prev = curr;
    curr = next;
}

// 快慢指针判环
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next; fast = fast.next.next;
    if (slow == fast) return true;
}

// 合并/交点：哑节点 + 双指针
// K 个一组翻转：递归 or 迭代
```

**识别信号**：链表题优先想快慢指针、哑节点、递归反转。

---

## 八、栈与队列

**来源：LeetCode Hot 100**

<a id="p-20"></a>
## 20. 有效的括号

- 难度：简单
- 标签：栈、字符串
- 跳转：[官方题目](https://leetcode.cn/problems/valid-parentheses/) | [参考题解](https://leetcode.doocs.org/lc/20/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0020.Valid%20Parentheses/README.md)

### 题目要求
给定一个只包括 `'('`，`')'`，`'{'`，`'}'`，`'['`，`']'` 的字符串 `s` ，判断字符串是否有效。 有效字符串需满足： - 左括号必须用相同类型的右括号闭合。 - 左括号必须以正确的顺序闭合。 - 每个右括号都有一个对应的相同类型的左括号。

### 样例数据
样例 1:
```text
输入：s = "()"
输出：true
```

样例 2:
```text
输入：s = "()[]{}"
输出：true
```

### 核心思路
`方法一：栈`

遍历括号字符串 s，遇到左括号时，压入当前的左括号；遇到右括号时，弹出栈顶元素（若栈为空，直接返回 `false`），判断是否匹配，若不匹配，直接返回 `false`。 也可以选择遇到左括号时，将右括号压入栈中；遇到右括号时，弹出栈顶元素（若栈为空，直接返回 `false`），判断是否是相等。 若不匹配，直接返回 `false`。 > 两者的区别仅限于括号转换时机，一个是在入栈时，一个是在出栈时。 遍历结束，若栈为空，说明括号字符串有效，返回 `true`；否则，返回 `false`。 其中 n 为括号字符串 s 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public boolean isValid(String s) {
        Deque<Character> stk = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') {
                stk.push(c);
            } else if (stk.isEmpty() || !match(stk.pop(), c)) {
                return false;
            }
        }
        return stk.isEmpty();
    }

    private boolean match(char l, char r) {
        return (l == '(' && r == ')') || (l == '{' && r == '}') || (l == '[' && r == ']');
    }
}
```

---

<a id="p-155"></a>
## 155. 最小栈

- 难度：中等
- 标签：栈、设计
- 跳转：[官方题目](https://leetcode.cn/problems/min-stack/) | [参考题解](https://leetcode.doocs.org/lc/155/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0155.Min%20Stack/README.md)

### 题目要求
设计一个支持 `push` ，`pop` ，`top` 操作，并能在常数时间内检索到最小元素的栈。 实现 `MinStack` 类: - `MinStack()` 初始化堆栈对象。 - `void push(int val)` 将元素val推入堆栈。 - `void pop()` 删除堆栈顶部的元素。 - `int top()` 获取堆栈顶部的元素。 - `int getMin()` 获取堆栈中的最小元素。

### 样例数据
样例 1:
```text
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]
输出：
[null,null,null,null,-3,null,0,-2]
解释：
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); --> 返回 -3.
minStack.pop();
minStack.top(); --> 返回 0.
minStack.getMin(); --> 返回 -2.
```

### 核心思路
`方法一：双栈`

我们用两个栈来实现，其中 `stk1` 用来存储数据，`stk2` 用来存储当前栈中的最小值。 初始时，`stk2` 中存储一个极大值。 - 当我们向栈中压入一个元素 x 时，我们将 x 压入 `stk1`，并将 `min(x, stk2[-1])` 压入 `stk2`。 - 当我们从栈中弹出一个元素时，我们将 `stk1` 和 `stk2` 的栈顶元素都弹出。 - 当我们要获取当前栈中的栈顶元素时，我们只需要返回 `stk1` 的栈顶元素即可。 - 当我们要获取当前栈中的最小值时，我们只需要返回 `stk2` 的栈顶元素即可。

### 复杂度
每个操作的时间复杂度为 O(1)。 整体的空间复杂度为 O(n)，其中 n 为栈中元素的个数。

### Java 代码
```java
class MinStack {
    private Deque<Integer> stk1 = new ArrayDeque<>();
    private Deque<Integer> stk2 = new ArrayDeque<>();

    public MinStack() {
        stk2.push(Integer.MAX_VALUE);
    }

    public void push(int val) {
        stk1.push(val);
        stk2.push(Math.min(val, stk2.peek()));
    }

    public void pop() {
        stk1.pop();
        stk2.pop();
    }

    public int top() {
        return stk1.peek();
    }

    public int getMin() {
        return stk2.peek();
    }
}

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack obj = new MinStack();
 * obj.push(val);
 * obj.pop();
 * int param_3 = obj.top();
 * int param_4 = obj.getMin();
 */
```

---

<a id="p-394"></a>
## 394. 字符串解码

- 难度：中等
- 标签：栈、递归、字符串
- 跳转：[官方题目](https://leetcode.cn/problems/decode-string/) | [参考题解](https://leetcode.doocs.org/lc/394/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0300-0399/0394.Decode%20String/README.md)

### 题目要求
给定一个经过编码的字符串，返回它解码后的字符串。 编码规则为: `k[encoded_string]`，表示其中方括号内部的 `encoded_string` 正好重复 `k` 次。注意 `k` 保证为正整数。 你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的。 此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 `k` ，例如不会出现像 `3a` 或 `2[4]` 的输入。 测试用例保证输出的长度不会超过 `10^5`。

### 样例数据
样例 1:
```text
输入：s = "3[a]2[bc]"
输出："aaabcbc"
```

样例 2:
```text
输入：s = "3[a2[c]]"
输出："accaccacc"
```

### 核心思路
`方法一`

优先按题目所属专题套用对应模板，再处理边界。

### Java 代码
```java
class Solution {
    public String decodeString(String s) {
        Deque<Integer> s1 = new ArrayDeque<>();
        Deque<String> s2 = new ArrayDeque<>();
        int num = 0;
        String res = "";
        for (char c : s.toCharArray()) {
            if ('0' <= c && c <= '9') {
                num = num * 10 + c - '0';
            } else if (c == '[') {
                s1.push(num);
                s2.push(res);
                num = 0;
                res = "";
            } else if (c == ']') {
                StringBuilder t = new StringBuilder();
                for (int i = 0, n = s1.pop(); i < n; ++i) {
                    t.append(res);
                }
                res = s2.pop() + t.toString();
            } else {
                res += String.valueOf(c);
            }
        }
        return res;
    }
}
```

---

<a id="p-739"></a>
## 739. 每日温度

- 难度：中等
- 标签：栈、数组、单调栈
- 跳转：[官方题目](https://leetcode.cn/problems/daily-temperatures/) | [参考题解](https://leetcode.doocs.org/lc/739/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0700-0799/0739.Daily%20Temperatures/README.md)

### 题目要求
给定一个整数数组 `temperatures` ，表示每天的温度，返回一个数组 `answer` ，其中 `answer[i]` 是指对于第 `i` 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 `0` 来代替。

### 样例数据
样例 1:
```text
输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]
```

样例 2:
```text
输入: temperatures = [30,40,50,60]
输出: [1,1,1,0]
```

### 核心思路
`方法一：单调栈`

本题需要我们找出每个元素右边第一个比它大的元素的位置，这是一个典型的单调栈应用场景。 我们从右往左遍历数组 temperatures，维护一个从栈顶到栈底温度单调递增的栈 stk，栈中存储的是数组元素的下标。 对于每个元素 temperatures[i]，我们不断将其与栈顶元素进行比较，如果栈顶元素对应的温度小于等于 temperatures[i]，那么循环将栈顶元素弹出，直到栈为空或者栈顶元素对应的温度大于 temperatures[i]。 此时，栈顶元素就是右边第一个比 temperatures[i] 大的元素，距离为 stk.top() - i，我们更新答案数组。 然后将 temperatures[i] 入栈，继续遍历。 遍历结束后，返回答案数组即可。 其中 n 为数组 temperatures 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        Deque<Integer> stk = new ArrayDeque<>();
        int[] ans = new int[n];
        for (int i = n - 1; i >= 0; --i) {
            while (!stk.isEmpty() && temperatures[stk.peek()] <= temperatures[i]) {
                stk.pop();
            }
            if (!stk.isEmpty()) {
                ans[i] = stk.peek() - i;
            }
            stk.push(i);
        }
        return ans;
    }
}
```

---

<a id="p-84"></a>
## 84. 柱状图中最大的矩形

- 难度：困难
- 标签：栈、数组、单调栈
- 跳转：[官方题目](https://leetcode.cn/problems/largest-rectangle-in-histogram/) | [参考题解](https://leetcode.doocs.org/lc/84/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0084.Largest%20Rectangle%20in%20Histogram/README.md)

### 题目要求
给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。 求在该柱状图中，能够勾勒出来的矩形的最大面积。

### 样例数据
样例 1:
```text
输入：heights = [2,1,5,6,2,3]
输出：10
解释：最大的矩形为图中红色区域，面积为 10
```

样例 2:
```text
输入： heights = [2,4]
输出： 4
```

### 核心思路
`方法一：单调栈`

我们可以枚举每根柱子的高度 h 作为矩形的高度，利用单调栈，向左右两边找第一个高度小于 h 的下标 left_i, right_i。 那么此时矩形面积为 h \times (right_i-left_i-1)，求最大值即可。 其中 n 表示 heights 的长度。 单调栈常见模型：找出每个数左/右边**离它最近的**且**比它大/小的数**。 模板：

```python
stk = []
for i in range(n):
    while stk and check(stk[-1], i):
        stk.pop()
    stk.append(i)
```

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int largestRectangleArea(int[] heights) {
        int res = 0, n = heights.length;
        Deque<Integer> stk = new ArrayDeque<>();
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        for (int i = 0; i < n; ++i) {
            while (!stk.isEmpty() && heights[stk.peek()] >= heights[i]) {
                right[stk.pop()] = i;
            }
            left[i] = stk.isEmpty() ? -1 : stk.peek();
            stk.push(i);
        }
        for (int i = 0; i < n; ++i) {
            res = Math.max(res, heights[i] * (right[i] - left[i] - 1));
        }
        return res;
    }
}
```


**来源：剑指 Offer**

<a id="offer-9"></a>
## 剑指 Offer 09. 用两个栈实现队列

- 难度：简单
- 标签：栈与队列
- 跳转：[官方题目](https://leetcode.cn/problems/yong-liang-ge-zhan-shi-xian-dui-lie-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/9/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9809.%20%E7%94%A8%E4%B8%A4%E4%B8%AA%E6%A0%88%E5%AE%9E%E7%8E%B0%E9%98%9F%E5%88%97/README.md)

### 题目要求
用两个栈实现一个队列。队列的声明如下，请实现它的两个函数 `appendTail` 和 `deleteHead` ，分别完成在队列尾部插入整数和在队列头部删除整数的功能。(若队列中没有元素，`deleteHead` 操作返回 -1 )

### 样例数据
样例 1:
```text
输入：
["CQueue","appendTail","deleteHead","deleteHead"]
[[],[3],[],[]]
输出：[null,null,3,-1]
```

样例 2:
```text
输入：
["CQueue","deleteHead","appendTail","appendTail","deleteHead","deleteHead"]
[[],[],[5],[2],[],[]]
输出：[null,-1,null,null,5,2]
```

### 核心思路
`方法一：双栈`

我们可以使用两个栈来实现队列，其中一个栈 `stk1` 用来存储输入的元素，另一个栈 `stk2` 用来输出元素。 当调用 `appendTail()` 方法时，我们将元素压入 `stk1` 中。 当调用 `deleteHead()` 方法时，如果此时栈 `stk2` 为空，我们将栈 `stk1` 中的元素逐个弹出并压入栈 `stk2` 中，然后弹出栈 `stk2` 的栈顶元素即可。 如果此时栈 `stk2` 不为空，我们直接弹出栈 `stk2` 的栈顶元素即可。 如果两个栈都为空，说明队列中没有元素，返回 `-1`。 其中 n 为队列中的元素个数。

### 复杂度
时间复杂度上，对于 `appendTail()` 方法，时间复杂度为 O(1)；对于 `deleteHead()` 方法，时间复杂度为 O(n)；空间复杂度为 O(n)。

### Java 代码
```java
class CQueue {
    private Deque<Integer> stk1 = new ArrayDeque<>();
    private Deque<Integer> stk2 = new ArrayDeque<>();

    public CQueue() {
    }

    public void appendTail(int value) {
        stk1.push(value);
    }

    public int deleteHead() {
        if (stk2.isEmpty()) {
            while (!stk1.isEmpty()) {
                stk2.push(stk1.pop());
            }
        }
        return stk2.isEmpty() ? -1 : stk2.pop();
    }
}

/**
 * Your CQueue object will be instantiated and called as such:
 * CQueue obj = new CQueue();
 * obj.appendTail(value);
 * int param_2 = obj.deleteHead();
 */
```

---

<a id="offer-30"></a>
## 剑指 Offer 30. 包含min函数的栈

- 难度：简单
- 标签：栈与队列
- 跳转：[官方题目](https://leetcode.cn/problems/bao-han-minhan-shu-de-zhan-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/30/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9830.%20%E5%8C%85%E5%90%ABmin%E5%87%BD%E6%95%B0%E7%9A%84%E6%A0%88/README.md)

### 题目要求
定义栈的数据结构，请在该类型中实现一个能够得到栈的最小元素的 min 函数在该栈中，调用 min、push 及 pop 的时间复杂度都是 O(1)。

### 样例数据
样例 1:
```text
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.min(); --> 返回 -3.
minStack.pop();
minStack.top(); --> 返回 0.
minStack.min(); --> 返回 -2.
```

### 核心思路
`方法一：双栈`

我们用两个栈来实现，其中`stk1` 用来存储数据，`stk2` 用来存储当前栈中的最小值。 初始时，`stk2` 中存储一个极大值。 - 当我们向栈中压入一个元素 `x` 时，我们将 `x` 压入 `stk1`，并将 `min(x, stk2[-1])` 压入 `stk2`。 - 当我们从栈中弹出一个元素时，我们将 `stk1` 和 `stk2` 的栈顶元素都弹出。 - 当我们要获取当前栈中的栈顶元素时，我们只需要返回 `stk1` 的栈顶元素即可。 - 当我们要获取当前栈中的最小值时，我们只需要返回 `stk2` 的栈顶元素即可。

### 复杂度
时间复杂度：对于每个操作，时间复杂度均为 O(1)，空间复杂度 O(n)。

### Java 代码
```java
class MinStack {
    private Deque<Integer> stk1 = new ArrayDeque<>();
    private Deque<Integer> stk2 = new ArrayDeque<>();

    /** initialize your data structure here. */
    public MinStack() {
        stk2.push(Integer.MAX_VALUE);
    }

    public void push(int x) {
        stk1.push(x);
        stk2.push(Math.min(x, stk2.peek()));
    }

    public void pop() {
        stk1.pop();
        stk2.pop();
    }

    public int top() {
        return stk1.peek();
    }

    public int getMin() {
        return stk2.peek();
    }
}

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack obj = new MinStack();
 * obj.push(x);
 * obj.pop();
 * int param_3 = obj.top();
 * int param_4 = obj.getMin();
 */
```

---

<a id="offer-31"></a>
## 剑指 Offer 31. 栈的压入、弹出序列

- 难度：中等
- 标签：栈与队列
- 跳转：[官方题目](https://leetcode.cn/problems/zhan-de-ya-ru-dan-chu-xu-lie-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/31/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9831.%20%E6%A0%88%E7%9A%84%E5%8E%8B%E5%85%A5%E3%80%81%E5%BC%B9%E5%87%BA%E5%BA%8F%E5%88%97/README.md)

### 题目要求
输入两个整数序列，第一个序列表示栈的压入顺序，请判断第二个序列是否为该栈的弹出顺序。假设压入栈的所有数字均不相等。例如，序列 {1,2,3,4,5} 是某栈的压栈序列，序列 {4,5,3,2,1} 是该压栈序列对应的一个弹出序列，但 {4,3,5,1,2} 就不可能是该压栈序列的弹出序列。

### 样例数据
样例 1:
```text
输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
输出：true
解释：我们可以按以下顺序执行：
push(1), push(2), push(3), push(4), pop() -> 4,
push(5), pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1
```

样例 2:
```text
输入：pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
输出：false
解释：1 不能在 2 之前弹出。
```

### 核心思路
`方法一：栈模拟`

遍历 `pushed` 序列，将每个数 `v` 依次压入栈中，压入后检查这个数是不是 `popped` 序列中下一个要弹出的值，如果是就循环把栈顶元素弹出。 遍历结束，如果 `popped` 序列已经到末尾，说明是一个合法的序列，否则不是。 其中 n 是 `pushed` 序列的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public boolean validateStackSequences(int[] pushed, int[] popped) {
        Deque<Integer> stk = new ArrayDeque<>();
        int j = 0;
        for (int v : pushed) {
            stk.push(v);
            while (!stk.isEmpty() && stk.peek() == popped[j]) {
                stk.pop();
                ++j;
            }
        }
        return j == pushed.length;
    }
}
```

---

<a id="offer-59-2"></a>
## 剑指 Offer 59 - II. 队列的最大值

- 难度：中等
- 标签：栈与队列
- 跳转：[官方题目](https://leetcode.cn/problems/dui-lie-de-zui-da-zhi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/59.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9859%20-%20II.%20%E9%98%9F%E5%88%97%E7%9A%84%E6%9C%80%E5%A4%A7%E5%80%BC/README.md)

### 题目要求
请定义一个队列并实现函数 `max_value` 得到队列里的最大值，要求函数`max_value`、`push_back` 和 `pop_front` 的均摊时间复杂度都是O(1)。 若队列为空，`pop_front` 和 `max_value` 需要返回 -1

### 样例数据
样例 1:
```text
输入:
["MaxQueue","push_back","push_back","max_value","pop_front","max_value"]
[[],[1],[2],[],[],[]]
输出: [null,null,null,2,1,2]
```

样例 2:
```text
输入:
["MaxQueue","pop_front","max_value"]
[[],[],[]]
输出: [null,-1,-1]
```

### 核心思路
`方法一：双队列`

我们维护两个队列 q_1 和 q_2，其中 q_1 用于存储所有元素，而 q_2 用于存储当前队列中的最大值。 当获取队列中的最大值时，如果队列 q_2 不为空，则队列中的最大值即为 q_2 的队首元素；否则队列为空，返回 -1。 当向队列中添加元素时，我们需要将 q_2 弹出所有队尾元素小于当前元素的元素，然后将当前元素添加到 q_2 的队尾，最后将当前元素添加到 q_1 的队尾。 当从队列中弹出元素时，如果 q_1 为空，则返回 -1；否则，如果 q_1 的队首元素等于 q_2 的队首元素，则将 q_2 的队首元素弹出，然后将 q_1 的队首元素弹出；否则，只将 q_1 的队首元素弹出。 其中 n 为队列中的元素个数。

### 复杂度
以上操作的时间复杂度均为 O(1)，空间复杂度为 O(n)。

### Java 代码
```java
class MaxQueue {
    private Deque<Integer> q1 = new ArrayDeque<>();
    private Deque<Integer> q2 = new ArrayDeque<>();

    public MaxQueue() {
    }

    public int max_value() {
        return q2.isEmpty() ? -1 : q2.peek();
    }

    public void push_back(int value) {
        while (!q2.isEmpty() && q2.peekLast() < value) {
            q2.pollLast();
        }
        q1.offer(value);
        q2.offer(value);
    }

    public int pop_front() {
        if (q1.isEmpty()) {
            return -1;
        }
        int ans = q1.poll();
        if (q2.peek() == ans) {
            q2.poll();
        }
        return ans;
    }
}

/**
 * Your MaxQueue object will be instantiated and called as such:
 * MaxQueue obj = new MaxQueue();
 * int param_1 = obj.max_value();
 * obj.push_back(value);
 * int param_3 = obj.pop_front();
 */
```

---

<a id="offer-59-1"></a>
## 剑指 Offer 59 - I. 滑动窗口的最大值

- 难度：简单
- 标签：栈与队列
- 跳转：[官方题目](https://leetcode.cn/problems/hua-dong-chuang-kou-de-zui-da-zhi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/59.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9859%20-%20I.%20%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%E7%9A%84%E6%9C%80%E5%A4%A7%E5%80%BC/README.md)

### 题目要求
给定一个数组 `nums` 和滑动窗口的大小 `k`，请找出所有滑动窗口里的最大值。

### 样例数据
样例 1:
```text
输入: nums = `[1,3,-1,-3,5,3,6,7]`, 和 k = 3
输出: `[3,3,5,5,6,7]
解释:
`
滑动窗口的位置 最大值
--------------- -----
[1 3 -1] -3 5 3 6 7 3
1 [3 -1 -3] 5 3 6 7 3
1 3 [-1 -3 5] 3 6 7 5
1 3 -1 [-3 5 3] 6 7 5
1 3 -1 -3 [5 3 6] 7 6
1 3 -1 -3 5 [3 6 7] 7
```

### 核心思路
`方法一：单调队列`

单调队列常见模型：找出滑动窗口中的最大值/最小值。 其中 n 为数组长度。

### 复杂度
模板：

```python
q = deque()
for i in range(n):
    # 判断队头是否滑出窗口
    while q and checkout_out(q[0]):
        q.popleft()
    while q and check(q[-1]):
        q.pop()
    q.append(i)
```

时间复杂度 O(n)，空间复杂度 O(k)。

### Java 代码
```java
class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        int[] ans = new int[n - k + 1];
        Deque<Integer> q = new ArrayDeque<>();
        for (int i = 0; i < n; ++i) {
            if (!q.isEmpty() && i - q.peek() + 1 > k) {
                q.poll();
            }
            while (!q.isEmpty() && nums[q.peekLast()] <= nums[i]) {
                q.pollLast();
            }
            q.offer(i);
            if (i >= k - 1) {
                ans[i - k + 1] = nums[q.peek()];
            }
        }
        return ans;
    }
}
```


### 解题模板

```
// 有效的括号
Deque<Character> stk = new ArrayDeque<>();
for (char c : s.toCharArray()) {
    if (c == '(') stk.push(')');
    else if (stk.isEmpty() || stk.pop() != c) return false;
}

// 单调栈：下一个更大元素
Deque<Integer> stk = new ArrayDeque<>();
for (int i = n - 1; i >= 0; i--) {
    while (!stk.isEmpty() && stk.peek() <= nums[i]) stk.pop();
    ans[i] = stk.isEmpty() ? -1 : stk.peek();
    stk.push(nums[i]);
}

// 最小栈：辅助栈同步记录最小值
```

**识别信号**：匹配/配对 → 栈；最近更大/更小 → 单调栈。

---

## 九、二叉树

**来源：LeetCode Hot 100**

<a id="p-94"></a>
## 94. 二叉树的中序遍历

- 难度：简单
- 标签：栈、树、深度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/binary-tree-inorder-traversal/) | [参考题解](https://leetcode.doocs.org/lc/94/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0094.Binary%20Tree%20Inorder%20Traversal/README.md)

### 题目要求
给定一个二叉树的根节点 `root` ，返回 它的 中序 遍历 。

### 样例数据
样例 1:
```text
输入：root = [1,null,2,3]
输出：[1,3,2]
```

样例 2:
```text
输入：root = []
输出：[]
```

### 核心思路
`方法一：递归遍历`

我们先递归左子树，再访问根节点，接着递归右子树。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。 其中 n 是二叉树的节点数，空间复杂度主要取决于递归调用的栈空间。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private List<Integer> ans = new ArrayList<>();

    public List<Integer> inorderTraversal(TreeNode root) {
        dfs(root);
        return ans;
    }

    private void dfs(TreeNode root) {
        if (root == null) {
            return;
        }
        dfs(root.left);
        ans.add(root.val);
        dfs(root.right);
    }
}
```

---

<a id="p-104"></a>
## 104. 二叉树的最大深度

- 难度：简单
- 标签：树、深度优先搜索、广度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) | [参考题解](https://leetcode.doocs.org/lc/104/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0104.Maximum%20Depth%20of%20Binary%20Tree/README.md)

### 题目要求
给定一个二叉树 `root` ，返回其最大深度。 二叉树的 最大深度 是指从根节点到最远叶子节点的最长路径上的节点数。

### 样例数据
样例 1:
```text
输入：root = [3,9,20,null,null,15,7]
输出：3
```

样例 2:
```text
输入：root = [1,null,2]
输出：2
```

### 核心思路
`方法一：递归`

递归遍历左右子树，求左右子树的最大深度，然后取最大值加 1 即可。 每个节点在递归中只被遍历一次。

### 复杂度
时间复杂度 O(n)，其中 n 是二叉树的节点数。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int l = maxDepth(root.left);
        int r = maxDepth(root.right);
        return 1 + Math.max(l, r);
    }
}
```

---

<a id="p-226"></a>
## 226. 翻转二叉树

- 难度：简单
- 标签：树、深度优先搜索、广度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/invert-binary-tree/) | [参考题解](https://leetcode.doocs.org/lc/226/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0226.Invert%20Binary%20Tree/README.md)

### 题目要求
给你一棵二叉树的根节点 `root` ，翻转这棵二叉树，并返回其根节点。

### 样例数据
样例 1:
```text
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

样例 2:
```text
输入：root = [2,1,3]
输出：[2,3,1]
```

### 核心思路
`方法一：递归`

我们首先判断 root 是否为空，若为空则直接返回 \text{null}。 然后递归地对树的左右子树进行翻转，将翻转后的右子树作为新的左子树，将翻转后的左子树作为新的右子树，返回 root。 其中 n 是二叉树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) {
            return null;
        }
        TreeNode l = invertTree(root.left);
        TreeNode r = invertTree(root.right);
        root.left = r;
        root.right = l;
        return root;
    }
}
```

---

<a id="p-101"></a>
## 101. 对称二叉树

- 难度：简单
- 标签：树、深度优先搜索、广度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/symmetric-tree/) | [参考题解](https://leetcode.doocs.org/lc/101/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0101.Symmetric%20Tree/README.md)

### 题目要求
给你一个二叉树的根节点 `root` ， 检查它是否轴对称。

### 样例数据
样例 1:
```text
输入：root = [1,2,2,3,4,4,3]
输出：true
```

样例 2:
```text
输入：root = [1,2,2,null,3,null,3]
输出：false
```

### 核心思路
`方法一：递归`

我们设计一个函数 dfs(root1, root2)，用于判断两个二叉树是否对称。 答案即为 dfs(root.left, root.right)。 函数 dfs(root1, root2) 的逻辑如下：

- 如果 root1 和 root2 都为空，则两个二叉树对称，返回 `true`；
- 如果 root1 和 root2 中只有一个为空，或者 root1.val \neq root2.val
- 否则，判断 root1 的左子树和 root2 的右子树是否对称，以及 root1 的右子树和 root2 的左子树是否对称，这里使用了递归。 其中 n 是二叉树的节点数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public boolean isSymmetric(TreeNode root) {
        return dfs(root.left, root.right);
    }

    private boolean dfs(TreeNode root1, TreeNode root2) {
        if (root1 == root2) {
            return true;
        }
        if (root1 == null || root2 == null || root1.val != root2.val) {
            return false;
        }
        return dfs(root1.left, root2.right) && dfs(root1.right, root2.left);
    }
}
```

---

<a id="p-543"></a>
## 543. 二叉树的直径

- 难度：简单
- 标签：树、深度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/diameter-of-binary-tree/) | [参考题解](https://leetcode.doocs.org/lc/543/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0500-0599/0543.Diameter%20of%20Binary%20Tree/README.md)

### 题目要求
给你一棵二叉树的根节点，返回该树的 直径 。 二叉树的 直径 是指树中任意两个节点之间最长路径的 长度 。这条路径可能经过也可能不经过根节点 `root` 。 两节点之间路径的 长度 由它们之间边数表示。

### 样例数据
样例 1:
```text
输入：root = [1,2,3,4,5]
输出：3
解释：3 ，取路径 [4,2,1,3] 或 [5,2,1,3] 的长度。
```

样例 2:
```text
输入：root = [1,2]
输出：1
```

### 核心思路
`方法一：枚举 + DFS`

我们可以枚举二叉树的每个节点，以该节点为根节点，计算其左右子树的最大深度 l 和 r，则该节点的直径为 l + r。 取所有节点的直径的最大值即为二叉树的直径。 其中 n 为二叉树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private int ans;

    public int diameterOfBinaryTree(TreeNode root) {
        dfs(root);
        return ans;
    }

    private int dfs(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int l = dfs(root.left);
        int r = dfs(root.right);
        ans = Math.max(ans, l + r);
        return 1 + Math.max(l, r);
    }
}
```

---

<a id="p-102"></a>
## 102. 二叉树的层序遍历

- 难度：中等
- 标签：树、广度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/binary-tree-level-order-traversal/) | [参考题解](https://leetcode.doocs.org/lc/102/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0102.Binary%20Tree%20Level%20Order%20Traversal/README.md)

### 题目要求
给你二叉树的根节点 `root` ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。

### 样例数据
样例 1:
```text
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
```

样例 2:
```text
输入：root = [1]
输出：[[1]]
```

### 核心思路
`方法一：BFS`

我们可以使用 BFS 的方法来解决这道题。 首先将根节点入队，然后不断地进行以下操作，直到队列为空：

- 遍历当前队列中的所有节点，将它们的值存储到一个临时数组 t 中，然后将它们的孩子节点入队。 - 将临时数组 t 存储到答案数组中。 最后返回答案数组即可。 其中 n 是二叉树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> ans = new ArrayList<>();
        if (root == null) {
            return ans;
        }
        Deque<TreeNode> q = new ArrayDeque<>();
        q.offer(root);
        while (!q.isEmpty()) {
            List<Integer> t = new ArrayList<>();
            for (int n = q.size(); n > 0; --n) {
                TreeNode node = q.poll();
                t.add(node.val);
                if (node.left != null) {
                    q.offer(node.left);
                }
                if (node.right != null) {
                    q.offer(node.right);
                }
            }
            ans.add(t);
        }
        return ans;
    }
}
```

---

<a id="p-108"></a>
## 108. 将有序数组转换为二叉搜索树

- 难度：简单
- 标签：树、二叉搜索树、数组、分治、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/) | [参考题解](https://leetcode.doocs.org/lc/108/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0108.Convert%20Sorted%20Array%20to%20Binary%20Search%20Tree/README.md)

### 题目要求
给你一个整数数组 `nums` ，其中元素已经按 升序 排列，请你将其转换为一棵 平衡 二叉搜索树。

### 样例数据
样例 1:
```text
输入：nums = [-10,-3,0,5,9]
输出：[0,-3,9,-10,null,5]
解释：[0,-10,5,null,-3,null,9] 也将被视为正确答案：
```

样例 2:
```text
输入：nums = [1,3]
输出：[3,1]
解释：[1,null,3] 和 [3,1] 都是高度平衡二叉搜索树。
```

### 核心思路
`方法一：二分 + 递归`

我们设计一个递归函数 dfs(l, r)，表示当前待构造的二叉搜索树的节点值都在数组 nums 的下标范围 [l, r] 内。 该函数返回构造出的二叉搜索树的根节点。 函数 dfs(l, r) 的执行流程如下：

1. 如果 l > r，说明当前数组为空，返回 `null`。 2. 如果 l \leq r，取数组中下标为 mid = \lfloor \frac{l + r}{2} \rfloor 的元素作为当前二叉搜索树的根节点，其中 \lfloor x \rfloor 表示对 x 向下取整。 3. 递归地构造当前二叉搜索树的左子树，其根节点的值为数组中下标为 mid - 1 的元素，左子树的节点值都在数组的下标范围 [l, mid - 1] 内。 4. 递归地构造当前二叉搜索树的右子树，其根节点的值为数组中下标为 mid + 1 的元素，右子树的节点值都在数组的下标范围 [mid + 1, r] 内。 5. 返回当前二叉搜索树的根节点。 答案即为函数 dfs(0, n - 1) 的返回值。 其中 n 为数组 nums 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(\log n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private int[] nums;

    public TreeNode sortedArrayToBST(int[] nums) {
        this.nums = nums;
        return dfs(0, nums.length - 1);
    }

    private TreeNode dfs(int l, int r) {
        if (l > r) {
            return null;
        }
        int mid = (l + r) >> 1;
        return new TreeNode(nums[mid], dfs(l, mid - 1), dfs(mid + 1, r));
    }
}
```

---

<a id="p-98"></a>
## 98. 验证二叉搜索树

- 难度：中等
- 标签：树、深度优先搜索、二叉搜索树、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/validate-binary-search-tree/) | [参考题解](https://leetcode.doocs.org/lc/98/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0098.Validate%20Binary%20Search%20Tree/README.md)

### 题目要求
给你一个二叉树的根节点 `root` ，判断其是否是一个有效的二叉搜索树。 有效 二叉搜索树定义如下： - 节点的左子树只包含 严格小于 当前节点的数。 - 节点的右子树只包含 严格大于 当前节点的数。 - 所有左子树和右子树自身必须也是二叉搜索树。

### 样例数据
样例 1:
```text
输入：root = [2,1,3]
输出：true
```

样例 2:
```text
输入：root = [5,1,4,null,null,3,6]
输出：false
解释：根节点的值是 5 ，但是右子节点的值是 4 。
```

### 核心思路
`方法一：递归`

我们可以对二叉树进行递归中序遍历，如果遍历到的结果是严格升序的，那么这棵树就是一个二叉搜索树。 因此，我们使用一个变量 prev 来保存上一个遍历到的节点，初始时 prev = -\infty，然后我们递归遍历左子树，如果左子树不是二叉搜索树，直接返回 False，否则判断当前节点的值是否大于 prev，如果不是，返回 False，否则更新 prev 为当前节点的值，然后递归遍历右子树。 其中 n 是二叉树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private TreeNode prev;

    public boolean isValidBST(TreeNode root) {
        return dfs(root);
    }

    private boolean dfs(TreeNode root) {
        if (root == null) {
            return true;
        }
        if (!dfs(root.left)) {
            return false;
        }
        if (prev != null && prev.val >= root.val) {
            return false;
        }
        prev = root;
        return dfs(root.right);
    }
}
```

---

<a id="p-230"></a>
## 230. 二叉搜索树中第 K 小的元素

- 难度：中等
- 标签：树、深度优先搜索、二叉搜索树、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/) | [参考题解](https://leetcode.doocs.org/lc/230/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0230.Kth%20Smallest%20Element%20in%20a%20BST/README.md)

### 题目要求
给定一个二叉搜索树的根节点 `root` ，和一个整数 `k` ，请你设计一个算法查找其中第 `k` 小的元素（`k` 从 1 开始计数）。

### 样例数据
样例 1:
```text
输入：root = [3,1,4,null,2], k = 1
输出：1
```

样例 2:
```text
输入：root = [5,3,6,2,4,null,null,1], k = 3
输出：3
```

### 核心思路
`方法一：中序遍历`

由于二叉搜索树的性质，中序遍历一定能得到升序序列，因此可以采用中序遍历找出第 k 小的元素。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public int kthSmallest(TreeNode root, int k) {
        Deque<TreeNode> stk = new ArrayDeque<>();
        while (root != null || !stk.isEmpty()) {
            if (root != null) {
                stk.push(root);
                root = root.left;
            } else {
                root = stk.pop();
                if (--k == 0) {
                    return root.val;
                }
                root = root.right;
            }
        }
        return 0;
    }
}
```

---

<a id="p-199"></a>
## 199. 二叉树的右视图

- 难度：中等
- 标签：树、深度优先搜索、广度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/binary-tree-right-side-view/) | [参考题解](https://leetcode.doocs.org/lc/199/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0199.Binary%20Tree%20Right%20Side%20View/README.md)

### 题目要求
给定一个二叉树的 根节点 `root`，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。

### 样例数据
样例 1:
```text
输入：root = [1,2,3,null,5,null,4]
输出：[1,3,4]
解释：
```

样例 2:
```text
输入：root = [1,2,3,4,null,null,null,5]
输出：[1,3,4,5]
解释：
```

### 核心思路
`方法一：BFS`

我们可以使用广度优先搜索，定义一个队列 q，将根节点放入队列中。 每次从队列中取出当前层的所有节点，对于当前节点，我们先判断右子树是否存在，若存在则将右子树放入队列中；再判断左子树是否存在，若存在则将左子树放入队列中。 这样每次取出队列中的第一个节点即为该层的右视图节点。 其中 n 为二叉树节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> ans = new ArrayList<>();
        if (root == null) {
            return ans;
        }
        Deque<TreeNode> q = new ArrayDeque<>();
        q.offer(root);
        while (!q.isEmpty()) {
            ans.add(q.peekFirst().val);
            for (int k = q.size(); k > 0; --k) {
                TreeNode node = q.poll();
                if (node.right != null) {
                    q.offer(node.right);
                }
                if (node.left != null) {
                    q.offer(node.left);
                }
            }
        }
        return ans;
    }
}
```

---

<a id="p-114"></a>
## 114. 二叉树展开为链表

- 难度：中等
- 标签：栈、树、深度优先搜索、链表、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/) | [参考题解](https://leetcode.doocs.org/lc/114/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0114.Flatten%20Binary%20Tree%20to%20Linked%20List/README.md)

### 题目要求
给你二叉树的根结点 `root` ，请你将它展开为一个单链表： - 展开后的单链表应该同样使用 `TreeNode` ，其中 `right` 子指针指向链表中下一个结点，而左子指针始终为 `null` 。 - 展开后的单链表应该与二叉树 先序遍历 顺序相同。

### 样例数据
样例 1:
```text
输入：root = [1,2,5,3,4,null,6]
输出：[1,null,2,null,3,null,4,null,5,null,6]
```

样例 2:
```text
输入：root = []
输出：[]
```

### 核心思路
`方法一：寻找前驱节点`

先序遍历的访问顺序是“根、左子树、右子树”，左子树最后一个节点访问完后，接着会访问根节点的右子树节点。 因此，对于当前节点，如果其左子节点不为空，我们找到左子树的最右节点，作为前驱节点，然后将当前节点的右子节点赋给前驱节点的右子节点。 然后将当前节点的左子节点赋给当前节点的右子节点，并将当前节点的左子节点置为空。 然后将当前节点的右子节点作为下一个节点，继续处理，直至所有节点处理完毕。

### 复杂度
时间复杂度 O(n)，其中 n 是树中节点的个数。 空间复杂度 O(1)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public void flatten(TreeNode root) {
        while (root != null) {
            if (root.left != null) {
                // 找到当前节点左子树的最右节点
                TreeNode pre = root.left;
                while (pre.right != null) {
                    pre = pre.right;
                }

                // 将左子树的最右节点指向原来的右子树
                pre.right = root.right;

                // 将当前节点指向左子树
                root.right = root.left;
                root.left = null;
            }
            root = root.right;
        }
    }
}
```

---

<a id="p-105"></a>
## 105. 从前序与中序遍历序列构造二叉树

- 难度：中等
- 标签：树、数组、哈希表、分治、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | [参考题解](https://leetcode.doocs.org/lc/105/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0105.Construct%20Binary%20Tree%20from%20Preorder%20and%20Inorder%20Traversal/README.md)

### 题目要求
给定两个整数数组 `preorder` 和 `inorder` ，其中 `preorder` 是二叉树的先序遍历， `inorder` 是同一棵树的中序遍历，请构造二叉树并返回其根节点。

### 样例数据
样例 1:
```text
输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
输出: [3,9,20,null,null,15,7]
```

样例 2:
```text
输入: preorder = [-1], inorder = [-1]
输出: [-1]
```

### 核心思路
`方法一：哈希表 + 递归`

前序序列的第一个节点 preorder[0] 为根节点，我们在中序序列中找到根节点的位置 k，可以将中序序列划分为左子树 inorder[0..k] 、右子树 inorder[k+1..]。 通过左右子树的区间，可以计算出左、右子树节点的个数，假设为 a 和 b。 然后在前序节点中，从根节点往后的 a 个节点为左子树，再往后的 b 个节点为右子树。 因此，我们设计一个函数 dfs(i, j, n)，其中 i 和 j 分别表示前序序列和中序序列的起始位置，而 n 表示节点个数。 函数的返回值是以 preorder[i..i+n-1] 为前序序列，以 inorder[j..j+n-1] 为中序序列构造出的二叉树。 函数 dfs(i, j, n) 的执行过程如下：

- 如果 n \leq 0，说明没有节点，返回空节点。 - 取出前序序列的第一个节点 v = preorder[i] 作为根节点，然后利用哈希表 d 找到根节点在中序序列中的位置 k，那么左子树的节点个数为 k - j，右子树的节点个数为 n - k + j - 1。 - 递归构造左子树 l = dfs(i + 1, j, k - j) 和右子树 r = dfs(i + 1 + k - j, k + 1, n - k + j - 1)。 - 最后返回以 v 为根节点且左右子树分别为 l 和 r 的二叉树。 其中 n 为二叉树节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private int[] preorder;
    private Map<Integer, Integer> d = new HashMap<>();

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        int n = preorder.length;
        this.preorder = preorder;
        for (int i = 0; i < n; ++i) {
            d.put(inorder[i], i);
        }
        return dfs(0, 0, n);
    }

    private TreeNode dfs(int i, int j, int n) {
        if (n <= 0) {
            return null;
        }
        int v = preorder[i];
        int k = d.get(v);
        TreeNode l = dfs(i + 1, j, k - j);
        TreeNode r = dfs(i + 1 + k - j, k + 1, n - 1 - (k - j));
        return new TreeNode(v, l, r);
    }
}
```

---

<a id="p-437"></a>
## 437. 路径总和 III

- 难度：中等
- 标签：树、深度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/path-sum-iii/) | [参考题解](https://leetcode.doocs.org/lc/437/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0400-0499/0437.Path%20Sum%20III/README.md)

### 题目要求
给定一个二叉树的根节点 `root` ，和一个整数 `targetSum` ，求该二叉树里节点值之和等于 `targetSum` 的 路径 的数目。 路径 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。

### 样例数据
样例 1:
```text
输入：root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
输出：3
解释：和等于 8 的路径有 3 条，如图所示。
```

样例 2:
```text
输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
输出：3
```

### 核心思路
`方法一：哈希表 + 前缀和 + 递归`

我们可以运用前缀和的思想，对二叉树进行递归遍历，同时用哈希表 cnt 统计从根节点到当前节点的路径上各个前缀和出现的次数。 我们设计一个递归函数 dfs(node, s)，表示当前遍历到的节点为 node，从根节点到当前节点的路径上的前缀和为 s。 函数的返回值是统计以 node 节点及其子树节点作为路径终点且路径和为 targetSum 的路径数目。 那么答案就是 dfs(root, 0)。 函数 dfs(node, s) 的递归过程如下：

- 如果当前节点 node 为空，则返回 0。 - 计算从根节点到当前节点的路径上的前缀和 s。 - 用 cnt[s - targetSum] 表示以当前节点为路径终点且路径和为 targetSum 的路径数目，其中 cnt[s - targetSum] 即为 cnt 中前缀和为 s - targetSum 的个数。 - 将前缀和 s 的计数值加 1，即 cnt[s] = cnt[s] + 1。 - 递归地遍历当前节点的左右子节点，即调用函数 dfs(node.left, s) 和 dfs(node.right, s)，并将它们的返回值相加。 - 在返回值计算完成以后，需要将当前节点的前缀和 s 的计数值减 1，即执行 cnt[s] = cnt[s] - 1。 - 最后返回答案。 其中 n 是二叉树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private Map<Long, Integer> cnt = new HashMap<>();
    private int targetSum;

    public int pathSum(TreeNode root, int targetSum) {
        cnt.put(0L, 1);
        this.targetSum = targetSum;
        return dfs(root, 0);
    }

    private int dfs(TreeNode node, long s) {
        if (node == null) {
            return 0;
        }
        s += node.val;
        int ans = cnt.getOrDefault(s - targetSum, 0);
        cnt.merge(s, 1, Integer::sum);
        ans += dfs(node.left, s);
        ans += dfs(node.right, s);
        cnt.merge(s, -1, Integer::sum);
        return ans;
    }
}
```

---

<a id="p-236"></a>
## 236. 二叉树的最近公共祖先

- 难度：中等
- 标签：树、深度优先搜索、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/) | [参考题解](https://leetcode.doocs.org/lc/236/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0236.Lowest%20Common%20Ancestor%20of%20a%20Binary%20Tree/README.md)

### 题目要求
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。 百度百科中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

### 样例数据
样例 1:
```text
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
解释：节点 `5 `和节点 `1 `的最近公共祖先是节点 `3 。`
```

样例 2:
```text
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出：5
解释：节点 `5 `和节点 `4 `的最近公共祖先是节点 `5 。`因为根据定义最近公共祖先节点可以为节点本身。
```

### 核心思路
`方法一：递归`

我们递归遍历二叉树：

如果当前节点为空或者等于 p 或者 q，则返回当前节点；

否则，我们递归遍历左右子树，将返回的结果分别记为 left 和 right。 如果 left 和 right 都不为空，则说明 p 和 q 分别在左右子树中，因此当前节点即为最近公共祖先；如果 left 和 right 中只有一个不为空，返回不为空的那个。 其中 n 为二叉树节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root;
        }
        var left = lowestCommonAncestor(root.left, p, q);
        var right = lowestCommonAncestor(root.right, p, q);
        if (left != null && right != null) {
            return root;
        }
        return left == null ? right : left;
    }
}
```

---

<a id="p-124"></a>
## 124. 二叉树中的最大路径和

- 难度：困难
- 标签：树、深度优先搜索、动态规划、二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/binary-tree-maximum-path-sum/) | [参考题解](https://leetcode.doocs.org/lc/124/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0124.Binary%20Tree%20Maximum%20Path%20Sum/README.md)

### 题目要求
二叉树中的 路径 被定义为一条节点序列，序列中每对相邻节点之间都存在一条边。同一个节点在一条路径序列中 至多出现一次 。该路径 至少包含一个 节点，且不一定经过根节点。 路径和 是路径中各节点值的总和。 给你一个二叉树的根节点 `root` ，返回其 最大路径和 。

### 样例数据
样例 1:
```text
输入：root = [1,2,3]
输出：6
解释：最优路径是 2 -> 1 -> 3 ，路径和为 2 + 1 + 3 = 6
```

样例 2:
```text
输入：root = [-10,9,20,null,null,15,7]
输出：42
解释：最优路径是 15 -> 20 -> 7 ，路径和为 15 + 20 + 7 = 42
```

### 核心思路
`方法一：递归`

我们思考二叉树递归问题的经典套路：

1. 终止条件（何时终止递归）
2. 递归处理左右子树
3. 合并左右子树的计算结果

对于本题，我们设计一个函数 dfs(root)，它返回以 root 为根节点的二叉树的最大路径和。 函数 dfs(root) 的执行逻辑如下：

如果 root 不存在，那么 dfs(root) 返回 0；

否则，我们递归计算 root 的左子树和右子树的最大路径和，分别记为 left 和 right。 如果 left 小于 0，那么我们将其置为 0，同理，如果 right 小于 0，那么我们将其置为 0。 然后，我们用 root.val + left + right 更新答案。 最后，函数返回 root.val + \max(left, right)。 在主函数中，我们调用 dfs(root)，即可得到每个节点的最大路径和，其中的最大值即为答案。 其中 n 是二叉树的节点数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private int ans = -1001;

    public int maxPathSum(TreeNode root) {
        dfs(root);
        return ans;
    }

    private int dfs(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int left = Math.max(0, dfs(root.left));
        int right = Math.max(0, dfs(root.right));
        ans = Math.max(ans, root.val + left + right);
        return root.val + Math.max(left, right);
    }
}
```


**来源：剑指 Offer**

<a id="offer-7"></a>
## 剑指 Offer 07. 重建二叉树

- 难度：中等
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/zhong-jian-er-cha-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/7/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9807.%20%E9%87%8D%E5%BB%BA%E4%BA%8C%E5%8F%89%E6%A0%91/README.md)

### 题目要求
输入某二叉树的前序遍历和中序遍历的结果，请构建该二叉树并返回其根节点。 假设输入的前序遍历和中序遍历的结果中都不含重复的数字。

### 样例数据
样例 1:
```text
Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]
```

样例 2:
```text
Input: preorder = [-1], inorder = [-1]
Output: [-1]
```

### 核心思路
`方法一：哈希表 + 递归`

接下来，我们设计一个递归函数 dfs(i, j, n)，表示在前序序列中，从第 i 个节点开始的 n 个节点，对应的中序序列中，从第 j 个节点开始的 n 个节点，构造出的二叉树。 函数 dfs(i, j, n) 的执行过程如下：

如果 n = 0，说明已经没有节点了，返回 null；

否则，我们取前序序列的第 i 个节点作为根节点，创建一个树节点，即 `root = new TreeNode(preorder[i])`，然后我们在中序序列中找到根节点的位置，记为 k，则根节点左边的 k - j 个节点为左子树，右边的 n - k + j - 1 个节点为右子树。 递归地调用函数 dfs(i + 1, j, k - j) 构造左子树，调用函数 dfs(i + k - j + 1, k + 1, n - k + j - 1) 构造右子树。 最后返回根节点 `root`。 其中 n 是二叉树的节点个数。

### 复杂度
由于我们每一次都需要在中序序列中找到根节点的位置，因此我们可以使用哈希表 d 来存储中序序列的值和索引，这样可以将查找的时间复杂度降低到 O(1)。 时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    private Map<Integer, Integer> d = new HashMap<>();
    private int[] preorder;
    private int[] inorder;

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        int n = inorder.length;
        for (int i = 0; i < n; ++i) {
            d.put(inorder[i], i);
        }
        this.preorder = preorder;
        this.inorder = inorder;
        return dfs(0, 0, n);
    }

    private TreeNode dfs(int i, int j, int n) {
        if (n < 1) {
            return null;
        }
        int k = d.get(preorder[i]);
        int l = k - j;
        TreeNode root = new TreeNode(preorder[i]);
        root.left = dfs(i + 1, j, l);
        root.right = dfs(i + 1 + l, k + 1, n - l - 1);
        return root;
    }
}
```

---

<a id="offer-26"></a>
## 剑指 Offer 26. 树的子结构

- 难度：中等
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/shu-de-zi-jie-gou-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/26/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9826.%20%E6%A0%91%E7%9A%84%E5%AD%90%E7%BB%93%E6%9E%84/README.md)

### 题目要求
输入两棵二叉树A和B，判断B是不是A的子结构。(约定空树不是任意一个树的子结构) B是A的子结构， 即 A中有出现和B相同的结构和节点值。 例如: 给定的树 A: ` 3 / \ 4 5 / \ 1 2` 给定的树 B： ` 4 / 1` 返回 true，因为 B 与 A 的一个子树拥有相同的结构和节点值。

### 样例数据
样例 1:
```text
输入：A = [1,2,3], B = [3,1]
输出：false
```

样例 2:
```text
输入：A = [3,4,5,1,2], B = [4,1]
输出：true
```

### 核心思路
`方法一：递归`

我们设计一个函数 dfs(A, B)，用于判断树 A 中以节点 A 为根节点的子树是否包含树 B。 函数 dfs(A, B) 的执行步骤如下：

1. 如果树 B 为空，则树 B 是树 A 的子结构，返回 `true`；
2. 如果树 A 为空，或者树 A 的根节点的值不等于树 B 的根节点的值，则树 B 不是树 A 的子结构，返回 `false`；
3. 判断树 A 的左子树是否包含树 B 的左子树，即调用 dfs(A.left, B.left)，并且判断树 A 的右子树是否包含树 B 的右子树，即调用 dfs(A.right, B.right)。 如果其中有一个函数返回 `false`，则树 B 不是树 A 的子结构，返回 `false`；否则，返回 `true`。 在函数 `isSubStructure` 中，我们首先判断树 A 和树 B 是否为空，如果其中有一个为空，则树 B 不是树 A 的子结构，返回 `false`。 然后，我们调用 dfs(A, B)，判断树 A 是否包含树 B。 如果是，则返回 `true`；否则，递归判断树 A 的左子树是否包含树 B，以及树 A 的右子树是否包含树 B。 如果其中有一个返回 `true`，则树 B 是树 A 的子结构，返回 `true`；否则，返回 `false`。 其中 n 和 m 分别是树 A 和树 B 的节点个数。

### 复杂度
时间复杂度 O(n \times m)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public boolean isSubStructure(TreeNode A, TreeNode B) {
        if (A == null || B == null) {
            return false;
        }
        return dfs(A, B) || isSubStructure(A.left, B) || isSubStructure(A.right, B);
    }

    private boolean dfs(TreeNode A, TreeNode B) {
        if (B == null) {
            return true;
        }
        if (A == null || A.val != B.val) {
            return false;
        }
        return dfs(A.left, B.left) && dfs(A.right, B.right);
    }
}
```

---

<a id="offer-27"></a>
## 剑指 Offer 27. 二叉树的镜像

- 难度：简单
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/er-cha-shu-de-jing-xiang-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/27/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9827.%20%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E9%95%9C%E5%83%8F/README.md)

### 题目要求
请完成一个函数，输入一个二叉树，该函数输出它的镜像。 例如输入： ` 4 / \ 2 7 / \ / \ 1 3 6 9` 镜像输出： ` 4 / \ 7 2 / \ / \ 9 6 3 1`

### 样例数据
样例 1:
```text
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

### 核心思路
`方法一：递归`

我们先判断根节点是否为空，如果为空，直接返回空。 如果不为空，我们交换根节点的左右子树，然后递归地交换左子树和右子树。 其中 n 是二叉树的节点个数。 最坏情况下，二叉树退化为链表，递归深度为 n，因此系统使用 O(n) 大小的栈空间。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public TreeNode mirrorTree(TreeNode root) {
        if (root == null) {
            return null;
        }
        TreeNode t = root.left;
        root.left = root.right;
        root.right = t;
        mirrorTree(root.left);
        mirrorTree(root.right);
        return root;
    }
}
```

---

<a id="offer-28"></a>
## 剑指 Offer 28. 对称的二叉树

- 难度：简单
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/dui-cheng-de-er-cha-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/28/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9828.%20%E5%AF%B9%E7%A7%B0%E7%9A%84%E4%BA%8C%E5%8F%89%E6%A0%91/README.md)

### 题目要求
请实现一个函数，用来判断一棵二叉树是不是对称的。如果一棵二叉树和它的镜像一样，那么它是对称的。 例如，二叉树 [1,2,2,3,4,4,3] 是对称的。 ` 1 / \ 2 2 / \ / \ 3 4 4 3` 但是下面这个 [1,2,2,null,3,null,3] 则不是镜像对称的: ` 1 / \ 2 2 \ \ 3 3`

### 样例数据
样例 1:
```text
输入：root = [1,2,2,3,4,4,3]
输出：true
```

样例 2:
```text
输入：root = [1,2,2,null,3,null,3]
输出：false
```

### 核心思路
`方法一：递归`

我们设计一个递归函数 `dfs`，它接收两个参数 `a` 和 `b`，分别代表两棵树的根节点。 我们可以对 `a` 和 `b` 进行如下判断：

- 如果 `a` 和 `b` 都为空，说明两棵树都遍历完了，返回 `true`；
- 如果 `a` 和 `b` 中有且只有一个为空，说明两棵树的结构不同，返回 `false`；
- 如果 `a` 和 `b` 的值不相等，说明两棵树的结构不同，返回 `false`；
- 如果 `a` 和 `b` 的值相等，那么我们分别递归地判断 `a` 的左子树和 `b` 的右子树，以及 `a` 的右子树和 `b` 的左子树是否对称。 最后，我们返回 `dfs(root, root)`，即判断 `root` 的左子树和右子树是否对称。 其中 n 是二叉树的节点数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public boolean isSymmetric(TreeNode root) {
        return dfs(root, root);
    }

    private boolean dfs(TreeNode a, TreeNode b) {
        if (a == null && b == null) {
            return true;
        }
        if (a == null || b == null || a.val != b.val) {
            return false;
        }
        return dfs(a.left, b.right) && dfs(a.right, b.left);
    }
}
```

---

<a id="offer-32-1"></a>
## 剑指 Offer 32 - I. 从上到下打印二叉树

- 难度：中等
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/cong-shang-dao-xia-da-yin-er-cha-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/32.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9832%20-%20I.%20%E4%BB%8E%E4%B8%8A%E5%88%B0%E4%B8%8B%E6%89%93%E5%8D%B0%E4%BA%8C%E5%8F%89%E6%A0%91/README.md)

### 题目要求
从上到下打印出二叉树的每个节点，同一层的节点按照从左到右的顺序打印。 例如: 给定二叉树: `[3,9,20,null,null,15,7]`,

### 样例数据
样例 1:
```text
3
/ \
9 20
/ \
15 7
```

样例 2:
```text
[3,9,20,15,7]
```

### 核心思路
`方法一：BFS`

我们可以通过 BFS 遍历二叉树，将每一层的节点值存入数组中，最后返回数组即可。 其中 n 为二叉树的节点数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public int[] levelOrder(TreeNode root) {
        if (root == null) {
            return new int[] {};
        }
        Deque<TreeNode> q = new ArrayDeque<>();
        q.offer(root);
        List<Integer> res = new ArrayList<>();
        while (!q.isEmpty()) {
            for (int n = q.size(); n > 0; --n) {
                TreeNode node = q.poll();
                res.add(node.val);
                if (node.left != null) {
                    q.offer(node.left);
                }
                if (node.right != null) {
                    q.offer(node.right);
                }
            }
        }
        int[] ans = new int[res.size()];
        for (int i = 0; i < ans.length; ++i) {
            ans[i] = res.get(i);
        }
        return ans;
    }
}
```

---

<a id="offer-32-2"></a>
## 剑指 Offer 32 - II. 从上到下打印二叉树 II

- 难度：简单
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/cong-shang-dao-xia-da-yin-er-cha-shu-ii-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/32.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9832%20-%20II.%20%E4%BB%8E%E4%B8%8A%E5%88%B0%E4%B8%8B%E6%89%93%E5%8D%B0%E4%BA%8C%E5%8F%89%E6%A0%91%20II/README.md)

### 题目要求
从上到下按层打印二叉树，同一层的节点按从左到右的顺序打印，每一层打印到一行。 例如: 给定二叉树: `[3,9,20,null,null,15,7]`,

### 样例数据
样例 1:
```text
3
/ \
9 20
/ \
15 7
```

样例 2:
```text
[
[3],
[9,20],
[15,7]
]
```

### 核心思路
`方法一：BFS`

我们可以使用 BFS 的方法来解决这道题。 首先将根节点入队，然后不断地进行以下操作，直到队列为空：

- 遍历当前队列中的所有节点，将它们的值存储到一个临时数组 t 中，然后将它们的孩子节点入队。 - 将临时数组 t 存储到答案数组中。 最后返回答案数组即可。 其中 n 是二叉树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> ans = new ArrayList<>();
        if (root == null) {
            return ans;
        }
        Deque<TreeNode> q = new ArrayDeque<>();
        q.offer(root);
        while (!q.isEmpty()) {
            List<Integer> t = new ArrayList<>();
            for (int n = q.size(); n > 0; --n) {
                TreeNode node = q.poll();
                t.add(node.val);
                if (node.left != null) {
                    q.offer(node.left);
                }
                if (node.right != null) {
                    q.offer(node.right);
                }
            }
            ans.add(t);
        }
        return ans;
    }
}
```

---

<a id="offer-32-3"></a>
## 剑指 Offer 32 - III. 从上到下打印二叉树 III

- 难度：中等
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/cong-shang-dao-xia-da-yin-er-cha-shu-iii-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/32.3/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9832%20-%20III.%20%E4%BB%8E%E4%B8%8A%E5%88%B0%E4%B8%8B%E6%89%93%E5%8D%B0%E4%BA%8C%E5%8F%89%E6%A0%91%20III/README.md)

### 题目要求
请实现一个函数按照之字形顺序打印二叉树，即第一行按照从左到右的顺序打印，第二层按照从右到左的顺序打印，第三行再按照从左到右的顺序打印，其他行以此类推。 例如: 给定二叉树: `[3,9,20,null,null,15,7]`,

### 样例数据
样例 1:
```text
3
/ \
9 20
/ \
15 7
```

样例 2:
```text
[
[3],
[20,9],
[15,7]
]
```

### 核心思路
`方法一：BFS`

为了实现锯齿形层序遍历，我们每次将当前层的节点添加到结果数组之前，先判断一下当前结果数组的长度，如果是奇数，就将当前层的节点反转一下。 之后把当前层的节点添加到结果数组中即可。 其中 n 为二叉树的节点数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> ans = new ArrayList<>();
        if (root == null) {
            return ans;
        }
        Deque<TreeNode> q = new ArrayDeque<>();
        q.offer(root);
        while (!q.isEmpty()) {
            List<Integer> t = new ArrayList<>();
            for (int n = q.size(); n > 0; --n) {
                TreeNode node = q.poll();
                t.add(node.val);
                if (node.left != null) {
                    q.offer(node.left);
                }
                if (node.right != null) {
                    q.offer(node.right);
                }
            }
            if (ans.size() % 2 == 1) {
                Collections.reverse(t);
            }
            ans.add(t);
        }
        return ans;
    }
}
```

---

<a id="offer-33"></a>
## 剑指 Offer 33. 二叉搜索树的后序遍历序列

- 难度：中等
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/er-cha-sou-suo-shu-de-hou-xu-bian-li-xu-lie-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/33/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9833.%20%E4%BA%8C%E5%8F%89%E6%90%9C%E7%B4%A2%E6%A0%91%E7%9A%84%E5%90%8E%E5%BA%8F%E9%81%8D%E5%8E%86%E5%BA%8F%E5%88%97/README.md)

### 题目要求
输入一个整数数组，判断该数组是不是某二叉搜索树的后序遍历结果。如果是则返回 `true`，否则返回 `false`。假设输入的数组的任意两个数字都互不相同。 参考以下这颗二叉搜索树：

### 样例数据
样例 1:
```text
5
/ \
2 6
/ \
1 3
```

样例 2:
```text
输入: [1,6,3,2,5]
输出: false
```

### 核心思路
`方法一：递归`

后序遍历的最后一个元素为根节点，根据二叉搜索树的性质，根节点左边的元素都小于根节点，根节点右边的元素都大于根节点。 因此，我们找到第一个大于根节点的位置 i，那么 i 右边的元素都应该大于根节点，否则返回 `false`。 然后递归判断左右子树。 其中 n 为数组长度。

### 复杂度
时间复杂度 O(n^2)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    private int[] postorder;

    public boolean verifyPostorder(int[] postorder) {
        this.postorder = postorder;
        return dfs(0, postorder.length - 1);
    }

    private boolean dfs(int l, int r) {
        if (l >= r) {
            return true;
        }
        int v = postorder[r];
        int i = l;
        while (i < r && postorder[i] < v) {
            ++i;
        }
        for (int j = i; j < r; ++j) {
            if (postorder[j] < v) {
                return false;
            }
        }
        return dfs(l, i - 1) && dfs(i, r - 1);
    }
}
```

---

<a id="offer-34"></a>
## 剑指 Offer 34. 二叉树中和为某一值的路径

- 难度：中等
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/er-cha-shu-zhong-he-wei-mou-yi-zhi-de-lu-jing-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/34/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9834.%20%E4%BA%8C%E5%8F%89%E6%A0%91%E4%B8%AD%E5%92%8C%E4%B8%BA%E6%9F%90%E4%B8%80%E5%80%BC%E7%9A%84%E8%B7%AF%E5%BE%84/README.md)

### 题目要求
给你二叉树的根节点 `root` 和一个整数目标和 `targetSum` ，找出所有 从根节点到叶子节点 路径总和等于给定目标和的路径。 叶子节点 是指没有子节点的节点。

### 样例数据
样例 1:
```text
输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
输出：[[5,4,11,2],[5,8,4,5]]
```

样例 2:
```text
输入：root = [1,2,3], targetSum = 5
输出：[]
```

### 核心思路
`方法一：递归`

从根节点开始，递归遍历每个节点，每次递归时，将当前节点值加入到路径中，然后判断当前节点是否为叶子节点，如果是叶子节点并且路径和等于目标值，则将该路径加入到结果中。 如果当前节点不是叶子节点，则递归遍历其左右子节点。 递归遍历时，需要将当前节点从路径中移除，以确保返回父节点时路径刚好是从根节点到父节点。 其中 n 是二叉树的节点数。

### 复杂度
时间复杂度 O(n^2)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private List<Integer> t = new ArrayList<>();
    private List<List<Integer>> ans = new ArrayList<>();

    public List<List<Integer>> pathSum(TreeNode root, int target) {
        dfs(root, target);
        return ans;
    }

    private void dfs(TreeNode root, int s) {
        if (root == null) {
            return;
        }
        t.add(root.val);
        s -= root.val;
        if (root.left == null && root.right == null && s == 0) {
            ans.add(new ArrayList<>(t));
        }
        dfs(root.left, s);
        dfs(root.right, s);
        t.remove(t.size() - 1);
    }
}
```

---

<a id="offer-37"></a>
## 剑指 Offer 37. 序列化二叉树

- 难度：困难
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/xu-lie-hua-er-cha-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/37/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9837.%20%E5%BA%8F%E5%88%97%E5%8C%96%E4%BA%8C%E5%8F%89%E6%A0%91/README.md)

### 题目要求
请实现两个函数，分别用来序列化和反序列化二叉树。 你需要设计一个算法来实现二叉树的序列化与反序列化。这里不限定你的序列 / 反序列化算法执行逻辑，你只需要保证一个二叉树可以被序列化为一个字符串并且将这个字符串反序列化为原始的树结构。 提示：输入输出格式与 LeetCode 目前使用的方式一致，详情请参阅 LeetCode 序列化二叉树的格式。你并非必须采取这种方式，你也可以采用其他的方法解决这个问题。

### 样例数据
样例 1:
```text
输入：root = [1,2,3,null,null,4,5]
输出：[1,2,3,null,null,4,5]
```

### 核心思路
`方法一：层序遍历`

我们可以采用层序遍历的方式对二叉树进行序列化，即从根节点开始，依次将二叉树的节点按照从上到下、从左到右的顺序加入队列中，然后将队列中的节点依次出队。 如果节点不为空，则将其值加入序列化字符串中，否则加入特殊字符 `#`。 最后将序列化字符串返回即可。 反序列化时，我们将序列化字符串按照分隔符进行切分，得到一个字符串数组，然后依次将字符串数组中的元素加入队列中。 队列中的元素即为二叉树的节点，我们从队列中依次取出元素，如果元素不为 `#`，则将其转换为整数后作为节点的值，然后将该节点加入队列中，否则将其置为 `null`。 最后返回根节点即可。 其中 n 为二叉树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
public class Codec {

    // Encodes a tree to a single string.
    public String serialize(TreeNode root) {
        if (root == null) {
            return null;
        }
        List<String> ans = new ArrayList<>();
        Deque<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            if (node != null) {
                ans.add(node.val + "");
                q.offer(node.left);
                q.offer(node.right);
            } else {
                ans.add("#");
            }
        }
        return String.join(",", ans);
    }

    // Decodes your encoded data to tree.
    public TreeNode deserialize(String data) {
        if (data == null) {
            return null;
        }
        String[] vals = data.split(",");
        int i = 0;
        TreeNode root = new TreeNode(Integer.valueOf(vals[i++]));
        Deque<TreeNode> q = new ArrayDeque<>();
        q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            if (!"#".equals(vals[i])) {
                node.left = new TreeNode(Integer.valueOf(vals[i]));
                q.offer(node.left);
            }
            ++i;
            if (!"#".equals(vals[i])) {
                node.right = new TreeNode(Integer.valueOf(vals[i]));
                q.offer(node.right);
            }
            ++i;
        }
        return root;
    }
}

// Your Codec object will be instantiated and called as such:
// Codec codec = new Codec();
// codec.deserialize(codec.serialize(root));
```

---

<a id="offer-54"></a>
## 剑指 Offer 54. 二叉搜索树的第k大节点

- 难度：简单
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/er-cha-sou-suo-shu-de-di-kda-jie-dian-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/54/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9854.%20%E4%BA%8C%E5%8F%89%E6%90%9C%E7%B4%A2%E6%A0%91%E7%9A%84%E7%AC%ACk%E5%A4%A7%E8%8A%82%E7%82%B9/README.md)

### 题目要求
给定一棵二叉搜索树，请找出其中第 `k` 大的节点的值。

### 样例数据
样例 1:
```text
输入: root = [3,1,4,null,2], k = 1
3
/ \
1 4
\
2
输出: 4
```

样例 2:
```text
输入: root = [5,3,6,2,4,null,null,1], k = 3
5
/ \
3 6
/ \
2 4
/
1
输出: 4
```

### 核心思路
`方法一：反序中序遍历`

由于二叉搜索树的中序遍历是升序的，因此可以反序中序遍历，即先递归遍历右子树，再访问根节点，最后递归遍历左子树。 这样就可以得到一个降序的序列，第 k 个节点就是第 k 大的节点。 其中 n 是二叉搜索树的节点个数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    private int k;
    private int ans;

    public int kthLargest(TreeNode root, int k) {
        this.k = k;
        dfs(root);
        return ans;
    }

    private void dfs(TreeNode root) {
        if (root == null || k == 0) {
            return;
        }
        dfs(root.right);
        if (--k == 0) {
            ans = root.val;
        }
        dfs(root.left);
    }
}
```

---

<a id="offer-55-1"></a>
## 剑指 Offer 55 - I. 二叉树的深度

- 难度：简单
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/er-cha-shu-de-shen-du-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/55.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9855%20-%20I.%20%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E6%B7%B1%E5%BA%A6/README.md)

### 题目要求
输入一棵二叉树的根节点，求该树的深度。从根节点到叶节点依次经过的节点（含根、叶节点）形成树的一条路径，最长路径的长度为树的深度。 例如： 给定二叉树 `[3,9,20,null,null,15,7]`，

### 样例数据
样例 1:
```text
3
/ \
9 20
/ \
15 7
```

### 核心思路
`方法一：递归`

我们可以用递归的方法来解决这道题。 递归的终止条件是当前节点为空，此时深度为 0；如果当前节点不为空，则当前的深度为其左右子树深度的最大值加 1，递归计算当前节点的左右子节点的深度，然后返回它们的最大值加 1。 其中 n 是二叉树的节点数。 最坏情况下，二叉树退化为链表，递归深度达到 n，系统使用 O(n) 大小的栈空间。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}
```

---

<a id="offer-55-2"></a>
## 剑指 Offer 55 - II. 平衡二叉树

- 难度：简单
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/ping-heng-er-cha-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/55.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9855%20-%20II.%20%E5%B9%B3%E8%A1%A1%E4%BA%8C%E5%8F%89%E6%A0%91/README.md)

### 题目要求
输入一棵二叉树的根节点，判断该树是不是平衡二叉树。如果某二叉树中任意节点的左右子树的深度相差不超过1，那么它就是一棵平衡二叉树。

### 样例数据
样例 1:
```text
3
/ \
9 20
/ \
15 7
```

样例 2:
```text
1
/ \
2 2
/ \
3 3
/ \
4 4
```

### 核心思路
`方法一：递归`

我们设计一个递归函数 dfs(root)，函数返回值为 root 节点的深度，如果 root 节点不平衡，返回值为 -1。 函数 dfs(root) 的递归过程如下：

- 如果 root 为空，返回 0。 - 递归计算左右子树的深度，记为 l 和 r。 - 如果 l 或 r 为 -1，或者 l 和 r 的差的绝对值大于 1，返回 -1。 - 否则，返回 max(l, r) + 1。 如果 dfs(root) 返回值不为 -1，则说明 root 节点平衡，返回 `true`，否则返回 `false`。 其中 n 为二叉树的节点数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public boolean isBalanced(TreeNode root) {
        return dfs(root) != -1;
    }

    private int dfs(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int l = dfs(root.left);
        int r = dfs(root.right);
        if (l == -1 || r == -1 || Math.abs(l - r) > 1) {
            return -1;
        }
        return 1 + Math.max(l, r);
    }
}
```

---

<a id="offer-68-1"></a>
## 剑指 Offer 68 - I. 二叉搜索树的最近公共祖先

- 难度：简单
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/er-cha-sou-suo-shu-de-zui-jin-gong-gong-zu-xian-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/68.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9868%20-%20I.%20%E4%BA%8C%E5%8F%89%E6%90%9C%E7%B4%A2%E6%A0%91%E7%9A%84%E6%9C%80%E8%BF%91%E5%85%AC%E5%85%B1%E7%A5%96%E5%85%88/README.md)

### 题目要求
给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。 百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。” 例如，给定如下二叉搜索树: root = [6,2,8,0,4,7,9,null,null,3,5]

### 样例数据
样例 1:
```text
输入: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
输出: 6
解释: 节点 2 和节点 8 的最近公共祖先是 6。
```

样例 2:
```text
输入: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
输出: 2
解释: 节点 2 和节点 4 的最近公共祖先是 2, 因为根据定义最近公共祖先节点可以为节点本身。
```

### 核心思路
`方法一：一次遍历`

从上到下遍历二叉树，找到第一个值位于 [p.val,.. q.val] 之间的结点即可。 既可以用迭代实现，也可以用递归实现。

### 复杂度
时间复杂度 O(n)，其中 n 是二叉树的结点数。 空间复杂度方面，迭代实现的空间复杂度为 O(1)，递归实现的空间复杂度为 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        while (true) {
            if (root.val < p.val && root.val < q.val) {
                root = root.right;
            } else if (root.val > p.val && root.val > q.val) {
                root = root.left;
            } else {
                return root;
            }
        }
    }
}
```

---

<a id="offer-68-2"></a>
## 剑指 Offer 68 - II. 二叉树的最近公共祖先

- 难度：简单
- 标签：二叉树
- 跳转：[官方题目](https://leetcode.cn/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/68.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9868%20-%20II.%20%E4%BA%8C%E5%8F%89%E6%A0%91%E7%9A%84%E6%9C%80%E8%BF%91%E5%85%AC%E5%85%B1%E7%A5%96%E5%85%88/README.md)

### 题目要求
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。 百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。” 例如，给定如下二叉树: root = [3,5,1,6,2,0,8,null,null,7,4]

### 样例数据
样例 1:
```text
输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出: 3
解释: 节点 5 和节点 1 的最近公共祖先是节点 3。
```

样例 2:
```text
输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出: 5
解释: 节点 5 和节点 4 的最近公共祖先是节点 5。因为根据定义最近公共祖先节点可以为节点本身。
```

### 核心思路
`方法一：递归`

根据“**最近公共祖先**”的定义，若 root 是 p, q 的最近公共祖先，则只可能为以下情况之一：

- 如果 p 和 q 分别是 root 的左右节点，那么 root 就是我们要找的最近公共祖先；
- 如果 p 和 q 都是 root 的左节点，那么返回 lowestCommonAncestor(root.left, p, q)；
- 如果 p 和 q 都是 root 的右节点，那么返回 lowestCommonAncestor(root.right, p, q)。 **边界条件讨论**：

- 如果 root 为 `null`，则说明我们已经找到最底了，返回 `null` 表示没找到；
- 如果 root 与 p 相等或者与 q 相等，则返回 root；
- 如果左子树没找到，递归函数返回 `null`，证明 p 和 q 同在 root 的右侧，那么最终的公共祖先就是右子树找到的结点；
- 如果右子树没找到，递归函数返回 `null`，证明 p 和 q 同在 root 的左侧，那么最终的公共祖先就是左子树找到的结点。 其中 n 是二叉树的节点数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) return root;
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        if (left == null) return right;
        if (right == null) return left;
        return root;
    }
}
```


### 解题模板

```
// 前中后序遍历（递归/迭代）
// 层序遍历：Queue
Queue<TreeNode> q = new LinkedList<>();
q.offer(root);
while (!q.isEmpty()) {
    int size = q.size();
    for (int i = 0; i < size; i++) {
        TreeNode node = q.poll();
        // 处理
        if (node.left != null) q.offer(node.left);
        if (node.right != null) q.offer(node.right);
    }
}

// 翻转/对称/最大深度：递归
// 最近公共祖先：后序遍历
// 路径总和：前缀和 + HashMap
```

**识别信号**：树的问题 → 先想递归（分治），再想层序（BFS），最后想迭代（栈）。

---

## 十、图 / 搜索与回溯

**来源：LeetCode Hot 100**

<a id="p-200"></a>
## 200. 岛屿数量

- 难度：中等
- 标签：深度优先搜索、广度优先搜索、并查集、数组、矩阵
- 跳转：[官方题目](https://leetcode.cn/problems/number-of-islands/) | [参考题解](https://leetcode.doocs.org/lc/200/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0200.Number%20of%20Islands/README.md)

### 题目要求
给你一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，请你计算网格中岛屿的数量。 岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。 此外，你可以假设该网格的四条边均被水包围。

### 样例数据
样例 1:
```text
输入：grid = [
['1','1','1','1','0'],
['1','1','0','1','0'],
['1','1','0','0','0'],
['0','0','0','0','0']
]
输出：1
```

样例 2:
```text
输入：grid = [
['1','1','0','0','0'],
['1','1','0','0','0'],
['0','0','1','0','0'],
['0','0','0','1','1']
]
输出：3
```

### 核心思路
`方法一：DFS`

我们可以使用深度优先搜索（DFS）来遍历每个岛屿。 遍历网格中的每个单元格 (i, j)，如果该单元格的值为 '1'，则说明我们找到了一个新的岛屿。 我们可以从该单元格开始进行 DFS，将与之相连的所有陆地单元格的值都标记为 '0'，以避免重复计数。 每次找到一个新的岛屿时，我们将岛屿数量加 1。 其中 m 和 n 分别为网格的行数和列数。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    private char[][] grid;
    private int m;
    private int n;

    public int numIslands(char[][] grid) {
        m = grid.length;
        n = grid[0].length;
        this.grid = grid;
        int ans = 0;
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (grid[i][j] == '1') {
                    dfs(i, j);
                    ++ans;
                }
            }
        }
        return ans;
    }

    private void dfs(int i, int j) {
        grid[i][j] = '0';
        int[] dirs = {-1, 0, 1, 0, -1};
        for (int k = 0; k < 4; ++k) {
            int x = i + dirs[k];
            int y = j + dirs[k + 1];
            if (x >= 0 && x < m && y >= 0 && y < n && grid[x][y] == '1') {
                dfs(x, y);
            }
        }
    }
}
```

---

<a id="p-994"></a>
## 994. 腐烂的橘子

- 难度：中等
- 标签：广度优先搜索、数组、矩阵
- 跳转：[官方题目](https://leetcode.cn/problems/rotting-oranges/) | [参考题解](https://leetcode.doocs.org/lc/994/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0900-0999/0994.Rotting%20Oranges/README.md)

### 题目要求
在给定的 `m x n` 网格 `grid` 中，每个单元格可以有以下三个值之一： - 值 `0` 代表空单元格； - 值 `1` 代表新鲜橘子； - 值 `2` 代表腐烂的橘子。 每分钟，腐烂的橘子 周围 4 个方向上相邻 的新鲜橘子都会腐烂。 返回 直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回 `-1` 。

### 样例数据
样例 1:
```text
输入：grid = [[2,1,1],[1,1,0],[0,1,1]]
输出：4
```

样例 2:
```text
输入：grid = [[2,1,1],[0,1,1],[1,0,1]]
输出：-1
解释：左下角的橘子（第 2 行， 第 0 列）永远不会腐烂，因为腐烂只会发生在 4 个方向上。
```

### 核心思路
`方法一：BFS`

我们首先遍历一遍整个网格，统计出新鲜橘子的数量，记为 cnt，并且将所有腐烂的橘子的坐标加入队列 q 中。 接下来，我们进行广度优先搜索，每一轮搜索，我们将队列中的所有腐烂的橘子向四个方向腐烂新鲜橘子，直到队列为空或者新鲜橘子的数量为 0 为止。 最后，如果新鲜橘子的数量为 0，则返回当前的轮数，否则返回 -1。 其中 m 和 n 分别是网格的行数和列数。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    public int orangesRotting(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        Deque<int[]> q = new ArrayDeque<>();
        int cnt = 0;
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (grid[i][j] == 1) {
                    ++cnt;
                } else if (grid[i][j] == 2) {
                    q.offer(new int[] {i, j});
                }
            }
        }
        final int[] dirs = {-1, 0, 1, 0, -1};
        for (int ans = 1; !q.isEmpty() && cnt > 0; ++ans) {
            for (int k = q.size(); k > 0; --k) {
                var p = q.poll();
                for (int d = 0; d < 4; ++d) {
                    int x = p[0] + dirs[d], y = p[1] + dirs[d + 1];
                    if (x >= 0 && x < m && y >= 0 && y < n && grid[x][y] == 1) {
                        grid[x][y] = 2;
                        q.offer(new int[] {x, y});
                        if (--cnt == 0) {
                            return ans;
                        }
                    }
                }
            }
        }
        return cnt > 0 ? -1 : 0;
    }
}
```

---

<a id="p-207"></a>
## 207. 课程表

- 难度：中等
- 标签：深度优先搜索、广度优先搜索、图、拓扑排序
- 跳转：[官方题目](https://leetcode.cn/problems/course-schedule/) | [参考题解](https://leetcode.doocs.org/lc/207/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0207.Course%20Schedule/README.md)

### 题目要求
你这个学期必须选修 `numCourses` 门课程，记为 `0` 到 `numCourses - 1` 。 在选修某些课程之前需要一些先修课程。 先修课程按数组 `prerequisites` 给出，其中 `prerequisites[i] = [ai, bi]` ，表示如果要学习课程 `ai` 则 必须 先学习课程 `bi` 。 - 例如，先修课程对 `[0, 1]` 表示：想要学习课程 `0` ，你需要先完成课程 `1` 。 请你判断是否可能完成所有课程的学习？如果可以，返回 `true` ；否则，返回 `false` 。

### 样例数据
样例 1:
```text
输入：numCourses = 2, prerequisites = [[1,0]]
输出：true
解释：总共有 2 门课程。学习课程 1 之前，你需要完成课程 0 。这是可能的。
```

样例 2:
```text
输入：numCourses = 2, prerequisites = [[1,0],[0,1]]
输出：false
解释：总共有 2 门课程。学习课程 1 之前，你需要先完成​课程 0 ；并且学习课程 0 之前，你还应先完成课程 1 。这是不可能的。
```

### 核心思路
`方法一：拓扑排序`

对于本题，我们可以将课程看作图中的节点，先修课程看作图中的边，那么我们可以将本题转化为判断有向图中是否存在环。 具体地，我们可以使用拓扑排序的思想，对于每个入度为 0 的节点，我们将其出度的节点的入度减 1，直到所有节点都被遍历到。 如果所有节点都被遍历到，说明图中不存在环，那么我们就可以完成所有课程的学习；否则，我们就无法完成所有课程的学习。 其中 n 和 m 分别为课程数和先修课程数。

### 复杂度
时间复杂度 O(n + m)，空间复杂度 O(n + m)。

### Java 代码
```java
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<Integer>[] g = new List[numCourses];
        Arrays.setAll(g, k -> new ArrayList<>());
        int[] indeg = new int[numCourses];
        for (var p : prerequisites) {
            int a = p[0], b = p[1];
            g[b].add(a);
            ++indeg[a];
        }
        Deque<Integer> q = new ArrayDeque<>();
        for (int i = 0; i < numCourses; ++i) {
            if (indeg[i] == 0) {
                q.offer(i);
            }
        }
        while (!q.isEmpty()) {
            int i = q.poll();
            --numCourses;
            for (int j : g[i]) {
                if (--indeg[j] == 0) {
                    q.offer(j);
                }
            }
        }
        return numCourses == 0;
    }
}
```

---

<a id="p-208"></a>
## 208. 实现 Trie (前缀树)

- 难度：中等
- 标签：设计、字典树、哈希表、字符串
- 跳转：[官方题目](https://leetcode.cn/problems/implement-trie-prefix-tree/) | [参考题解](https://leetcode.doocs.org/lc/208/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0208.Implement%20Trie%20%28Prefix%20Tree%29/README.md)

### 题目要求
Trie（发音类似 "try"）或者说 前缀树 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查。 请你实现 Trie 类： - `Trie()` 初始化前缀树对象。 - `void insert(String word)` 向前缀树中插入字符串 `word` 。 - `boolean search(String word)` 如果字符串 `word` 在前缀树中，返回 `true`（即，在检索之前已经插入）；否则，返回 `false` 。 - `boolean startsWith(String prefix)` 如果之前已经插入的字符串 `word` 的前缀之一为 `prefix` ，返回 `true` ；否则，返回 `false` 。

### 样例数据
样例 1:
```text
输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]
解释
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple"); // 返回 True
trie.search("app"); // 返回 False
trie.startsWith("app"); // 返回 True
trie.insert("app");
trie.search("app"); // 返回 True
```

### 核心思路
`方法一：前缀树`

前缀树每个节点包括两部分：

1. 指向子节点的指针数组 children，对于本题而言，数组长度为 26，即小写英文字母的数量。 children[0] 对应小写字母 a，...，children[25] 对应小写字母 z。 1. 布尔字段 isEnd，表示该节点是否为字符串的结尾。 ### 1. 插入字符串

我们从字典树的根开始，插入字符串。 对于当前字符对应的子节点，有两种情况：

- 子节点存在。 沿着指针移动到子节点，继续处理下一个字符。 - 子节点不存在。 创建一个新的子节点，记录在 children 数组的对应位置上，然后沿着指针移动到子节点，继续搜索下一个字符。 重复以上步骤，直到处理字符串的最后一个字符，然后将当前节点标记为字符串的结尾。 ### 2. 查找前缀

我们从字典树的根开始，查找前缀。 对于当前字符对应的子节点，有两种情况：

- 子节点存在。 沿着指针移动到子节点，继续搜索下一个字符。 - 子节点不存在。 说明字典树中不包含该前缀，返回空指针。 重复以上步骤，直到返回空指针或搜索完前缀的最后一个字符。 若搜索到了前缀的末尾，就说明字典树中存在该前缀。 此外，若前缀末尾对应节点的 isEnd 为真，则说明字典树中存在该字符串。

### 复杂度
时间复杂度方面，插入字符串的时间复杂度为 O(m \times |\Sigma|)，查找前缀的时间复杂度为 O(m)，其中 m 为字符串的长度，而 |\Sigma| 为字符集的大小（本题中为 26）。 空间复杂度为 O(q \times m \times |\Sigma|)，其中 q 为插入的字符串数量。

### Java 代码
```java
class Trie {
    private Trie[] children;
    private boolean isEnd;

    public Trie() {
        children = new Trie[26];
    }

    public void insert(String word) {
        Trie node = this;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new Trie();
            }
            node = node.children[idx];
        }
        node.isEnd = true;
    }

    public boolean search(String word) {
        Trie node = searchPrefix(word);
        return node != null && node.isEnd;
    }

    public boolean startsWith(String prefix) {
        Trie node = searchPrefix(prefix);
        return node != null;
    }

    private Trie searchPrefix(String s) {
        Trie node = this;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) {
                return null;
            }
            node = node.children[idx];
        }
        return node;
    }
}

/**
 * Your Trie object will be instantiated and called as such:
 * Trie obj = new Trie();
 * obj.insert(word);
 * boolean param_2 = obj.search(word);
 * boolean param_3 = obj.startsWith(prefix);
 */
```


**来源：剑指 Offer**

<a id="offer-4"></a>
## 剑指 Offer 04. 二维数组中的查找

- 难度：简单
- 标签：搜索与回溯
- 跳转：[官方题目](https://leetcode.cn/problems/er-wei-shu-zu-zhong-de-cha-zhao-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/4/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9804.%20%E4%BA%8C%E7%BB%B4%E6%95%B0%E7%BB%84%E4%B8%AD%E7%9A%84%E6%9F%A5%E6%89%BE/README.md)

### 题目要求
在一个 n * m 的二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个高效的函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。

### 样例数据
样例 1:
```text
[
[1, 4, 7, 11, 15],
[2, 5, 8, 12, 19],
[3, 6, 9, 16, 22],
[10, 13, 14, 17, 24],
[18, 21, 23, 26, 30]
]
```

### 核心思路
`方法一：二分查找`

由于每一行的所有元素升序排列，因此，对于每一行，我们可以使用二分查找找到第一个大于等于 `target` 的元素，然后判断该元素是否等于 `target`。 如果等于 `target`，说明找到了目标值，直接返回 `true`。 如果不等于 `target`，说明这一行的所有元素都小于 `target`，应该继续搜索下一行。 如果所有行都搜索完了，都没有找到目标值，说明目标值不存在，返回 `false`。 其中 m 和 n 分别为矩阵的行数和列数。

### 复杂度
时间复杂度 O(m \times \log n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public boolean findNumberIn2DArray(int[][] matrix, int target) {
        for (var row : matrix) {
            int j = Arrays.binarySearch(row, target);
            if (j >= 0) {
                return true;
            }
        }
        return false;
    }
}
```

---

<a id="offer-12"></a>
## 剑指 Offer 12. 矩阵中的路径

- 难度：中等
- 标签：搜索与回溯
- 跳转：[官方题目](https://leetcode.cn/problems/ju-zhen-zhong-de-lu-jing-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/12/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9812.%20%E7%9F%A9%E9%98%B5%E4%B8%AD%E7%9A%84%E8%B7%AF%E5%BE%84/README.md)

### 题目要求
给定一个 `m x n` 二维字符网格 `board` 和一个字符串单词 `word` 。如果 `word` 存在于网格中，返回 `true` ；否则，返回 `false` 。 单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。 例如，在下面的 3×4 的矩阵中包含单词 "ABCCED"（单词中的字母已标出）。

### 样例数据
样例 1:
```text
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
输出：true
```

样例 2:
```text
输入：board = [["a","b"],["c","d"]], word = "abcd"
输出：false
```

### 核心思路
`方法一：枚举 + DFS`

我们可以枚举矩阵的每个位置 (i, j)，以该位置为起点，采用深度优先搜索的方法寻找字符串 `word` 的路径。 如果找到了一条路径，即可返回 `true`，否则在枚举完所有的位置后，返回 `false`。 那么问题的转换为如何采用深度优先搜索的方法寻找字符串 `word` 的路径。 我们可以设计一个函数 dfs(i, j, k)，表示从位置 (i, j) 开始，且当前将要匹配的字符为 `word[k]` 的情况下，是否能够找到字符串 `word` 的路径。 如果能找到，返回 `true`，否则返回 `false`。 函数 dfs(i, j, k) 的执行流程如下：

- 如果当前字符 `word[k]` 已经匹配到字符串 `word` 的末尾，说明已经找到了字符串 `word` 的路径，返回 `true`。 - 如果当前位置 (i, j) 超出矩阵边界，或者当前位置的字符与 `word[k]` 不同，说明当前位置不在字符串 `word` 的路径上，返回 `false`。 - 否则，我们将当前位置的字符标记为已访问（防止重复搜索），然后分别向当前位置的上、下、左、右四个方向继续匹配字符 `word[k + 1]`，只要有一条路径能够匹配到字符串 `word` 的路径，就说明能够找到字符串 `word` 的路径，返回 `true`。 在回溯时，我们要将当前位置的字符还原为未访问过的状态。 其中 m 和 n 分别为矩阵的行数和列数，而 k 为字符串 `word` 的长度。 我们需要枚举矩阵中的每个位置，然后对于每个位置，我们最多需要搜索三个方向。

### 复杂度
时间复杂度 O(m \times n \times 3^k)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    private char[][] board;
    private String word;
    private int m;
    private int n;

    public boolean exist(char[][] board, String word) {
        m = board.length;
        n = board[0].length;
        this.board = board;
        this.word = word;
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (dfs(i, j, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean dfs(int i, int j, int k) {
        if (k == word.length()) {
            return true;
        }
        if (i < 0 || i >= m || j < 0 || j >= n || word.charAt(k) != board[i][j]) {
            return false;
        }
        board[i][j] = ' ';
        int[] dirs = {-1, 0, 1, 0, -1};
        boolean ans = false;
        for (int l = 0; l < 4; ++l) {
            ans = ans || dfs(i + dirs[l], j + dirs[l + 1], k + 1);
        }
        board[i][j] = word.charAt(k);
        return ans;
    }
}
```

---

<a id="offer-13"></a>
## 剑指 Offer 13. 机器人的运动范围

- 难度：中等
- 标签：搜索与回溯
- 跳转：[官方题目](https://leetcode.cn/problems/ji-qi-ren-de-yun-dong-fan-wei-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/13/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9813.%20%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%9A%84%E8%BF%90%E5%8A%A8%E8%8C%83%E5%9B%B4/README.md)

### 题目要求
地上有一个m行n列的方格，从坐标 `[0,0]` 到坐标 `[m-1,n-1]` 。一个机器人从坐标 `[0, 0] `的格子开始移动，它每次可以向左、右、上、下移动一格（不能移动到方格外），也不能进入行坐标和列坐标的数位之和大于k的格子。例如，当k为18时，机器人能够进入方格 [35, 37] ，因为3+5+3+7=18。但它不能进入方格 [35, 38]，因为3+5+3+8=19。请问该机器人能够到达多少个格子？

### 样例数据
样例 1:
```text
输入：m = 2, n = 3, k = 1
输出：3
```

样例 2:
```text
输入：m = 3, n = 1, k = 0
输出：1
```

### 核心思路
`方法一：DFS + 哈希表`

由于部分单元格不可达，因此，我们不能直接枚举所有坐标点 (i, j) 进行判断，而是应该从起点 (0, 0) 出发，搜索所有可达的节点，记录答案。 过程中，为了避免重复搜索同一个单元格，我们可以使用数组或哈希表记录所有访问过的节点。 其中 m 和 n 分别为方格的行数和列数。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    private boolean[][] vis;
    private int m;
    private int n;
    private int k;

    public int movingCount(int m, int n, int k) {
        this.m = m;
        this.n = n;
        this.k = k;
        vis = new boolean[m][n];
        return dfs(0, 0);
    }

    private int dfs(int i, int j) {
        if (i >= m || j >= n || vis[i][j] || (i % 10 + i / 10 + j % 10 + j / 10) > k) {
            return 0;
        }
        vis[i][j] = true;
        return 1 + dfs(i + 1, j) + dfs(i, j + 1);
    }
}
```

---

<a id="offer-38"></a>
## 剑指 Offer 38. 字符串的排列

- 难度：中等
- 标签：搜索与回溯
- 跳转：[官方题目](https://leetcode.cn/problems/zi-fu-chuan-de-pai-lie-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/38/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9838.%20%E5%AD%97%E7%AC%A6%E4%B8%B2%E7%9A%84%E6%8E%92%E5%88%97/README.md)

### 题目要求
输入一个字符串，打印出该字符串中字符的所有排列。 你可以以任意顺序返回这个字符串数组，但里面不能有重复元素。

### 样例数据
样例 1:
```text
输入：s = "abc"
输出：["abc","acb","bac","bca","cab","cba"]
```

### 核心思路
`方法一：回溯 + 哈希表`

我们设计一个函数 dfs(i)，表示当前排列到了第 i 个位置，我们需要在第 i 个位置上填入一个字符，这个字符可以从 s[i..n-1] 中任意选择。 函数 dfs(i) 的执行过程如下：

- 如果 i = n-1，说明当前排列已经填满，将当前排列加入答案，返回。 - 否则，我们需要在 s[i..n-1] 中选择一个字符填入第 i 个位置，我们可以使用哈希表记录哪些字符已经被填过，从而避免重复填入相同的字符。 - 在 s[i..n-1] 中选择一个字符填入第 i 个位置，然后递归执行函数 dfs(i+1)，即填入第 i+1 个位置。 - 回溯，撤销选择，即将第 i 个位置的字符填回原位。 我们在主函数中调用函数 dfs(0)，即从第 0 个位置开始填入字符。 最后返回答案数组即可。 其中 n 是字符串 s 的长度。 需要进行 n! 次排列，每次排列需要 O(n) 的时间复制字符串。

### 复杂度
时间复杂度 O(n! \times n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    private List<String> ans = new ArrayList<>();
    private char[] cs;

    public String[] permutation(String s) {
        cs = s.toCharArray();
        dfs(0);
        return ans.toArray(new String[ans.size()]);
    }

    private void dfs(int i) {
        if (i == cs.length - 1) {
            ans.add(String.valueOf(cs));
            return;
        }
        Set<Character> vis = new HashSet<>();
        for (int j = i; j < cs.length; ++j) {
            if (vis.add(cs[j])) {
                swap(i, j);
                dfs(i + 1);
                swap(i, j);
            }
        }
    }

    private void swap(int i, int j) {
        char t = cs[i];
        cs[i] = cs[j];
        cs[j] = t;
    }
}
```


### 解题模板

```
// 岛屿数量：DFS/BFS 染色
void dfs(int i, int j) {
    if (越界 || grid[i][j] != '1') return;
    grid[i][j] = '0';
    dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1);
}

// 拓扑排序：BFS + 入度
int[] indegree = new int[n];
Queue<Integer> q = new LinkedList<>();
// 入度为0的入队，依次删除边

// Trie：嵌套数组
int[][] trie = new int[N][26];
int cnt = 0;
```

**识别信号**：网格/连通分量 → DFS/BFS；课程依赖 → 拓扑排序；前缀匹配 → Trie。

---

## 十一、回溯

**来源：LeetCode Hot 100**

<a id="p-46"></a>
## 46. 全排列

- 难度：中等
- 标签：数组、回溯
- 跳转：[官方题目](https://leetcode.cn/problems/permutations/) | [参考题解](https://leetcode.doocs.org/lc/46/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0046.Permutations/README.md)

### 题目要求
给定一个不含重复数字的数组 `nums` ，返回其 所有可能的全排列 。你可以 按任意顺序 返回答案。

### 样例数据
样例 1:
```text
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

样例 2:
```text
输入：nums = [0,1]
输出：[[0,1],[1,0]]
```

### 核心思路
`方法一：DFS（回溯）`

我们设计一个函数 dfs(i) 表示已经填完了前 i 个位置，现在需要填第 i+1 个位置。 枚举所有可能的数，如果这个数没有被填过，就填入这个数，然后继续填下一个位置，直到填完所有的位置。 一共有 n! 个排列，每个排列需要 O(n) 的时间来构造。 相似题目：

- [47. 全排列 II](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0047.Permutations%20II/README.md)

### 复杂度
时间复杂度 O(n \times n!)，其中 n 是数组的长度。

### Java 代码
```java
class Solution {
    private List<List<Integer>> ans = new ArrayList<>();
    private List<Integer> t = new ArrayList<>();
    private boolean[] vis;
    private int[] nums;

    public List<List<Integer>> permute(int[] nums) {
        this.nums = nums;
        vis = new boolean[nums.length];
        dfs(0);
        return ans;
    }

    private void dfs(int i) {
        if (i == nums.length) {
            ans.add(new ArrayList<>(t));
            return;
        }
        for (int j = 0; j < nums.length; ++j) {
            if (!vis[j]) {
                vis[j] = true;
                t.add(nums[j]);
                dfs(i + 1);
                t.remove(t.size() - 1);
                vis[j] = false;
            }
        }
    }
}
```

---

<a id="p-78"></a>
## 78. 子集

- 难度：中等
- 标签：位运算、数组、回溯
- 跳转：[官方题目](https://leetcode.cn/problems/subsets/) | [参考题解](https://leetcode.doocs.org/lc/78/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0078.Subsets/README.md)

### 题目要求
给你一个整数数组 `nums` ，数组中的元素 互不相同 。返回该数组所有可能的子集（幂集）。 解集 不能 包含重复的子集。你可以按 任意顺序 返回解集。

### 样例数据
样例 1:
```text
输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

样例 2:
```text
输入：nums = [0]
输出：[[],[0]]
```

### 核心思路
`方法一：DFS(回溯)`

我们设计一个函数 dfs(i)，表示从数组的第 i 个元素开始搜索所有子集。 函数 dfs(i) 的执行逻辑如下：

- 如果 i=n，表示当前已经搜索结束，将当前得到的子集 t 加入答案数组 ans 中，然后返回；
- 否则，我们可以选择不选择当前元素，直接执行 dfs(i+1)；也可以选择当前元素，即把当前元素 nums[i] 加入子集 t，然后执行 dfs(i+1)，注意要在执行 dfs(i+1) 以后再将 nums[i] 从子集 t 中移除（回溯）。 在主函数中，我们调用 dfs(0)，即从数组的第一个元素开始搜索所有子集。 最后返回答案数组 ans 即可。 其中 n 为数组的长度。 一共有 2^n 个子集，每个子集需要 O(n) 的时间来构造。

### 复杂度
时间复杂度 O(n\times 2^n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    private List<List<Integer>> ans = new ArrayList<>();
    private List<Integer> t = new ArrayList<>();
    private int[] nums;

    public List<List<Integer>> subsets(int[] nums) {
        this.nums = nums;
        dfs(0);
        return ans;
    }

    private void dfs(int i) {
        if (i == nums.length) {
            ans.add(new ArrayList<>(t));
            return;
        }
        dfs(i + 1);
        t.add(nums[i]);
        dfs(i + 1);
        t.remove(t.size() - 1);
    }
}
```

---

<a id="p-17"></a>
## 17. 电话号码的字母组合

- 难度：中等
- 标签：哈希表、字符串、回溯
- 跳转：[官方题目](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/) | [参考题解](https://leetcode.doocs.org/lc/17/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0017.Letter%20Combinations%20of%20a%20Phone%20Number/README.md)

### 题目要求
给定一个仅包含数字 `2-9` 的字符串，返回所有它能表示的字母组合。答案可以按 任意顺序 返回。 给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

### 样例数据
样例 1:
```text
输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

样例 2:
```text
输入：digits = "2"
输出：["a","b","c"]
```

### 核心思路
`方法一：遍历`

我们先用一个数组或者哈希表存储每个数字对应的字母，然后遍历每个数字，将其对应的字母与之前的结果进行组合，得到新的结果。 其中 n 是输入数字的长度。

### 复杂度
时间复杂度 O(4^n)。 空间复杂度 O(4^n)。

### Java 代码
```java
class Solution {
    public List<String> letterCombinations(String digits) {
        List<String> ans = new ArrayList<>();
        if (digits.length() == 0) {
            return ans;
        }
        ans.add("");
        String[] d = new String[] {"abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
        for (char i : digits.toCharArray()) {
            String s = d[i - '2'];
            List<String> t = new ArrayList<>();
            for (String a : ans) {
                for (String b : s.split("")) {
                    t.add(a + b);
                }
            }
            ans = t;
        }
        return ans;
    }
}
```

---

<a id="p-39"></a>
## 39. 组合总和

- 难度：中等
- 标签：数组、回溯
- 跳转：[官方题目](https://leetcode.cn/problems/combination-sum/) | [参考题解](https://leetcode.doocs.org/lc/39/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0039.Combination%20Sum/README.md)

### 题目要求
给你一个 无重复元素 的整数数组 `candidates` 和一个目标整数 `target` ，找出 `candidates` 中可以使数字和为目标数 `target` 的 所有 不同组合 ，并以列表形式返回。你可以按 任意顺序 返回这些组合。 `candidates` 中的 同一个 数字可以 无限制重复被选取 。如果至少一个数字的被选数量不同，则两种组合是不同的。 对于给定的输入，保证和为 `target` 的不同组合数少于 `150` 个。

### 样例数据
样例 1:
```text
输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
解释：
2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
7 也是一个候选， 7 = 7 。
仅有这两种组合。
```

样例 2:
```text
输入: candidates = [2,3,5], target = 8
输出: [[2,2,2,2],[2,3,3],[3,5]]
```

### 核心思路
`方法一：排序 + 剪枝 + 回溯`

我们可以先对数组进行排序，方便剪枝。 接下来，我们设计一个函数 dfs(i, s)，表示从下标 i 开始搜索，且剩余目标值为 s，其中 i 和 s 都是非负整数，当前搜索路径为 t，答案为 ans。 在函数 dfs(i, s) 中，我们先判断 s 是否为 0，如果是，则将当前搜索路径 t 加入答案 ans 中，然后返回。 如果 s \lt candidates[i]，说明当前下标及后面的下标的元素都大于剩余目标值 s，路径不合法，直接返回。 否则，我们从下标 i 开始搜索，搜索的下标范围是 j \in [i, n)，其中 n 为数组 candidates 的长度。 在搜索的过程中，我们将当前下标的元素加入搜索路径 t，递归调用函数 dfs(j, s - candidates[j])，递归结束后，将当前下标的元素从搜索路径 t 中移除。 在主函数中，我们只要调用函数 dfs(0, target)，即可得到答案。 其中 n 为数组 candidates 的长度。 相似题目：

- [40. 组合总和 II](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0040.Combination%20Sum%20II/README.md)
- [77. 组合](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0077.Combinations/README.md)
- [216. 组合总和 III](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0216.Combination%20Sum%20III/README.md)

### 复杂度
时间复杂度 O(2^n \times n)，空间复杂度 O(n)。 由于剪枝，实际的时间复杂度要远小于 O(2^n \times n)。

### Java 代码
```java
class Solution {
    private List<List<Integer>> ans = new ArrayList<>();
    private List<Integer> t = new ArrayList<>();
    private int[] candidates;

    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates);
        this.candidates = candidates;
        dfs(0, target);
        return ans;
    }

    private void dfs(int i, int s) {
        if (s == 0) {
            ans.add(new ArrayList(t));
            return;
        }
        if (s < candidates[i]) {
            return;
        }
        for (int j = i; j < candidates.length; ++j) {
            t.add(candidates[j]);
            dfs(j, s - candidates[j]);
            t.remove(t.size() - 1);
        }
    }
}
```

---

<a id="p-22"></a>
## 22. 括号生成

- 难度：中等
- 标签：字符串、动态规划、回溯
- 跳转：[官方题目](https://leetcode.cn/problems/generate-parentheses/) | [参考题解](https://leetcode.doocs.org/lc/22/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0022.Generate%20Parentheses/README.md)

### 题目要求
数字 `n` 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。

### 样例数据
样例 1:
```text
输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]
```

样例 2:
```text
输入：n = 1
输出：["()"]
```

### 核心思路
`方法一：DFS + 剪枝`

题目中 n 的范围为 [1, 8]，因此我们直接通过“暴力搜索 + 剪枝”的方式通过本题。 我们设计一个函数 dfs(l, r, t)，其中 l 和 r 分别表示左括号和右括号的数量，而 t 表示当前的括号序列。 那么我们可以得到如下的递归结构：

- 如果 l \gt n 或者 r \gt n 或者 l \lt r，那么当前括号组合 t 不合法，直接返回；
- 如果 l = n 且 r = n，那么当前括号组合 t 合法，将其加入答案数组 `ans` 中，直接返回；
- 我们可以选择添加一个左括号，递归执行 `dfs(l + 1, r, t + "(")`；
- 我们也可以选择添加一个右括号，递归执行 `dfs(l, r + 1, t + ")")`。

### 复杂度
时间复杂度 O(2^{n\times 2} \times n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    private List<String> ans = new ArrayList<>();
    private int n;

    public List<String> generateParenthesis(int n) {
        this.n = n;
        dfs(0, 0, "");
        return ans;
    }

    private void dfs(int l, int r, String t) {
        if (l > n || r > n || l < r) {
            return;
        }
        if (l == n && r == n) {
            ans.add(t);
            return;
        }
        dfs(l + 1, r, t + "(");
        dfs(l, r + 1, t + ")");
    }
}
```

---

<a id="p-79"></a>
## 79. 单词搜索

- 难度：中等
- 标签：深度优先搜索、数组、字符串、回溯、矩阵
- 跳转：[官方题目](https://leetcode.cn/problems/word-search/) | [参考题解](https://leetcode.doocs.org/lc/79/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0079.Word%20Search/README.md)

### 题目要求
给定一个 `m x n` 二维字符网格 `board` 和一个字符串单词 `word` 。如果 `word` 存在于网格中，返回 `true` ；否则，返回 `false` 。 单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

### 样例数据
样例 1:
```text
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCCED"
输出：true
```

样例 2:
```text
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "SEE"
输出：true
```

### 核心思路
`方法一：DFS(回溯)`

我们可以枚举网格的每一个位置 (i, j) 作为搜索的起点，然后从起点开始进行深度优先搜索，如果可以搜索到单词的末尾，就说明单词存在，否则说明单词不存在。 因此，我们设计一个函数 dfs(i, j, k)，表示从网格的 (i, j) 位置出发，且从单词的第 k 个字符开始搜索，是否能够搜索成功。 函数 dfs(i, j, k) 的执行步骤如下：

- 如果 k = |word|-1，说明已经搜索到单词的最后一个字符，此时只需要判断网格 (i, j) 位置的字符是否等于 word[k]，如果相等则说明单词存在，否则说明单词不存在。 无论单词是否存在，都无需继续往下搜索，因此直接返回结果。 - 否则，如果 word[k] 字符不等于网格 (i, j) 位置的字符，说明本次搜索失败，直接返回 `false`。 - 否则，我们将网格 (i, j) 位置的字符暂存于 c 中，然后将此位置的字符修改为一个特殊字符 `'0'`，代表此位置的字符已经被使用过，防止之后搜索时重复使用。 然后我们从 (i, j) 位置的上、下、左、右四个方向分别出发，去搜索网格中第 k+1 个字符，如果四个方向有任何一个方向搜索成功，就说明搜索成功，否则说明搜索失败，此时我们需要还原网格 (i, j) 位置的字符，即把 c 放回网格 (i, j) 位置（回溯）。 在主函数中，我们枚举网格中的每一个位置 (i, j) 作为起点，如果调用 dfs(i, j, 0) 返回 `true`，就说明单词存在，否则说明单词不存在，返回 `false`。 其中 m 和 n 分别是网格的行数和列数；而 k 是字符串 word 的长度。

### 复杂度
时间复杂度 O(m \times n \times 3^k)，空间复杂度 O(\min(m \times n, k))。

### Java 代码
```java
class Solution {
    private int m;
    private int n;
    private String word;
    private char[][] board;

    public boolean exist(char[][] board, String word) {
        m = board.length;
        n = board[0].length;
        this.word = word;
        this.board = board;
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (dfs(i, j, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean dfs(int i, int j, int k) {
        if (k == word.length() - 1) {
            return board[i][j] == word.charAt(k);
        }
        if (board[i][j] != word.charAt(k)) {
            return false;
        }
        char c = board[i][j];
        board[i][j] = '0';
        int[] dirs = {-1, 0, 1, 0, -1};
        for (int u = 0; u < 4; ++u) {
            int x = i + dirs[u], y = j + dirs[u + 1];
            if (x >= 0 && x < m && y >= 0 && y < n && board[x][y] != '0' && dfs(x, y, k + 1)) {
                return true;
            }
        }
        board[i][j] = c;
        return false;
    }
}
```

---

<a id="p-131"></a>
## 131. 分割回文串

- 难度：中等
- 标签：字符串、动态规划、回溯
- 跳转：[官方题目](https://leetcode.cn/problems/palindrome-partitioning/) | [参考题解](https://leetcode.doocs.org/lc/131/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0131.Palindrome%20Partitioning/README.md)

### 题目要求
给你一个字符串 `s`，请你将 `s` 分割成一些 子串，使每个子串都是 回文串 。返回 `s` 所有可能的分割方案。

### 样例数据
样例 1:
```text
输入：s = "aab"
输出：[["a","a","b"],["aa","b"]]
```

样例 2:
```text
输入：s = "a"
输出：[["a"]]
```

### 核心思路
`方法一：预处理 + DFS(回溯)`

我们可以使用动态规划，预处理出字符串中的任意子串是否为回文串，即 f[i][j] 表示子串 s[i..j] 是否为回文串。 接下来，我们设计一个函数 dfs(i)，表示从字符串的第 i 个字符开始，分割成若干回文串，当前分割方案为 t。 如果 i=|s|，说明已经分割完成，我们将 t 放入答案数组中，然后返回。 否则，我们可以从 i 开始，从小到大依次枚举结束位置 j，如果 s[i..j] 是回文串，那么就把 s[i..j] 加入到 t 中，然后继续递归 dfs(j+1)，回溯的时候要弹出 s[i..j]。 其中 n 是字符串的长度。

### 复杂度
时间复杂度 O(n \times 2^n)，空间复杂度 O(n^2)。

### Java 代码
```java
class Solution {
    private int n;
    private String s;
    private boolean[][] f;
    private List<String> t = new ArrayList<>();
    private List<List<String>> ans = new ArrayList<>();

    public List<List<String>> partition(String s) {
        n = s.length();
        f = new boolean[n][n];
        for (int i = 0; i < n; ++i) {
            Arrays.fill(f[i], true);
        }
        for (int i = n - 1; i >= 0; --i) {
            for (int j = i + 1; j < n; ++j) {
                f[i][j] = s.charAt(i) == s.charAt(j) && f[i + 1][j - 1];
            }
        }
        this.s = s;
        dfs(0);
        return ans;
    }

    private void dfs(int i) {
        if (i == s.length()) {
            ans.add(new ArrayList<>(t));
            return;
        }
        for (int j = i; j < n; ++j) {
            if (f[i][j]) {
                t.add(s.substring(i, j + 1));
                dfs(j + 1);
                t.remove(t.size() - 1);
            }
        }
    }
}
```

---

<a id="p-51"></a>
## 51. N 皇后

- 难度：困难
- 标签：数组、回溯
- 跳转：[官方题目](https://leetcode.cn/problems/n-queens/) | [参考题解](https://leetcode.doocs.org/lc/51/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0051.N-Queens/README.md)

### 题目要求
按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。 n 皇后问题 研究的是如何将 `n` 个皇后放置在 `n×n` 的棋盘上，并且使皇后彼此之间不能相互攻击。 给你一个整数 `n` ，返回所有不同的 n 皇后问题 的解决方案。 每一种解法包含一个不同的 n 皇后问题 的棋子放置方案，该方案中 `'Q'` 和 `'.'` 分别代表了皇后和空位。

### 样例数据
样例 1:
```text
输入：n = 4
输出：[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
解释：如上图所示，4 皇后问题存在两个不同的解法。
```

样例 2:
```text
输入：n = 1
输出：[["Q"]]
```

### 核心思路
`方法一：DFS(回溯)`

我们定义三个数组 col, dg 和 udg，分别表示列、正对角线和反对角线上的是否有皇后，如果位置 (i, j) 有皇后，那么 col[j], dg[i + j] 和 udg[n - i + j] 都为 1。 另外，我们用一个数组 g 记录当前棋盘的状态，初始时 g 中的所有元素都是 `'.'`。 接下来，我们定义一个函数 dfs(i)，表示从第 i 行开始放置皇后。 在 dfs(i) 中，如果 i=n，说明我们已经完成了所有皇后的放置，我们将当前 g 放入答案数组中，递归结束。 否则，我们枚举当前行的每一列 j，如果位置 (i, j) 没有皇后，即 col[j], dg[i + j] 和 udg[n - i + j] 都为 0，那么我们可以放置皇后，即把 g[i][j] 改为 `'Q'`，并将 col[j], dg[i + j] 和 udg[n - i + j] 都置为 1，然后继续搜索下一行，即调用 dfs(i + 1)，递归结束后，我们需要将 g[i][j] 改回 `'.'` 并将 col[j], dg[i + j] 和 udg[n - i + j] 都置为 0。 在主函数中，我们调用 dfs(0) 开始递归，最后返回答案数组即可。 其中 n 是题目给定的整数。

### 复杂度
时间复杂度 (n^2 \times n!)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    private List<List<String>> ans = new ArrayList<>();
    private int[] col;
    private int[] dg;
    private int[] udg;
    private String[][] g;
    private int n;

    public List<List<String>> solveNQueens(int n) {
        this.n = n;
        col = new int[n];
        dg = new int[n << 1];
        udg = new int[n << 1];
        g = new String[n][n];
        for (int i = 0; i < n; ++i) {
            Arrays.fill(g[i], ".");
        }
        dfs(0);
        return ans;
    }

    private void dfs(int i) {
        if (i == n) {
            List<String> t = new ArrayList<>();
            for (int j = 0; j < n; ++j) {
                t.add(String.join("", g[j]));
            }
            ans.add(t);
            return;
        }
        for (int j = 0; j < n; ++j) {
            if (col[j] + dg[i + j] + udg[n - i + j] == 0) {
                g[i][j] = "Q";
                col[j] = dg[i + j] = udg[n - i + j] = 1;
                dfs(i + 1);
                col[j] = dg[i + j] = udg[n - i + j] = 0;
                g[i][j] = ".";
            }
        }
    }
}
```


### 解题模板

```
// 全排列
void dfs(int i) {
    if (i == n) { ans.add(new ArrayList<>(path)); return; }
    for (int j = i; j < n; j++) {
        swap(i, j); dfs(i + 1); swap(i, j);
    }
}

// 子集/组合
void dfs(int start, int remain) {
    if (remain == 0) { ans.add(new ArrayList<>(path)); return; }
    for (int i = start; i < n; i++) {
        path.add(nums[i]); dfs(i + 1, remain - nums[i]); path.removeLast();
    }
}
```

**识别信号**：全排列/组合/子集/分割 → 回溯（选或不选 + 撤销）。

---

## 十二、二分查找

**来源：LeetCode Hot 100**

<a id="p-35"></a>
## 35. 搜索插入位置

- 难度：简单
- 标签：数组、二分查找
- 跳转：[官方题目](https://leetcode.cn/problems/search-insert-position/) | [参考题解](https://leetcode.doocs.org/lc/35/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0035.Search%20Insert%20Position/README.md)

### 题目要求
给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。 请必须使用时间复杂度为 `O(log n)` 的算法。

### 样例数据
样例 1:
```text
输入: nums = [1,3,5,6], target = 5
输出: 2
```

样例 2:
```text
输入: nums = [1,3,5,6], target = 2
输出: 1
```

### 核心思路
`方法一：二分查找`

由于 nums 数组已经有序，因此我们可以使用二分查找的方法找到目标值 target 的插入位置。 其中 n 为数组 nums 的长度。

### 复杂度
时间复杂度 O(\log n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int searchInsert(int[] nums, int target) {
        int l = 0, r = nums.length;
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (nums[mid] >= target) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }
}
```

---

<a id="p-74"></a>
## 74. 搜索二维矩阵

- 难度：中等
- 标签：数组、二分查找、矩阵
- 跳转：[官方题目](https://leetcode.cn/problems/search-a-2d-matrix/) | [参考题解](https://leetcode.doocs.org/lc/74/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0074.Search%20a%202D%20Matrix/README.md)

### 题目要求
给你一个满足下述两条属性的 `m x n` 整数矩阵： - 每行中的整数从左到右按非严格递增顺序排列。 - 每行的第一个整数大于前一行的最后一个整数。 给你一个整数 `target` ，如果 `target` 在矩阵中，返回 `true` ；否则，返回 `false` 。

### 样例数据
样例 1:
```text
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true
```

样例 2:
```text
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
输出：false
```

### 核心思路
`方法一：二分查找`

我们将二维矩阵逻辑展开，然后二分查找即可。 其中 m 和 n 分别是矩阵的行数和列数。

### 复杂度
时间复杂度 O(\log (m \times n))。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        int left = 0, right = m * n - 1;
        while (left < right) {
            int mid = (left + right) >> 1;
            int x = mid / n, y = mid % n;
            if (matrix[x][y] >= target) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return matrix[left / n][left % n] == target;
    }
}
```

---

<a id="p-34"></a>
## 34. 在排序数组中查找元素的第一个和最后一个位置

- 难度：中等
- 标签：数组、二分查找
- 跳转：[官方题目](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/) | [参考题解](https://leetcode.doocs.org/lc/34/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0034.Find%20First%20and%20Last%20Position%20of%20Element%20in%20Sorted%20Array/README.md)

### 题目要求
给你一个按照非递减顺序排列的整数数组 `nums`，和一个目标值 `target`。请你找出给定目标值在数组中的开始位置和结束位置。 如果数组中不存在目标值 `target`，返回 `[-1, -1]`。 你必须设计并实现时间复杂度为 `O(log n)` 的算法解决此问题。

### 样例数据
样例 1:
```text
输入：nums = [`5,7,7,8,8,10]`, target = 8
输出：[3,4]
```

样例 2:
```text
输入：nums = [`5,7,7,8,8,10]`, target = 6
输出：[-1,-1]
```

### 核心思路
`方法一：二分查找`

我们可以进行两次二分查找，分别查找出左边界和右边界。

### 复杂度
时间复杂度 O(\log n)，其中 n 是数组 nums 的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int[] searchRange(int[] nums, int target) {
        int l = search(nums, target);
        int r = search(nums, target + 1);
        return l == r ? new int[] {-1, -1} : new int[] {l, r - 1};
    }

    private int search(int[] nums, int x) {
        int left = 0, right = nums.length;
        while (left < right) {
            int mid = (left + right) >>> 1;
            if (nums[mid] >= x) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }
}
```

---

<a id="p-33"></a>
## 33. 搜索旋转排序数组

- 难度：中等
- 标签：数组、二分查找
- 跳转：[官方题目](https://leetcode.cn/problems/search-in-rotated-sorted-array/) | [参考题解](https://leetcode.doocs.org/lc/33/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0033.Search%20in%20Rotated%20Sorted%20Array/README.md)

### 题目要求
整数数组 `nums` 按升序排列，数组中的值 互不相同 。 在传递给函数之前，`nums` 在预先未知的某个下标 `k`（`0 <= k < nums.length`）上进行了 向左旋转，使数组变为 `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`（下标 从 0 开始 计数）。例如， `[0,1,2,4,5,6,7]` 下标 `3` 上向左旋转后可能变为 `[4,5,6,7,0,1,2]` 。 给你 旋转后 的数组 `nums` 和一个整数 `target` ，如果 `nums` 中存在这个目标值 `target` ，则返回它的下标，否则返回 `-1` 。 你必须设计一个时间复杂度为 `O(log n)` 的算法解决此问题。

### 样例数据
样例 1:
```text
输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4
```

样例 2:
```text
输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
```

### 核心思路
`方法一：二分查找`

我们使用二分，将数组分割成 [left,.. mid], [mid + 1,.. right] 两部分，这时候可以发现，其中有一部分一定是有序的。 因此，我们可以根据有序的那一部分，判断 target 是否在这一部分中：

- 若 [0,.. mid] 范围内的元素构成有序数组：
    - 若满足 nums[0] \leq target \leq nums[mid]，那么我们搜索范围可以缩小为 [left,.. mid]；
    - 否则，在 [mid + 1,.. right] 中查找；
- 若 [mid + 1, n - 1] 范围内的元素构成有序数组：
    - 若满足 nums[mid] \lt target \leq nums[n - 1]，那么我们搜索范围可以缩小为 [mid + 1,.. right]；
    - 否则，在 [left,.. mid] 中查找。 二分查找终止条件是 left \geq right，若结束后发现 nums[left] 与 target 不等，说明数组中不存在值为 target 的元素，返回 -1，否则返回下标 left。

### 复杂度
时间复杂度 O(\log n)，其中 n 是数组 nums 的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int search(int[] nums, int target) {
        int n = nums.length;
        int left = 0, right = n - 1;
        while (left < right) {
            int mid = (left + right) >> 1;
            if (nums[0] <= nums[mid]) {
                if (nums[0] <= target && target <= nums[mid]) {
                    right = mid;
                } else {
                    left = mid + 1;
                }
            } else {
                if (nums[mid] < target && target <= nums[n - 1]) {
                    left = mid + 1;
                } else {
                    right = mid;
                }
            }
        }
        return nums[left] == target ? left : -1;
    }
}
```

---

<a id="p-153"></a>
## 153. 寻找旋转排序数组中的最小值

- 难度：中等
- 标签：数组、二分查找
- 跳转：[官方题目](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/) | [参考题解](https://leetcode.doocs.org/lc/153/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0153.Find%20Minimum%20in%20Rotated%20Sorted%20Array/README.md)

### 题目要求
已知一个长度为 `n` 的数组，预先按照升序排列，经由 `1` 到 `n` 次 旋转 后，得到输入数组。例如，原数组 `nums = [0,1,2,4,5,6,7]` 在变化后可能得到： - 若旋转 `4` 次，则可以得到 `[4,5,6,7,0,1,2]` - 若旋转 `7` 次，则可以得到 `[0,1,2,4,5,6,7]` 注意，数组 `[a[0], a[1], a[2], ..., a[n-1]]` 旋转一次 的结果为数组 `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]` 。 给你一个元素值 互不相同 的数组 `nums` ，它原来是一个升序排列的数组，并按上述情形进行了多次旋转。请你找出并返回数组中的 最小元素 。 你必须设计一个时间复杂度为 `O(log n)` 的算法解决此问题。

### 样例数据
样例 1:
```text
输入：nums = [3,4,5,1,2]
输出：1
解释：原数组为 [1,2,3,4,5] ，旋转 3 次得到输入数组。
```

样例 2:
```text
输入：nums = [4,5,6,7,0,1,2]
输出：0
解释：原数组为 [0,1,2,4,5,6,7] ，旋转 4 次得到输入数组。
```

### 核心思路
`方法一：二分查找`

初始，判断数组首尾元素的大小关系，若 `nums[0] <= nums[n - 1]` 条件成立，则说明当前数组已经是递增数组，最小值一定是数组第一个元素，提前返回 `nums[0]`。 否则，进行二分判断。 若 `nums[0] <= nums[mid]`，说明 `[left, mid]` 范围内的元素构成递增数组，最小值一定在 `mid` 的右侧，否则说明 `[mid + 1, right]` 范围内的元素构成递增数组，最小值一定在 `mid` 的左侧。 ---

除了 `nums[0]`，也可以以 `nums[right]` 作为参照物，若 `nums[mid] < nums[right]` 成立，则最小值存在于 `[left, mid]` 范围当中，否则存在于 `[mid + 1, right]`。

### 复杂度
时间复杂度：O(logN)

### Java 代码
```java
class Solution {
    public int findMin(int[] nums) {
        int n = nums.length;
        if (nums[0] <= nums[n - 1]) {
            return nums[0];
        }
        int left = 0, right = n - 1;
        while (left < right) {
            int mid = (left + right) >> 1;
            if (nums[0] <= nums[mid]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return nums[left];
    }
}
```

---

<a id="p-4"></a>
## 4. 寻找两个正序数组的中位数

- 难度：困难
- 标签：数组、二分查找、分治
- 跳转：[官方题目](https://leetcode.cn/problems/median-of-two-sorted-arrays/) | [参考题解](https://leetcode.doocs.org/lc/4/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0004.Median%20of%20Two%20Sorted%20Arrays/README.md)

### 题目要求
给定两个大小分别为 `m` 和 `n` 的正序（从小到大）数组 `nums1` 和 `nums2`。请你找出并返回这两个正序数组的 中位数 。 算法的时间复杂度应该为 `O(log (m+n))` 。

### 样例数据
样例 1:
```text
输入：nums1 = [1,3], nums2 = [2]
输出：2.00000
解释：合并数组 = [1,2,3] ，中位数 2
```

样例 2:
```text
输入：nums1 = [1,2], nums2 = [3,4]
输出：2.50000
解释：合并数组 = [1,2,3,4] ，中位数 (2 + 3) / 2 = 2.5
```

### 核心思路
`方法一：分治`

如果 m + n 是奇数，那么中位数就是第 \lfloor\frac{m + n + 1}{2}\rfloor 个数；如果 m + n 是偶数，那么中位数就是第 \lfloor\frac{m + n + 1}{2}\rfloor 和第 \lfloor\frac{m + n + 2}{2}\rfloor 个数的平均数。 实际上，我们可以统一为求第 \lfloor\frac{m + n + 1}{2}\rfloor 个数和第 \lfloor\frac{m + n + 2}{2}\rfloor 个数的平均数。 因此，我们可以设计一个函数 f(i, j, k)，表示在数组 nums1 的区间 [i, m) 和数组 nums2 的区间 [j, n) 中，求第 k 小的数。 那么中位数就是 f(0, 0, \lfloor\frac{m + n + 1}{2}\rfloor) 和 f(0, 0, \lfloor\frac{m + n + 2}{2}\rfloor) 的平均数。 函数 f(i, j, k) 的实现思路如下：

- 如果 i \geq m，说明数组 nums1 的区间 [i, m) 为空，因此直接返回 nums2[j + k - 1]；
- 如果 j \geq n，说明数组 nums2 的区间 [j, n) 为空，因此直接返回 nums1[i + k - 1]；
- 如果 k = 1，说明要找第一个数，因此只需要返回 nums1[i] 和 nums2[j] 中的最小值；
- 否则，我们分别在两个数组中查找第 \lfloor\frac{k}{2}\rfloor 个数，设为 x 和 y。 （注意，如果某个数组不存在第 \lfloor\frac{k}{2}\rfloor 个数，那么我们将第 \lfloor\frac{k}{2}\rfloor 个数视为 +\infty。 ）比较 x 和 y 的大小：
    - 如果 x \leq y，则说明数组 nums1 的第 \lfloor\frac{k}{2}\rfloor 个数不可能是第 k 小的数，因此我们可以排除数组 nums1 的区间 [i, i + \lfloor\frac{k}{2}\rfloor)，递归调用 f(i + \lfloor\frac{k}{2}\rfloor, j, k - \lfloor\frac{k}{2}\rfloor)。 - 如果 x > y，则说明数组 nums2 的第 \lfloor\frac{k}{2}\rfloor 个数不可能是第 k 小的数，因此我们可以排除数组 nums2 的区间 [j, j + \lfloor\frac{k}{2}\rfloor)，递归调用 f(i, j + \lfloor\frac{k}{2}\rfloor, k - \lfloor\frac{k}{2}\rfloor)。 其中 m 和 n 分别是数组 nums1 和 nums2 的长度。

### 复杂度
题目要求算法的时间复杂度为 O(\log (m + n))，因此不能直接遍历两个数组，而是需要使用二分查找的方法。 时间复杂度 O(\log(m + n))，空间复杂度 O(\log(m + n))。

### Java 代码
```java
class Solution {
    private int m;
    private int n;
    private int[] nums1;
    private int[] nums2;

    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        m = nums1.length;
        n = nums2.length;
        this.nums1 = nums1;
        this.nums2 = nums2;
        int a = f(0, 0, (m + n + 1) / 2);
        int b = f(0, 0, (m + n + 2) / 2);
        return (a + b) / 2.0;
    }

    private int f(int i, int j, int k) {
        if (i >= m) {
            return nums2[j + k - 1];
        }
        if (j >= n) {
            return nums1[i + k - 1];
        }
        if (k == 1) {
            return Math.min(nums1[i], nums2[j]);
        }
        int p = k / 2;
        int x = i + p - 1 < m ? nums1[i + p - 1] : 1 << 30;
        int y = j + p - 1 < n ? nums2[j + p - 1] : 1 << 30;
        return x < y ? f(i + p, j, k - p) : f(i, j + p, k - p);
    }
}
```


**来源：剑指 Offer**

<a id="offer-11"></a>
## 剑指 Offer 11. 旋转数组的最小数字

- 难度：简单
- 标签：二分
- 跳转：[官方题目](https://leetcode.cn/problems/xuan-zhuan-shu-zu-de-zui-xiao-shu-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/11/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9811.%20%E6%97%8B%E8%BD%AC%E6%95%B0%E7%BB%84%E7%9A%84%E6%9C%80%E5%B0%8F%E6%95%B0%E5%AD%97/README.md)

### 题目要求
把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。 给你一个可能存在 重复 元素值的数组 `numbers` ，它原来是一个升序排列的数组，并按上述情形进行了一次旋转。请返回旋转数组的最小元素。例如，数组 `[3,4,5,1,2]` 为 `[1,2,3,4,5]` 的一次旋转，该数组的最小值为1。

### 样例数据
样例 1:
```text
输入：[3,4,5,1,2]
输出：1
```

样例 2:
```text
输入：[2,2,2,0,1]
输出：0
```

### 核心思路
`方法一：二分查找`

二分查找的变种，需要考虑重复元素的情况。 我们定义两个指针 l 和 r 分别指向数组的左右两端，每次取中间元素 `numbers[mid]` 与右端元素 `numbers[r]` 比较，有以下三种情况：

- `numbers[mid] > numbers[r]`：中间元素一定不是最小值，因此 l = mid + 1；
- `numbers[mid] < numbers[r]`：中间元素可能是最小值，因此 r = mid；
- `numbers[mid] == numbers[r]`：无法确定最小值的位置，但可以简单地缩小搜索范围，因此 r = r - 1。 循环结束时，指针 l 和 r 指向同一个元素，即为最小值。 其中 n 为数组长度。

### 复杂度
时间复杂度 (\log n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int minArray(int[] numbers) {
        int l = 0, r = numbers.length - 1;
        while (l < r) {
            int m = (l + r) >>> 1;
            if (numbers[m] > numbers[r]) {
                l = m + 1;
            } else if (numbers[m] < numbers[r]) {
                r = m;
            } else {
                --r;
            }
        }
        return numbers[l];
    }
}
```

---

<a id="offer-53-1"></a>
## 剑指 Offer 53 - I. 在排序数组中查找数字 I

- 难度：未标注
- 标签：二分
- 跳转：[官方题目](https://leetcode.cn/problems/zai-pai-xu-shu-zu-zhong-cha-zhao-shu-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/53.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9853%20-%20I.%20%E5%9C%A8%E6%8E%92%E5%BA%8F%E6%95%B0%E7%BB%84%E4%B8%AD%E6%9F%A5%E6%89%BE%E6%95%B0%E5%AD%97%20I/README.md)

### 题目要求
统计一个数字在排序数组中出现的次数。

### 样例数据
样例 1:
```text
输入: nums = [`5,7,7,8,8,10]`, target = 8
输出: 2
```

样例 2:
```text
输入: nums = [`5,7,7,8,8,10]`, target = 6
输出: 0
```

### 核心思路
`方法一：二分查找`

由于数组 `nums` 已排好序，我们可以使用二分查找的方法找到数组中第一个大于等于 `target` 的元素的下标 l，以及第一个大于 `target` 的元素的下标 r，那么 `target` 的个数就是 r - l。

### 复杂度
时间复杂度 O(\log n)，其中 n 为数组的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    private int[] nums;

    public int search(int[] nums, int target) {
        this.nums = nums;
        int l = search(target);
        int r = search(target + 1);
        return r - l;
    }

    private int search(int x) {
        int l = 0, r = nums.length;
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (nums[mid] >= x) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }
}
```

---

<a id="offer-53-2"></a>
## 剑指 Offer 53 - II. 0～n-1中缺失的数字

- 难度：未标注
- 标签：二分
- 跳转：[官方题目](https://leetcode.cn/problems/que-shi-de-shu-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/53.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9853%20-%20II.%200%EF%BD%9En-1%E4%B8%AD%E7%BC%BA%E5%A4%B1%E7%9A%84%E6%95%B0%E5%AD%97/README.md)

### 题目要求
一个长度为 n-1 的递增排序数组中的所有数字都是唯一的，并且每个数字都在范围0～n-1之内。在范围0～n-1内的n个数字中有且只有一个数字不在该数组中，请找出这个数字。

### 样例数据
样例 1:
```text
输入: [0,1,3]
输出: 2
```

样例 2:
```text
输入: [0,1,2,3,4,5,6,7,9]
输出: 8
```

### 核心思路
`方法一：二分查找`

我们可以使用二分查找的方法找到这个缺失的数字。 初始化左边界 l=0，右边界 r=n，其中 n 是数组的长度。 每次计算中间元素的下标 mid，如果 nums[mid] \gt mid，则缺失的数字一定在区间 [l,..mid] 中，否则缺失的数字一定在区间 [mid+1,..r] 中。 最后返回左边界 l 即可。

### 复杂度
时间复杂度 O(\log n)，其中 n 是数组的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int missingNumber(int[] nums) {
        int l = 0, r = nums.length;
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (nums[mid] > mid) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }
}
```


### 解题模板

```
// 查找左边界（第一个 >= target）
int l = 0, r = n;
while (l < r) {
    int mid = (l + r) >>> 1;
    if (nums[mid] >= target) r = mid; else l = mid + 1;
}
return l;

// 查找右边界（最后一个 <= target）
// 旋转数组：和右端点比较
// 搜索插入位置：左边界模板
```

**识别信号**：有序数组查找 → 二分；旋转数组 → 和端点比较缩小范围。

---

## 十三、堆

**来源：LeetCode Hot 100**

<a id="p-215"></a>
## 215. 数组中的第K个最大元素

- 难度：中等
- 标签：数组、分治、快速选择、排序、堆（优先队列）
- 跳转：[官方题目](https://leetcode.cn/problems/kth-largest-element-in-an-array/) | [参考题解](https://leetcode.doocs.org/lc/215/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0215.Kth%20Largest%20Element%20in%20an%20Array/README.md)

### 题目要求
给定整数数组 `nums` 和整数 `k`，请返回数组中第 `k` 个最大的元素。 请注意，你需要找的是数组排序后的第 `k` 个最大的元素，而不是第 `k` 个不同的元素。 你必须设计并实现时间复杂度为 `O(n)` 的算法解决此问题。

### 样例数据
样例 1:
```text
输入: `[3,2,1,5,6,4],` k = 2
输出: 5
```

样例 2:
```text
输入: `[3,2,3,1,2,4,5,5,6], `k = 4
输出: 4
```

### 核心思路
`方法一：快速选择`

快速选择算法是一种在未排序的数组中查找第 `k` 个最大元素或最小元素的算法。 它的基本思想是每次选择一个基准元素，将数组分为两部分，一部分的元素都比基准元素小，另一部分的元素都比基准元素大，然后根据基准元素的位置，决定继续在左边还是右边查找，直到找到第 `k` 个最大元素。 其中 n 为数组 nums 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(\log n)。

### Java 代码
```java
class Solution {
    private int[] nums;
    private int k;

    public int findKthLargest(int[] nums, int k) {
        this.nums = nums;
        this.k = nums.length - k;
        return quickSort(0, nums.length - 1);
    }

    private int quickSort(int l, int r) {
        if (l == r) {
            return nums[l];
        }
        int i = l - 1, j = r + 1;
        int x = nums[(l + r) >>> 1];
        while (i < j) {
            while (nums[++i] < x) {
            }
            while (nums[--j] > x) {
            }
            if (i < j) {
                int t = nums[i];
                nums[i] = nums[j];
                nums[j] = t;
            }
        }
        if (j < k) {
            return quickSort(j + 1, r);
        }
        return quickSort(l, j);
    }
}
```

---

<a id="p-347"></a>
## 347. 前 K 个高频元素

- 难度：中等
- 标签：数组、哈希表、分治、桶排序、计数、快速选择、排序、堆（优先队列）
- 跳转：[官方题目](https://leetcode.cn/problems/top-k-frequent-elements/) | [参考题解](https://leetcode.doocs.org/lc/347/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0300-0399/0347.Top%20K%20Frequent%20Elements/README.md)

### 题目要求
给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 任意顺序 返回答案。

### 样例数据
样例 1:
```text
输入：nums = [1,1,1,2,2,3], k = 2
输出：[1,2]
```

样例 2:
```text
输入：nums = [1], k = 1
输出：[1]
```

### 核心思路
`方法一：哈希表 + 优先队列（小根堆）`

我们可以使用一个哈希表 cnt 统计每个元素出现的次数，然后使用一个小根堆（优先队列）来保存前 k 个高频元素。 我们首先遍历一遍数组，统计每个元素出现的次数，然后遍历哈希表，将元素和出现次数存入小根堆中。 如果小根堆的大小超过了 k，我们就将堆顶元素弹出，保证堆的大小始终为 k。 最后，我们将小根堆中的元素依次弹出，放入结果数组中即可。 其中 n 是数组的长度。

### 复杂度
时间复杂度 O(n \times \log k)，空间复杂度 O(k)。

### Java 代码
```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> cnt = new HashMap<>();
        for (int x : nums) {
            cnt.merge(x, 1, Integer::sum);
        }
        PriorityQueue<Map.Entry<Integer, Integer>> pq
            = new PriorityQueue<>(Comparator.comparingInt(Map.Entry::getValue));
        for (var e : cnt.entrySet()) {
            pq.offer(e);
            if (pq.size() > k) {
                pq.poll();
            }
        }
        return pq.stream().mapToInt(Map.Entry::getKey).toArray();
    }
}
```

---

<a id="p-295"></a>
## 295. 数据流的中位数

- 难度：困难
- 标签：设计、双指针、数据流、排序、堆（优先队列）
- 跳转：[官方题目](https://leetcode.cn/problems/find-median-from-data-stream/) | [参考题解](https://leetcode.doocs.org/lc/295/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0295.Find%20Median%20from%20Data%20Stream/README.md)

### 题目要求
中位数是有序整数列表中的中间值。如果列表的大小是偶数，则没有中间值，中位数是两个中间值的平均值。 - 例如 `arr = [2,3,4]` 的中位数是 `3` 。 - 例如 `arr = [2,3]` 的中位数是 `(2 + 3) / 2 = 2.5` 。 实现 MedianFinder 类: - `MedianFinder()` 初始化 `MedianFinder` 对象。 - `void addNum(int num)` 将数据流中的整数 `num` 添加到数据结构中。 - `double findMedian()` 返回到目前为止所有元素的中位数。与实际答案相差 `10^-5` 以内的答案将被接受。

### 样例数据
样例 1:
```text
输入
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
输出
[null, null, null, 1.5, null, 2.0]
解释
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1); // arr = [1]
medianFinder.addNum(2); // arr = [1, 2]
medianFinder.findMedian(); // 返回 1.5 ((1 + 2) / 2)
medianFinder.addNum(3); // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0
```

### 核心思路
`方法一：大小根堆（优先队列）`

我们可以使用两个堆来维护所有的元素，一个小根堆 minQ 和一个大根堆 maxQ，其中小根堆 minQ 存储较大的一半，大根堆 maxQ 存储较小的一半。 调用 `addNum` 方法时，我们首先将元素加入到大根堆 maxQ，然后将 maxQ 的堆顶元素弹出并加入到小根堆 minQ。 如果此时 minQ 的大小与 maxQ 的大小差值大于 1，我们就将 minQ 的堆顶元素弹出并加入到 maxQ。 调用 `findMedian` 方法时，如果 minQ 的大小等于 maxQ 的大小，说明元素的总数为偶数，我们就可以返回 minQ 的堆顶元素与 maxQ 的堆顶元素的平均值；否则，我们返回 minQ 的堆顶元素。 其中 n 为元素的个数。

### 复杂度
时间复杂度为 O(\log n)。 时间复杂度为 O(1)。 空间复杂度为 O(n)。

### Java 代码
```java
class MedianFinder {
    private PriorityQueue<Integer> minQ = new PriorityQueue<>();
    private PriorityQueue<Integer> maxQ = new PriorityQueue<>(Collections.reverseOrder());

    public MedianFinder() {
    }

    public void addNum(int num) {
        maxQ.offer(num);
        minQ.offer(maxQ.poll());
        if (minQ.size() - maxQ.size() > 1) {
            maxQ.offer(minQ.poll());
        }
    }

    public double findMedian() {
        return minQ.size() == maxQ.size() ? (minQ.peek() + maxQ.peek()) / 2.0 : minQ.peek();
    }
}

/**
 * Your MedianFinder object will be instantiated and called as such:
 * MedianFinder obj = new MedianFinder();
 * obj.addNum(num);
 * double param_2 = obj.findMedian();
 */
```


**来源：剑指 Offer**

<a id="offer-41"></a>
## 剑指 Offer 41. 数据流中的中位数

- 难度：困难
- 标签：堆 (优先队列)
- 跳转：[官方题目](https://leetcode.cn/problems/shu-ju-liu-zhong-de-zhong-wei-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/41/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9841.%20%E6%95%B0%E6%8D%AE%E6%B5%81%E4%B8%AD%E7%9A%84%E4%B8%AD%E4%BD%8D%E6%95%B0/README.md)

### 题目要求
如何得到一个数据流中的中位数？如果从数据流中读出奇数个数值，那么中位数就是所有数值排序之后位于中间的数值。如果从数据流中读出偶数个数值，那么中位数就是所有数值排序之后中间两个数的平均值。 例如， [2,3,4] 的中位数是 3 [2,3] 的中位数是 (2 + 3) / 2 = 2.5 设计一个支持以下两种操作的数据结构： - void addNum(int num) - 从数据流中添加一个整数到数据结构中。 - double findMedian() - 返回目前所有元素的中位数。

### 样例数据
样例 1:
```text
输入：
["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]
[[],[1],[2],[],[3],[]]
输出：[null,null,null,1.50000,null,2.00000]
```

样例 2:
```text
输入：
["MedianFinder","addNum","findMedian","addNum","findMedian"]
[[],[2],[],[3],[]]
输出：[null,null,2.00000,null,2.50000]
```

### 核心思路
`方法一：大小根堆（优先队列）`

我们可以使用两个堆来维护所有的元素，一个小根堆 minQ 和一个大根堆 maxQ，其中小根堆 minQ 存储较大的一半，大根堆 maxQ 存储较小的一半。 调用 `addNum` 方法时，我们首先将元素加入到大根堆 maxQ，然后将 maxQ 的堆顶元素弹出并加入到小根堆 minQ。 如果此时 minQ 的大小与 maxQ 的大小差值大于 1，我们就将 minQ 的堆顶元素弹出并加入到 maxQ。 调用 `findMedian` 方法时，如果 minQ 的大小等于 maxQ 的大小，说明元素的总数为偶数，我们就可以返回 minQ 的堆顶元素与 maxQ 的堆顶元素的平均值；否则，我们返回 minQ 的堆顶元素。 其中 n 为元素的个数。

### 复杂度
时间复杂度为 O(\log n)。 时间复杂度为 O(1)。 空间复杂度为 O(n)。

### Java 代码
```java
class MedianFinder {
    private PriorityQueue<Integer> minQ = new PriorityQueue<>();
    private PriorityQueue<Integer> maxQ = new PriorityQueue<>(Collections.reverseOrder());

    public MedianFinder() {
    }

    public void addNum(int num) {
        maxQ.offer(num);
        minQ.offer(maxQ.poll());
        if (minQ.size() - maxQ.size() > 1) {
            maxQ.offer(minQ.poll());
        }
    }

    public double findMedian() {
        return minQ.size() == maxQ.size() ? (minQ.peek() + maxQ.peek()) / 2.0 : minQ.peek();
    }
}

/**
 * Your MedianFinder object will be instantiated and called as such:
 * MedianFinder obj = new MedianFinder();
 * obj.addNum(num);
 * double param_2 = obj.findMedian();
 */
```

---

<a id="offer-40"></a>
## 剑指 Offer 40. 最小的k个数

- 难度：简单
- 标签：堆 (优先队列)
- 跳转：[官方题目](https://leetcode.cn/problems/zui-xiao-de-kge-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/40/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9840.%20%E6%9C%80%E5%B0%8F%E7%9A%84k%E4%B8%AA%E6%95%B0/README.md)

### 题目要求
输入整数数组 `arr` ，找出其中最小的 `k` 个数。例如，输入4、5、1、6、2、7、3、8这8个数字，则最小的4个数字是1、2、3、4。

### 样例数据
样例 1:
```text
输入：arr = [3,2,1], k = 2
输出：[1,2] 或者 [2,1]
```

样例 2:
```text
输入：arr = [0,1,2,1], k = 1
输出：[0]
```

### 核心思路
`方法一：排序`

我们可以直接对数组 `arr` 按从小到大排序，然后取前 k 个数即可。 其中 n 为数组 `arr` 的长度。

### 复杂度
时间复杂度 O(n \times \log n)，空间复杂度 O(\log n)。

### Java 代码
```java
class Solution {
    public int[] getLeastNumbers(int[] arr, int k) {
        Arrays.sort(arr);
        int[] ans = new int[k];
        for (int i = 0; i < k; ++i) {
            ans[i] = arr[i];
        }
        return ans;
    }
}
```


### 解题模板

```
// TopK：小根堆保持 K 个最大元素
PriorityQueue<Integer> q = new PriorityQueue<>();
for (int x : nums) {
    q.offer(x);
    if (q.size() > k) q.poll();
}

// 数据流中位数：大根堆 + 小根堆
PriorityQueue<Integer> small = new PriorityQueue<>(Comparator.reverseOrder());
PriorityQueue<Integer> large = new PriorityQueue<>();
// small 存小半部分（大根堆），large 存大半部分（小根堆）
```

**识别信号**：TopK → 堆；动态中位数 → 双堆。

---

## 十四、贪心

**来源：LeetCode Hot 100**

<a id="p-121"></a>
## 121. 买卖股票的最佳时机

- 难度：简单
- 标签：数组、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/) | [参考题解](https://leetcode.doocs.org/lc/121/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0121.Best%20Time%20to%20Buy%20and%20Sell%20Stock/README.md)

### 题目要求
给定一个数组 `prices` ，它的第 `i` 个元素 `prices[i]` 表示一支给定股票第 `i` 天的价格。 你只能选择 某一天 买入这只股票，并选择在 未来的某一个不同的日子 卖出该股票。设计一个算法来计算你所能获取的最大利润。 返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 `0` 。

### 样例数据
样例 1:
```text
输入：[7,1,5,3,6,4]
输出：5
解释：在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。
```

样例 2:
```text
输入：prices = [7,6,4,3,1]
输出：0
解释：在这种情况下, 没有交易完成, 所以最大利润为 0。
```

### 核心思路
`方法一：枚举 + 维护前缀最小值`

我们可以枚举数组 nums 每个元素作为卖出价格，那么我们需要在前面找到一个最小值作为买入价格，这样才能使得利润最大化。 因此，我们用一个变量 mi 维护数组 nums 的前缀最小值。 接下来遍历数组 nums，对于每个元素 v，计算其与前面元素的最小值 mi 的差值，更新答案为差值的最大值。 然后更新 mi = min(mi, v)。 继续遍历数组 nums，直到遍历结束。 最后返回答案即可。

### 复杂度
时间复杂度 O(n)，其中 n 是数组 nums 的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int maxProfit(int[] prices) {
        int ans = 0, mi = prices[0];
        for (int v : prices) {
            ans = Math.max(ans, v - mi);
            mi = Math.min(mi, v);
        }
        return ans;
    }
}
```

---

<a id="p-55"></a>
## 55. 跳跃游戏

- 难度：中等
- 标签：贪心、数组、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/jump-game/) | [参考题解](https://leetcode.doocs.org/lc/55/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0055.Jump%20Game/README.md)

### 题目要求
给你一个非负整数数组 `nums` ，你最初位于数组的 第一个下标 。数组中的每个元素代表你在该位置可以跳跃的最大长度。 判断你是否能够到达最后一个下标，如果可以，返回 `true` ；否则，返回 `false` 。

### 样例数据
样例 1:
```text
输入：nums = [2,3,1,1,4]
输出：true
解释：可以先跳 1 步，从下标 0 到达下标 1, 然后再从下标 1 跳 3 步到达最后一个下标。
```

样例 2:
```text
输入：nums = [3,2,1,0,4]
输出：false
解释：无论怎样，总会到达下标为 3 的位置。但该下标的最大跳跃长度是 0 ， 所以永远不可能到达最后一个下标。
```

### 核心思路
`方法一：贪心`

我们用变量 mx 维护当前能够到达的最远下标，初始时 mx = 0。 我们从左到右遍历数组，对于遍历到的每个位置 i，如果 mx \lt i，说明当前位置无法到达，直接返回 `false`。 否则，我们可以通过跳跃从位置 i 到达的最远位置为 i+nums[i]，我们用 i+nums[i] 更新 mx 的值，即 mx = \max(mx, i + nums[i])。 遍历结束，直接返回 `true`。 相似题目：

- [45. 跳跃游戏 II](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0045.Jump%20Game%20II/README.md)
- [1024. 视频拼接](https://github.com/doocs/leetcode/blob/main/solution/1000-1099/1024.Video%20Stitching/README.md)
- [1326. 灌溉花园的最少水龙头数目](https://github.com/doocs/leetcode/blob/main/solution/1300-1399/1326.Minimum%20Number%20of%20Taps%20to%20Open%20to%20Water%20a%20Garden/README.md)

### 复杂度
时间复杂度 O(n)，其中 n 为数组的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public boolean canJump(int[] nums) {
        int mx = 0;
        for (int i = 0; i < nums.length; ++i) {
            if (mx < i) {
                return false;
            }
            mx = Math.max(mx, i + nums[i]);
        }
        return true;
    }
}
```

---

<a id="p-45"></a>
## 45. 跳跃游戏 II

- 难度：中等
- 标签：贪心、数组、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/jump-game-ii/) | [参考题解](https://leetcode.doocs.org/lc/45/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0045.Jump%20Game%20II/README.md)

### 题目要求
给定一个长度为 `n` 的 0 索引整数数组 `nums`。初始位置在下标 0。 每个元素 `nums[i]` 表示从索引 `i` 向后跳转的最大长度。换句话说，如果你在索引 `i` 处，你可以跳转到任意 `(i + j)` 处： - `0 <= j <= nums[i]` 且 - `i + j < n` 返回到达 `n - 1` 的最小跳跃次数。测试用例保证可以到达 `n - 1`。

### 样例数据
样例 1:
```text
输入: nums = [2,3,1,1,4]
输出: 2
解释: 跳到最后一个位置的最小跳跃数是 `2`。
从下标为 0 跳到下标为 1 的位置，跳 `1` 步，然后跳 `3` 步到达数组的最后一个位置。
```

样例 2:
```text
输入: nums = [2,3,0,1,4]
输出: 2
```

### 核心思路
`方法一：贪心`

我们可以用变量 mx 记录当前位置能够到达的最远位置，用变量 last 记录上一次跳跃到的位置，用变量 ans 记录跳跃的次数。 接下来，我们遍历 [0,..n - 2] 的每一个位置 i，对于每一个位置 i，我们可以通过 i + nums[i] 计算出当前位置能够到达的最远位置，我们用 mx 来记录这个最远位置，即 mx = max(mx, i + nums[i])。 接下来，判断当前位置是否到达了上一次跳跃的边界，即 i = last，如果到达了，那么我们就需要进行一次跳跃，将 last 更新为 mx，并且将跳跃次数 ans 增加 1。 最后，我们返回跳跃的次数 ans 即可。 相似题目：

- [55. 跳跃游戏](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0055.Jump%20Game/README.md)
- [1024. 视频拼接](https://github.com/doocs/leetcode/blob/main/solution/1000-1099/1024.Video%20Stitching/README.md)
- [1326. 灌溉花园的最少水龙头数目](https://github.com/doocs/leetcode/blob/main/solution/1300-1399/1326.Minimum%20Number%20of%20Taps%20to%20Open%20to%20Water%20a%20Garden/README.md)

### 复杂度
时间复杂度 O(n)，其中 n 是数组的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int jump(int[] nums) {
        int ans = 0, mx = 0, last = 0;
        for (int i = 0; i < nums.length - 1; ++i) {
            mx = Math.max(mx, i + nums[i]);
            if (last == i) {
                ++ans;
                last = mx;
            }
        }
        return ans;
    }
}
```

---

<a id="p-763"></a>
## 763. 划分字母区间

- 难度：中等
- 标签：贪心、哈希表、双指针、字符串
- 跳转：[官方题目](https://leetcode.cn/problems/partition-labels/) | [参考题解](https://leetcode.doocs.org/lc/763/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0700-0799/0763.Partition%20Labels/README.md)

### 题目要求
给你一个字符串 `s` 。我们要把这个字符串划分为尽可能多的片段，同一字母最多出现在一个片段中。例如，字符串 `"ababcc"` 能够被分为 `["abab", "cc"]`，但类似 `["aba", "bcc"]` 或 `["ab", "ab", "cc"]` 的划分是非法的。 注意，划分结果需要满足：将所有划分结果按顺序连接，得到的字符串仍然是 `s` 。 返回一个表示每个字符串片段的长度的列表。

### 样例数据
样例 1:
```text
输入：s = "ababcbacadefegdehijhklij"
输出：[9,7,8]
解释：
划分结果为 "ababcbaca"、"defegde"、"hijhklij" 。
每个字母最多出现在一个片段中。
像 "ababcbacadefegde", "hijhklij" 这样的划分是错误的，因为划分的片段数较少。
```

样例 2:
```text
输入：s = "eccbbbbdec"
输出：[10]
```

### 核心思路
`方法一：贪心`

我们先用数组或哈希表 last 记录字符串 s 中每个字母最后一次出现的位置。 接下来我们使用贪心的方法，将字符串划分为尽可能多的片段。 从左到右遍历字符串 s，遍历的同时维护当前片段的开始下标 j 和结束下标 i，初始均为 0。 对于每个访问到的字母 c，获取到最后一次出现的位置 last[c]。 由于当前片段的结束下标一定不会小于 last[c]，因此令 mx = \max(mx, last[c])。 当访问到下标 mx 时，意味着当前片段访问结束，当前片段的下标范围是 [j,.. i]，长度为 i - j + 1，我们将其添加到结果数组中。 然后令 j = i + 1, 继续寻找下一个片段。 重复上述过程，直至字符串遍历结束，即可得到所有片段的长度。 其中 n 为字符串 s 的长度，而 |\Sigma| 为字符集的大小。 本题中 |\Sigma| = 26。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(|\Sigma|)。

### Java 代码
```java
class Solution {
    public List<Integer> partitionLabels(String s) {
        int[] last = new int[26];
        int n = s.length();
        for (int i = 0; i < n; ++i) {
            last[s.charAt(i) - 'a'] = i;
        }
        List<Integer> ans = new ArrayList<>();
        int mx = 0, j = 0;
        for (int i = 0; i < n; ++i) {
            mx = Math.max(mx, last[s.charAt(i) - 'a']);
            if (mx == i) {
                ans.add(i - j + 1);
                j = i + 1;
            }
        }
        return ans;
    }
}
```


### 解题模板

```
// 买卖股票最佳时机：维护最低买入价
int mi = Integer.MAX_VALUE, ans = 0;
for (int x : prices) {
    ans = Math.max(ans, x - mi);
    mi = Math.min(mi, x);
}

// 跳跃游戏：维护最远可达位置
// 划分字母区间：记录每个字母最远位置
```

**识别信号**：局部最优推全局最优 → 贪心（买卖股票、跳跃、区间划分）。

---

## 十五、动态规划

**来源：LeetCode Hot 100**

<a id="p-70"></a>
## 70. 爬楼梯

- 难度：简单
- 标签：记忆化、数学、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/climbing-stairs/) | [参考题解](https://leetcode.doocs.org/lc/70/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0070.Climbing%20Stairs/README.md)

### 题目要求
假设你正在爬楼梯。需要 `n` 阶你才能到达楼顶。 每次你可以爬 `1` 或 `2` 个台阶。你有多少种不同的方法可以爬到楼顶呢？

### 样例数据
样例 1:
```text
输入：n = 2
输出：2
解释：有两种方法可以爬到楼顶。
1. 1 阶 + 1 阶
2. 2 阶
```

样例 2:
```text
输入：n = 3
输出：3
解释：有三种方法可以爬到楼顶。
1. 1 阶 + 1 阶 + 1 阶
2. 1 阶 + 2 阶
3. 2 阶 + 1 阶
```

### 核心思路
`方法一：递推`

我们定义 f[i] 表示爬到第 i 阶楼梯的方法数，那么 f[i] 可以由 f[i - 1] 和 f[i - 2] 转移而来，即：

$
f[i] = f[i - 1] + f[i - 2]

初始条件为 f[0] = 1，f[1] = 1，即爬到第 0 阶楼梯的方法数为 1，爬到第 1 阶楼梯的方法数也为 1。 答案即为 f[n]。

### 复杂度
由于 f[i] 只与 f[i - 1] 和 f[i - 2] 有关，因此我们可以只用两个变量 a 和 b 来维护当前的方法数，空间复杂度降低为 O(1)。 时间复杂度 O(n)，空间复杂度 O(1)$。

### Java 代码
```java
class Solution {
    public int climbStairs(int n) {
        int a = 0, b = 1;
        for (int i = 0; i < n; ++i) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
}
```

---

<a id="p-118"></a>
## 118. 杨辉三角

- 难度：简单
- 标签：数组、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/pascals-triangle/) | [参考题解](https://leetcode.doocs.org/lc/118/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0118.Pascal%27s%20Triangle/README.md)

### 题目要求
给定一个非负整数 `numRows`，生成「杨辉三角」的前 `numRows` 行。 在「杨辉三角」中，每个数是它左上方和右上方的数的和。

### 样例数据
样例 1:
```text
输入: numRows = 5
输出: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
```

样例 2:
```text
输入: numRows = 1
输出: [[1]]
```

### 核心思路
`方法一：模拟`

我们先创建一个答案数组 f，然后将 f 的第一行元素设为 [1]。 接下来，我们从第二行开始，每一行的开头和结尾元素都是 1，其它 f[i][j] = f[i - 1][j - 1] + f[i - 1][j]。

### 复杂度
时间复杂度 O(n^2)，其中 n 为给定的行数。 忽略答案的空间消耗，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> f = new ArrayList<>();
        f.add(List.of(1));
        for (int i = 0; i < numRows - 1; ++i) {
            List<Integer> g = new ArrayList<>();
            g.add(1);
            for (int j = 1; j < f.get(i).size(); ++j) {
                g.add(f.get(i).get(j - 1) + f.get(i).get(j));
            }
            g.add(1);
            f.add(g);
        }
        return f;
    }
}
```

---

<a id="p-198"></a>
## 198. 打家劫舍

- 难度：中等
- 标签：数组、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/house-robber/) | [参考题解](https://leetcode.doocs.org/lc/198/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0198.House%20Robber/README.md)

### 题目要求
你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。 给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。

### 样例数据
样例 1:
```text
输入：[1,2,3,1]
输出：4
解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
偷窃到的最高金额 = 1 + 3 = 4 。
```

样例 2:
```text
输入：[2,7,9,3,1]
输出：12
解释：偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
偷窃到的最高金额 = 2 + 9 + 1 = 12 。
```

### 核心思路
`方法一：记忆化搜索`

我们设计一个函数 dfs(i)，表示从第 i 间房屋开始偷窃能够得到的最高金额。 那么答案即为 dfs(0)。 函数 dfs(i) 的执行过程如下：

- 如果 i \ge len(nums)，表示所有房屋都被考虑过了，直接返回 0；
- 否则，考虑偷窃第 i 间房屋，那么 dfs(i) = nums[i] + dfs(i+2)；不偷窃第 i 间房屋，那么 dfs(i) = dfs(i+1)。 - 返回 \max(nums[i] + dfs(i+2), dfs(i+1))。 为了避免重复计算，我们使用记忆化搜索的方法，将 dfs(i) 的结果保存在一个数组或哈希表中，每次计算前先查询是否已经计算过，如果计算过直接返回结果。 其中 n 是数组长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    private Integer[] f;
    private int[] nums;

    public int rob(int[] nums) {
        this.nums = nums;
        f = new Integer[nums.length];
        return dfs(0);
    }

    private int dfs(int i) {
        if (i >= nums.length) {
            return 0;
        }
        if (f[i] == null) {
            f[i] = Math.max(nums[i] + dfs(i + 2), dfs(i + 1));
        }
        return f[i];
    }
}
```

---

<a id="p-279"></a>
## 279. 完全平方数

- 难度：中等
- 标签：广度优先搜索、数学、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/perfect-squares/) | [参考题解](https://leetcode.doocs.org/lc/279/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0279.Perfect%20Squares/README.md)

### 题目要求
给你一个整数 `n` ，返回 和为 `n` 的完全平方数的最少数量 。 完全平方数 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，`1`、`4`、`9` 和 `16` 都是完全平方数，而 `3` 和 `11` 不是。

### 样例数据
样例 1:
```text
输入：n = `12`
输出：3
解释：`12 = 4 + 4 + 4`
```

样例 2:
```text
输入：n = `13`
输出：2
解释：`13 = 4 + 9`
```

### 核心思路
`方法一：动态规划(完全背包)`

我们定义 f[i][j] 表示使用数字 1, 2, \cdots, i 的完全平方数组成和为 j 的最少数量。 初始时 f[0][0] = 0，其余位置的值均为正无穷。 我们可以枚举使用的最后一个数字的数量 k，那么：

$
f[i][j] = \min(f[i - 1][j], f[i - 1][j - i^2] + 1, \cdots, f[i - 1][j - k \times i^2] + k)

其中 i^2 表示最后一个数字 i 的完全平方数。 不妨令 j = j - i^2，那么有：

f[i][j - i^2] = \min(f[i - 1][j - i^2], f[i - 1][j - 2 \times i^2] + 1, \cdots, f[i - 1][j - k \times i^2] + k - 1)

将二式代入一式，我们可以得到以下状态转移方程：

f[i][j] = \min(f[i - 1][j], f[i][j - i^2] + 1)

最后答案即为 f[m][n]。 其中 m 为 sqrt(n) 的整数部分。 相似题目：

- [322. 零钱兑换](https://github.com/doocs/leetcode/blob/main/solution/0300-0399/0322.Coin%20Change/README.md)

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。 注意到 f[i][j] 只与 f[i - 1][j] 和 f[i][j - i^2] 有关，因此我们可以将二维数组优化为一维数组，空间复杂度降为 O(n)$。

### Java 代码
```java
class Solution {
    public int numSquares(int n) {
        int m = (int) Math.sqrt(n);
        int[][] f = new int[m + 1][n + 1];
        for (var g : f) {
            Arrays.fill(g, 1 << 30);
        }
        f[0][0] = 0;
        for (int i = 1; i <= m; ++i) {
            for (int j = 0; j <= n; ++j) {
                f[i][j] = f[i - 1][j];
                if (j >= i * i) {
                    f[i][j] = Math.min(f[i][j], f[i][j - i * i] + 1);
                }
            }
        }
        return f[m][n];
    }
}
```

---

<a id="p-322"></a>
## 322. 零钱兑换

- 难度：中等
- 标签：广度优先搜索、数组、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/coin-change/) | [参考题解](https://leetcode.doocs.org/lc/322/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0300-0399/0322.Coin%20Change/README.md)

### 题目要求
给你一个整数数组 `coins` ，表示不同面额的硬币；以及一个整数 `amount` ，表示总金额。 计算并返回可以凑成总金额所需的 最少的硬币个数 。如果没有任何一种硬币组合能组成总金额，返回 `-1` 。 你可以认为每种硬币的数量是无限的。

### 样例数据
样例 1:
```text
输入：coins = `[1, 2, 5]`, amount = `11`
输出：`3`
解释：11 = 5 + 5 + 1
```

样例 2:
```text
输入：coins = `[2]`, amount = `3`
输出：-1
```

### 核心思路
`方法一：动态规划(完全背包)`

我们定义 f[i][j] 表示使用前 i 种硬币，凑出金额 j 的最少硬币数。 初始时 f[0][0] = 0，其余位置的值均为正无穷。 我们可以枚举使用的最后一枚硬币的数量 k，那么有：

$
f[i][j] = \min(f[i - 1][j], f[i - 1][j - x] + 1, \cdots, f[i - 1][j - k \times x] + k)

其中 x 表示第 i 种硬币的面值。 不妨令 j = j - x，那么有：

f[i][j - x] = \min(f[i - 1][j - x], f[i - 1][j - 2 \times x] + 1, \cdots, f[i - 1][j - k \times x] + k - 1)

将二式代入一式，我们可以得到以下状态转移方程：

f[i][j] = \min(f[i - 1][j], f[i][j - x] + 1)

最后答案即为 f[m][n]。 其中 m 和 n$ 分别为硬币的种类数和总金额。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    public int coinChange(int[] coins, int amount) {
        final int inf = 1 << 30;
        int m = coins.length;
        int n = amount;
        int[][] f = new int[m + 1][n + 1];
        for (var g : f) {
            Arrays.fill(g, inf);
        }
        f[0][0] = 0;
        for (int i = 1; i <= m; ++i) {
            for (int j = 0; j <= n; ++j) {
                f[i][j] = f[i - 1][j];
                if (j >= coins[i - 1]) {
                    f[i][j] = Math.min(f[i][j], f[i][j - coins[i - 1]] + 1);
                }
            }
        }
        return f[m][n] >= inf ? -1 : f[m][n];
    }
}
```

---

<a id="p-139"></a>
## 139. 单词拆分

- 难度：中等
- 标签：字典树、记忆化、数组、哈希表、字符串、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/word-break/) | [参考题解](https://leetcode.doocs.org/lc/139/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0139.Word%20Break/README.md)

### 题目要求
给你一个字符串 `s` 和一个字符串列表 `wordDict` 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 `s` 则返回 `true`。 注意：不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。

### 样例数据
样例 1:
```text
输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。
```

样例 2:
```text
输入: s = "applepenapple", wordDict = ["apple", "pen"]
输出: true
解释: 返回 true 因为 "applepenapple" 可以由 "apple" "pen" "apple" 拼接成。
注意，你可以重复使用字典中的单词。
```

### 核心思路
`方法一：哈希表 + 动态规划`

我们定义 f[i] 表示字符串 s 的前 i 个字符能否拆分成 wordDict 中的单词，初始时 f[0]=true，其余为 false。 答案为 f[n]。 考虑 f[i]，如果存在 j \in [0, i) 使得 f[j] \land s[j:i] \in wordDict，则 f[i]=true。 为了优化效率，我们可以使用哈希表存储 wordDict 中的单词，这样可以快速判断 s[j:i] 是否在 wordDict 中。 其中 n 为字符串 s 的长度。

### 复杂度
时间复杂度 O(n^3)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> words = new HashSet<>(wordDict);
        int n = s.length();
        boolean[] f = new boolean[n + 1];
        f[0] = true;
        for (int i = 1; i <= n; ++i) {
            for (int j = 0; j < i; ++j) {
                if (f[j] && words.contains(s.substring(j, i))) {
                    f[i] = true;
                    break;
                }
            }
        }
        return f[n];
    }
}
```

---

<a id="p-300"></a>
## 300. 最长递增子序列

- 难度：中等
- 标签：数组、二分查找、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/longest-increasing-subsequence/) | [参考题解](https://leetcode.doocs.org/lc/300/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0300-0399/0300.Longest%20Increasing%20Subsequence/README.md)

### 题目要求
给你一个整数数组 `nums` ，找到其中最长严格递增子序列的长度。 子序列 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，`[3,6,2,7]` 是数组 `[0,3,1,6,2,2,7]` 的子序列。

### 样例数据
样例 1:
```text
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
```

样例 2:
```text
输入：nums = [0,1,0,3,2,3]
输出：4
```

### 核心思路
`方法一：动态规划`

我们定义 f[i] 表示以 nums[i] 结尾的最长递增子序列的长度，初始时 f[i] = 1，答案为 f[i] 的最大值。 对于 f[i]，我们需要枚举 0 \le j \lt i，如果 nums[j] \lt nums[i]，则 f[i] = \max(f[i], f[j] + 1)。 最后的答案即为 f[i] 的最大值。 其中 n 为数组长度。

### 复杂度
时间复杂度 O(n^2)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int n = nums.length;
        int[] f = new int[n];
        Arrays.fill(f, 1);
        int ans = 1;
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < i; ++j) {
                if (nums[j] < nums[i]) {
                    f[i] = Math.max(f[i], f[j] + 1);
                }
            }
            ans = Math.max(ans, f[i]);
        }
        return ans;
    }
}
```

---

<a id="p-152"></a>
## 152. 乘积最大子数组

- 难度：中等
- 标签：数组、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/maximum-product-subarray/) | [参考题解](https://leetcode.doocs.org/lc/152/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0152.Maximum%20Product%20Subarray/README.md)

### 题目要求
给你一个整数数组 `nums` ，请你找出数组中乘积最大的非空连续 子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。 测试用例的答案是一个 32-位 整数。 请注意，一个只包含一个元素的数组的乘积是这个元素的值。

### 样例数据
样例 1:
```text
输入: nums = [2,3,-2,4]
输出: `6`
解释: 子数组 [2,3] 有最大乘积 6。
```

样例 2:
```text
输入: nums = [-2,0,-1]
输出: 0
解释: 结果不能为 2, 因为 [-2,-1] 不是子数组。
```

### 核心思路
`方法一：动态规划`

我们定义两个变量 f 和 g，其中 f 表示以 nums[i] 结尾的乘积最大子数组的乘积，而 g 表示以 nums[i] 结尾的乘积最小子数组的乘积。 初始时 f 和 g 都等于 nums[0]。 答案为所有 f 中的最大值。 从 i=1 开始，我们可以考虑将第 i 个数 nums[i] 添加到前面的乘积最大或者乘积最小的子数组乘积的后面，或者单独作为一个子数组乘积（即此时子数组长度只有 1）。 我们将此前的乘积最大值记为 ff，乘积最小值记为 gg，那么 f = \max(f, ff \times nums[i], gg \times nums[i])，而 g = \min(g, ff \times nums[i], gg \times nums[i])。 接下来，我们更新答案 ans = \max(ans, f)，然后继续计算下一个位置。 最后的答案即为 ans。 我们只需要遍历数组一次即可求得答案。

### 复杂度
时间复杂度 O(n)，其中 n 是数组 nums 的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int maxProduct(int[] nums) {
        int f = nums[0], g = nums[0], ans = nums[0];
        for (int i = 1; i < nums.length; ++i) {
            int ff = f, gg = g;
            f = Math.max(nums[i], Math.max(ff * nums[i], gg * nums[i]));
            g = Math.min(nums[i], Math.min(ff * nums[i], gg * nums[i]));
            ans = Math.max(ans, f);
        }
        return ans;
    }
}
```

---

<a id="p-416"></a>
## 416. 分割等和子集

- 难度：中等
- 标签：数组、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/partition-equal-subset-sum/) | [参考题解](https://leetcode.doocs.org/lc/416/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0400-0499/0416.Partition%20Equal%20Subset%20Sum/README.md)

### 题目要求
给你一个 只包含正整数 的 非空 数组 `nums` 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。

### 样例数据
样例 1:
```text
输入：nums = [1,5,11,5]
输出：true
解释：数组可以分割成 [1, 5, 5] 和 [11] 。
```

样例 2:
```text
输入：nums = [1,2,3,5]
输出：false
解释：数组不能分割成两个元素和相等的子集。
```

### 核心思路
`方法一：动态规划`

我们先计算出数组的总和 s，如果总和是奇数，那么一定不能分割成两个和相等的子集，直接返回 false。 如果总和是偶数，我们记目标子集的和为 m = \frac{s}{2}，那么问题就转化成了：是否存在一个子集，使得其元素的和为 m。 我们定义 f[i][j] 表示前 i 个数中选取若干个数，使得其元素的和恰好为 j。 初始时 f[0][0] = true，其余 f[i][j] = false。 答案为 f[n][m]。 考虑 f[i][j]，如果我们选取了第 i 个数 x，那么 f[i][j] = f[i - 1][j - x]；如果我们没有选取第 i 个数 x，那么 f[i][j] = f[i - 1][j]。 因此状态转移方程为：

$
f[i][j] = f[i - 1][j]  or  f[i - 1][j - x]  if  j \geq x

最终答案为 f[n][m]。 其中 m 和 n$ 分别为数组的总和的一半和数组的长度。

### 复杂度
时间复杂度 (m \times n)，空间复杂度 (m \times n)。

### Java 代码
```java
class Solution {
    public boolean canPartition(int[] nums) {
        // int s = Arrays.stream(nums).sum();
        int s = 0;
        for (int x : nums) {
            s += x;
        }
        if (s % 2 == 1) {
            return false;
        }
        int n = nums.length;
        int m = s >> 1;
        boolean[][] f = new boolean[n + 1][m + 1];
        f[0][0] = true;
        for (int i = 1; i <= n; ++i) {
            int x = nums[i - 1];
            for (int j = 0; j <= m; ++j) {
                f[i][j] = f[i - 1][j] || (j >= x && f[i - 1][j - x]);
            }
        }
        return f[n][m];
    }
}
```

---

<a id="p-32"></a>
## 32. 最长有效括号

- 难度：困难
- 标签：栈、字符串、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/longest-valid-parentheses/) | [参考题解](https://leetcode.doocs.org/lc/32/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0032.Longest%20Valid%20Parentheses/README.md)

### 题目要求
给你一个只包含 `'('` 和 `')'` 的字符串，找出最长有效（格式正确且连续）括号 子串 的长度。 左右括号匹配，即每个左括号都有对应的右括号将其闭合的字符串是格式正确的，比如 `"(()())"`。

### 样例数据
样例 1:
```text
输入：s = "(()"
输出：2
解释：最长有效括号子串是 "()"
```

样例 2:
```text
输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"
```

### 核心思路
`方法一：动态规划`

我们定义 f[i] 表示以 s[i-1] 结尾的最长有效括号的长度，那么答案就是 \max\limits_{i=1}^n f[i]。 - 如果 s[i-1] 是左括号，那么以 s[i-1] 结尾的最长有效括号的长度一定为 0，因此 f[i] = 0。 - 如果 s[i-1] 是右括号，有以下两种情况：
    - 如果 s[i-2] 是左括号，那么以 s[i-1] 结尾的最长有效括号的长度为 f[i-2] + 2。 - 如果 s[i-2] 是右括号，那么以 s[i-1] 结尾的最长有效括号的长度为 f[i-1] + 2，但是还需要考虑 s[i-f[i-1]-2] 是否是左括号，如果是左括号，那么以 s[i-1] 结尾的最长有效括号的长度为 f[i-1] + 2 + f[i-f[i-1]-2]。 因此，我们可以得到状态转移方程：

$
\begin{cases}
f[i] = 0, & if  s[i-1] = '(',\\
f[i] = f[i-2] + 2, & if  s[i-1] = ')'  and  s[i-2] = '(',\\
f[i] = f[i-1] + 2 + f[i-f[i-1]-2], & if  s[i-1] = ')'  and  s[i-2] = ')'  and  s[i-f[i-1]-2] = '(',\\
\end{cases}

最后返回 \max\limits_{i=1}^n f[i] 即可。 其中 n$ 为字符串的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int longestValidParentheses(String s) {
        int n = s.length();
        int[] f = new int[n + 1];
        int ans = 0;
        for (int i = 2; i <= n; ++i) {
            if (s.charAt(i - 1) == ')') {
                if (s.charAt(i - 2) == '(') {
                    f[i] = f[i - 2] + 2;
                } else {
                    int j = i - f[i - 1] - 1;
                    if (j > 0 && s.charAt(j - 1) == '(') {
                        f[i] = f[i - 1] + 2 + f[j - 1];
                    }
                }
                ans = Math.max(ans, f[i]);
            }
        }
        return ans;
    }
}
```


**来源：剑指 Offer**

<a id="offer-10-1"></a>
## 剑指 Offer 10- I. 斐波那契数列

- 难度：简单
- 标签：动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/fei-bo-na-qi-shu-lie-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/10.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9810-%20I.%20%E6%96%90%E6%B3%A2%E9%82%A3%E5%A5%91%E6%95%B0%E5%88%97/README.md)

### 题目要求
写一个函数，输入 `n` ，求斐波那契（Fibonacci）数列的第 `n` 项（即 `F(N)`）。斐波那契数列的定义如下：

### 样例数据
样例 1:
```text
F(0) = 0, F(1) = 1
F(N) = F(N - 1) + F(N - 2), 其中 N > 1.
```

样例 2:
```text
输入：n = 2
输出：1
```

### 核心思路
`方法一：递推`

我们定义初始项 a=0, b=1，接下来执行 n 次循环，每次循环中，计算 c=a+b，并更新 a=b, b=c，循环 n 次后，答案即为 a。 其中 n 为输入的整数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int fib(int n) {
        int a = 0, b = 1;
        while (n-- > 0) {
            int c = (a + b) % 1000000007;
            a = b;
            b = c;
        }
        return a;
    }
}
```

---

<a id="offer-10-2"></a>
## 剑指 Offer 10- II. 青蛙跳台阶问题

- 难度：简单
- 标签：动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/qing-wa-tiao-tai-jie-wen-ti-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/10.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9810-%20II.%20%E9%9D%92%E8%9B%99%E8%B7%B3%E5%8F%B0%E9%98%B6%E9%97%AE%E9%A2%98/README.md)

### 题目要求
一只青蛙一次可以跳上1级台阶，也可以跳上2级台阶。求该青蛙跳上一个 `n` 级的台阶总共有多少种跳法。 答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

### 样例数据
样例 1:
```text
输入：n = 2
输出：2
```

样例 2:
```text
输入：n = 7
输出：21
```

### 核心思路
`方法一：递推`

青蛙想上第 n 级台阶，可从第 n-1 级台阶跳一级上去，也可从第 n-2 级台阶跳两级上去，即 f(n) = f(n-1) + f(n-2)。 这实际上可以转换为斐波那契数列的问题。 我们定义初始项 a=1, b=1，接下来执行 n 次循环，每次循环中，计算 c=a+b，并更新 a=b, b=c，循环 n 次后，答案即为 a。 其中 n 为输入的整数。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int numWays(int n) {
        int a = 1, b = 1;
        while (n-- > 0) {
            int c = (a + b) % 1000000007;
            a = b;
            b = c;
        }
        return a;
    }
}
```

---

<a id="offer-19"></a>
## 剑指 Offer 19. 正则表达式匹配

- 难度：困难
- 标签：动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/zheng-ze-biao-da-shi-pi-pei-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/19/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9819.%20%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E5%8C%B9%E9%85%8D/README.md)

### 题目要求
请实现一个函数用来匹配包含`'. '`和`'*'`的正则表达式。模式中的字符`'.'`表示任意一个字符，而`'*'`表示它前面的字符可以出现任意次（含0次）。在本题中，匹配是指字符串的所有字符匹配整个模式。例如，字符串`"aaa"`与模式`"a.a"`和`"ab*ac*a"`匹配，但与`"aa.a"`和`"ab*a"`均不匹配。

### 样例数据
样例 1:
```text
输入:
s = "aa"
p = "a"
输出: false
解释: "a" 无法匹配 "aa" 整个字符串。
```

样例 2:
```text
输入:
s = "aa"
p = "a*"
输出: true
解释: 因为 '*' 代表可以匹配零个或多个前面的那一个元素, 在这里前面的元素就是 'a'。因此，字符串 "aa" 可被视为 'a' 重复了一次。
```

### 核心思路
`方法一：记忆化搜索`

我们设计一个函数 dfs(i, j)，表示从 s 的第 i 个字符开始，和 p 的第 j 个字符开始是否匹配。 那么答案就是 dfs(0, 0)。 函数 dfs(i, j) 的计算过程如下：

- 如果 j 已经到达 p 的末尾，那么如果 i 也到达了 s 的末尾，那么匹配成功，否则匹配失败。 - 如果 j 的下一个字符是 `'*'`，我们可以选择匹配 0 个 s[i] 字符，那么就是 dfs(i, j + 2)。 如果此时 i \lt m 并且 s[i] 和 p[j] 匹配，那么我们可以选择匹配 1 个 s[i] 字符，那么就是 dfs(i + 1, j)。 - 如果 j 的下一个字符不是 `'*'`，那么如果 i \lt m 并且 s[i] 和 p[j] 匹配，那么就是 dfs(i + 1, j + 1)。 否则匹配失败。 过程中，我们可以使用记忆化搜索，避免重复计算。 其中 m 和 n 分别是 s 和 p 的长度。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    private Boolean[][] f;
    private String s;
    private String p;
    private int m;
    private int n;

    public boolean isMatch(String s, String p) {
        m = s.length();
        n = p.length();
        f = new Boolean[m + 1][n + 1];
        this.s = s;
        this.p = p;
        return dfs(0, 0);
    }

    private boolean dfs(int i, int j) {
        if (j >= n) {
            return i == m;
        }
        if (f[i][j] != null) {
            return f[i][j];
        }
        boolean res = false;
        if (j + 1 < n && p.charAt(j + 1) == '*') {
            res = dfs(i, j + 2)
                || (i < m && (s.charAt(i) == p.charAt(j) || p.charAt(j) == '.') && dfs(i + 1, j));
        } else {
            res = i < m && (s.charAt(i) == p.charAt(j) || p.charAt(j) == '.') && dfs(i + 1, j + 1);
        }
        return f[i][j] = res;
    }
}
```

---

<a id="offer-42"></a>
## 剑指 Offer 42. 连续子数组的最大和

- 难度：简单
- 标签：动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/lian-xu-zi-shu-zu-de-zui-da-he-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/42/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9842.%20%E8%BF%9E%E7%BB%AD%E5%AD%90%E6%95%B0%E7%BB%84%E7%9A%84%E6%9C%80%E5%A4%A7%E5%92%8C/README.md)

### 题目要求
输入一个整型数组，数组中的一个或连续多个整数组成一个子数组。求所有子数组的和的最大值。 要求时间复杂度为O(n)。

### 样例数据
样例 1:
```text
输入: nums = [-2,1,-3,4,-1,2,1,-5,4]
输出: 6
解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。
```

### 核心思路
`方法一：动态规划`

优先按题目所属专题套用对应模板，再处理边界。

### 复杂度
我们定义 f[i] 表示以第 i 个数结尾的「连续子数组的最大和」，那么很显然我们要求的答案就是：

$
\max_{0 \leq i \leq n-1} f[i]

那么我们如何求 f[i] 呢？我们可以考虑 nums[i] 单独成为一段还是加入 f[i-1] 对应的那一段，这取决于 nums[i] 和 f[i-1] + nums[i] 哪个大，我们希望获得一个比较大的，于是可以写出这样的状态转移方程：

f[i] = \max(f[i-1] + nums[i], nums[i])

或者可以写成这样：

f[i] = \max(f[i-1], 0) + nums[i]

我们可以不用开一个数组来存储所有的计算结果，而是只用两个变量 f 和 ans 来维护对于每一个位置 i 我们的最大值，这样我们可以省去空间复杂度的开销。 时间复杂度 O(n)，其中 n 为数组长度。 空间复杂度 O(1)$。

### Java 代码
```java
class Solution {
    public int maxSubArray(int[] nums) {
        int ans = Integer.MIN_VALUE;
        int f = 0;
        for (int x : nums) {
            f = Math.max(f, 0) + x;
            ans = Math.max(ans, f);
        }
        return ans;
    }
}
```

---

<a id="offer-46"></a>
## 剑指 Offer 46. 把数字翻译成字符串

- 难度：中等
- 标签：动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/ba-shu-zi-fan-yi-cheng-zi-fu-chuan-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/46/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9846.%20%E6%8A%8A%E6%95%B0%E5%AD%97%E7%BF%BB%E8%AF%91%E6%88%90%E5%AD%97%E7%AC%A6%E4%B8%B2/README.md)

### 题目要求
给定一个数字，我们按照如下规则把它翻译为字符串：0 翻译成 “a” ，1 翻译成 “b”，……，11 翻译成 “l”，……，25 翻译成 “z”。一个数字可能有多个翻译。请编程实现一个函数，用来计算一个数字有多少种不同的翻译方法。

### 样例数据
样例 1:
```text
输入: 12258
输出: `5
`解释: 12258有5种不同的翻译，分别是"bccfi", "bwfi", "bczi", "mcfi"和"mzi"
```

### 核心思路
`方法一：记忆化搜索`

我们先将数字 `num` 转为字符串 s，字符串 s 的长度记为 n。 然后我们设计一个函数 dfs(i)，表示从索引为 i 的数字开始的不同翻译的数目。 那么答案就是 dfs(0)。 函数 dfs(i) 的计算如下：

- 如果 i \ge n - 1，说明已经翻译到最后一个数字或者越过最后一个字符，均只有一种翻译方法，返回 1；
- 否则，我们可以选择翻译索引为 i 的数字，此时翻译方法数目为 dfs(i + 1)；如果索引为 i 的数字和索引为 i + 1 的数字可以组成一个有效的字符（即 s[i] == 1 或者 s[i] == 2 且 s[i + 1] \lt 6），那么我们还可以选择翻译索引为 i 和索引为 i + 1 的数字，此时翻译方法数目为 dfs(i + 2)。 因此 dfs(i) = dfs(i+1) + dfs(i+2)。 过程中我们可以使用记忆化搜索，将已经计算过的 dfs(i) 的值存储起来，避免重复计算。 其中 num 为给定的数字。

### 复杂度
时间复杂度 O(\log num)，空间复杂度 O(\log num)。

### Java 代码
```java
class Solution {
    private int n;
    private char[] s;
    private Integer[] f;

    public int translateNum(int num) {
        s = String.valueOf(num).toCharArray();
        n = s.length;
        f = new Integer[n];
        return dfs(0);
    }

    private int dfs(int i) {
        if (i >= n - 1) {
            return 1;
        }
        if (f[i] != null) {
            return f[i];
        }
        int ans = dfs(i + 1);
        if (s[i] == '1' || (s[i] == '2' && s[i + 1] < '6')) {
            ans += dfs(i + 2);
        }
        return f[i] = ans;
    }
}
```

---

<a id="offer-47"></a>
## 剑指 Offer 47. 礼物的最大价值

- 难度：中等
- 标签：动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/li-wu-de-zui-da-jie-zhi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/47/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9847.%20%E7%A4%BC%E7%89%A9%E7%9A%84%E6%9C%80%E5%A4%A7%E4%BB%B7%E5%80%BC/README.md)

### 题目要求
在一个 m*n 的棋盘的每一格都放有一个礼物，每个礼物都有一定的价值（价值大于 0）。你可以从棋盘的左上角开始拿格子里的礼物，并每次向右或者向下移动一格、直到到达棋盘的右下角。给定一个棋盘及其上面的礼物的价值，请计算你最多能拿到多少价值的礼物？

### 样例数据
样例 1:
```text
输入:
`[
[1,3,1],
[1,5,1],
[4,2,1]
]`
输出: `12
`解释: 路径 1→3→5→2→1 可以拿到最多价值的礼物
```

### 核心思路
`方法一：动态规划`

我们定义 f[i][j] 为从棋盘左上角走到 (i-1, j-1) 的礼物最大累计价值，那么 f[i][j] 的值由 f[i-1][j] 和 f[i][j-1] 决定，即从上方格子和左方格子走过来的两个方案中选择一个价值较大的方案。 因此我们可以写出动态规划转移方程：

$
f[i][j] = max(f[i-1][j], f[i][j-1]) + grid[i-1][j-1]

答案为 f[m][n]。 其中 m 和 n$ 分别为棋盘的行数和列数。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    public int maxValue(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] f = new int[m + 1][n + 1];
        for (int i = 1; i <= m; ++i) {
            for (int j = 1; j <= n; ++j) {
                f[i][j] = Math.max(f[i - 1][j], f[i][j - 1]) + grid[i - 1][j - 1];
            }
        }
        return f[m][n];
    }
}
```

---

<a id="offer-60"></a>
## 剑指 Offer 60. n个骰子的点数

- 难度：简单
- 标签：动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/nge-tou-zi-de-dian-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/60/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9860.%20n%E4%B8%AA%E9%AA%B0%E5%AD%90%E7%9A%84%E7%82%B9%E6%95%B0/README.md)

### 题目要求
把n个骰子扔在地上，所有骰子朝上一面的点数之和为s。输入n，打印出s的所有可能的值出现的概率。 你需要用一个浮点数数组返回答案，其中第 i 个元素代表这 n 个骰子所能掷出的点数集合中第 i 小的那个的概率。

### 样例数据
样例 1:
```text
输入: 1
输出: [0.16667,0.16667,0.16667,0.16667,0.16667,0.16667]
```

样例 2:
```text
输入: 2
输出: [0.02778,0.05556,0.08333,0.11111,0.13889,0.16667,0.13889,0.11111,0.08333,0.05556,0.02778]
```

### 核心思路
`方法一：动态规划`

我们定义 f[i][j] 表示投掷 i 个骰子，点数和为 j 的方案数。 那么我们可以写出状态转移方程：

$
f[i][j] = \sum_{k=1}^6 f[i-1][j-k]

其中 k 表示当前骰子的点数，而 f[i-1][j-k] 表示投掷 i-1 个骰子，点数和为 j-k 的方案数。 初始条件为 f[1][j] = 1，表示投掷一个骰子，点数和为 j 的方案数为 1。 最终，我们要求的答案即为 \frac{f[n][j]}{6^n}，其中 n 为骰子个数，而 j 的取值范围为 [n, 6n]。 其中 n$ 为骰子个数。

### 复杂度
时间复杂度 O(n^2)，空间复杂度 O(6n)。

### Java 代码
```java
class Solution {
    public double[] dicesProbability(int n) {
        int[][] f = new int[n + 1][6 * n + 1];
        for (int j = 1; j <= 6; ++j) {
            f[1][j] = 1;
        }
        for (int i = 2; i <= n; ++i) {
            for (int j = i; j <= 6 * i; ++j) {
                for (int k = 1; k <= 6; ++k) {
                    if (j >= k) {
                        f[i][j] += f[i - 1][j - k];
                    }
                }
            }
        }
        double m = Math.pow(6, n);
        double[] ans = new double[5 * n + 1];
        for (int j = n; j <= 6 * n; ++j) {
            ans[j - n] = f[n][j] / m;
        }
        return ans;
    }
}
```

---

<a id="offer-63"></a>
## 剑指 Offer 63. 股票的最大利润

- 难度：中等
- 标签：动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/gu-piao-de-zui-da-li-run-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/63/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9863.%20%E8%82%A1%E7%A5%A8%E7%9A%84%E6%9C%80%E5%A4%A7%E5%88%A9%E6%B6%A6/README.md)

### 题目要求
假设把某股票的价格按照时间先后顺序存储在数组中，请问买卖该股票一次可能获得的最大利润是多少？

### 样例数据
样例 1:
```text
输入: [7,1,5,3,6,4]
输出: 5
解释: 在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格。
```

样例 2:
```text
输入: [7,6,4,3,1]
输出: 0
解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。
```

### 核心思路
`方法一：动态规划`

我们可以枚举当前的股票价格作为卖出价格，那么买入价格就是在它之前的最低股票价格，此时的利润就是卖出价格减去买入价格。 我们可以用一个变量 `mi` 记录之前的最低股票价格，用一个变量 `ans` 记录最大利润，找出最大利润即可。 其中 n 是数组 `prices` 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int maxProfit(int[] prices) {
        int mi = 1 << 30, ans = 0;
        for (int x : prices) {
            ans = Math.max(ans, x - mi);
            mi = Math.min(mi, x);
        }
        return ans;
    }
}
```


### 解题模板

```
// 一维 DP
dp[i] = 从 dp[i-1] 或 dp[i-2] 转移
// 空间压缩：两个变量滚动

// 爬楼梯/斐波那契
int a = 1, b = 1;
while (n-- > 0) { int c = a + b; a = b; b = c; }

// 最长递增子序列：dp[i] = max(dp[j]) + 1 (j < i && nums[j] < nums[i])
// 0-1 背包：dp[j] = max(dp[j], dp[j - nums[i]] + nums[i])
// 完全背包：dp[j] += dp[j - coins[i]]
```

**识别信号**：最优子结构 + 重叠子问题 → DP；先推状态转移方程，再考虑空间压缩。

---

## 十六、多维动态规划

**来源：LeetCode Hot 100**

<a id="p-62"></a>
## 62. 不同路径

- 难度：中等
- 标签：数学、动态规划、组合数学
- 跳转：[官方题目](https://leetcode.cn/problems/unique-paths/) | [参考题解](https://leetcode.doocs.org/lc/62/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0062.Unique%20Paths/README.md)

### 题目要求
一个机器人位于一个 `m x n` 网格的左上角 （起始点在下图中标记为 “Start” ）。 机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。 问总共有多少条不同的路径？

### 样例数据
样例 1:
```text
输入：m = 3, n = 7
输出：28
```

样例 2:
```text
输入：m = 3, n = 2
输出：3
解释：
从左上角开始，总共有 3 条路径可以到达右下角。
1. 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右
3. 向下 -> 向右 -> 向下
```

### 核心思路
`方法一：动态规划`

我们定义 f[i][j] 表示从左上角走到 (i, j) 的路径数量，初始时 f[0][0] = 1，答案为 f[m - 1][n - 1]。 考虑 f[i][j]：

- 如果 i \gt 0，那么 f[i][j] 可以从 f[i - 1][j] 走一步到达，因此 f[i][j] = f[i][j] + f[i - 1][j]；
- 如果 j \gt 0，那么 f[i][j] 可以从 f[i][j - 1] 走一步到达，因此 f[i][j] = f[i][j] + f[i][j - 1]。 因此，我们有如下的状态转移方程：

$
f[i][j] = \begin{cases}
1 & i = 0, j = 0 \\
f[i - 1][j] + f[i][j - 1] & otherwise
\end{cases}

最终的答案即为 f[m - 1][n - 1]。 其中 m 和 n 分别是网格的行数和列数。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。 我们注意到 f[i][j] 仅与 f[i - 1][j] 和 f[i][j - 1] 有关，因此我们优化掉第一维空间，仅保留第二维空间，得到时间复杂度 O(m \times n)，空间复杂度 O(n)$ 的实现。

### Java 代码
```java
class Solution {
    public int uniquePaths(int m, int n) {
        var f = new int[m][n];
        f[0][0] = 1;
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (i > 0) {
                    f[i][j] += f[i - 1][j];
                }
                if (j > 0) {
                    f[i][j] += f[i][j - 1];
                }
            }
        }
        return f[m - 1][n - 1];
    }
}
```

---

<a id="p-64"></a>
## 64. 最小路径和

- 难度：中等
- 标签：数组、动态规划、矩阵
- 跳转：[官方题目](https://leetcode.cn/problems/minimum-path-sum/) | [参考题解](https://leetcode.doocs.org/lc/64/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0064.Minimum%20Path%20Sum/README.md)

### 题目要求
给定一个包含非负整数的 `m x n` 网格 `grid` ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。 说明：每次只能向下或者向右移动一步。

### 样例数据
样例 1:
```text
输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
输出：7
解释：因为路径 1→3→1→1→1 的总和最小。
```

样例 2:
```text
输入：grid = [[1,2,3],[4,5,6]]
输出：12
```

### 核心思路
`方法一：动态规划`

我们定义 f[i][j] 表示从左上角走到 (i, j) 位置的最小路径和。 初始时 f[0][0] = grid[0][0]，答案为 f[m - 1][n - 1]。 考虑 f[i][j]：

- 如果 j = 0，那么 f[i][j] = f[i - 1][j] + grid[i][j]；
- 如果 i = 0，那么 f[i][j] = f[i][j - 1] + grid[i][j]；
- 如果 i \gt 0 且 j \gt 0，那么 f[i][j] = \min(f[i - 1][j], f[i][j - 1]) + grid[i][j]。 最后返回 f[m - 1][n - 1] 即可。 其中 m 和 n 分别是网格的行数和列数。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    public int minPathSum(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] f = new int[m][n];
        f[0][0] = grid[0][0];
        for (int i = 1; i < m; ++i) {
            f[i][0] = f[i - 1][0] + grid[i][0];
        }
        for (int j = 1; j < n; ++j) {
            f[0][j] = f[0][j - 1] + grid[0][j];
        }
        for (int i = 1; i < m; ++i) {
            for (int j = 1; j < n; ++j) {
                f[i][j] = Math.min(f[i - 1][j], f[i][j - 1]) + grid[i][j];
            }
        }
        return f[m - 1][n - 1];
    }
}
```

---

<a id="p-5"></a>
## 5. 最长回文子串

- 难度：中等
- 标签：双指针、字符串、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/longest-palindromic-substring/) | [参考题解](https://leetcode.doocs.org/lc/5/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0005.Longest%20Palindromic%20Substring/README.md)

### 题目要求
给你一个字符串 `s`，找到 `s` 中最长的 回文 子串。

### 样例数据
样例 1:
```text
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。
```

样例 2:
```text
输入：s = "cbbd"
输出："bb"
```

### 核心思路
`方法一：动态规划`

我们定义 f[i][j] 表示字符串 s[i..j] 是否为回文串，初始时 f[i][j] = true。 接下来，我们定义变量 k 和 mx，其中 k 表示最长回文串的起始位置，mx 表示最长回文串的长度。 初始时 k = 0, mx = 1。 考虑 f[i][j]，如果 s[i] = s[j]，那么 f[i][j] = f[i + 1][j - 1]；否则 f[i][j] = false。 如果 f[i][j] = true 并且 mx \lt j - i + 1，那么我们更新 k = i, mx = j - i + 1。 由于 f[i][j] 依赖于 f[i + 1][j - 1]，因此我们需要保证 i + 1 在 j - 1 之前，因此我们需要从大到小地枚举 i，从小到大地枚举 j。 其中 n 是字符串 s 的长度。

### 复杂度
时间复杂度 O(n^2)，空间复杂度 O(n^2)。

### Java 代码
```java
class Solution {
    public String longestPalindrome(String s) {
        int n = s.length();
        boolean[][] f = new boolean[n][n];
        for (var g : f) {
            Arrays.fill(g, true);
        }
        int k = 0, mx = 1;
        for (int i = n - 2; i >= 0; --i) {
            for (int j = i + 1; j < n; ++j) {
                f[i][j] = false;
                if (s.charAt(i) == s.charAt(j)) {
                    f[i][j] = f[i + 1][j - 1];
                    if (f[i][j] && mx < j - i + 1) {
                        mx = j - i + 1;
                        k = i;
                    }
                }
            }
        }
        return s.substring(k, k + mx);
    }
}
```

---

<a id="p-1143"></a>
## 1143. 最长公共子序列

- 难度：中等
- 标签：字符串、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/longest-common-subsequence/) | [参考题解](https://leetcode.doocs.org/lc/1143/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/1100-1199/1143.Longest%20Common%20Subsequence/README.md)

### 题目要求
给定两个字符串 `text1` 和 `text2`，返回这两个字符串的最长 公共子序列 的长度。如果不存在 公共子序列 ，返回 `0` 。 一个字符串的 子序列 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。 - 例如，`"ace"` 是 `"abcde"` 的子序列，但 `"aec"` 不是 `"abcde"` 的子序列。 两个字符串的 公共子序列 是这两个字符串所共同拥有的子序列。

### 样例数据
样例 1:
```text
输入：text1 = "abcde", text2 = "ace"
输出：3
解释：最长公共子序列是 "ace" ，它的长度为 3 。
```

样例 2:
```text
输入：text1 = "abc", text2 = "abc"
输出：3
解释：最长公共子序列是 "abc" ，它的长度为 3 。
```

### 核心思路
`方法一：动态规划`

我们定义 f[i][j] 表示 text1 的前 i 个字符和 text2 的前 j 个字符的最长公共子序列的长度。 那么答案为 f[m][n]，其中 m 和 n 分别为 text1 和 text2 的长度。 如果 text1 的第 i 个字符和 text2 的第 j 个字符相同，则 f[i][j] = f[i - 1][j - 1] + 1；如果 text1 的第 i 个字符和 text2 的第 j 个字符不同，则 f[i][j] = max(f[i - 1][j], f[i][j - 1])。 其中 m 和 n 分别为 text1 和 text2$ 的长度。

### 复杂度
即状态转移方程为：

$
f[i][j] =
\begin{cases}
f[i - 1][j - 1] + 1, & text1[i - 1] = text2[j - 1] \\
\max(f[i - 1][j], f[i][j - 1]), & text1[i - 1] \neq text2[j - 1]
\end{cases}

时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length(), n = text2.length();
        int[][] f = new int[m + 1][n + 1];
        for (int i = 1; i <= m; ++i) {
            for (int j = 1; j <= n; ++j) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    f[i][j] = f[i - 1][j - 1] + 1;
                } else {
                    f[i][j] = Math.max(f[i - 1][j], f[i][j - 1]);
                }
            }
        }
        return f[m][n];
    }
}
```

---

<a id="p-72"></a>
## 72. 编辑距离

- 难度：中等
- 标签：字符串、动态规划
- 跳转：[官方题目](https://leetcode.cn/problems/edit-distance/) | [参考题解](https://leetcode.doocs.org/lc/72/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0072.Edit%20Distance/README.md)

### 题目要求
给你两个单词 `word1` 和 `word2`， 请返回将 `word1` 转换成 `word2` 所使用的最少操作数 。 你可以对一个单词进行如下三种操作： - 插入一个字符 - 删除一个字符 - 替换一个字符

### 样例数据
样例 1:
```text
输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
```

样例 2:
```text
输入：word1 = "intention", word2 = "execution"
输出：5
解释：
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')
```

### 核心思路
`方法一：动态规划`

我们定义 f[i][j] 表示将 word1 的前 i 个字符转换成 word2 的前 j 个字符所使用的最少操作数。 初始时 f[i][0] = i, f[0][j] = j。 其中 i \in [1, m], j \in [0, n]。 考虑 f[i][j]：

- 如果 word1[i - 1] = word2[j - 1]，那么我们只需要考虑将 word1 的前 i - 1 个字符转换成 word2 的前 j - 1 个字符所使用的最少操作数，因此 f[i][j] = f[i - 1][j - 1]；
- 否则，我们可以考虑插入、删除、替换操作，那么 f[i][j] = \min(f[i - 1][j], f[i][j - 1], f[i - 1][j - 1]) + 1。 综上，我们可以得到状态转移方程：

$
f[i][j] = \begin{cases}
i, & if  j = 0 \\
j, & if  i = 0 \\
f[i - 1][j - 1], & if  word1[i - 1] = word2[j - 1] \\
\min(f[i - 1][j], f[i][j - 1], f[i - 1][j - 1]) + 1, & otherwise
\end{cases}

最后，我们返回 f[m][n] 即可。 其中 m 和 n 分别是 word1 和 word2$ 的长度。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    public int minDistance(String word1, String word2) {
        int m = word1.length(), n = word2.length();
        int[][] f = new int[m + 1][n + 1];
        for (int j = 1; j <= n; ++j) {
            f[0][j] = j;
        }
        for (int i = 1; i <= m; ++i) {
            f[i][0] = i;
            for (int j = 1; j <= n; ++j) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    f[i][j] = f[i - 1][j - 1];
                } else {
                    f[i][j] = Math.min(f[i - 1][j], Math.min(f[i][j - 1], f[i - 1][j - 1])) + 1;
                }
            }
        }
        return f[m][n];
    }
}
```


### 解题模板

```
// 网格路径：dp[i][j] = dp[i-1][j] + dp[i][j-1]
// 最长公共子序列：dp[i][j] = dp[i-1][j-1] + 1 或 max(dp[i-1][j], dp[i][j-1])
// 编辑距离：dp[i][j] = min(插入, 删除, 替换) + 1
// 最小路径和：dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
```

**识别信号**：两个序列/二维网格的最优解 → 二维 DP；只依赖前一行时可滚动数组压缩。

---

## 十七、位运算

**来源：LeetCode Hot 100**

<a id="p-136"></a>
## 136. 只出现一次的数字

- 难度：简单
- 标签：位运算、数组
- 跳转：[官方题目](https://leetcode.cn/problems/single-number/) | [参考题解](https://leetcode.doocs.org/lc/136/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0136.Single%20Number/README.md)

### 题目要求
给你一个 非空 整数数组 `nums` ，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。 你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间。

### 样例数据
样例 1:
```text
：
输入：nums = [2,2,1]
输出：1
```

样例 2:
```text
：
输入：nums = [4,1,2,1,2]
输出：4
```

### 核心思路
`方法一：位运算`

异或运算的性质：

- 任何数和 0 做异或运算，结果仍然是原来的数，即 x \oplus 0 = x；
- 任何数和其自身做异或运算，结果是 0，即 x \oplus x = 0；

我们对该数组所有元素进行异或运算，结果就是那个只出现一次的数字。 其中 n 是数组 nums 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int singleNumber(int[] nums) {
        int ans = 0;
        for (int v : nums) {
            ans ^= v;
        }
        return ans;
    }
}
```

---

<a id="p-169"></a>
## 169. 多数元素

- 难度：简单
- 标签：数组、哈希表、分治、计数、排序
- 跳转：[官方题目](https://leetcode.cn/problems/majority-element/) | [参考题解](https://leetcode.doocs.org/lc/169/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0100-0199/0169.Majority%20Element/README.md)

### 题目要求
给定一个大小为 `n` 的数组 `nums` ，返回其中的多数元素。多数元素是指在数组中出现次数 大于 `⌊ n/2 ⌋` 的元素。 你可以假设数组是非空的，并且给定的数组总是存在多数元素。

### 样例数据
样例 1:
```text
输入：nums = [3,2,3]
输出：3
```

样例 2:
```text
输入：nums = [2,2,1,1,1,2,2]
输出：2
```

### 核心思路
`方法一：摩尔投票法`

摩尔投票法的基本步骤如下：

初始化元素 m，并初始化计数器 cnt=0。 接下来，对于输入列表中每一个元素 x：

1. 如果 cnt=0，那么 m=x 并且 cnt=1；
1. 否则，如果 m=x，那么 cnt = cnt + 1，否则 cnt = cnt - 1。 一般而言，摩尔投票法需要对输入的列表进行**两次遍历**。 在第一次遍历中，我们生成候选值 m，如果存在多数，那么该候选值就是多数值。 在第二次遍历中，只需要简单地计算候选值的频率，以确认是否是多数值。 由于本题已经明确说明存在多数值，所以第一次遍历结束后，直接返回 m 即可，无需二次遍历确认是否是多数值。

### 复杂度
时间复杂度 O(n)，其中 n 是数组 nums 的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int majorityElement(int[] nums) {
        int cnt = 0, m = 0;
        for (int x : nums) {
            if (cnt == 0) {
                m = x;
                cnt = 1;
            } else {
                cnt += m == x ? 1 : -1;
            }
        }
        return m;
    }
}
```

---

<a id="p-75"></a>
## 75. 颜色分类

- 难度：中等
- 标签：数组、双指针、排序
- 跳转：[官方题目](https://leetcode.cn/problems/sort-colors/) | [参考题解](https://leetcode.doocs.org/lc/75/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0075.Sort%20Colors/README.md)

### 题目要求
给定一个包含红色、白色和蓝色、共 `n` 个元素的数组 `nums` ，原地 对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。 我们使用整数 `0`、 `1` 和 `2` 分别表示红色、白色和蓝色。 必须在不使用库内置的 sort 函数的情况下解决这个问题。

### 样例数据
样例 1:
```text
输入：nums = [2,0,2,1,1,0]
输出：[0,0,1,1,2,2]
```

样例 2:
```text
输入：nums = [2,0,1]
输出：[0,1,2]
```

### 核心思路
`方法一：三指针`

我们定义三个指针 i, j 和 k，其中指针 i 用于指向数组中元素值为 0 的最右边界，指针 j 用于指向数组中元素值为 2 的最左边界，初始时 i=-1, j=n。 指针 k 用于指向当前遍历的元素，初始时 k=0。 当 k \lt j 时，我们执行如下操作：

- 若 nums[k]=0，则将其与 nums[i+1] 交换，然后 i 和 k 都加 1；
- 若 nums[k]=2，则将其与 nums[j-1] 交换，然后 j 减 1；
- 若 nums[k]=1，则 k 加 1。 遍历结束后，数组中的元素就被分成了 [0,i], [i+1,j-1] 和 [j,n-1] 三个部分。 只需要遍历一遍数组即可。

### 复杂度
时间复杂度 O(n)，其中 n 是数组的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public void sortColors(int[] nums) {
        int i = -1, j = nums.length, k = 0;
        while (k < j) {
            if (nums[k] == 0) {
                swap(nums, ++i, k++);
            } else if (nums[k] == 2) {
                swap(nums, --j, k);
            } else {
                ++k;
            }
        }
    }

    private void swap(int[] nums, int i, int j) {
        int t = nums[i];
        nums[i] = nums[j];
        nums[j] = t;
    }
}
```

---

<a id="p-31"></a>
## 31. 下一个排列

- 难度：中等
- 标签：数组、双指针
- 跳转：[官方题目](https://leetcode.cn/problems/next-permutation/) | [参考题解](https://leetcode.doocs.org/lc/31/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0000-0099/0031.Next%20Permutation/README.md)

### 题目要求
整数数组的一个 排列 就是将其所有成员以序列或线性顺序排列。 - 例如，`arr = [1,2,3]` ，以下这些都可以视作 `arr` 的排列：`[1,2,3]`、`[1,3,2]`、`[3,1,2]`、`[2,3,1]` 。 整数数组的 下一个排列 是指其整数的下一个字典序更大的排列。更正式地，如果数组的所有排列根据其字典顺序从小到大排列在一个容器中，那么数组的 下一个排列 就是在这个有序容器中排在它后面的那个排列。如果不存在下一个更大的排列，那么这个数组必须重排为字典序最小的排列（即，其元素按升序排列）。 - 例如，`arr = [1,2,3]` 的下一个排列是 `[1,3,2]` 。 - 类似地，`arr = [2,3,1]` 的下一个排列是 `[3,1,2]` 。 - 而 `arr = [3,2,1]` 的下一个排列是 `[1,2,3]` ，因为 `[3,2,1]` 不存在一个字典序更大的排列。 给你一个整数数组 `nums` ，找出 `nums` 的下一个排列。 必须 原地 修改，只允许使用额外常数空间。

### 样例数据
样例 1:
```text
输入：nums = [1,2,3]
输出：[1,3,2]
```

样例 2:
```text
输入：nums = [3,2,1]
输出：[1,2,3]
```

### 核心思路
`方法一：两次遍历`

我们先从后往前遍历数组 nums，找到第一个满足 nums[i] \lt nums[i + 1] 的位置 i，那么 nums[i] 就是我们需要交换的元素，而 nums[i + 1] 到 nums[n - 1] 的元素是一个降序序列。 接下来，我们再从后往前遍历数组 nums，找到第一个满足 nums[j] \gt nums[i] 的位置 j，然后我们交换 nums[i] 和 nums[j]。 最后，我们将 nums[i + 1] 到 nums[n - 1] 的元素反转，即可得到下一个排列。 其中 n 为数组的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public void nextPermutation(int[] nums) {
        int n = nums.length;
        int i = n - 2;
        for (; i >= 0; --i) {
            if (nums[i] < nums[i + 1]) {
                break;
            }
        }
        if (i >= 0) {
            for (int j = n - 1; j > i; --j) {
                if (nums[j] > nums[i]) {
                    swap(nums, i, j);
                    break;
                }
            }
        }

        for (int j = i + 1, k = n - 1; j < k; ++j, --k) {
            swap(nums, j, k);
        }
    }

    private void swap(int[] nums, int i, int j) {
        int t = nums[j];
        nums[j] = nums[i];
        nums[i] = t;
    }
}
```

---

<a id="p-287"></a>
## 287. 寻找重复数

- 难度：中等
- 标签：位运算、数组、双指针、二分查找
- 跳转：[官方题目](https://leetcode.cn/problems/find-the-duplicate-number/) | [参考题解](https://leetcode.doocs.org/lc/287/) | [题解源码](https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0287.Find%20the%20Duplicate%20Number/README.md)

### 题目要求
给定一个包含 `n + 1` 个整数的数组 `nums` ，其数字都在 `[1, n]` 范围内（包括 `1` 和 `n`），可知至少存在一个重复的整数。 假设 `nums` 只有 一个重复的整数 ，返回 这个重复的数 。 你设计的解决方案必须 不修改 数组 `nums` 且只用常量级 `O(1)` 的额外空间。

### 样例数据
样例 1:
```text
输入：nums = [1,3,4,2,2]
输出：2
```

样例 2:
```text
输入：nums = [3,1,3,4,2]
输出：3
```

### 核心思路
`方法一：二分查找`

我们可以发现，如果 [1,..x] 中的数字个数大于 x，那么重复的数字一定在 [1,..x] 中，否则重复的数字一定在 [x+1,..n] 中。 因此，我们可以二分枚举 x，每次判断 [1,..x] 中的数字个数是否大于 x，从而确定重复的数字在哪个区间中，进而缩小区间范围，直到找到重复的数字。

### 复杂度
时间复杂度 O(n \times \log n)，其中 n 是数组 nums 的长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int findDuplicate(int[] nums) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int mid = (l + r) >> 1;
            int cnt = 0;
            for (int v : nums) {
                if (v <= mid) {
                    ++cnt;
                }
            }
            if (cnt > mid) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
    }
}
```


**来源：剑指 Offer**

<a id="offer-15"></a>
## 剑指 Offer 15. 二进制中1的个数

- 难度：简单
- 标签：位运算
- 跳转：[官方题目](https://leetcode.cn/problems/er-jin-zhi-zhong-1de-ge-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/15/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9815.%20%E4%BA%8C%E8%BF%9B%E5%88%B6%E4%B8%AD1%E7%9A%84%E4%B8%AA%E6%95%B0/README.md)

### 题目要求
编写一个函数，输入是一个无符号整数（以二进制串的形式），返回其二进制表达式中数字位数为 '1' 的个数（也被称为 汉明重量).）。 提示： - 请注意，在某些语言（如 Java）中，没有无符号整数类型。在这种情况下，输入和输出都将被指定为有符号整数类型，并且不应影响您的实现，因为无论整数是有符号的还是无符号的，其内部的二进制表示形式都是相同的。 - 在 Java 中，编译器使用 二进制补码 记法来表示有符号整数。因此，在上面的

### 样例数据
样例 1:
```text
输入：n = 11 (控制台输入 00000000000000000000000000001011)
输出：3
解释：输入的二进制串 `00000000000000000000000000001011 中，共有三位为 '1'。`
```

样例 2:
```text
输入：n = 128 (控制台输入 00000000000000000000000010000000)
输出：1
解释：输入的二进制串 00000000000000000000000010000000 中，共有一位为 '1'。
```

### 核心思路
`方法一：位运算`

由于 n \& (n - 1) 可以消除 n 的二进制表示中最右边的 1，因此不断执行 n \& (n - 1)，直到 n = 0，统计执行次数即可。

### 复杂度
时间复杂度 O(\log n)，空间复杂度 O(1)。

### Java 代码
```java
public class Solution {
    // you need to treat n as an unsigned value
    public int hammingWeight(int n) {
        int ans = 0;
        while (n != 0) {
            n &= (n - 1);
            ++ans;
        }
        return ans;
    }
}
```

---

<a id="offer-56-1"></a>
## 剑指 Offer 56 - I. 数组中数字出现的次数

- 难度：中等
- 标签：位运算
- 跳转：[官方题目](https://leetcode.cn/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/56.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9856%20-%20I.%20%E6%95%B0%E7%BB%84%E4%B8%AD%E6%95%B0%E5%AD%97%E5%87%BA%E7%8E%B0%E7%9A%84%E6%AC%A1%E6%95%B0/README.md)

### 题目要求
一个整型数组 `nums` 里除两个数字之外，其他数字都出现了两次。请写程序找出这两个只出现一次的数字。要求时间复杂度是O(n)，空间复杂度是O(1)。

### 样例数据
样例 1:
```text
输入：nums = [4,1,4,6]
输出：[1,6] 或 [6,1]
```

样例 2:
```text
输入：nums = [1,2,10,4,1,4,3,3]
输出：[2,10] 或 [10,2]
```

### 核心思路
`方法一：位运算`

由于数组中除了两个数字之外，其他数字都出现了两次，因此对数组中的所有数字进行异或运算，得到的结果即为两个只出现一次的数字的异或结果。 由于这两个数字不相等，因此异或结果中至少存在一位为 1。 我们通过 `lowbit` 运算找到异或结果中最低位的 1，并将数组中的所有数字按照该位是否为 1 分为两组，这样两个只出现一次的数字就被分到了不同的组中。 对两个组分别进行异或运算，即可得到两个只出现一次的数字。

### 复杂度
时间复杂度 O(n)，其中 n 为数组长度。 空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int[] singleNumbers(int[] nums) {
        int xs = 0;
        for (int x : nums) {
            xs ^= x;
        }
        int lb = xs & -xs;
        int a = 0;
        for (int x : nums) {
            if ((x & lb) != 0) {
                a ^= x;
            }
        }
        int b = xs ^ a;
        return new int[] {a, b};
    }
}
```

---

<a id="offer-56-2"></a>
## 剑指 Offer 56 - II. 数组中数字出现的次数 II

- 难度：中等
- 标签：位运算
- 跳转：[官方题目](https://leetcode.cn/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-ii-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/56.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9856%20-%20II.%20%E6%95%B0%E7%BB%84%E4%B8%AD%E6%95%B0%E5%AD%97%E5%87%BA%E7%8E%B0%E7%9A%84%E6%AC%A1%E6%95%B0%20II/README.md)

### 题目要求
在一个数组 `nums` 中除一个数字只出现一次之外，其他数字都出现了三次。请找出那个只出现一次的数字。

### 样例数据
样例 1:
```text
输入：nums = [3,4,3,3]
输出：4
```

样例 2:
```text
输入：nums = [9,1,7,9,7,9,7]
输出：1
```

### 核心思路
`方法一：位运算`

我们用一个长度为 32 的数组 cnt 来统计所有数字的每一位中 1 的出现次数。 如果某一位的 1 的出现次数能被 3 整除，那么那个只出现一次的数字二进制表示中对应的那一位也是 0；否则，那个只出现一次的数字二进制表示中对应的那一位是 1。 其中 n 是数组的长度；而 C 是整数的位数，本题中 C=32。

### 复杂度
时间复杂度 O(n \times C)，空间复杂度 O(C)。

### Java 代码
```java
class Solution {
    public int singleNumber(int[] nums) {
        int[] cnt = new int[32];
        for (int x : nums) {
            for (int i = 0; i < 32; ++i) {
                cnt[i] += x & 1;
                x >>= 1;
            }
        }
        int ans = 0;
        for (int i = 0; i < 32; ++i) {
            if (cnt[i] % 3 == 1) {
                ans |= 1 << i;
            }
        }
        return ans;
    }
}
```

---

<a id="offer-64"></a>
## 剑指 Offer 64. 求1+2+…+n

- 难度：中等
- 标签：位运算
- 跳转：[官方题目](https://leetcode.cn/problems/qiu-12n-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/64/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9864.%20%E6%B1%821%2B2%2B%E2%80%A6%2Bn/README.md)

### 题目要求
求 `1+2+...+n` ，要求不能使用乘除法、for、while、if、else、switch、case等关键字及条件判断语句（A?B:C）。

### 样例数据
样例 1:
```text
输入: n = 3
输出: 6
```

样例 2:
```text
输入: n = 9
输出: 45
```

### 核心思路
`方法一`

优先按题目所属专题套用对应模板，再处理边界。

### Java 代码
```java
class Solution {
    public int sumNums(int n) {
        int s = n;
        boolean t = n > 0 && (s += sumNums(n - 1)) > 0;
        return s;
    }
}
```

---

<a id="offer-65"></a>
## 剑指 Offer 65. 不用加减乘除做加法

- 难度：简单
- 标签：位运算
- 跳转：[官方题目](https://leetcode.cn/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/65/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9865.%20%E4%B8%8D%E7%94%A8%E5%8A%A0%E5%87%8F%E4%B9%98%E9%99%A4%E5%81%9A%E5%8A%A0%E6%B3%95/README.md)

### 题目要求
写一个函数，求两个整数之和，要求在函数体内不得使用 “+”、“-”、“*”、“/” 四则运算符号。

### 样例数据
样例 1:
```text
输入: a = 1, b = 1
输出: 2
```

### 核心思路
`方法一：位运算`

两数字 a, b 求和。 假设 a_i 和 b_i 分别表示 a 和 b 的第 i 个二进制位。 一共有 4 种情况：

| a_i | b_i | 不进位的和 | 进位 |
| ----- | ----- | ---------- | ---- |
| 0     | 0     | 0          | 0    |
| 0     | 1     | 1          | 0    |
| 1     | 0     | 1          | 0    |
| 1     | 1     | 0          | 1    |

观察可以发现，“不进位的和”与“异或运算”有相同规律，而进位则与“与”运算规律相同，并且需要左移一位。 - 对两数进行按位 `&` 与运算，然后左移一位，得到进位；
- 对两数进行按位 `^` 异或运算，得到不进位的和；
- 问题转换为求：“不进位的数 + 进位” 之和；
- 循环，直至进位为 0，返回不进位的数即可（也可以用递归实现）。 其中 M 为整数的最大值。

### 复杂度
时间复杂度 O(\log M)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int add(int a, int b) {
        while (b != 0) {
            int c = (a & b) << 1;
            a ^= b;
            b = c;
        }
        return a;
    }
}
```


### 解题模板

```
// 统计 1 的个数：n & (n - 1) 消除最低位 1
while (n != 0) { n &= (n - 1); ans++; }

// 只出现一次的数字：异或抵消
// 两个只出现一次：异或后 lowbit 分组
int lb = xor & (-xor);

// 只出现一次（其他三次）：逐位统计 % 3
```

**识别信号**：出现次数奇偶、二进制位操作 → 位运算（异或消除、lowbit 分组、逐位统计）。

---

## 十八、数学 / 模拟 / 排序 / 快速幂

**来源：剑指 Offer**

<a id="offer-14-1"></a>
## 剑指 Offer 14- I. 剪绳子

- 难度：中等
- 标签：数学
- 跳转：[官方题目](https://leetcode.cn/problems/jian-sheng-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/14.1/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9814-%20I.%20%E5%89%AA%E7%BB%B3%E5%AD%90/README.md)

### 题目要求
给你一根长度为 `n` 的绳子，请把绳子剪成整数长度的 `m` 段（m、n都是整数，n>1并且m>1），每段绳子的长度记为 `k[0],k[1]...k[m-1]` 。请问 `k[0]*k[1]*...*k[m-1]` 可能的最大乘积是多少？例如，当绳子的长度是8时，我们把它剪成长度分别为2、3、3的三段，此时得到的最大乘积是18。

### 样例数据
样例 1:
```text
输入: 2
输出: 1
解释: 2 = 1 + 1, 1 × 1 = 1
```

样例 2:
```text
输入: 10
输出: 36
解释: 10 = 3 + 3 + 4, 3 × 3 × 4 = 36
```

### 核心思路
`方法一：动态规划`

我们定义 f[i] 表示正整数 i 拆分后能获得的最大乘积，初始时 f[1] = 1。 答案即为 f[n]。 考虑 i 最后拆分出的数字 j，其中 j \in [1, i)。 对于 i 拆分出的数字 j，有两种情况：

1. 将 i 拆分成 i - j 和 j 的和，不继续拆分，此时乘积为 (i - j) \times j；
2. 将 i 拆分成 i - j 和 j 的和，继续拆分，此时乘积为 f[i - j] \times j。 因此，我们可以得到状态转移方程：

$
f[i] = \max(f[i], f[i - j] \times j, (i - j) \times j) \quad (j \in [0, i))

最后返回 f[n] 即可。 其中 n$ 为给定的正整数。

### 复杂度
时间复杂度 O(n^2)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int cuttingRope(int n) {
        int[] f = new int[n + 1];
        f[1] = 1;
        for (int i = 2; i <= n; ++i) {
            for (int j = 1; j < i; ++j) {
                f[i] = Math.max(Math.max(f[i], f[i - j] * j), (i - j) * j);
            }
        }
        return f[n];
    }
}
```

---

<a id="offer-14-2"></a>
## 剑指 Offer 14- II. 剪绳子 II

- 难度：中等
- 标签：数学
- 跳转：[官方题目](https://leetcode.cn/problems/jian-sheng-zi-ii-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/14.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9814-%20II.%20%E5%89%AA%E7%BB%B3%E5%AD%90%20II/README.md)

### 题目要求
给你一根长度为 `n` 的绳子，请把绳子剪成整数长度的 `m` 段（m、n都是整数，n>1并且m>1），每段绳子的长度记为 `k[0],k[1]...k[m - 1]` 。请问 `k[0]*k[1]*...*k[m - 1]` 可能的最大乘积是多少？例如，当绳子的长度是8时，我们把它剪成长度分别为2、3、3的三段，此时得到的最大乘积是18。 答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

### 样例数据
样例 1:
```text
输入: 2
输出: 1
解释: 2 = 1 + 1, 1 × 1 = 1
```

样例 2:
```text
输入: 10
输出: 36
解释: 10 = 3 + 3 + 4, 3 × 3 × 4 = 36
```

### 核心思路
`方法一：数学（快速幂）`

当 n \lt 4，此时 n 不能拆分成至少两个正整数的和，因此 n - 1 是最大乘积。 当 n \ge 4 时，我们尽可能多地拆分 3，当剩下的最后一段为 4 时，我们将其拆分为 2 + 2，这样乘积最大。

### 复杂度
时间复杂度 O(\log n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    private final int mod = (int) 1e9 + 7;

    public int cuttingRope(int n) {
        if (n < 4) {
            return n - 1;
        }
        if (n % 3 == 0) {
            return qpow(3, n / 3);
        }
        if (n % 3 == 1) {
            return (int) (4L * qpow(3, n / 3 - 1) % mod);
        }
        return 2 * qpow(3, n / 3) % mod;
    }

    private int qpow(long a, long n) {
        long ans = 1;
        for (; n > 0; n >>= 1) {
            if ((n & 1) == 1) {
                ans = ans * a % mod;
            }
            a = a * a % mod;
        }
        return (int) ans;
    }
}
```

---

<a id="offer-43"></a>
## 剑指 Offer 43. 1～n 整数中 1 出现的次数

- 难度：中等
- 标签：数学
- 跳转：[官方题目](https://leetcode.cn/problems/1nzheng-shu-zhong-1chu-xian-de-ci-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/43/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9843.%201%EF%BD%9En%E6%95%B4%E6%95%B0%E4%B8%AD1%E5%87%BA%E7%8E%B0%E7%9A%84%E6%AC%A1%E6%95%B0/README.md)

### 题目要求
输入一个整数 `n` ，求1～n这n个整数的十进制表示中1出现的次数。 例如，输入12，1～12这些整数中包含1 的数字有1、10、11和12，1一共出现了5次。

### 样例数据
样例 1:
```text
输入：n = 12
输出：5
```

样例 2:
```text
输入：n = 13
输出：6
```

### 核心思路
`方法一：数位 DP`

这道题实际上是求在给定区间 [l,..r] 中，数字中出现 1 个数。 个数与数的位数以及每一位上的数字有关。 我们可以用数位 DP 的思路来解决这道题。 对于区间 [l,..r] 问题，我们一般会将其转化为 [1,..r] 然后再减去 [1,..l - 1] 的问题，即：

$
ans = \sum_{i=1}^{r} ans_i -  \sum_{i=1}^{l-1} ans_i

不过对于本题而言，我们只需要求出区间 [1,..r] 的值即可。 这里我们用记忆化搜索来实现数位 DP。 从起点向下搜索，到最底层得到方案数，一层层向上返回答案并累加，最后从搜索起点得到最终的答案。 基本步骤如下：

1. 将数字 n 转为 int 数组 a，其中 a[0] 为最低位，而 a[i] 为最高位；
1. 根据题目信息，设计函数 dfs()，对于本题，我们定义 dfs(pos, cnt, limit)，其中：

- `pos` 表示数字的位数，从末位或者第一位开始，一般根据题目的数字构造性质来选择顺序。 对于本题，我们选择从高位开始，因此，`pos` 的初始值为 `len`；
- `cnt` 表示当前数字中包含的 1 的个数。 - `limit` 表示可填的数字的限制，如果无限制，那么可以选择 [0,1,..9]，否则，只能选择 [0,..a[pos]]。 如果 `limit` 为 `true` 且已经取到了能取到的最大值，那么下一个 `limit` 同样为 `true`；如果 `limit` 为 `true` 但是还没有取到最大值，或者 `limit` 为 `false`，那么下一个 `limit` 为 `false`。 那么答案为 dfs(i, 0, true)。 关于函数的实现细节，可以参考下面的代码。 相似题目：

- [357. 统计各位数字都不同的数字个数](https://github.com/doocs/leetcode/blob/main/solution/0300-0399/0357.Count%20Numbers%20with%20Unique%20Digits/README.md)
- [600. 不含连续 1 的非负整数](https://github.com/doocs/leetcode/blob/main/solution/0600-0699/0600.Non-negative%20Integers%20without%20Consecutive%20Ones/README.md)
- [788. 旋转数字](https://github.com/doocs/leetcode/blob/main/solution/0700-0799/0788.Rotated%20Digits/README.md)
- [902. 最大为 N 的数字组合](https://github.com/doocs/leetcode/blob/main/solution/0900-0999/0902.Numbers%20At%20Most%20N%20Given%20Digit%20Set/README.md)
- [1012. 至少有 1 位重复的数字](https://github.com/doocs/leetcode/blob/main/solution/1000-1099/1012.Numbers%20With%20Repeated%20Digits/README.md)
- [2376. 统计特殊整数](https://github.com/doocs/leetcode/blob/main/solution/2300-2399/2376.Count%20Special%20Integers/README.md)

### 复杂度
数位 DP 中，数的大小对复杂度的影响很小。 时间复杂度 O(\log n)$。

### Java 代码
```java
class Solution {
    private int[] a = new int[12];
    private Integer[][] f = new Integer[12][12];

    public int countDigitOne(int n) {
        int i = -1;
        for (; n > 0; n /= 10) {
            a[++i] = n % 10;
        }
        return dfs(i, 0, true);
    }

    private int dfs(int pos, int cnt, boolean limit) {
        if (pos < 0) {
            return cnt;
        }
        if (!limit && f[pos][cnt] != null) {
            return f[pos][cnt];
        }
        int up = limit ? a[pos] : 9;
        int ans = 0;
        for (int i = 0; i <= up; ++i) {
            ans += dfs(pos - 1, cnt + (i == 1 ? 1 : 0), limit && i == up);
        }
        return f[pos][cnt] = ans;
    }
}
```

---

<a id="offer-44"></a>
## 剑指 Offer 44. 数字序列中某一位的数字

- 难度：中等
- 标签：数学
- 跳转：[官方题目](https://leetcode.cn/problems/shu-zi-xu-lie-zhong-mou-yi-wei-de-shu-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/44/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9844.%20%E6%95%B0%E5%AD%97%E5%BA%8F%E5%88%97%E4%B8%AD%E6%9F%90%E4%B8%80%E4%BD%8D%E7%9A%84%E6%95%B0%E5%AD%97/README.md)

### 题目要求
数字以123456789101112131415…的格式序列化到一个字符序列中。在这个序列中，第5位是5，第13位是1，第19位是4，等等。 请写一个函数，求任意第n位对应的数字。

### 样例数据
样例 1:
```text
输入：n = 3
输出：3
```

样例 2:
```text
输入：n = 11
输出：0
```

### 核心思路
`方法一：数学`

位数为 k 的最小整数和最大整数分别为 10^{k-1} 和 10^k-1，因此 k 位数的总位数为 k \times 9 \times 10^{k-1}。 我们用 k 表示当前数字的位数，用 cnt 表示当前位数的数字的总数，初始时 k=1, cnt=9。 每次将 n 减去 cnt \times k，当 n 小于等于 cnt \times k 时，说明 n 对应的数字在当前位数的数字范围内，此时可以计算出对应的数字。 具体做法是，首先计算出 n 对应的是当前位数的哪一个数字，然后计算出是该数字的第几位，从而得到该位上的数字。 其中 n 为给定的数字。

### 复杂度
时间复杂度 O(\log_{10} n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int findNthDigit(int n) {
        int k = 1, cnt = 9;
        while ((long) k * cnt < n) {
            n -= k * cnt;
            ++k;
            cnt *= 10;
        }
        int num = (int) Math.pow(10, k - 1) + (n - 1) / k;
        int idx = (n - 1) % k;
        return String.valueOf(num).charAt(idx) - '0';
    }
}
```

---

<a id="offer-62"></a>
## 剑指 Offer 62. 圆圈中最后剩下的数字

- 难度：简单
- 标签：数学
- 跳转：[官方题目](https://leetcode.cn/problems/yuan-quan-zhong-zui-hou-sheng-xia-de-shu-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/62/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9862.%20%E5%9C%86%E5%9C%88%E4%B8%AD%E6%9C%80%E5%90%8E%E5%89%A9%E4%B8%8B%E7%9A%84%E6%95%B0%E5%AD%97/README.md)

### 题目要求
0,1,···,n-1这n个数字排成一个圆圈，从数字0开始，每次从这个圆圈里删除第m个数字（删除后从下一个数字开始计数）。求出这个圆圈里剩下的最后一个数字。 例如，0、1、2、3、4这5个数字组成一个圆圈，从数字0开始每次删除第3个数字，则删除的前4个数字依次是2、0、4、1，因此最后剩下的数字是3。

### 样例数据
样例 1:
```text
输入: n = 5, m = 3
输出: 3
```

样例 2:
```text
输入: n = 10, m = 17
输出: 2
```

### 核心思路
`方法一：数学 + 递归（迭代）`

我们不妨设 f(n, m) 表示从 n 个数中每次删除第 m 个，最后剩下的是第几个数字。 我们第一次删除了第 m 个数字，剩下 n-1 个数，那么 x=f(n - 1, m) 就表示从剩下的 n-1 个数中，每次删除第 m 个，最后剩下的是第几个数字。 我们求得 x 之后，便可以知道 f(n, m) 应该是从 m \% n 开始数的第 x 个元素，即 f(n, m) = (m \% n + x) \% n。 当 n 为 1 时，最后留下的数字序号一定为 0。 递归求解即可，也可以改成迭代。

### 复杂度
时间复杂度 O(n)，递归的空间复杂度 O(n)，迭代的空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int lastRemaining(int n, int m) {
        return f(n, m);
    }

    private int f(int n, int m) {
        if (n == 1) {
            return 0;
        }
        int x = f(n - 1, m);
        return (m + x) % n;
    }
}
```


**来源：剑指 Offer**

<a id="offer-5"></a>
## 剑指 Offer 05. 替换空格

- 难度：简单
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/ti-huan-kong-ge-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/5/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9805.%20%E6%9B%BF%E6%8D%A2%E7%A9%BA%E6%A0%BC/README.md)

### 题目要求
请实现一个函数，把字符串 `s` 中的每个空格替换成"%20"。

### 样例数据
样例 1:
```text
输入：s = "We are happy."
输出："We%20are%20happy."
```

### 核心思路
`方法一：字符串内置方法`

使用 `replace()` 方法。 其中 n 为字符串长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public String replaceSpace(String s) {
        return s.replaceAll(" ", "%20");
    }
}
```

---

<a id="offer-17"></a>
## 剑指 Offer 17. 打印从1到最大的n位数

- 难度：简单
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/da-yin-cong-1dao-zui-da-de-nwei-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/17/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9817.%20%E6%89%93%E5%8D%B0%E4%BB%8E1%E5%88%B0%E6%9C%80%E5%A4%A7%E7%9A%84n%E4%BD%8D%E6%95%B0/README.md)

### 题目要求
输入数字 `n`，按顺序打印出从 1 到最大的 n 位十进制数。比如输入 3，则打印出 1、2、3 一直到最大的 3 位数 999。

### 样例数据
样例 1:
```text
输入: n = 1
输出: [1,2,3,4,5,6,7,8,9]
```

### 核心思路
`方法一：模拟`

直接根据题意模拟即可。 如果 n 的值比较大，那么直接使用整数会溢出，因此可以使用字符串来模拟，参考以下代码中的 `print()` 函数。

### 复杂度
时间复杂度 O(10^n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int[] printNumbers(int n) {
        int[] ans = new int[(int) Math.pow(10, n) - 1];
        for (int i = 0; i < ans.length; ++i) {
            ans[i] = i + 1;
        }
        return ans;
    }

    private StringBuilder s = new StringBuilder();
    private List<String> ans = new ArrayList<>();

    public List<String> print(int n) {
        for (int i = 1; i <= n; ++i) {
            dfs(0, i);
        }
        return ans;
    }

    private void dfs(int i, int j) {
        if (i == j) {
            ans.add(s.toString());
            return;
        }
        int k = i > 0 ? 0 : 1;
        for (; k < 10; ++k) {
            s.append(k);
            dfs(i + 1, j);
            s.deleteCharAt(s.length() - 1);
        }
    }
}
```

---

<a id="offer-20"></a>
## 剑指 Offer 20. 表示数值的字符串

- 难度：中等
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/biao-shi-shu-zhi-de-zi-fu-chuan-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/20/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9820.%20%E8%A1%A8%E7%A4%BA%E6%95%B0%E5%80%BC%E7%9A%84%E5%AD%97%E7%AC%A6%E4%B8%B2/README.md)

### 题目要求
请实现一个函数用来判断字符串是否表示数值（包括整数和小数）。 数值（按顺序）可以分成以下几个部分： - 若干空格 - 一个 小数 或者 整数 - （可选）一个 `'e'` 或 `'E'` ，后面跟着一个 整数 - 若干空格 小数（按顺序）可以分成以下几个部分： - （可选）一个符号字符（`'+'` 或 `'-'`） - 下述格式之一： - 至少一位数字，后面跟着一个点 `'.'` - 至少一位数字，后面跟着一个点 `'.'` ，后面再跟着至少一位数字 - 一个点 `'.'` ，后面跟着至少一位数字 整数（按顺序）可以分成以下几个部分： - （可选）一个符号字符（`'+'` 或 `'-'`） - 至少一位数字 部分数值列举如下： - `["+100", "5e2", "-123", "3.1416", "-1E-16", "0123"]` 部分非数值列举如下： - `["12e", "1a3.14", "1.2.3", "+-5", "12e+5.4"]`

### 样例数据
样例 1:
```text
输入：s = "0"
输出：true
```

样例 2:
```text
输入：s = "e"
输出：false
```

### 核心思路
`方法一：分类讨论`

我们先去除字符串 s 首尾的空格，此时 i 和 j 分别指向字符串 s 的第一个非空格字符和最后一个非空格字符。 然后我们维护以下几个变量，其中：

- `digit`：表示是否出现过数字
- `dot`：表示是否出现过点
- `e`：表示是否出现过 `e` 或者 `E`

遍历 s[i,..j] 范围内的每个字符，根据字符的类型进行分类讨论：

- 如果当前字符是 `+` 或者 `-`，那么该字符必须是第一个有效字符（即空格后的第一个非空字符），或者该字符的前一个字符必须是 `e` 或者 `E`，否则返回 `false`。 - 如果当前字符是数字，那么我们将 `digit` 置为 `true`。 - 如果当前字符是 `.`，那么该字符之前不能出现过 `.` 或者 `e`/`E`，否则返回 `false`，否则我们将 `dot` 置为 `true`。 - 如果当前字符是 `e` 或者 `E`，那么该字符之前不能出现过 `e`/`E`，并且必须出现过数字，否则返回 `false`，否则我们将 `e` 置为 `true`，并且将 `digit` 置为 `false`，表示 `e` 之后必须出现数字。 - 如果当前字符是其它字符，那么返回 `false`。 遍历结束后，我们返回 `digit`，即是否出现过数字。 其中 n 为字符串 s 的长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public boolean isNumber(String s) {
        int i = 0, j = s.length() - 1;
        while (i < j && s.charAt(i) == ' ') {
            ++i;
        }
        while (i <= j && s.charAt(j) == ' ') {
            --j;
        }
        if (i > j) {
            return false;
        }
        boolean digit = false;
        boolean dot = false;
        boolean e = false;
        for (; i <= j; ++i) {
            if (s.charAt(i) == '+' || s.charAt(i) == '-') {
                if (i > 0 && s.charAt(i - 1) != ' ' && s.charAt(i - 1) != 'e'
                    && s.charAt(i - 1) != 'E') {
                    return false;
                }
            } else if (Character.isDigit(s.charAt(i))) {
                digit = true;
            } else if (s.charAt(i) == '.') {
                if (dot || e) {
                    return false;
                }
                dot = true;
            } else if (s.charAt(i) == 'e' || s.charAt(i) == 'E') {
                if (!digit || e) {
                    return false;
                }
                e = true;
                digit = false;
            } else {
                return false;
            }
        }
        return digit;
    }
}
```

---

<a id="offer-29"></a>
## 剑指 Offer 29. 顺时针打印矩阵

- 难度：简单
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/shun-shi-zhen-da-yin-ju-zhen-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/29/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9829.%20%E9%A1%BA%E6%97%B6%E9%92%88%E6%89%93%E5%8D%B0%E7%9F%A9%E9%98%B5/README.md)

### 题目要求
输入一个矩阵，按照从外向里以顺时针的顺序依次打印出每一个数字。

### 样例数据
样例 1:
```text
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]
```

样例 2:
```text
输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出：[1,2,3,4,8,12,11,10,9,5,6,7]
```

### 核心思路
`方法一：模拟`

我们用 i 和 j 分别表示当前访问到的元素的行和列，用 k 表示当前的方向，用数组或哈希表 vis 记录每个元素是否被访问过。 每次我们访问到一个元素后，将其标记为已访问，然后按照当前的方向前进一步，如果前进一步后发现越界或者已经访问过，则改变方向继续前进，直到遍历完整个矩阵。 其中 m 和 n 分别是矩阵的行数和列数。

### 复杂度
时间复杂度 O(m \times n)，空间复杂度 O(m \times n)。

### Java 代码
```java
class Solution {
    public int[] spiralOrder(int[][] matrix) {
        if (matrix.length == 0 || matrix[0].length == 0) {
            return new int[] {};
        }
        int m = matrix.length, n = matrix[0].length;
        boolean[][] vis = new boolean[m][n];
        int[] ans = new int[m * n];
        int i = 0, j = 0, k = 0;
        int[] dirs = {0, 1, 0, -1, 0};
        for (int h = 0; h < m * n; ++h) {
            ans[h] = matrix[i][j];
            vis[i][j] = true;
            int x = i + dirs[k], y = j + dirs[k + 1];
            if (x < 0 || y < 0 || x >= m || y >= n || vis[x][y]) {
                k = (k + 1) % 4;
                x = i + dirs[k];
                y = j + dirs[k + 1];
            }
            i = x;
            j = y;
        }
        return ans;
    }
}
```

---

<a id="offer-39"></a>
## 剑指 Offer 39. 数组中出现次数超过一半的数字

- 难度：简单
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-ban-de-shu-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/39/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9839.%20%E6%95%B0%E7%BB%84%E4%B8%AD%E5%87%BA%E7%8E%B0%E6%AC%A1%E6%95%B0%E8%B6%85%E8%BF%87%E4%B8%80%E5%8D%8A%E7%9A%84%E6%95%B0%E5%AD%97/README.md)

### 题目要求
数组中有一个数字出现的次数超过数组长度的一半，请找出这个数字。 你可以假设数组是非空的，并且给定的数组总是存在多数元素。

### 样例数据
样例 1:
```text
输入: [1, 2, 3, 2, 2, 2, 5, 4, 2]
输出: 2
```

### 核心思路
`方法一：摩尔投票法`

摩尔投票法的基本步骤如下：

初始化元素 m，并给计数器 cnt 赋初值 cnt=0。 对于输入列表中每一个元素 x：

1. 若 cnt=0，那么 m=x and cnt=1；
1. 否则若 m=x，那么 cnt=cnt+1；
1. 否则 cnt=cnt-1。 一般而言，摩尔投票法需要对输入的列表进行**两次遍历**。 在第一次遍历中，我们生成候选值 m，如果存在多数，那么该候选值就是多数值。 在第二次遍历中，只需要简单地计算候选值的频率，以确认是否是多数值。 由于本题已经明确说明存在多数值，所以第一次遍历结束后，直接返回 m 即可，无需二次遍历确认是否是多数值。 其中 n 为数组长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int majorityElement(int[] nums) {
        int cnt = 0, m = 0;
        for (int v : nums) {
            if (cnt == 0) {
                m = v;
                cnt = 1;
            } else {
                cnt += (m == v ? 1 : -1);
            }
        }
        return m;
    }
}
```

---

<a id="offer-58-2"></a>
## 剑指 Offer 58 - II. 左旋转字符串

- 难度：简单
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/zuo-xuan-zhuan-zi-fu-chuan-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/58.2/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9858%20-%20II.%20%E5%B7%A6%E6%97%8B%E8%BD%AC%E5%AD%97%E7%AC%A6%E4%B8%B2/README.md)

### 题目要求
字符串的左旋转操作是把字符串前面的若干个字符转移到字符串的尾部。请定义一个函数实现字符串左旋转操作的功能。比如，输入字符串"abcdefg"和数字2，该函数将返回左旋转两位得到的结果"cdefgab"。

### 样例数据
样例 1:
```text
输入: s = "abcdefg", k = 2
输出: "cdefgab"
```

样例 2:
```text
输入: s = "lrloseumgh", k = 6
输出: "umghlrlose"
```

### 核心思路
`方法一：模拟`

我们可以将字符串分为两部分，分别对两部分进行翻转，然后再对整个字符串进行翻转，即可得到结果。 或者直接截取两个子串，然后拼接起来。 其中 n 为字符串长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public String reverseLeftWords(String s, int n) {
        return s.substring(n, s.length()) + s.substring(0, n);
    }
}
```

---

<a id="offer-61"></a>
## 剑指 Offer 61. 扑克牌中的顺子

- 难度：简单
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/bu-ke-pai-zhong-de-shun-zi-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/61/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9861.%20%E6%89%91%E5%85%8B%E7%89%8C%E4%B8%AD%E7%9A%84%E9%A1%BA%E5%AD%90/README.md)

### 题目要求
从若干副扑克牌中随机抽 `5` 张牌，判断是不是一个顺子，即这5张牌是不是连续的。2～10为数字本身，A为1，J为11，Q为12，K为13，而大、小王为 0 ，可以看成任意数字。A 不能视为 14。

### 样例数据
样例 1:
```text
输入: [1,2,3,4,5]
输出: True
```

样例 2:
```text
输入: [0,0,1,2,5]
输出: True
```

### 核心思路
`方法一：遍历`

我们首先明确顺子不成立的核心条件：

1. 存在非 0 的重复。 2. 最大值与最小值的差距超过 4（最大最小值比较不包括 0 在内）。 因此，我们可以用一个哈希表或数组 `vis` 记录数字是否出现过，用 `mi` 和 `mx` 记录最大值和最小值。 遍历数组，忽略大小王（0），求出数组的最大、最小值。 若最后差值超过 4，则无法构成顺子。 其中 n 为数组长度。

### 复杂度
时间复杂度 O(n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public boolean isStraight(int[] nums) {
        boolean[] vis = new boolean[14];
        int mi = 20, mx = -1;
        for (int x : nums) {
            if (x == 0) {
                continue;
            }
            if (vis[x]) {
                return false;
            }
            vis[x] = true;
            mi = Math.min(mi, x);
            mx = Math.max(mx, x);
        }
        return mx - mi <= 4;
    }
}
```

---

<a id="offer-66"></a>
## 剑指 Offer 66. 构建乘积数组

- 难度：简单
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/gou-jian-cheng-ji-shu-zu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/66/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9866.%20%E6%9E%84%E5%BB%BA%E4%B9%98%E7%A7%AF%E6%95%B0%E7%BB%84/README.md)

### 题目要求
给定一个数组 `A[0,1,…,n-1]`，请构建一个数组 `B[0,1,…,n-1]`，其中 `B[i]` 的值是数组 `A` 中除了下标 `i` 以外的元素的积, 即 `B[i]=A[0]×A[1]×…×A[i-1]×A[i+1]×…×A[n-1]`。不能使用除法。

### 样例数据
样例 1:
```text
输入: [1,2,3,4,5]
输出: [120,60,40,30,24]
```

### 核心思路
`方法一：两次遍历`

我们先创建一个长度为 n 的答案数组 ans。 接下来，我们从左到右遍历数组 a，过程中维护一个变量 left，表示当前元素左边所有元素的乘积，初始时 left=1。 当遍历到 a[i] 时，我们将 left 赋值给 ans[i]，然后 left 乘以 a[i]，即 left arrow left \times a[i]。 然后，我们从右到左遍历数组 a，过程中维护一个变量 right，表示当前元素右边所有元素的乘积，初始时 right=1。 当遍历到 a[i] 时，我们将 ans[i] 乘上 right，然后 right 乘以 a[i]，即 right arrow right \times a[i]。 最终，数组 ans 即为所求的答案。

### 复杂度
时间复杂度 O(n)，其中 n 为数组 a 的长度。 忽略答案数组的空间消耗，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public int[] constructArr(int[] a) {
        int n = a.length;
        int[] ans = new int[n];
        for (int i = 0, left = 1; i < n; ++i) {
            ans[i] = left;
            left *= a[i];
        }
        for (int i = n - 1, right = 1; i >= 0; --i) {
            ans[i] *= right;
            right *= a[i];
        }
        return ans;
    }
}
```

---

<a id="offer-67"></a>
## 剑指 Offer 67. 把字符串转换成整数

- 难度：中等
- 标签：模拟
- 跳转：[官方题目](https://leetcode.cn/problems/ba-zi-fu-chuan-zhuan-huan-cheng-zheng-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/67/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9867.%20%E6%8A%8A%E5%AD%97%E7%AC%A6%E4%B8%B2%E8%BD%AC%E6%8D%A2%E6%88%90%E6%95%B4%E6%95%B0/README.md)

### 题目要求
写一个函数 StrToInt，实现把字符串转换成整数这个功能。不能使用 atoi 或者其他类似的库函数。 首先，该函数会根据需要丢弃无用的开头空格字符，直到寻找到第一个非空格的字符为止。 当我们寻找到的第一个非空字符为正或者负号时，则将该符号与之后面尽可能多的连续数字组合起来，作为该整数的正负号；假如第一个非空字符是数字，则直接将其与之后连续的数字字符组合起来，形成整数。 该字符串除了有效的整数部分之后也可能会存在多余的字符，这些字符可以被忽略，它们对于函数不应该造成影响。 注意：假如该字符串中的第一个非空格字符不是一个有效整数字符、字符串为空或字符串仅包含空白字符时，则你的函数不需要进行转换。 在任何情况下，若函数不能进行有效的转换时，请返回 0。 说明： 假设我们的环境只能存储 32 位大小的有符号整数，那么其数值范围为 [−2^31, 2^31 − 1]。如果数值超过这个范围，请返回 INT_MAX (2^31 − 1) 或 INT_MIN (−2^31) 。

### 样例数据
样例 1:
```text
输入: "42"
输出: 42
```

样例 2:
```text
输入: " -42"
输出: -42
解释: 第一个非空白字符为 '-', 它是一个负号。
我们尽可能将负号与后面所有连续出现的数字组合起来，最后得到 -42 。
```

### 核心思路
`方法一`

优先按题目所属专题套用对应模板，再处理边界。

### Java 代码
```java
class Solution {
    public int strToInt(String str) {
        if (str == null) return 0;
        int n = str.length();
        if (n == 0) return 0;
        int i = 0;
        while (str.charAt(i) == ' ') {
            // 仅包含空格
            if (++i == n) return 0;
        }
        int sign = 1;
        if (str.charAt(i) == '-') sign = -1;
        if (str.charAt(i) == '-' || str.charAt(i) == '+') ++i;
        int res = 0, flag = Integer.MAX_VALUE / 10;
        for (; i < n; ++i) {
            // 非数字，跳出循环体
            if (str.charAt(i) < '0' || str.charAt(i) > '9') break;
            // 溢出判断
            if (res > flag || (res == flag) && str.charAt(i) > '7')
                return sign > 0 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
            res = res * 10 + (str.charAt(i) - '0');
        }
        return sign * res;
    }
}
```


**来源：剑指 Offer**

<a id="offer-45"></a>
## 剑指 Offer 45. 把数组排成最小的数

- 难度：中等
- 标签：排序
- 跳转：[官方题目](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/45/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9845.%20%E6%8A%8A%E6%95%B0%E7%BB%84%E6%8E%92%E6%88%90%E6%9C%80%E5%B0%8F%E7%9A%84%E6%95%B0/README.md)

### 题目要求
输入一个非负整数数组，把数组里所有数字拼接起来排成一个数，打印能拼接出的所有数字中最小的一个。

### 样例数据
样例 1:
```text
输入: `[10,2]`
输出: "`102"`
```

样例 2:
```text
输入: `[3,30,34,5,9]`
输出: "`3033459"`
```

### 核心思路
`方法一：自定义排序`

我们将数组中的数字转换为字符串，然后按照字符串拼接的大小进行排序。 具体地，比较两个字符串 a 和 b，如果 a + b \lt b + a，则 a 小于 b，否则 a 大于 b。 其中 n  和 m 分别为数组的长度和字符串的平均长度。

### 复杂度
时间复杂度 O(n \times \log n + n \times m)，空间复杂度 O(n \times m)。

### Java 代码
```java
class Solution {
    public String minNumber(int[] nums) {
        return Arrays.stream(nums)
            .mapToObj(String::valueOf)
            .sorted((a, b) -> (a + b).compareTo(b + a))
            .collect(Collectors.joining());
    }
}
```

---

<a id="offer-49"></a>
## 剑指 Offer 49. 丑数

- 难度：中等
- 标签：排序
- 跳转：[官方题目](https://leetcode.cn/problems/chou-shu-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/49/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9849.%20%E4%B8%91%E6%95%B0/README.md)

### 题目要求
我们把只包含质因子 2、3 和 5 的数称作丑数（Ugly Number）。求按从小到大的顺序的第 n 个丑数。

### 样例数据
样例 1:
```text
输入: n = 10
输出: 12
解释: `1, 2, 3, 4, 5, 6, 8, 9, 10, 12` 是前 10 个丑数。
```

### 核心思路
`方法一：优先队列（最小堆）`

初始时，将第一个丑数 1 加入堆。 每次取出堆顶元素 x，由于 2x, 3x, 5x 也是丑数，因此将它们加入堆中。 为了避免重复元素，可以用哈希表 vis 去重。

### 复杂度
时间复杂度 O(n \times \log n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    public int nthUglyNumber(int n) {
        Set<Long> vis = new HashSet<>();
        PriorityQueue<Long> q = new PriorityQueue<>();
        int[] f = new int[] {2, 3, 5};
        q.offer(1L);
        vis.add(1L);
        long ans = 0;
        while (n-- > 0) {
            ans = q.poll();
            for (int v : f) {
                long next = ans * v;
                if (vis.add(next)) {
                    q.offer(next);
                }
            }
        }
        return (int) ans;
    }
}
```

---

<a id="offer-51"></a>
## 剑指 Offer 51. 数组中的逆序对

- 难度：困难
- 标签：排序
- 跳转：[官方题目](https://leetcode.cn/problems/shu-zu-zhong-de-ni-xu-dui-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/51/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9851.%20%E6%95%B0%E7%BB%84%E4%B8%AD%E7%9A%84%E9%80%86%E5%BA%8F%E5%AF%B9/README.md)

### 题目要求
在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个逆序对。输入一个数组，求出这个数组中的逆序对的总数。

### 样例数据
样例 1:
```text
输入: [7,5,6,4]
输出: 5
```

### 核心思路
`方法一：归并排序`

归并排序的过程中，如果左边的数大于右边的数，则右边的数与左边的数之后的数都构成逆序对。 其中 n 为数组长度。

### 复杂度
时间复杂度 O(n \times \log n)，空间复杂度 O(n)。

### Java 代码
```java
class Solution {
    private int[] nums;
    private int[] t;

    public int reversePairs(int[] nums) {
        this.nums = nums;
        int n = nums.length;
        this.t = new int[n];
        return mergeSort(0, n - 1);
    }

    private int mergeSort(int l, int r) {
        if (l >= r) {
            return 0;
        }
        int mid = (l + r) >> 1;
        int ans = mergeSort(l, mid) + mergeSort(mid + 1, r);
        int i = l, j = mid + 1, k = 0;
        while (i <= mid && j <= r) {
            if (nums[i] <= nums[j]) {
                t[k++] = nums[i++];
            } else {
                ans += mid - i + 1;
                t[k++] = nums[j++];
            }
        }
        while (i <= mid) {
            t[k++] = nums[i++];
        }
        while (j <= r) {
            t[k++] = nums[j++];
        }
        for (i = l; i <= r; ++i) {
            nums[i] = t[i - l];
        }
        return ans;
    }
}
```


**来源：剑指 Offer**

<a id="offer-16"></a>
## 剑指 Offer 16. 数值的整数次方

- 难度：中等
- 标签：快速幂
- 跳转：[官方题目](https://leetcode.cn/problems/shu-zhi-de-zheng-shu-ci-fang-lcof/) | [参考题解](https://leetcode.doocs.org/lcof/16/) | [题解源码](https://github.com/doocs/leetcode/blob/main/lcof/%E9%9D%A2%E8%AF%95%E9%A2%9816.%20%E6%95%B0%E5%80%BC%E7%9A%84%E6%95%B4%E6%95%B0%E6%AC%A1%E6%96%B9/README.md)

### 题目要求
实现 pow(x, n) ，即计算 x 的 n 次幂函数（即，x^n）。不得使用库函数，同时不需要考虑大数问题。

### 样例数据
样例 1:
```text
输入：x = 2.00000, n = 10
输出：1024.00000
```

样例 2:
```text
输入：x = 2.10000, n = 3
输出：9.26100
```

### 核心思路
`方法一：数学（快速幂）`

快速幂算法的核心思想是将幂指数 n 拆分为若干个二进制位上的 1 的和，然后将 x 的 n 次幂转化为 x 的若干个幂的乘积。 其中 n 为幂指数。

### 复杂度
时间复杂度 O(\log n)，空间复杂度 O(1)。

### Java 代码
```java
class Solution {
    public double myPow(double x, int n) {
        return n >= 0 ? qpow(x, n) : 1 / qpow(x, -(long) n);
    }

    private double qpow(double a, long n) {
        double ans = 1;
        for (; n > 0; n >>= 1) {
            if ((n & 1) == 1) {
                ans = ans * a;
            }
            a = a * a;
        }
        return ans;
    }
}
```


### 解题模板

```
// 快速幂
double qpow(double a, long n) {
    double ans = 1;
    for (; n > 0; n >>= 1) {
        if ((n & 1) == 1) ans *= a;
        a *= a;
    }
    return ans;
}

// 归并排序求逆序对：merge 时统计
// 丑数：三指针 or 最小堆
// 数学：取模、整数溢出用 long
```

**识别信号**：幂运算 → 快速幂；逆序对 → 归并排序；丑数/约数 → 堆或指针。

---

