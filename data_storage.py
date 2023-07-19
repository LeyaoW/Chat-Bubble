from ds_messenger import *
from pathlib import Path
#p = Path('/Users/laurawang/Desktop/UCI/2022Winter/ICS32/lecture/final_project/final_project/lll.dsu')
#ds_messager= DirectMessenger('168.235.86.101', 'Daddy', '123')
# dm.send('Hi', 'wobuzhidao')
def get_all_history(ds_messager):
    lst = ds_messager.retrieve_all()

    #print(lst)

    hist = {}
    temp_lst = []
    for i in lst:
        set = [i.sender, i]
        temp_lst.append(set)
    for p in range(len(temp_lst)):
        if temp_lst[p][0] in hist.keys():
            hist[temp_lst[p][0]].append(temp_lst[p][1])
        else:
            hist[temp_lst[p][0]] = [temp_lst[p][1]]

    print(hist.keys())

    return hist


'''
def add_retrived_history(hist,my_name)->None:
    'add objects of DirectMessage into the dsu file'
    for i in hist:
        p=Path('.').joinpath(i+'.dsu')
        print(p)
        try:
            if p.exists():
            #if p.exists() and i.sender == my_name:

                for dm in hist[i]:
                    dm.save(p)
            
        except:
            pass

'''

def add_retrived_history(hist, my_name) -> None:
    'add objects of DirectMessage into the dsu file'
    try:
        for i in hist:
            p = Path('.').joinpath(i + '.dsu')
            print(p)
            if not p.exists():
                p.touch()
            for dm in hist[i]:
                dm.save(p)

    except:
        pass

#hist=get_all_history(ds_messager)
#dd_retirved_history(hist, "Somebody")





