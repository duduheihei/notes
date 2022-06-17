## KMP算法
常用于字符串匹配与查找，可以将复杂度从O(M*N)降低至O(min(m,n))，试探回溯的经典问题
[参考博客](https://blog.csdn.net/tolearnmore/article/details/105519098)
注意，参考博客代码有错，无法全部AC，修改后代码为：
```c++
vector<int> getNext(string needle) {
	int len = needle.size();
	vector<int> ret(len, -1);
	int i = 1, j = 0;
	while (i < len)
	{
		j = ret[i - 1];
		while (j >= 0 && needle[i] != needle[j + 1])
		{
			j = ret[j];
		}
		if (needle[i] == needle[j + 1])
		{
			ret[i] = j + 1;
		}
		else {
			ret[i] = -1;
		}
		i++;

	}

	return ret;
}

int my_strStr(string haystack, string needle) {
	int a = haystack.size();
	int b = needle.size();
	if (a < b) {
		return -1;
	}
	vector<int> next = getNext(needle);
	int i = 0, j = 0;
	while (i < a && j < b) {
		if (haystack[i] == needle[j]) {
			i++;
			j++;
		}
		else if (j > 0) {
			j = next[j - 1] + 1;
		}
		else {
			i++;
		}
	}
	return j == b ? (i - b) : -1;
}
```