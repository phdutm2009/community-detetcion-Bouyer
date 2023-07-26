#!/usr/bin/env python
# coding: utf-8

# In[22]:


from numpy import loadtxt
import time


# In[23]:


#khandane file e liste hamsayegiha
dataset_name = 'Neighboring_List'
with open("./datasets/LFR/500000/0.1/"+dataset_name+".txt") as c:
    arrr = list(map(str.split, c))
    
dataset=[]    
for i in range((len(arrr))):
    dataset.append([])

for i in range(len(arrr)):
    for j in range(len(arrr[i])):
        dataset[i].append(int(arrr[i][j]))
        
#print("liste hamsayegiha(dataset):",dataset)


# In[24]:


#MARHALE 2 tabe 
def find_main_node(first_node):
    # ta 3 gam be samte bishtarin daraje az hamsayegane gerehe feli pish boro
    # darajeye gereh haye entekhab shode ra list kon
    # max ra az list entekhab kon
    mylist=[]
    mylist.append([first_node,len(dataset[first_node])]) #first node

    #gam1
    a1=[]
    for i in range(len(dataset[first_node])):
        a1.append([dataset[first_node][i],len(dataset[dataset[first_node][i]])])
    mylist.append(max(a1, key=lambda x: x[1]))

    #gam2
    a2=[]
    for i in range(len(dataset[mylist[1][0]])):
        a2.append([dataset[mylist[1][0]][i],len(dataset[dataset[mylist[1][0]][i]])])
            
    if (max(a2, key=lambda x: x[1])[0] not in list_of_mains): #agar qablan pakhsh konande nabashad ya #agar gerehe game 2 label nadashte bashad
        mylist.append(max(a2, key=lambda x: x[1]))  
 
        #gam3
        a3=[]
        for i in range(len(dataset[mylist[2][0]])):
            a3.append([dataset[mylist[2][0]][i],len(dataset[dataset[mylist[2][0]][i]])])
    
        if (max(a3, key=lambda x: x[1])[0] not in list_of_mains): #agar qablan pakhsh konande nabashad
            mylist.append(max(a3, key=lambda x: x[1]))
############################################################################################################
    #entekhabe max
    #print("first node and steps nodes and their degrees :" , mylist)
    main_node=max(mylist, key=lambda x: x[1])[0]
    #print("main node is :" , main_node )
    #print ("\n")
    return main_node


# In[25]:


#tabe find max value from a list of lists:
def max_value(inputlist):
    return max([sublist[-1] for sublist in inputlist])


# In[26]:


#MARHALE3 TABE
def set_labels(main_node):
    global lbl  
    global moratabshode_sorensen
    global sorensen
    global m
    global ii
    global max_labels
    global liste_tedade_labelhaa
    
    if len(MEMORY[main_node]) != 0:
        if len(MEMORY[main_node])>1: #agar bishtaraz yek label dashte bashad:
            #baiad tedade label hara beshmarim:
            liste_tedade_labelhaa=[]
            faqat_tedadha=[]
            uniks=[]
            max_labels=[]    
            for j in MEMORY[main_node]:
                if j in uniks: 
                    liste_tedade_labelhaa[uniks.index(j)][1]+=1 
                    faqat_tedadha[uniks.index(j)]+=1 
                else:
                    liste_tedade_labelhaa.append([j,1])
                    faqat_tedadha.append(1)
                    uniks.append(j)
            #labelhayi ke bishtarin tedad ra darand miyabim:
            maxx=max_value(liste_tedade_labelhaa)   #max count of labels
            #baresi mikonim ke aya labele digari ham hast ke be hamin tedad bashad:
            pp=0
            for p in faqat_tedadha:
                if p==maxx :
                    #moshakhas kardane label hayi ke bishtarin tedad ra darand:       
                    max_labels.append(liste_tedade_labelhaa[pp][0])
                pp=pp+1
            #print("max_labels",max_labels)
            if (len(max_labels))>1: #agar tedade barchasb ha barabar bashand:
                #az sorens estefade mikonim:
                sorensen=[]
                for ii in range(len(dataset[main_node])):
                    sorensen.append([])
                    
                seet=set(dataset[main_node])
                ppp=0
                for ii in dataset[main_node]: #hamsayegane main_node
                    #formul:
                    common=list(seet.intersection(dataset[ii]))
                    sorensen[ppp]=[((2*len(common))/(len(dataset[main_node])+len(dataset[ii])))]
                    ppp=ppp+1
                #print("sorensen:",sorensen)
                moratabshode_sorensen=[]
                for ii in range(len(max_labels)):
                    moratabshode_sorensen.append([0])
                    
                op=0
                for ii in dataset[main_node]:#hamsayeha
                    for n in MEMORY[ii]: #labele hamsayeha
                        for m in range(len(max_labels)):
                            if n==max_labels[m]:
                                moratabshode_sorensen[m][0]= moratabshode_sorensen[m][0]+sorensen[op][0]
                    op=op+1
                #print("memory before:",MEMORY[main_node])
                #print("max_labels",max_labels)
                #print("moratabshode_sorensen:",moratabshode_sorensen)
                lliisstt=[]
                for ii in range(len(moratabshode_sorensen)):
                    lliisstt.append(moratabshode_sorensen[ii][0])  
                MEMORY[main_node]=[max_labels[lliisstt.index(max(lliisstt))]] 
                #print("memory after:",MEMORY[main_node])

        for x in dataset[main_node]:
            if x not in list_of_mains:  # agar in hamsaye qablan pakhsh konande nabashad,labele jadid begirad
                #print("before",x,MEMORY[x])
                MEMORY[x].append(MEMORY[main_node][0])
                #print("after",x,MEMORY[x])
 

    if len(MEMORY[main_node]) == 0:
        MEMORY[main_node].append(lbl)
        for x in dataset[main_node]:     #x hamsaye sathe 1 ast
            if x not in list_of_mains:  # agar in hamsaye qablan pakhsh konande nabashad,labele jadid begirad
                MEMORY[x].append(lbl)
        lbl=lbl+1


# In[27]:


#KOLLI, estefade az tamame marahel
run_time= time.time()
list_of_mains=[]
#MEMORY, label haye har node ra zakhire mikonad
MEMORY = []
for p in range(len(dataset)):
    MEMORY.append([])
#print("MEMORY IS(3):",MEMORY)
#print('\n')
lbl=0

for tekrar in range(2):
    #satr(gereh) hara baresi mikonim.agar satri(gerehi) bedune label bashad(tule liste an gereh 0 bashad)
    for empty_node in list(range(len(dataset))):
       # print("empty_node:",empty_node+1)
        if len(dataset[empty_node])!=1:  #agar gereh daraje 1 nabashad, baresi ra anjam bede
            if len(MEMORY[empty_node]) == 0 :
                #print("no_labeled node is:" ,empty_node)
                #print ("\n")
                #mohemtarin hamsaye ash ra miyabim
                ooo=dataset[empty_node]
                max_degree_node=[]
                for i in range(len(ooo)):
                    max_degree_node.append([])
                    max_degree_node[i].append(ooo[i])
                    max_degree_node[i].append(len(dataset[ooo[i]]))
                max_degree_node=max(max_degree_node, key=lambda x: x[1])
    
                important_neighbor=max_degree_node[0]
                #baresi mikonim agar mohemtarin hamsayeash barchasb dashte bashad, barchasbe an ra be gerehe bedune barchashb midahim
                if len(MEMORY[important_neighbor]) != 0 :
                   # print("important_neighbor",important_neighbor+1)
                    MEMORY[empty_node]=MEMORY[important_neighbor] 
             #       print("MEMORY IS(4):",MEMORY)
             #       print('\n')
                #agar mohem tarin hamsaye barchasb nadashte bashad, be marhale 2 barmigardim ta gerehe asliash ra biabim
                if len(MEMORY[important_neighbor]) == 0 :
                    #print("important neighbor of no_labeled node, doesnt have label so we should find no_labeled node's main node")
                    #print ("\n")
                    main_node= find_main_node(empty_node)
                    list_of_mains.append(main_node)
                    #va be marhale 3 miayim ta barchasb dahim
                    set_labels(main_node) 

            
print("...run time: % seconds..." % (time.time() - run_time) ) 


# In[28]:


#label dehi be gereh haye darajeye 1:(baiad labele hamsayeshan ra begirand)
run_time= time.time()

for i in range(len(dataset)):
    if len(dataset[i]) == 1 :  
        for j in range(len(MEMORY[dataset[i][0]])):
            MEMORY[i].append(MEMORY[dataset[i][0]][j])
          #  print("MEMORY IS(5):",MEMORY)
            
print("...run time: % seconds..." % (time.time() - run_time) ) 


# In[29]:


#marhaleye tayin taklife node haye daraye chand label va hazfe label haye ezafi:
run_time= time.time()
#print old memory
#print("my labels are (old memory):",MEMORY)  

#baiad tedade label hara dar har gereh beshmarim:
liste_tedade_labelha=[]
faqat_tedadha=[]
new_labels=[]
for i in range(len(MEMORY)):
    liste_tedade_labelha.append([])
    faqat_tedadha.append([])
    new_labels.append([])
for i in range(len(MEMORY)):
    uniks=[]
    for j in MEMORY[i]:
        if j in uniks: 
            liste_tedade_labelha[i][uniks.index(j)][1]+=1 
            faqat_tedadha[i][uniks.index(j)]+=1 
        else:
            liste_tedade_labelha[i].append([j,1])
            faqat_tedadha[i].append(1)
            uniks.append(j)
#print("liste_tedade_labelha:",liste_tedade_labelha)

    #labelhayi ke bishtarin tedad ra darand miyabim:
    maxx=max_value(liste_tedade_labelha[i])   #max count of labels
    #baresi mikonim ke aya labele digari ham hast ke be hamin tedad bashad:
    pp=0
    for p in faqat_tedadha[i]:
        if p==maxx :
            #moshakhas kardane label hayi ke bishtarin tedad ra darand:       
            new_labels[i].append(liste_tedade_labelha[i][pp][0])
      #      print("change is:",new_labels)
      #      print('\n')
        pp=pp+1
        
#print new memory
MEMORY=new_labels
#print("my labels are (new memory)(6):",MEMORY)  
print("...run time: % seconds..." % (time.time() - run_time) ) 


# In[30]:


#marhaleye dekhalat dadane labele hamsayeha:
run_time= time.time()
#be tartibe KAHESHE daraje, gereh hara baresi mikonim:
liste_darajat=[]
 
for ah in range(3):
    new_labelss=[]
    for i in range(len(MEMORY)):
        new_labelss.append([])
    for i in range(len(dataset)): #in gereh 
        #print(i)
        uniks=[]
        labelhaye_hamsayegane_yekgereh=[]
        faqat_tedadha=[]
        #label haye hamsayegane in gereh ra yekja jam mikonim:
        for j in range(len(dataset[i])):  #hamsayeye in gereh
            #print("hamsayeha:",j)
            for p in MEMORY[dataset[i][j]]: #labele hamsayeye in gereh
                #print("labele hamsaye",p)
                if p in uniks: 
                    labelhaye_hamsayegane_yekgereh[uniks.index(p)][1]+=1 
                    faqat_tedadha[uniks.index(p)]+=1 
                else:
                    labelhaye_hamsayegane_yekgereh.append([p,1])
                    faqat_tedadha.append(1) 
                    uniks.append(p)
        #print("labelhaye_hamsayegane_yekgereh:",labelhaye_hamsayegane_yekgereh)

        #labelhayi ke bishtarin tedad ra darand miyabim:
        maxx=max_value(labelhaye_hamsayegane_yekgereh)   #max count of labels

        #baresi mikonim ke aya labele digari ham hast ke be hamin tedad bashad:
        pp=0
        for p in faqat_tedadha:
            if p==maxx :
                #moshakhas kardane label hayi ke bishtarin tedad ra darand:       
                new_labelss[i].append(labelhaye_hamsayegane_yekgereh[pp][0])
       #         print("change is:",new_labels)
       #         print('\n')
            pp=pp+1
    #print new memory
    MEMORY=new_labelss
#############################################################################################################################

for i in range(len(MEMORY)):
    if len(MEMORY[i])>1:    #agar gerehi bish az chand label dasht, labeli ba bishtarin hamsaye moshtaak entekhab mishavad
        liste_coommonha=[] #hamsaye haye moshtarak ra negah midarad
        
        sett=set(dataset[i])
        ppp=0
        for x in dataset[i]: #hamsayegane i
            coommon=list(sett.intersection(dataset[x]))
            if len(coommon)>1:
                for xx in range(len(coommon)):
                    liste_coommonha.append(coommon[xx])
            ppp=ppp+1
        #hala baiad labele in hamsaye haye moshtarak ra yeja jam konim:
        listee_labeelha=[]
        uuniks=[]
        for x in liste_coommonha:
            for xx in MEMORY[x]:
                listee_labeelha.append(xx)
                if xx not in uuniks:
                    uuniks.append(xx)
        #hala baiad bebinim tedade kodam label bishtar ast:
        moratab_shode=[]
        for x in uniks:
            moratab_shode.append([x,listee_labeelha.count(x)])
        #hala baiad labele ba tedade bishtar ra entekhab konim va jaygozine label haye qabli konim:
        llliisstt=[]
        for x in range(len(moratab_shode)):
            llliisstt.append(moratab_shode[x][1])
        #maxe llliisstt ra peida mikonim..agar llliisstt faqat 1 ta dakhelash an tedade max ra dasht,label ra jaygozin mikonim
        ccount=0
        for x in range(len(moratab_shode)):
            if moratab_shode[x][1]==max(llliisstt):
                ccount=ccount+1
        if ccount==1:
            MEMORY[i]=[moratab_shode[llliisstt.index(max(llliisstt))][0]]
            
        
print("akharin memory:",MEMORY)
print("...run time: % seconds..." % (time.time() - run_time) ) 


# In[31]:


#eshkal yabi:
#mohasebeye tedade gereh hayi ke label nagerefteand:
tedad=0
for i in range(len(MEMORY)):
    if MEMORY[i]==[]:
        tedad=tedad+1
print(tedad)


# In[32]:


#MARHALE4:
#ijade liste javame e overlap e man:
print("tedad javameyi ke tashkhis dadam:",lbl)
com=[]
for i in range(lbl):
    com.append([])

for i in range(len(MEMORY)): #HAR GEREH
        for j in MEMORY[i]: #LABEL HAYE HAR GEREH
            com[j].append(i)

#hazfe tekrari ha                
for i in range(len(com)):
    com[i]=list(set(com[i]))  
    
#print(" list of my overlap communities:" , com)        


# In[33]:


'''
#pish pardazeshe edqam
#MIX(emale sharte miangine size va yaftane javame kujak va mohasebeye [hamsaye,tedade yalhaye beyne 2 jamee])(bekhatere edqam)
run_time= time.time()
tedade_yalhaye_beyne_javame=[]
majmue_sizeha=0
small_coms=[]
just_number_of_small_coms=[]

#miangin yabi:
temp=[]#faqat size ha dakhelesh hast
for c in range(len(com)):
    temp.append(len(com[c]))
    majmue_sizeha=majmue_sizeha+len(com[c]) 
majmue_sizeha=majmue_sizeha-max(temp)
miangine_sizeha=majmue_sizeha/(len(com)-1)

#yaftane javame kuchak:
i=0
for c in range(len(com)):
    if len(com[c])<=miangine_sizeha:
        just_number_of_small_coms.append(c)
        small_coms.append([c])
        small_coms[i].append(com[c])
        i=i+1
#print("just number of small coms:",just_number_of_small_coms)
print("tedade small coms:",len(small_coms)) 
#print("small coms:",small_coms)
#print("\n")

for c in range(len(small_coms)):
    tedade_yalhaye_darune_yek_jame=0
    tedade_yalhaye_beyne_do_jame=[]
    teemp=[] #javame hamsayeye yek jame
    tedade_yalhaye_beyne_javame.append([])
    tedade_yalhaye_beyne_javame[c].append(small_coms[c][0])
    for k in small_coms[c][1]: #gereh haye yek jamee
        for n in dataset[k]: #hamsayehaye gereh
            for i in MEMORY[n]: #label haye gerehe hamsaye
                if small_coms[c][0] != i: #(yani dar yek jame nistand)
                    if (i in teemp)==False:
                        tedade_yalhaye_beyne_do_jame.append([i,1])
                        teemp.append(i)
                    if (i in teemp)==True:
                        tedade_yalhaye_beyne_do_jame[teemp.index(i)][1]=tedade_yalhaye_beyne_do_jame[teemp.index(i)][1]+1
    tedade_yalhaye_beyne_javame[c].append(tedade_yalhaye_beyne_do_jame)


#print("tedade yalhaye beyne javame:",tedade_yalhaye_beyne_javame)

print("...run time: % seconds..." % (time.time() - run_time) )
'''
print(" ")


# In[34]:


'''
#tabe modularity hampushani before va after:
def overlap_modularity_for_two(a,b):
    modubefor=0
    moduafter=0
    
    for k in [a,b]: 
        for i in com[k]:
            Qibefor=len(MEMORY[i])
            if (a in MEMORY[i])==True and (b in MEMORY[i])==True: 
                Qiafter=Qibefor-1
            else:
                 Qiafter=Qibefor
                
            for j in com[k][((com[k].index(i))+1):]:
                Qjbefor=len(MEMORY[j])
                if (a in MEMORY[j])==True and (b in MEMORY[j])==True:
                    Qjafter=Qjbefor-1
                else:
                    Qjafter=Qjbefor 
                
                modubefor=modubefor+(Qibefor*Qjbefor)
                moduafter=moduafter+(Qiafter*Qjafter)
                    
    return(modubefor,moduafter)
'''
print(" ")


# In[35]:


'''
#MARHALE 5 (edqam)
run_time= time.time()
count=len(com)
print("tedade kolle coms(qabl az edqam):",count)

for c in range(len(tedade_yalhaye_beyne_javame)):#baresie javame kuchak
    #print("jameye kujak:",tedade_yalhaye_beyne_javame[c][0])
    #agar jameye kujak hamsayei nadasht,soraqe jameye kujake badi miravim
    if len(tedade_yalhaye_beyne_javame[c][1])==0: 
        continue
    #yaftane jameeyi ke bishtarin yale beyne jameeyi ra ba jameye kuchak darad
    yalha=[]
    for i in range(len(tedade_yalhaye_beyne_javame[c][1])):
        yalha.append(tedade_yalhaye_beyne_javame[c][1][i][1])
    jameye_qabele_edqam=tedade_yalhaye_beyne_javame[c][1][yalha.index(max(yalha))][0] #jameeyi ba bishtarin yale beyni 
    #print("jameye_qabele_edqam:",jameye_qabele_edqam)
    #mohasebeye modularity qabl va bad az edqam:
    EQ=overlap_modularity_for_two(tedade_yalhaye_beyne_javame[c][0],jameye_qabele_edqam)
    EQ_qabl=EQ[0]
    print("modularity qabl az edqam:",EQ_qabl)
    EQ_bad=EQ[1]
    print("modularity bad az edqam:",EQ_bad)
    if EQ_qabl<EQ_bad :#baiad edgham shavad  #################################################################################
        #__________________________________________________________________________________________
        #UPDATE MEMORY:(د)
        for i in com[tedade_yalhaye_beyne_javame[c][0]]:
            MEMORY[i].append(jameye_qabele_edqam)
            MEMORY[i].remove(tedade_yalhaye_beyne_javame[c][0])
        #___________________________________________________________________________________________
        #jameye kuchak ra beriz dakhele jameye bozorg
        for i in range(len(com[tedade_yalhaye_beyne_javame[c][0]])):
            com[jameye_qabele_edqam].append(com[tedade_yalhaye_beyne_javame[c][0]][i])
        com[tedade_yalhaye_beyne_javame[c][0]]=[] #jameye kujak hast vali khali shode
        count=count-1
        #hazfe jameye kujake baresi shode az liste tedade_yalhaye_beyne_javame
        #tedade_yalhaye_beyne_javame[c][1]=[]
        #print("tedade yalhaye beyne javame:",tedade_yalhaye_beyne_javame)
       
        #______________________________________________________________________________________
        #UPDATE-agar jameye qabele edqam joze small coms bashad,hamsayegan va yalhayash update shavad:(ج)
        if jameye_qabele_edqam in just_number_of_small_coms:  
            tedade_yalhaye_beyne_do_jame=[]
            teemp=[] #javame hamsayeye yek jame
            for k in com[jameye_qabele_edqam]: #gereh haye yek jamee
                for n in dataset[k]: #hamsayehaye gereh
                    for i in MEMORY[n]: #label haye gerehe hamsaye
                        if jameye_qabele_edqam != i: #(yani dar yek jame nistand)
                            if (i in teemp)==False:
                                tedade_yalhaye_beyne_do_jame.append([i,1])
                                teemp.append(i)
                            if (i in teemp)==True:
                                tedade_yalhaye_beyne_do_jame[teemp.index(i)][1]=tedade_yalhaye_beyne_do_jame[teemp.index(i)][1]+1
            tedade_yalhaye_beyne_javame[just_number_of_small_coms.index(jameye_qabele_edqam)][1]=tedade_yalhaye_beyne_do_jame #ج
            #print("tedade yalhaye beyne javame(jim):",tedade_yalhaye_beyne_javame)
            #print("jim done")
        #_______________________________________________________________________________________
        #UPDATE tedade yalhaye beyne javame:(الف)
        for i in range(len(tedade_yalhaye_beyne_javame[c][1])):#jameye kuchak
            if tedade_yalhaye_beyne_javame[c][0]<tedade_yalhaye_beyne_javame[c][1][i][0] and tedade_yalhaye_beyne_javame[c][1][i][0] in just_number_of_small_coms:
                tt=[]
                indexx=just_number_of_small_coms.index(tedade_yalhaye_beyne_javame[c][1][i][0])
                for j in range(len(tedade_yalhaye_beyne_javame[indexx][1])):
                    tt.append(tedade_yalhaye_beyne_javame[indexx][1][j][0])
                if tedade_yalhaye_beyne_javame[c][0] in tt:
                    tedade_yalhaye_beyne_javame[indexx][1][tt.index(tedade_yalhaye_beyne_javame[c][0])][1]=0 #الف
                    #print("tedade yalhaye beyne javame(alef):",tedade_yalhaye_beyne_javame)
       #_______________________________________________________________________________________________         
        #UPDATE tedade yalhaye beyne javame:(پ-ب)        
        #javame hamsayeye jameye qabele edqam ra peida kon
        tt=[]
        for i in com[jameye_qabele_edqam]:#gereh haye yek jamee
            for j in dataset[i]: #hamsayehaye gereh
                for x in MEMORY[j]:#label haye gerehe hamsaye
                    tt.append(x) #javame hamsaye
        tt = list(dict.fromkeys(tt)) #(hazfe tekrari ha) 
        #print("hamsaye haye jame qabele edqam(tt):",tt)
        #tedade yale beyneshan update shavad
        for i in tt:
            if i>tedade_yalhaye_beyne_javame[c][0] and i in just_number_of_small_coms: #and
                #print("tt feli:",i)
                indexx=just_number_of_small_coms.index(i)
                tete=[]
                for k in range(len(tedade_yalhaye_beyne_javame[indexx][1])):
                    tete.append(tedade_yalhaye_beyne_javame[indexx][1][k][0])
                #print("hamsaye haye hamsaye ha(tete):",tete)
                tedade_yalhaye_beyne_do_jame=0
                for k in com[i]: #gereh haye yek jamee
                    for n in dataset[k]: #hamsayehaye gereh
                        if jameye_qabele_edqam in MEMORY[n]: #label haye gerehe hamsaye
                            tedade_yalhaye_beyne_do_jame=tedade_yalhaye_beyne_do_jame+1
                if jameye_qabele_edqam in tete:    
                    tedade_yalhaye_beyne_javame[indexx][1][tete.index(jameye_qabele_edqam)][1]=tedade_yalhaye_beyne_do_jame #ب
                    #print("tedade yalhaye beyne javame(be):",tedade_yalhaye_beyne_javame)
                else:
                    tedade_yalhaye_beyne_javame[indexx][1].append([jameye_qabele_edqam,tedade_yalhaye_beyne_do_jame]) #پ
        #_______________________________________________________________________________________
print("tedade coms bad az edqam:",count)
print("...run time: % seconds..." % (time.time() - run_time) )
'''
print(" ")


# In[36]:


# #yaftane javame e ground truth (FAQAT BARAYE 4 TA SHABAKEYE KUCHAK)(dar ground truth har satr label an gereh ast)

# #estekhraje label haye overlape gt
# gt_labels=[]

# with open("polbooks_groundtruth.txt") as f:
#     arr = list(map(str.split, f))
    
# for p in range((len(arr))):
#     gt_labels.append([])

# for i in range(len(arr)):
#     for j in range(len(arr[i])):
#         gt_labels[i].append(int(arr[i][j]))
        
# #print("ground truth labels are:",gt_labels)
# #print("\n")

# #ijade liste javame e hampushane gt:
# comm_ogt=[]
# for p in range(max_value(gt_labels)):
#     comm_ogt.append([])
    
# for k in range(max_value(gt_labels)):
#     for j in range(len(dataset)):
#         for h in range(len(gt_labels[j])):
#             if gt_labels[j][h]==(k+1): 
#                 comm_ogt[k].append(j)

# #tabdile list ha be set ha be khatere hazfe tekrari ha                
# com_ogt=[]
# for p in range(max_value(gt_labels)):
#     com_ogt.append([]) 
    
# for x in range(len(comm_ogt)):
#     com_ogt[x]=(set(comm_ogt[x]))
    

# #tabdile dobareye set be list:
# for i in range(len(com_ogt)):
#     com_ogt[i]=list(com_ogt[i])
# #print(" list of ground truth overlap communities:" , com_ogt)
# print("done")


# In[37]:


#yaftane javame e ground truth (FAQAT BARAYE AMAZON-DBLP-YOUTUBE)..dar ground truth har satr yek jamee ast
com_ogt=[]

with open("com-amazon.top5000.cmty.txt") as f:
    arr = list(map(str.split, f))
    
for i in range((len(arr))):
    com_ogt.append([])

for i in range(len(arr)):
    for j in range(len(arr[i])):
        com_ogt[i].append(int(arr[i][j]))
        
#print("ground truth communities are:",com_ogt)
print("yaftane javame e ground truth (FAQAT BARAYE AMAZON-DBLP-YOUTUBE)..dar ground truth har satr yek jamee: done")


# In[38]:


#TAQIRE JAVAME E MAN MOTANASEB BA GROUNDTRUTH BARAYE MOHASEBEYE NMI (FAQAT BARAYE AMAZON-DBLP-YOUTUBE)(entekhabe gerehe kamtar)
nodes_map=loadtxt("amazon_nodes_map.txt",comments="#",delimiter="\t",unpack=False)

n_m=[]
for i in nodes_map-1:
        n_m.append(int(i))
        
#ijade new_MEMORY baraye zakhireye label ha baraye gereh haye kamtar
new_MEMORY=[]
for i in range(len(n_m)):
    new_MEMORY.append([]) 

j=0
for i in n_m:
    new_MEMORY[j].append(i)
    new_MEMORY[j].append(MEMORY[i])
    j=j+1
#print("new_MEMORY:",new_MEMORY)

#yaftane unique label ha:
unique_labels=[]
for i in range(len(new_MEMORY)):
    for j in range(len(new_MEMORY[i][1])):
        unique_labels.append(new_MEMORY[i][1][j])
unique_labels=list(set(unique_labels))
#print("unique_labels",unique_labels)

#ijade javame ba gereh haye kamtar
new_com=[]
for i in range(len(unique_labels)):
    new_com.append([])

j=0
for i in unique_labels:
    new_com[j].append(i)#avalin ozve har jamee, labele an jamee ast
    j=j+1

for i in range(len(new_MEMORY)):
    for j in range(len(new_MEMORY[i][1])):
        new_com[unique_labels.index(new_MEMORY[i][1][j])].append(new_MEMORY[i][0])
        
#hazfe shomareye label ha az avalin ozve har list:
for i in range(len(new_com)):
    new_com[i].pop(0)
#print("new_com",new_com)
print("ijade javame ba gereh haye kamtar: done")


# In[39]:


#TAQire id gereh ha BARAYE MOHASEBEYE NMI (FAQAT BARAYE AMAZON-DBLP-YOUTUBE)
#unique node haye dataset ra peida kon 
snap=loadtxt("com-amazon.ungraph.txt",comments="#",delimiter="\t",unpack=False)
main_nodess=[]
for i in range(len(snap)):
    main_nodess.append(snap[i][0])
    main_nodess.append(snap[i][1])
main_nodess=list(set(main_nodess))

#unique node haye dataset ra moratab kon
sorted_main_nodess=[]
sorted_main_nodess=sorted(main_nodess)

#map tori besaz
map_tori=[]
for i in range(len(sorted_main_nodess)):
    map_tori.append([i,int(sorted_main_nodess[i])])
    
#id gereh hara avaz kon
new_com2=[]

for i in range(len(new_com)):
    new_com2.append([])
    for j in range(len(new_com[i])):
        new_com2[i].append(map_tori[new_com[i][j]][1])
print("id gereh ha ra avaz kon: done")


# In[42]:


#------------------------------- Groundtruth convert for ONMI-------------------------------------     
from numpy import loadtxt
from itertools import groupby
from operator import itemgetter
from sklearn.metrics.cluster import normalized_mutual_info_score

real_labels= loadtxt('./datasets/LFR/500000/0.1/community.txt', comments="#", delimiter="\t", unpack=False)

tuples = []
c = 1
for i in real_labels:
    tuples.append([c,i])
    c +=1

sorted_input = sorted(tuples, key=itemgetter(1))
groups = groupby(sorted_input, key=itemgetter(1))

final = []
for i in groups:
    temp = []
    for j in i[1]:
        temp.append(j[0]-1)
    final.append(temp)

#-------------------------------------------------------------------------------
from cdlib import evaluation

class obj:
    def __init__(self,name, communities):
        self.name = name
        self.communities = communities

obj_ogt = obj("list of ground truth overlap communities:", final)

obj_ome = obj("list of my overlap communities:", com)


#print("NMI(MGH) is:",evaluation.overlapping_normalized_mutual_information_MGH(obj_ogt,obj_ome))
print("NMI(LFK) is:",evaluation.overlapping_normalized_mutual_information_LFK(obj_ogt,obj_ome))

# In[41]:


#tabdile javame be text(baraye mohasebeye NMI)(FAQAT BARAYE AMAZON-DBLP-YOUTUBE)
import  csv

with open("mycom_amazon.txt","w") as f:
    wr = csv.writer(f)
    wr.writerows(new_com2)

with open('mycom_amazon.txt') as fin, open('nmycom_amazon.txt', 'w') as fout:
    for line in fin:
        fout.write(line.replace(',','\t'))
print("mycom_amazon.txt:  done")
# In[19]:


# #tabdile javame be text(baraye mohasebeye NMI)(be joz AMAZON-DBLP-YOUTUBE)
# import  csv

# with open("mycom_polbooks.txt","w") as f:
#     wr = csv.writer(f)
#     wr.writerows(com)

# with open('mycom_polbooks.txt') as fin, open('nmycom_polbooks.txt', 'w') as fout:
#     for line in fin:
#         fout.write(line.replace(',','\t'))    
#    #_______________________________________________________________________________________________ 

# with open("gtcom_polbooks.txt","w") as f:
#     wr = csv.writer(f)
#     wr.writerows(com_ogt)

# with open('gtcom_polbooks.txt') as fin, open('ngtcom_polbooks.txt', 'w') as fout:
#     for line in fin:
#         fout.write(line.replace(',','\t'))


# In[20]:


#tabe modularity baraye hampushani ha(EQ)(kolle shabake):
def overlap_modularity(COMMUNITY):
    modu=0.0
    m=0 #tedade kolle yalha
    ki=0 #darajeye i
    kj=0
    Aij=0 #i va j hamsaye hastand ya kheir
    Qi=0 #tedade label haye i
    Qj=0

    #mohasebeye tedade yalhaye shabake:
    for i in range(len(dataset)):
        m=m+len(dataset[i])
    m=m/2

    #formul nevisi:
    for k in range(len(COMMUNITY)):
    
        for i in COMMUNITY[k]:
            Qi=len(MEMORY[i])
            ki=len(dataset[i])

            for j in COMMUNITY[k]:
                Qj=len(MEMORY[j])
                kj=len(dataset[j])
            
                if (j in dataset[i])==True:
                    Aij=1
                else:
                    Aij=0
                    
                modu=modu+((Aij-(ki*kj)/(2*m))*(1.0/Qi*Qj))
                    
            
    EQ=(1.0/(2*m))*modu
    return(EQ)


# In[21]:


#bikhial
#mohasebeye modularity
run_time= time.time()
gt_mod=0
my_mod=0

#yaftane modularity baraye javameye groundtruth:
#gt_mod=overlap_modularity(com_ogt)
#print("modularity baraye javameye groundtruth:",gt_mod)

#yaftane modularity baraye javameye man:
#my_mod=overlap_modularity(com)
#print("modularity baraye javameye man:",my_mod)
print("...run time: % seconds..." % (time.time() - run_time) )


# In[ ]:




