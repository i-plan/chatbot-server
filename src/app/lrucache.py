import collections


class LRUCache:
    '''
    LRU Cache 最近最少使用页面置换算法
    1. 双向链表
    2. O(1)查询最近的，如果查询中间就不是O(1)
    3. O(1)修改、更新
    LFU Cache 最近最不常用页面置换算法
    '''

    def __init__(self, capacity: int):
        self.dic = collections.OrderedDict()
        self.remain = capacity

    def get(self, key: str):
        if key not in self.dic:
            return None
        v = self.dic.pop(key)
        self.dic[key] = v
        return v

    def put(self, key: str, value: str) -> None:
        if key in self.dic:
            self.dic.pop(key)
        else:
            if self.remain > 0:
                self.remain -= 1
            else:
                self.dic.popitem(last=False)
        self.dic[key] = value
