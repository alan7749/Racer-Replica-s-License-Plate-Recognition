import numpy as np
import numpy as np

plate_list = np.array([[], ['1', 'R'], ['I'], ['0'], ['R'], ['0'], ['6'], ['R', '1', '0'], ['R'], ['2'], ['Y', '0'], ['0', '0'], ['0', '0'], ['0'], ['9', '1', '0'], ['9', '1'], ['2', '9', '1'], ['2', '9', '1'], ['R', '2', '9', '1'], ['R', '2', '9', '1'], ['R', '2', '9', '1'], ['R', '2', '9', '1'], ['R', '2', '9', '1'], ['R', '2', '9', '1'], ['R', '2', '9', '1'], ['R', '2', '1', '0', '0'], ['R', '2', '9', '1', '0'], ['R', '2', '1', '0'], ['R', '2', '9', '1', '0'], ['R', '2', '9', '1', '0'], ['R', '2', '9', '0'], ['R', '2', '9', '1', '0'], ['R', '2', '9', '1', '0'], ['R', '2', '9', '1', '0'], ['R', '2', '9', '1', '0'], ['R', '2', '9', '1'], ['2', '1']], dtype = object)
class replace_tree:
    def __init__(self, plate_list):
        self.plate_list = plate_list
        max_idx_list = []
        max_num = -1
        for index, num_list in enumerate(plate_list[0:len(self.plate_list)]):
            if max_num < len(num_list):
                max_idx_list = []
                max_num = len(num_list)
                max_idx_list.append(index)
            elif max_num == len(num_list):
                max_idx_list.append(index)
            else:
                pass
        self.tree = []
        self.count = []
        for item in max_idx_list:
            print(plate_list[item])
        for item in max_idx_list:
            self.append(plate_list[item])

    def append(self, num_list):
        if not self.tree:
            for num in num_list:
                self.tree.append({num:1})
        elif self.tree:
            unexisist_list = []
            flag = 0
            start = 0
            for num in num_list:
                for i in range(start, len(self.tree)):
                    if self.tree[i].get(num) != None and flag == 0:
                        # 將unexsist_list放到i前面
                        
                        # =======================================
                        for j in range(len(unexisist_list)):
                            if (i - 1 - j) < 0:
                                # insert到最前面
                                self.tree.insert(0, {unexisist_list.pop():1})
                                i += 1
                                # start += 1
                            elif (i - 1 - j) >= 0:
                                self.tree[i - 1 - j][unexisist_list.pop()] = 1
                        # =======================================

                        self.tree[i][num] = self.tree[i][num] + 1
                        start = i + 1
                        flag = 1
                        break
                    elif self.tree[i].get(num) != None and flag == 1:
                        self.tree[i][num] = self.tree[i][num] + 1
                        start = i + 1
                        flag = 1
                        break
                    elif self.tree[i].get(num) == None and flag == 1:
                        # 連續
                        self.tree[i][num] = 1
                        start = i + 1
                        break
                    elif self.tree[i].get(num) == None and flag == 0:
                        # 放到unexsist_list
                        if i == (len(self.tree) - 1):
                            unexisist_list.append(num)
                    else :
                        print('else')
tree = replace_tree(plate_list)
print(tree.tree)
for i in plate_list:
    tree.append(i)
print(tree.tree)

for item in tree.tree:
    max_val = max(item, key=item.get)
    print(max_val)