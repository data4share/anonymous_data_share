
# Anonymous Edition, only for loading "*_grouper.pkl" results.
# ======================
# Each "*_grouper.pkl" file contains a Grouper/Grouper_Overlap instance.
# Each nodes in the "Grouper.groups" are represented as the index, named func_id
# The function name is stored in "Grouper._list", where can be fetch by "Grouper._list[func_id]"
# The method "Grouper.readable_show(group_id)" might be help.

import os
class Grouper():
    def __init__(self, total_elem:int):
        self.groups = {}
        self.grouped_id = [-1 for _ in range(total_elem)]
        self.ig = self.grouped_id 
        self.overlap_gid = {}
        self.og = self.overlap_gid
        self.g = self.groups
        self.total_elem = total_elem
        self.grouped_elem_count = 0 # the number of functions that owns groups
        self._g_count = 0
        self.has_list = False
        self._list = None # a function name list
        self.added_groups = {} # appendix functions the around the group
        self.ag = self.added_groups
    def __str__(self):
        return str([self.g[key] for key in self.g])
    __repr__ = __str__
    def add(self, elem_id1, elem_id2, is_symbol_1=False, is_symbol_2=False):
        i1, i2 = elem_id1, elem_id2
        if is_symbol_1:
            bak_ig1 = self.ig[i1]
        if is_symbol_2:
            bak_ig2 = self.ig[i2]
        if self.ig[i1] == -1:
            if self.ig[i2] == -1:
                target_group = list(set([i1, i2]))
                self.g.update({self._g_count:target_group})
                self.ig[i1] = self._g_count
                self.ig[i2] = self._g_count
                self._g_count += 1
                self.grouped_elem_count += 2
            else:
                target_group = self.g[self.ig[i2]]
                target_group.append(i1)
                self.ig[i1] = self.ig[i2]
                self.grouped_elem_count += 1
        else:
            target_group = self.g[self.ig[i1]]
            if self.ig[i2] == -1:

                target_group.append(i2)
                self.ig[i2] = self.ig[i1]
                self.grouped_elem_count += 1
            elif self.ig[i1] != self.ig[i2]:
                target_group.extend(self.g[self.ig[i2]])
                self.remove_group(self.ig[i2], self.ig[i1])
            else:
                pass
        if is_symbol_1:
            self.ig[i1] = bak_ig1
        if is_symbol_2:
            self.ig[i2] = bak_ig2
    def add_overlap(self, elem_id1, elem_id2):
        i1, i2 = elem_id1, elem_id2
        if i1 not in self.og:
            if i2 not in self.og:
                target_group = [i1, i2]
                self.g.update({self._g_count:target_group})
                self.og[i1] = [self._g_count]
                self.og[i2] = [self._g_count]
                self._g_count += 1
                self.grouped_elem_count += 2
            else:
                self.og[i1] = []
                for g_id in self.og[i2]:
                    self.g[g_id].append(i1)
                    self.og[i1].append(g_id)
                    self.grouped_elem_count += 1
        else: 
            if i2 not in self.og:
                self.og[i2] = []
                for g_id in self.og[i1]:
                    self.g[g_id].append(i2)
                    self.og[i2].append(g_id)
                    self.grouped_elem_count += 1
            else:
                for g_id in self.og[i1]:
                    if i2 not in self.g[g_id]:
                        self.g[g_id].append(i2)
                        self.og[i2].append(g_id)
                        self.grouped_elem_count += 1
                for g_id in self.og[i2]:
                    if i1 not in self.g[g_id]:
                        self.g[g_id].append(i1)
                        self.og[i1].append(g_id)
                        self.grouped_elem_count += 1
    def ag_add(self, key_id:int, group_list:list):
        self.ag[key_id] = group_list
    def remove_group(self, rm_group_id, new_group_id=-1):
        rg = self.g.pop(rm_group_id)
        for idx in rg:
            self.ig[idx] = new_group_id
        if new_group_id == -1:
            self.grouped_elem_count -= len(rg)
    def feed(self, elem_list):
        self._list = elem_list
        self.has_list = True
    def readable_show(self, gid = None, _show_group=0):
        if _show_group:
            if gid != None:
                print([self._list[e_id] for e_id in self.ag[gid]])
            else:
                for g in list(map(lambda gp: [self._list[e_id] for e_id in gp], [self.ag[key] for key in self.ag])):
                    print(g)
        else:
            if gid != None:
                print([self._list[e_id] for e_id in self.g[gid]])
            else:
                for g in list(map(lambda gp: [self._list[e_id] for e_id in gp], [self.g[key] for key in self.g])):
                    print(g)
    def gids(self):
        return self.groups.keys()

class Grouper_Overlap(): # allowing overlap
    def __init__(self, total_elem:int):
        self.groups = {}
        self.grouped_id = [-1 for _ in range(total_elem)]
        self.ig = self.grouped_id 
        self.overlap_gid = {} 
        self.og = self.overlap_gid
        self.g = self.groups
        self.total_elem = total_elem
        self.grouped_elem_count = 0
        self.cur_group = -1
        self._g_count = 0
        self.has_list = False
        self._list = None
        self.added_groups = {}
        self.ag = self.added_groups
    def __str__(self):
        return str([self.g[key] for key in self.g])
    __repr__ = __str__
    def add(self, elem_id1, elem_id2, is_symbol_1=False, is_symbol_2=False):
        i1, i2 = elem_id1, elem_id2
        if i1 not in self.og:
            if i2 not in self.og:
                target_group = [i1, i2]
                self.g.update({self._g_count:target_group})
                self.og[i1] = [self._g_count]
                self.og[i2] = [self._g_count]
                self._g_count += 1
                self.grouped_elem_count += 2
            else:
                self.og[i1] = []
                for g_id in self.og[i2]:
                    self.g[g_id].append(i1)
                    self.og[i1].append(g_id)
                    self.grouped_elem_count += 1
        else:
            if i2 not in self.og:
                self.og[i2] = []
                for g_id in self.og[i1]:
                    self.g[g_id].append(i2)
                    self.og[i2].append(g_id)
                    self.grouped_elem_count += 1
            else:
                for g_id in self.og[i1]:
                    if i2 not in self.g[g_id]:
                        self.g[g_id].append(i2)
                        self.og[i2].append(g_id)
                        self.grouped_elem_count += 1
                for g_id in self.og[i2]:
                    if i1 not in self.g[g_id]:
                        self.g[g_id].append(i1)
                        self.og[i1].append(g_id)
                        self.grouped_elem_count += 1
    def add_overlap(self, elem_id1, elem_id2 = None):
        i1, i2 = elem_id1, elem_id2
        if self.cur_group == -1:
            print("add_overlap not avaliable")
            return
        if i1 not in self.g[self.cur_group]:
            self.g[self.cur_group].append(i1)
            if i1 not in self.og:
                self.og[i1] = [self.cur_group]
            else:
                self.og[i1].append(self.cur_group)
        if i2 == None:
            return
        if i2 not in self.g[self.cur_group]:
            self.g[self.cur_group].append(i2)
            if i2 not in self.og:
                self.og[i2] = [self.cur_group]
            else:
                self.og[i2].append(self.cur_group)
    def ag_add(self, key_id:int, group_list:list):
        # FIXME: 
        self.ag[key_id] = group_list
    def remove_group(self, rm_group_id, new_group_id=-1):
        rg = self.g.pop(rm_group_id)
        for idx in rg:
            self.ig[idx] = new_group_id
        if new_group_id == -1:
            self.grouped_elem_count -= len(rg)
    def feed(self, elem_list):
        self._list = elem_list
        self.has_list = True
    def readable_show(self, gid = None, _show_group=0):
        if _show_group:
            if gid != None:
                print([self._list[e_id] for e_id in self.ag[gid]])
            else:
                for g in list(map(lambda gp: [self._list[e_id] for e_id in gp], [self.ag[key] for key in self.ag])):
                    print(g)
        else: 
            if gid != None:
                print([self._list[e_id] for e_id in self.g[gid]])
            else:
                for g in list(map(lambda gp: [self._list[e_id] for e_id in gp], [self.g[key] for key in self.g])):
                    print(g)
    def new_group(self):
        self.cur_group = self._g_count
        self.g[self.cur_group] = []
        self._g_count += 1
    def done_new_group(self):
        self.cur_group = -1
    def gids(self):
        return self.groups.keys()
    def has_new(self):
        return self.cur_group != -1

class SRC_Grouper():
    def __init__(self):
        self.groups = {}
        self.func_to_gid_dict = {}
        self.func_to_project_dict = {}
        self.group_to_file = {}
        self.project_record = [] 
        self.default_project = None
        self.gid = None
        self.cur_dir = None
        self.cur_dir_file = None
        self.cur_dir_gid = None
        self.group_count = 0
        self.g = self.groups
    def set_project(self, project):
        assert isinstance(project, str)
        self.default_project = project
        if project not in self.project_record:
            self.project_record.append(project)
    def new_group(self, file_name):
        _path, _file = os.path.split(os.path.abspath(file_name))
        # Step 1: check if there is any file in the same dir
        if _path == self.cur_dir:
            pass
        else:
            self.cur_dir = _path
            self.cur_dir_file = []
            self.cur_dir_gid = []
            for gid in self.gids():
                if os.path.split(self.group_to_file[gid]) == _path:
                    self.cur_dir_file.append(self.group_to_file[gid])
                    self.cur_dir_gid.append(gid)
        # Step 2: set group 
        _module_name, _ext = os.path.splitext(os.path.abspath(file_name))
        for i in range(len(self.cur_dir_file)):
            # if the .c or .h file has already seem,
            # using old group
            f = self.cur_dir_file[i]
            if f == _module_name:
                self.gid = self.cur_dir_gid[i]
                break
        else:
            # create new group
            self.gid = self.group_count
            self.group_count += 1
            self.groups[self.gid] = []
            self.group_to_file[self.gid] = _module_name
            self.cur_dir_file.append(_module_name)
            self.cur_dir_gid.append(self.gid)
    def add(self, func_name):
        assert isinstance(func_name, str)
        # current group add this function
        self.groups[self.gid].append(func_name)
        # function add the group id, and record the project
        if func_name in self.func_to_gid_dict:
            self.func_to_gid_dict[func_name].append(self.gid)
            self.func_to_project_dict[func_name].append(self.default_project)
        else:
            self.func_to_gid_dict[func_name] = [self.gid]
            self.func_to_project_dict[func_name] = [self.default_project]
    def get_item(self, func_name, project=None):
        if func_name in self.func_to_gid_dict:
            gid_pre_fetch = self.func_to_gid_dict[func_name]
            project_list = self.func_to_project_dict[func_name]
        else:
            return []
        if project == None:
            project = self.default_project
        result =[]
        for i in range(len(gid_pre_fetch)):
            if project_list[i] == project:
                result.append(gid_pre_fetch[i])
        return result
    def __getitem__(self, func_name):
        return self.get_item(func_name, self.default_project)
    def gids(self):
        return self.groups.keys()
    def funcs(self):
        return self.func_to_gid_dict.keys()
