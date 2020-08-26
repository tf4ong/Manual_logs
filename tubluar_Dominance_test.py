'''
Tubluar dominance test data collection script
'''

from RFIDTagReader import TagReader
import itertools
import os
import datetime as dt
import pymysql
RFID_serialPort = '/dev/tty.usbserial-A60243NK'
#RFID_serialPort = '/dev/serial0'
#RFID_serialPort='/dev/cu.usbserial-AL00ES9A'
RFID_kind = 'ID'
RFID_timeout = None
RFID_doCheckSum = True
insert_statment='INSERT INTO Social_Dominance (Timestap, Cage, Rank_1, Rank_2,Rank_3,Rank_4) VALUES(%s,%s,%s,%s,%s,%s)'
try:
    tagReader = TagReader (RFID_serialPort, RFID_doCheckSum, timeOutSecs = RFID_timeout, kind=RFID_kind)
except Exception as e:
    raise e
list_compared=[]
def get_tag():
    tag= None
    while tag is None:
        try:
            tag = tagReader.readTag ()
            return tag
            print(tag)
        except ValueError as e:
            print (str (e))
            tagReader.clearBuffer()
            print('Error detected(above), try again')
def store_compared_tag():
    print('Waiting for Tags')
    a=get_tag()
    print('Tag 1 read! ID:'+str(a))
    b=get_tag()
    print('Tag 2 read! ID:'+str(b))
    temp_dic={'1':a,'2':b}
    return temp_dic
def compare_mice():
    global list_compared
    a=store_compared_tag()
    while (a['1'] == a['2']) or tuple(sorted((a['1'],a['2']))) in list_compared:
        print('Same Tag read twice or pairs already compared, Try again')
        a=store_compared_tag()
    else:
        print('Mice to be compared:')
        for key, values in a.items():
            print(key,values)
        list_compared.append(tuple(sorted((a['1'],a['2']))))
        dominance= input('Which mouse is dominant?')
    score_dict[str(a[dominance])]=score_dict[str(a[dominance])]+1
def rank_mice():
    global ranked_dic
    ranked_dic={}
    ranked={key: rank for rank, key in enumerate(sorted(score_dict,key=score_dict.get,reverse=True),1)}
    ranked_dic[dt.datetime.now().strftime("%Y-%m-%d")]=ranked
    return ranked_dic
def csv_save():
    record_filename_csv=os.getcwd()+'/Dominance/'+cage+'_Dominance_test'+'.csv'
    record_filename_txt=os.getcwd()+'/Dominance/'+cage+'_Dominance_test'+'.txt'
    dic_loc=dt.datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists('Dominance'):
        print('Creating data dictionary: %s','Dominance/')
        os.mkdir('Dominance/')
    if os.path.exists(record_filename_csv)==False:
        with open(record_filename_csv,'a') as file:
            file.write('Timestamp, Mouse_1, Mouse_2, Mouse_3, Mouse_4')
            file.write('\n')
            file.write(dic_loc)
            for i in sorted(ranked_dic[dic_loc],key=ranked_dic[dic_loc].get):
                file.write(','+str(i))
            file.write('\n')
        with open('Dominance/'+cage+'_Dominance_test.txt','w') as file2:
            file2.write(dic_loc+':')
            for i in score_dict:
                file2.write(str(i)+score_dict[i]+'     ') 
            file2.write('\n')
    else:
        with open(record_filename_txt,'a') as file:
                        file.write(dic_loc)
                        for i in sorted(ranked_dic[dic_loc],key=ranked_dic[dic_loc].get):
                            file.write(','+str(i))
                        file.write('\n')      
def save_db():
    dic_loc=dt.datetime.now().strftime("%Y-%m-%d")
    db1=pymysql.connect(host=HOST, user=USER, db=DATABASE,password=PASSWD,autocommit=True)
    cur1=db1.cursor()
    values=[dic_loc,cage]
    for i in sorted(ranked_dic[dic_loc],key=ranked_dic[dic_loc].get):
        values .append(i)
    if len(values)<5:
        values.append('NA')
    cur1.execute(insert_statment,values)
def save_new_subjects():
    nReads=input('How many mice to compare in dominance test?')
    cage=input('CageID:')
    record_filename=os.getcwd()+'/Dominance/'+cage+'_Dominance_test'+'.txt'
    print ('Waiting for tags...')
    i = 0
    listm=[]
    tag=12
    while i < int(nReads) :
        tag=get_tag()
        print(tag)
        while tag not in listm:
            listm.append(tag)
            i+=1
        else:
            pass
    else:
        print(listm)
    with open(record_filename,'w') as f:
        for i in listm:
            f.writelines("%s\n" %i)
        f.writelines('History:\n')
    print ('Saved all {:d} tags'.format (int(nReads)))
def open_load_subjects(cage):
    global score_dict, list_compare
    record_filename=os.getcwd()+'/Dominance/'+cage+'_Dominance_test'+'.txt'
    listm=[]
    score_dict={}
    with open(record_filename,'r') as f:
        for line in f:
            if line != 'History:\n':
                listm.append(int(line.strip('\n')))
            else:
                break
    listm=sorted(listm)
    for i in listm:
        score_dict[str(i)]=0
    list_compare=list(itertools.combinations(listm,2))   
if __name__=='__main__':
    save_db=input('Save to a remote database? (Y/N)')
    if save_db.lower() =='y':
        HOST=input('Enter host database IP:')
        USER=input('Enter user associated:')
        DATABASE=input('Enter database to access:')
        PASSWD=input('Enter password:')
    else:
        pass
    try:
        cage=input('Enter cage to compare:')
        open_load_subjects(cage)
    except :
        print('no corresponding cage configs data' )
        save_new_subjects()
        print('Cage added')
        cage=input('Enter cage to compare:')
        open_load_subjects(cage)    
    while list(set(list_compare)-set(list_compared)) !=[]:
        for i in list(set(list_compare)-set(list_compared)):
            print('Pairs left to compare:'+str(i))
        print('Please scan mice')
        compare_mice()
    else:
        rank_mice()
        csv_save()
        if save_db.lower()=='y':
            save_db()
        else: 
            pass
        print('All pairs compared')




