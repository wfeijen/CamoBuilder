#%%

from typing import List

def func(ls: List[str] = []) -> List[str]:
    ls.append('pie')
    return ls

print(func())  # ['pie']
print(func())  # ['pie', 'pie']
print(func())  # ['pie', 'pie', 'pie']

# %%
