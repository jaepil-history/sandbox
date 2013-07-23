import  json, codecs, pymssql

f =codecs.open("D:\Workspace\python\DB_work\Item_purchase_20121213-20130111.csv", 'r','utf16')
conn = pymssql.connect(host='192.168.0.242', user='taejun', password='ahn1004', database='kilroy_game',charset='utf8') #@UndefinedVariable
cur = conn.cursor()

cnt = 0
while 1:
    #try:
        line = f.readline()
        if 'CHARGE_NO' in line :
            print '============================= Cash item ====================================='
        
        elif 'NEW_SKILL_POINT' in line :
            print ' ============================== Skill Purchase ==============================' 
    
        else :
        
            if not line : break
        
            line = line.replace('"','')
            list = line.split(',')
            
     
            raw = list[7].split('[PLAYER_NICK')
                    
            #print raw[0] +',' + list[1]
            #break
        
            
                
            
            action_describe = raw[0].replace('][','\",\"')
            action_describe = action_describe.replace(':','-')
            action_describe = action_describe.replace('=','\":\"')
            action_describe = action_describe.replace('[','{\"')
            action_describe = action_describe.replace(']','\"}')
    
            try:  
            #print action_describe
                data=json.loads(action_describe)
            
                hexitem = int(data['ITEM_NO'] , 16)
                q1 = 'insert into TJ_ITEM_PURCHASE values ( ' + '%d' %hexitem + ',' + '\'' +  list[1] + '\'' + ')'
                
                print '%d' %cnt 
                cur.execute(q1) 
                conn.commit()
                cnt = cnt + 1
                
                             
                        
            except ValueError, x:
                print 'value', x, 'undefined'
                print list 
                print '\n'
                print '%d' %cnt + ',' + action_describe
                break
          
        
f.close()