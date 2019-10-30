'''
Edit Json file associated with AHF system
'''
import json 
dic_main={0:'HeadFixer',1:'Rewarder',2:'Stimulator'}  
dic_headFixer={0:'headFixTime', 1: 'propHeadFix',2:'tightnessHeadFix'}
dic_rewarder={1:'breakBeamDelay',2:'breakBeamSize',3:'entryDelay',4:'entrySize',
              5:'lastBreakBeamTime',6:'lastEntryTime',7:'maxBreakBeamRewards',
              8:'maxEntryRewards',9:'taskSize',10:'totalBreakBeamRewardsToday',11:'totalEntryRewardsToday'}
dic_stimulator={0:'delayTime',1:'lickWithholdTime',2:'mouseLevel',3:'nRewards',4:'responseTime',5:'rewardInterval',6:'rewardNoGo'}
m1=None 
m2=None
m3=None
m4=None
with open("AHF_mice_subjects.jsn", 'r') as f:
    a=f.read()
    b=a.replace('\n',',')
    c=json.loads(b.replace('=',':'))
    
def main():
    try:
        display_mice()
        for i,y in mouse_dic.items():
            print(i,y)
        Tag=input('Choose animal to edit or return to edit all:')
        if Tag != '':
            edit_mouse(int(Tag))
        else:
            for key, values in dic_main.items():
                print (key, values)
            manuel_edit_all()
    except KeyboardInterrupt: 
        loop_manuel()
def display_mice():
    global mouse_dic
    mouse_dic={}
    mouse=[]
    for i in c:
        mouse.append(i)
    for i, y in enumerate(mouse):
        mouse_dic[i]=y
def edit_mouse(Tag):
    for key, values in dic_main.items():
        print (key, values)
    manuel1=input('Chose parameter to edit:')
    if int(manuel1) ==0:
        a=dic_headFixer
    elif int(manuel1)==1:
        a=dic_rewarder
    elif int(manuel1) ==2:
        a=dic_stimulator
    dic_edit=c[mouse_dic[Tag]][dic_main[int(manuel1)]]
    for i,z in zip(dic_edit,range(len(dic_edit))):
        print(z,i)
    manuel2= input('Chose parameter to edit:')
    manuel3 = input('Values to change to (currently: %s)' % dic_edit[a[int(manuel2)]])
    if manuel3 != '':
        c[mouse_dic[Tag]][dic_main[int(manuel1)]][a[int(manuel2)]]= eval(type(dic_edit[a[int(manuel2)]]).__name__+'('+str(manuel3)+')')
        save_reload()
        loop_manuel()
    else:
        loop_manuel()
def manuel_edit_all():
    global m1, m2, m3,c
    m1=input('Choose class to alter or any key to return: ')
    if m1 == '0':
        for key, values in dic_headFixer.items():
            print(key, values)
        User_input()
        for i in c:
            c[i]['HeadFixer'][dic_headFixer[int(m2)]] =eval(type(c[i]['HeadFixer'][dic_headFixer[int(m2)]]).__name__+'('+str(m3)+')')
        save_reload()
        loop_manuel()
    elif m1 =='1':
        for key, values in dic_rewarder.items():
            print(key, values)
        User_input()
        for i in c:
            c[i]['Rewarder'][dic_rewarder[int(m2)]] =eval(type(c[i]['Rewarder'][dic_rewarder[int(m2)]]).__name__+'('+str(m3)+')')
        save_reload()
        loop_manuel()
    elif m1 =='2':
        for key, values in dic_stimulator.items():
            print(key, values)
        User_input()
        for i in c:
            c[i]['Stimulator'][dic_stimulator[int(m2)]] =eval(type(c[i]['Stimulator'][dic_stimulator[int(m2)]]).__name__+'('+str(m3)+')')
        save_reload()
        loop_manuel()
    else:
        main()
def User_input(): 
    global a,m2, m3
    a=''
    m2=input('Enter settings to change: ')
    if m1 == '0':
        a=eval(type(c['1']['HeadFixer'][dic_headFixer[int(m2)]]).__name__)
    elif m1 =='1':
        a=eval(type(c['1']['Rewarder'][dic_rewarder[int(m2)]]))
    elif m1 =='2':
        a=eval(type(c['1']['Stimulator'][dic_stimulator[int(m2)]]).__name__)
    m3=input('Value to change to  ' +str(a)+' :')
    return m2, m3 
def save_reload():
    global c
    c2=json.dumps(c)
    c2=c2.replace(':','=')
    c2=c2.replace(',','\n')
    with open('AHF_mice_subjects.jsn','w') as f2:
        f2.write(c2)
    with open("AHF_mice_subjects.jsn", 'r') as f:
        a=f.read()
        b=a.replace('\n',',')
        c=json.loads(b.replace('=',':'))
def loop_manuel():
    global m4 
    m4=input('Edit additional settings (Yes) or press any to exit:')
    if m4.lower()=='yes' or m4.lower()=='y':
        main()
    else: 
        return 
if __name__ == "__main__":
    main()        
      
        
        




