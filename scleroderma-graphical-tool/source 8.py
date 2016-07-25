from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pandas import DataFrame, concat, read_csv
from os import chmod
from stat import S_IREAD
from datetime import date
from multiprocessing import Queue, Process, freeze_support
from pylab import figure, xlim, ylim, ylabel, title, tick_params, axvspan, gca, plot, figtext
from numpy import array

__version__ = '1.8.0'
__author__ = 'Karl Märka'

def readFile(filename, colName = "NAME", colName2 = "CLID"):
    geneExp = read_csv(filename, sep="\t", header = 0)
    #geneExp = geneExp[[colName, colName2, patientID]]
    geneList = ["COL4A1", "COL4A2", "SP5", "CTGF", "GPX1", "GTF2I", "HRPT1", "PRKRIP1", "RPL19", "USP7"]
    probeList = ["AGI_HUM1_OLIGO_A_23_P135381", "AGI_HUM1_OLIGO_A_23_P19663", "AGI_HUM1_OLIGO_A_23_P205031", "AGI_HUM1_OLIGO_A_23_P65240", "A_33_P3239849", "AGI_HUM1_OLIGO_A_23_P168567", "AGI_HUM1_OLIGO_A_24_P320759", "AGI_HUM1_OLIGO_A_23_P77779", "AGI_HUM1_OLIGO_A_32_P116881", "AGI_HUM1_OLIGO_A_23_P49481"]
    dataCropped = DataFrame(data=[])
    for i in geneList:
        dt = geneExp.loc[geneExp[colName] == i]
        dataCropped = concat([dataCropped, dt])
    geneExp = None
    dataCropped2 = DataFrame(data=[])
    dataCropped3 = DataFrame(data=[])
    names = dataCropped[colName].tolist()
    for i in geneList:
        if names.count(i) == 1:
            dt = dataCropped.loc[dataCropped[colName] == i]
            dataCropped2 = concat([dataCropped2, dt])
        else:
            dt = dataCropped.loc[dataCropped[colName] == i]
            dataCropped3 = concat([dataCropped3, dt])
            for n,a in enumerate(dataCropped3[colName2]):
                if dataCropped3[colName2].iloc[n] in probeList:
                     #print(dataCropped3.iloc[n])  
                    dt = dataCropped3.iloc[n]
                    dt = DataFrame(data = dt)
                    dt = dt.T
                    dataCropped2 = concat([dataCropped2, dt])
    dataCropped = dataCropped2.drop_duplicates()
    return dataCropped

 
class diseaseScore:

    file = DataFrame(data=[], index = None, columns = None)

    def __init__(self, patientID, testAll, patientAge, patientW, duration, diseaseType):
        self.patientID = patientID
        self.testAll = testAll
        self.patientAge = patientAge
        self.patientW = patientW
        self.duration = duration
        self.diseaseType = diseaseType
               
    def readGeneExp(self, patientID, file, colName = "NAME", colName2 = "CLID"):
        geneExp = file
        geneExp = geneExp[[colName, colName2, patientID]]
        return geneExp
       
    def concatenator(self, geneExp, geneList, colName = "NAME"):
        dt = DataFrame(data=[])
        for i in geneList:
            dts = geneExp.loc[geneExp[colName] == i]
            dt = concat([dt, dts])
        return dt
    
    def score(self):
        geneExp = self.readGeneExp(self.patientID, self.file)
        geneList = ["GTF2I", "HRPT1", "PRKRIP1", "RPL19", "USP7"]
        testedGeneList = ["SP5", "CTGF", "COL4A2", "COL4A1", "GPX1"]
        referenceGeneExp = self.concatenator(geneExp, geneList)        
        referenceGeneExp = referenceGeneExp[self.patientID]
        avgReference = sum(referenceGeneExp)/len(referenceGeneExp)
        addToGene = - 0.198470080719094 - avgReference
        addToGeneList = [addToGene, addToGene, addToGene, addToGene, addToGene]   
        testedGenes = self.concatenator(geneExp, testedGeneList)
        testedGeneValues = testedGenes[self.patientID].values.tolist()
        center = [-1.803792563, 1.621776229, 1.837872721, 2.147204293, 0.150832608]
        scale = [1.107777831, 1.084507906, 0.641595511, 0.681444395, 0.447443382]
        result = [(x + y - z)/a for x, y, z, a in zip(testedGeneValues, addToGeneList, center, scale)]
        if self.testAll == True:
            score = 2.4558780137 + 0.0036315824 * self.patientAge - 0.0009938834 * self.duration - 0.1909135701 * self.patientW  - 0.6332020954 * self.diseaseType + 0.0780679639 * result[3] + 0.0180144849 * result[2] + 0.0252636850 * result[1] + 0.0296154999 * result[4] - 0.1353340459 * result[0] + 0.005
        else:
            score = 2.21299866958507 + 0.0644114082730535 * result[3] + 0.0117213806235561 * result[2] + 0.043059130842487 * result[1] + 0.0257447259168477 * result[4] - 0.133351227934197 * result[0] + 0.005        
        interface.scoreVal = score
        return score

class diagnosis:

    filename = "data.txt"
    
    def __init__(self, patientID):
        self.patientID = patientID

    def readFileDiagnosis(self, filename, patientID):
        oligos_sc = ['XIST','RPS4Y2','RPS4Y1','DDX3Y','MS4A4A','MYOF','ARL4C','VRK2','S100A11','FZD1','C11orf75','RAB15','LMO2','RCOR1','IGJ','DYSF','RAD51C','FCGR2A','ARHGEF10L','CYBB','KYNU','LOC93622','KIAA1522','42623','CTSB','DHRS7B','ACSL1','CSTB','PLA2G4A','UPF3A','SLC31A2','CAMKK2','CALML4','GNG5','C9orf167','CCR1','MZB1','C5orf32','CTNNA1','LOC100652840','GOLGA6L9','CHST15','TTTY14','CREB5','GLT1D1','WARS','ESRRA','SMPD4','ATP6V1B2','NAGK','TIMP2','VAMP5','TXNDC5','S100P','C2','PTX3','ANKS6','HMGB1','PDK4','CTSL1','RINT1','VPS37C','GRN','GLCCI1','STRBP']
        oligos_PAH = ['ZBTB40','RBM17','TIMP1','FBRSL1','HSF2','GLOD4','ABLIM1','LOC390705','CEP72','ADM','ALAS2','BCAT1','TMEM158','ALKBH2','RASGRP1','MCM3','GSTO1','S100A10','ATP6V0A1','TMEM164','C12orf23','NSMCE4A','C5orf39','TRIB2','CORO1C','SELENBP1','LOC93622','SH3GLB1','MKL2','GEMIN4','EVL','GLUL','FBXO21','MRPL48','ZCWPW1','LGALS3','MSH2','LCK','CTNNA1','OCIAD2','PPP2R3B','SPEG','LBH','ANKS6','HAUS8','ZNF22','TYW1','CLEC2D','SEL1L3','ARHGEF4','NOSIP','SNCA','PUS1','PUM2','HADHB','SLC27A5','HIP1R','TNFAIP8','SFI1','IMPA2','DNMT1','MAGEH1','LEF1','SRGAP2','CTSB']
        means = array([-7.2508,-2.67407778,-5.62846667,-2.86860556,-1.36541111,-2.36407778,-2.27974444,-5.01005,-5.50435556,-3.12296667,-3.05374444,-2.93088333,-1.52182778,-2.40443889,-3.25210556,-4.92518889,-5.2333,-3.55938333,-6.48432778,0.85436667,-6.50599444,-4.09310556,-1.67813333,-4.22541111,-1.22743889,-4.09716111,-4.39443889,-1.2018,-4.53074444,-6.02960556,-2.18221667,-3.76107778,-4.96255,-7.19313333,-4.23368889,-1.22635556,-2.65982778,-4.17452222,-3.95421667,-4.9353,-6.14138333,-1.45252222,-4.25641111,-6.76024444,-7.15746667,-5.63343889,-6.0523,-4.04338333,-5.3433,-7.43291111,-7.48360556,-3.60727222,-6.74832778,-0.52532778,-4.87527222,-5.70468889,-3.56868889,-5.40032778,-5.92549444,-4.02732778,-2.09643889,-4.24977222,-3.73610556,-3.35071667,-3.52974444])       
        scales = array([0.64012431,0.48644003,0.38126755,0.38895023,0.53052328,0.48778576,0.49807297,0.5971372,0.58102997,0.35492456,0.42872699,0.3511465,0.60229235,0.47275821,0.46769339,0.3230946,0.37759403,0.4308013,0.68179109,0.32208992,2.49611833,0.33738646,0.46875436,0.33033987,0.60419482,0.47778749,0.41107253,0.31601268,0.35915973,0.42817738,0.4227548,0.19555594,0.91245211,0.58704444,0.40104286,0.41405216,0.30157285,0.2961911,0.68120062,0.55607422,0.58102261,0.40702269,0.84641725,0.59481162,0.51046074,0.60413407,0.2918044,0.30595161,0.29806585,2.99733465,3.06453882,0.45402224,0.7214568,0.59115988,0.21016818,0.31385124,0.36536889,0.42501994,0.40787234,0.27886479,0.47295374,0.47554771,0.33143456,0.4482326,3.63471967])
        means_PAH = array([-3.12208333,-7.10347222,-4.56233333,-5.44347222,-5.73447222,-5.58894444,-4.11030556,-7.18466667,-5.63466667,-1.85297222,-5.68872222,-1.34144444,-4.00611111,-5.16125,-3.47361111,-4.33552778,-2.92763889,-2.812,-4.59813889,-5.02736111,-4.17630556,-4.38347222,-4.799,-4.19444444,-5.13583333,-4.03788889,-4.57963889,-4.03633333,-1.48638889,-1.79041667,-3.42233333,-4.98155556,-4.90247222,-4.21816667,-3.31636111,-6.16036111,-5.82405556,-4.91691667,-6.05708333,-2.33216667,-4.39994444,-3.94036111,-4.83877778,-3.06369444,-4.32119444,-1.24025,-3.68625,-3.7015,-3.03108333,-5.59352778,-2.74713889,-4.115,-5.73516667,-4.15736111,-5.51825,-4.76769444,-4.45747222,-7.89680556,-3.50227778,-1.57858333,-4.51075,-4.25294444,-3.32391667,-3.70422222,-4.47977778])
        scales_PAH = array([0.45548222,0.80531853,2.17800769,0.3312269,0.5574636,0.60266161,0.42579448,0.62891094,0.43979169,0.44390793,0.48784922,0.50522849,0.4829818,0.45891681,0.4967105,0.29290801,0.43744214,0.29929587,0.29863102,0.2803095,0.30981128,0.62333251,0.42782953,0.2712991,0.28531397,0.55639679,0.41519319,0.53463343,0.39496016,0.55651379,0.67715503,0.61693834,0.40185575,0.36765366,0.39692754,0.33544954,0.3896228,0.25982953,0.35702993,0.43382046,0.2227585,0.55168622,0.4477026,0.25315803,0.29330632,0.51658375,0.25700168,0.43494464,0.38839504,2.05306783,0.49589193,0.34088007,0.41657098,1.77035289,0.78410655,0.50427511,0.50024233,1.15517392,0.31911043,0.30325876,0.45989289,0.32215513,0.30175457,0.26866934,0.27823404])
        data = read_csv(filename, header = 0, index_col = 0, sep = '\t')
        data = data[patientID]
        test = data.ix[oligos_sc]
        test_PAH = data.ix[oligos_PAH]
        test = test.sort_index(axis = 0)
        test_PAH = test_PAH.sort_index(axis = 0)
        gene_exp = test.copy()
        gene_exp_PAH = test_PAH.copy()
        test = test.T
        test_PAH = test_PAH.T
        #PAH_header = test_PAH.columns
        PAH_index = test_PAH.index
        #header_test = test.columns
        index_test = test.index
        test = test.as_matrix()
        test = array(test)
        test = (test - means)/scales
        test = DataFrame(data = test, columns = [patientID], index = index_test)
        test_PAH = test_PAH.as_matrix()
        test_PAH = array(test_PAH)
        test_PAH = (test_PAH - means_PAH)/scales_PAH
        test_PAH = DataFrame(data = test_PAH, columns = [patientID], index = PAH_index)
        gene_data = read_csv('./gene_data.txt', header = 0, index_col = 0, sep = '\t')
        return test, test_PAH, gene_data

    def diagnose(self):
        Sc, PAH, gene_data = self.readFileDiagnosis(self.filename ,self.patientID)                
        intercept = 0.77777777777777823
        coefs = [0.00098243,-0.0047879,0.03617133,-0.02130785,-0.02896074,0.04615671,-0.03039921,0.04184694,0.0391919,0.07393678,-0.05860535,-0.03349191,-0.05559615,-0.06198412,-0.0031149,0.00410208,-0.05777838,0.02920087,-0.00509455,0.06931355,-0.02210376,-0.02595638,0.0555343,-0.03700598,-0.01215271,0.07227833,0.02423346,0.01654485,0.03780628,-0.00961191,0.01403966,-0.05467147,-0.03159076,0.07839167,0.00365092,0.02541324,-0.01783945,-0.0125312,0.03157752,-0.02567822,-0.02937399,-0.05961683,-0.02032554,-0.02578202,-0.01745548,-0.02262699,-0.0886352,0.0191839,-0.05568611,-0.00835254,-0.02070594,0.02658609,-0.00396051,0.00763121,-0.03916338,0.02739357,-0.03501477,-0.01223597,-0.02754169,0.01253852,0.03934351,-0.00386323,0.12492334,0.03539774,0.02246754]
        #predictions = []
        intercept_PAH = 0.33333333333333476
        coefs_PAH = [0.00241079,-0.04230075,0.00515046,0.09402087,-0.0136427,0.02391159,0.03906091,0.13015909,-0.02400155,-0.15671898,-0.04971214,-0.00087562,-0.23052752,0.0503485,0.05411411,-0.1688456,0.04719709,-0.05567729,0.00108363,0.04508738,-0.07245604,0.00434705,0.00958327,0.04460761,0.01081198,0.0176367,-0.00435113,-0.06923663,-0.00033952,0.05871552,0.08685009,-0.0592945,-0.15864829,0.07290631,-0.04356502,-0.02311336,-0.06134274,-0.11681974,-0.05852237,-0.02166232,-0.14428914,0.03089396,0.1065567,0.04188958,0.05318762,-0.0847391,0.03926316,0.06534825,-0.04783862,0.04632451,0.19659504,0.2245639,0.00442051,-0.13100712,0.02495979,-0.11869847,-0.01535175,0.19565282,0.08549097,0.04298571,-0.04405261,-0.04324238,0.04641843,-0.00584063,-0.0739041]
        #predictions_PAH = []
        # Predicting Sc
        value = 0 
        values = Sc[self.patientID].tolist()
        for x in range(len(values)):
            a = coefs[x] * values[x]
            value += a
        prediction_Sc = intercept + value
        # Predicting PAH
        values = PAH[self.patientID].tolist()
        value = 0    
        for y in range(len(values)):
            a = coefs_PAH[y] * values[y]
            value += a
        prediction_PAH = intercept_PAH + value
        if prediction_PAH <= 0.1:
            prediction_PAH = '< 10%'
        elif prediction_PAH <= 0.3:
            prediction_PAH = '< 30%'
        elif prediction_PAH <= 0.5:
            prediction_PAH = '< 50%'
        elif prediction_PAH <= 0.75: 
            prediction_PAH = '75%'
        elif prediction_PAH <= 0.9:
            prediction_PAH = '90%'
        elif prediction_PAH > 0.9:
            prediction_PAH = '> 90%'
        # Predicting similarity to Sc 
        up = dict()
        down = dict() 
        for i in gene_data.index:
            condition = gene_data.loc[i,'condition']
            value = gene_data.loc[i,'value']
            if condition == 'UP':
                up.update({i : value})
            elif condition == 'DOWN':
                down.update({i : value})
        score = 0
        data = Sc[self.patientID]        
        for gene in data.index:
            if gene in up.keys():
                if data.ix[gene] > up.get(gene):
                    score += 1
            elif gene in down.keys():
                if data.ix[gene] < down.get(gene):
                        score += 1
        probability = int(round((score/65)*100,0))
        PAH_probability = prediction_PAH
        if float(prediction_Sc) >= 0.5:
            if probability < 50:
                return 'Patient ' + str(self.patientID) + ' is Scleroderma negative' 
            if 70 > probability >= 50 :
                return 'Patient ' + str(self.patientID) + ' is borderline with a gene exp. similiarity of ' + str(probability) + '% to a reference Scleroderma gene exp. pattern. The probability for PAH is: ' + str(PAH_probability)
            elif probability >= 70 :
                return 'Patient ' + str(self.patientID) + ' is Scleroderma positive with a gene exp. similiarity of ' + str(probability) + '% to a reference Scleroderma gene exp. pattern. The probability for PAH is: ' + str(PAH_probability)              
        elif float(prediction_Sc) < 0.5 :
            return 'Patient ' + str(self.patientID) + ' is Scleroderma negative'
        


class interface:

    scoreVal = 0.00

    def helpM(self):
        helpBox = Toplevel(self.top)
        w = 245
        h = 260
        helpBox.geometry('%dx%d+%d+%d' % (w, h, self.x, self.y))
        helpBox.wm_title("Help")
        helpBox.resizable(width=FALSE, height=FALSE)
        helpBox.iconbitmap('logo.ico')
        helpFrame = Frame(helpBox, height=290)
        helpFrame.grid(padx=1, pady=1, row = 0, column = 0)
        H2 = Label (helpFrame, text="1. Fill in the required parameters. Patient ID, 'Use data' and gene exression file are mandatory. The rest of the fields must be filled out when using 'Use data' with the parameter 'All'. With the parameter 'Gene' selected, the algorithm takes into account only the gene expression values." , justify = LEFT, wraplength = 240)
        H2.grid(row=0,column=0, padx=5, pady=5)
        H1 = Label (helpFrame, text="2. Press 'Calculate'. The program will output the predicted MRSS value in the output console. The output can be printed into plain text file or copied from the console with 'CTRL + C'" , justify = LEFT, wraplength = 240)
        H1.grid(row=1,column=0, padx=5, pady=10)
        button = Button(helpBox, text="Close", command=helpBox.withdraw)
        button.grid(row=4,column=0, padx=5, pady=5)
  
    def aboutM(self):
        aboutBox = Toplevel(self.top)
        w = 280
        h = 140
        aboutBox.geometry('%dx%d+%d+%d' % (w, h, self.x, self.y))
        aboutBox.wm_title("About")
        aboutBox.resizable(width=FALSE, height=FALSE)
        aboutBox.iconbitmap('logo.ico')
        aboutFrame = Frame(aboutBox, height=290)
        aboutFrame.grid(padx=1, pady=1, row = 0, column = 0)
        global img2
        img2 = PhotoImage(file = "header.png")
        panel2 = Label(aboutFrame, image = img)
        panel2.grid(row = 0, column = 0)
        A1 = Label (aboutFrame, text="July 21, 2016  Karl Märka", justify = CENTER)
        A1.grid(row=1,column=0, padx=5, pady=2)
        button = ttk.Button(aboutBox, text="Close", command=aboutBox.withdraw)
        button.grid(row=5,column=0, padx=5, pady=5)

    def dataFile(self):
        try:       
            self.outputBox.config(state = 'normal')
            self.outputBox.delete('1.0', 'end')
            self.outputBox.insert('1.0 + 2 lines', 'Please wait. Reading data...')
            self.outputBox.config(state = 'disabled')
            fileObj = filedialog.askopenfile()
            filename = fileObj.name
            filename = str(filename) 
            q = Queue()
            db = Process(target=q.put, args=(readFile(filename),))
            db.start()        
            db.join
            file = q.get()
            diseaseScore.file = file
            self.B5.config(state = 'normal')
            self.outputBox.config(state = 'normal')
            self.outputBox.delete('1.0', 'end')
            self.outputBox.insert('1.0 + 2 lines', 'Ready!')
            self.outputBox.config(state = 'disabled')
        except:
            self.outputBox.config(state = 'normal')
            self.outputBox.delete('1.0', 'end')
            self.outputBox.insert('1.0 + 2 lines', 'No data read.')
            self.outputBox.config(state = 'disabled') 

    def dataFile2(self):
        try:       
            fileObj = filedialog.askopenfile()
            filename = fileObj.name
            filename = str(filename) 
            diagnosis.filename = filename
            self.B5.config(state = 'normal')
        except:
            self.outputBox.config(state = 'normal')
            self.outputBox.delete('1.0', 'end')
            self.outputBox.insert('1.0 + 2 lines', 'No data read.')
            self.outputBox.config(state = 'disabled')            
              
    def useAll(self):
        gene = self.options1[self.geneExp.get()]
        self.outputBox.config(state = 'normal')
        self.outputBox.delete('1.0', 'end')
        if len(self.race.get()) == 0 or len(self.typeVar.get()) == 0 or len(self.E2.get()) == 0 or len(self.E3.get()) == 0:
            self.outputBox.config(state = 'normal')
            self.outputBox.insert('1.0 + 2 lines', 'Please fill out all the fields.')
            return
        else:
            self.outputBox.delete('1.0', 'end')
            raceVal = self.options2[self.race.get()]
            typeVal = self.options3[self.typeVar.get()]
            patientID = self.E1.get()
            patientAge = self.E2.get()
            duration = self.E3.get()
            output = diseaseScore(str(patientID), gene, int(patientAge), int(raceVal), int(duration), int(typeVal)).score()    
            output = "Patient " + str(patientID) + " disease score: " + str(round(output, 2))
            self.outputBox.config(state = 'normal')
            self.outputBox.insert('1.0 + 2 lines', output)
            self.outputBox.insert('2.0 + 2 lines', '\n\nAll patient data was used in calculating the final score.')

    def useGene(self):
        gene = self.options1[self.geneExp.get()]
        self.outputBox.config(state = 'normal')
        self.outputBox.delete('1.0', 'end')
        patientID = self.E1.get()
        output = diseaseScore(str(patientID), gene, 1, 1, 1, 1).score()
        try:           
            output = "Patient " + str(patientID) + " disease score: " + str(round(output, 2))
            self.outputBox.insert('1.0 + 2 lines', output)
            self.outputBox.insert('3.0 + 2 lines lineend', '\n\nOnly gene expression data was used in calculating final score.')
        except:
            self.outputBox.insert('1.0 + 2 lines', output)

    def putDiagnosis(self):
        patientID = self.E1_1.get()
        output = diagnosis(str(patientID)).diagnose()
        #print (output)
        self.outputBox.config(state = 'normal')
        self.outputBox.insert('1.0 + 2 lines', output)
        self.B6.config(state = 'normal')       
  
    def click(self):
        #print(self.notebook.index(self.notebook.select()))
        if self.notebook.index(self.notebook.select()) == 1:
            self.outputBox.config(state = 'normal')
            self.outputBox.delete('1.0', 'end')
            self.outputBox.config(state = 'disabled')
            if len(self.E1.get()) == 0:    
                self.outputBox.config(state = 'normal')
                self.outputBox.insert('1.0 + 2 lines', 'Please insert patient ID.')
                return
            elif len(self.geneExp.get()) == 0:
                print(self.geneExp.get())
                self.outputBox.config(state = 'normal')
                self.outputBox.insert('1.0 + 2 lines', 'Please select what parameters to use.')
                return        
            else:
                gene = self.options1[self.geneExp.get()]
                if gene == True:            
                    self.useAll()
                else:
                    self.useGene()
                self.outputBox.config(state = 'disabled')
                self.B6.config(state = 'normal')
        elif self.notebook.index(self.notebook.select()) == 0:
            self.outputBox.config(state = 'normal')
            self.outputBox.delete('1.0', 'end')
            self.outputBox.config(state = 'disabled')
            if len(self.E1_1.get()) == 0:    
                self.outputBox.config(state = 'normal')
                self.outputBox.insert('1.0 + 2 lines', 'Please insert patient ID.')
                return
            else:
                self.putDiagnosis()



    def writeFile(self):
        if self.notebook.index(self.notebook.select()) == 0:
            dateStamp = date.today()
            content = str(self.outputBox.get('1.0', 'end')) + '\n\n' + str(dateStamp)
            patientID = self.E1_1.get()
            filename = './logs/' + str(dateStamp) + '_Patient_' + str(patientID) + '_diagnosis.txt'
            f = open(filename, 'w')
            f.write(content)
            f.close
            infoMessage = 'The result was printed to file: ' + str(filename)            
            messagebox.showinfo(title = "Output to file", message = infoMessage)
            self.B6.config(state = 'disabled')
        elif self.notebook.index(self.notebook.select()) == 1:
            score = self.scoreVal
            dateStamp = date.today()
            patientID = self.E1.get()
            filename = './logs/' + str(dateStamp) + '_Patient_' + str(patientID) + '_score.pdf'
            if self.geneExp.get() == 'All':
                score = 26.166 * score - 31.261
                content = str(self.outputBox.get('1.0', 'end')) + '\nAge: ' + str(self.E2.get()) + '\nDisease duration: ' + str(self.E3.get()) + '\nDisease type: ' + str(self.typeVar.get()) + '\nEthnicity: ' + str(self.race.get()) + '\n\n' + str(dateStamp)
                x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222]
                y = [0,0,3,3,3,4,4,5,5,5,5,6,6,8,8,9,9,9,10,10,11,12,12,12,12,12,12,13,13,13,13,13,14,14,15,15,15,15,16,16,16,17,17,17,18,18,18,18,18,19,19,19,19,19,20,20,20,20,21,21,22,23,23,24,24,24,24,25,25,25,25,25,26,26,26,26,26,27,27,27,27,27,27,27,27,27,28,28,28,28,28,28,28,28,29,29,29,29,29,29,29,29,29,30,30,30,30,31,31,31,31,31,32,32,32,32,32,33,33,33,33,33,33,33,33,34,34,34,34,34,34,34,34,34,34,34,34,34,34,35,35,35,35,35,35,35,35,35,35,35,35,36,36,36,36,36,36,37,37,37,37,37,37,37,37,38,38,38,38,38,38,38,39,39,39,39,39,39,39,39,39,39,40,40,40,40,40,41,41,41,41,41,41,41,41,42,42,42,42,42,43,43,43,43,43,43,44,44,44,44,45,45,45,46,46,47,47,49,49,50,50,51]
                limit = 222
                val1 = 4.6068*score - 11
                val2 = 4.6068*score - 10
            else:
                score = 45.93 * score - 80.843
                content = str(self.outputBox.get('1.0', 'end')) + '\n\n' + str(dateStamp)
                x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260]
                y = [0,0,1,1,1,2,2,4,4,4,5,5,5,5,5,5,5,5,5,6,7,7,7,8,8,8,8,9,9,9,9,10,10,11,11,11,11,11,11,12,12,12,12,12,12,12,12,13,13,13,13,13,13,14,14,14,15,15,15,15,15,15,15,15,16,16,16,16,16,16,17,17,17,17,17,17,17,17,17,17,17,17,18,18,18,18,18,19,19,19,19,19,19,19,19,19,19,19,19,19,19,20,20,20,20,20,20,20,20,20,21,21,21,21,21,21,21,21,21,21,21,22,22,22,22,22,22,22,22,23,23,23,23,23,23,23,23,23,23,23,23,23,23,24,24,24,24,24,24,24,24,24,24,24,24,25,25,25,25,25,25,25,26,26,26,26,26,26,26,26,26,26,26,26,26,27,27,27,27,27,27,27,27,27,27,28,28,28,28,28,28,28,28,29,29,29,29,30,30,30,30,31,31,31,31,31,31,31,31,31,31,32,32,32,32,32,32,32,32,32,33,33,33,33,34,34,34,34,35,35,35,35,35,36,36,36,36,36,37,37,37,38,38,38,39,39,39,39,40,41,41,42,42,43,43,44,44,48,50,51]
                limit = 260
                val1 = 5.4365*score - 1
                val2 = 5.4365*score - 0.4
            self.createPlot(x, y, filename, content, limit, val1, val2)
            infoMessage = 'The result was printed to file: ' + str(filename)            
            messagebox.showinfo(title = "Output to file", message = infoMessage)
            self.B6.config(state = 'disabled')

    def createPlot(self, x, y, filename, content, limit, val1, val2):
        fig = figure(figsize=(8, 8))     
        xlim(0, limit)
        ylim(0, 51)
        ylabel("MRSS score 0 - 51")
        title("Severity of the score according to a reference MRSS distribution")
        tick_params(
            axis='x',          
            which='both',     
            bottom='off',      
            top='off',        
            labelbottom='off') 
        axvspan(val1, val2, color='red', alpha=0.5)
        gca().set_position((.1, .3, .8, .6)) 
        figtext(.04, .05, content)
        plot(x, y)
        fig.savefig(filename)

    def __init__(self, master):
        self.top = master
        w = 285
        h = 550
        ws = top.winfo_screenwidth()
        hs = top.winfo_screenheight()
        self.x = (ws/2) - (w/2)
        self.y = (hs/2) - (h/2)
        master.geometry('%dx%d+%d+%d' % (w, h, self.x, self.y))
        master.wm_title("SDSS v1.0")
        master.resizable(width=FALSE, height=FALSE)
        self.notebook = ttk.Notebook(top)
        self.notebook.grid(row = 1, column = 0)
        frame1 = ttk.Frame(self.notebook)
        frame2 = ttk.Frame(self.notebook)        
        self.notebook.add(frame1, text = 'Diagnosis')
        self.notebook.add(frame2, text = 'MRSS')
        menubar = Menu(top)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.helpM)
        helpmenu.add_command(label="About...", command=self.aboutM)
        menubar.add_cascade(label="Help", menu=helpmenu)
        inputfield = LabelFrame(frame2, width = 285, text = "Patient Data:")
        inputfield.grid(padx=10, pady=5, row = 0, column = 0)
        diagnosis = LabelFrame(frame1, width = 285, text = "Patient Data:")
        diagnosis.grid(padx=10, pady=5, row = 0, column = 0)
        L1 = Label (inputfield, text="Patient ID:")
        L1.grid(row=0,column=0, padx=5, pady=5)
        L1_1 = Label (diagnosis, text="Patient ID:")
        L1_1.grid(row=0,column=0, padx=23, pady=5)
        L2_1 = Label (diagnosis, text="")
        L2_1.grid(row=1,column=0, padx=23, pady=71)
        self.E1_1 = ttk.Entry(diagnosis)
        self.E1_1.grid(row=0,column=1, padx=16, pady=5)
        self.E1_1.entrytext = StringVar()
        self.E1 = ttk.Entry(inputfield)
        self.E1.grid(row=0,column=1, padx=16, pady=5)
        self.E1.entrytext = StringVar()
        L2 = Label (inputfield, text="Age:")
        L2.grid(row=1,column=0, padx=5, pady=5)
        self.E2 = ttk.Entry(inputfield)
        self.E2.grid(row=1,column=1, padx=16, pady=9)
        self.E2.entrytext = IntVar()
        L3 = Label (inputfield, text="Disease duration:")
        L3.grid(row=2,column=0, padx=5, pady=5)
        self.E3 = ttk.Entry(inputfield)
        self.E3.grid(row=2,column=1, padx=16, pady=5)
        self.E3.entrytext = IntVar()
        L4 = Label (inputfield, text="Use data:")
        L4.grid(row=3,column=0, padx=5, pady=5)
        self.geneExp = StringVar(inputfield)
        self.options1 = {"All": True, "Gene": False}
        O4 = ttk.Combobox(inputfield, state = 'readonly', width = 17, textvariable = self.geneExp, values = (list(self.options1.keys()))).grid(row=3,column=1, padx=5, pady=1)
        L5 = Label (inputfield, text="Patient ethnicity:")
        L5.grid(row=4,column=0, padx=5, pady=5)
        self.race = StringVar(inputfield)
        self.options2 = {"White": "1", "Black": "0"}
        O5 = ttk.Combobox(inputfield, state = 'readonly', width = 17, textvariable = self.race, values = (list(self.options2.keys()))).grid(row=4,column=1, padx=5, pady=1)
        L6 = Label (inputfield, text="Disease type:")
        L6.grid(row=5,column=0, padx=5, pady=5)
        self.typeVar = StringVar(inputfield)
        self.options3 = {"Diffuse": "1", "Limited": "0"}
        O6 = ttk.Combobox(inputfield, state = 'readonly', width = 17, textvariable = self.typeVar, values = (list(self.options3.keys()))).grid(row=5,column=1, padx=1, pady=1)
        outputfield = LabelFrame(top, width = 285, text = "Output:")
        outputfield.grid(padx=10, pady=2, row = 2, column = 0)
        scrollbar = Scrollbar(outputfield)
        scrollbar.grid(row = 0, column = 1, pady = 5, padx=(0, 8), sticky = 'ns')
        self.outputBox = Text(outputfield, width = 28, height = 5, state = 'disabled', wrap = 'word', yscrollcommand = scrollbar.set, font = ('Courier', 10))
        self.outputBox.grid(pady=5, padx=(8, 0), row = 0, column = 0)
        scrollbar.config(command=self.outputBox.yview)
        buttonfield = Frame(top, width = 285, borderwidth = 2)
        buttonfield.grid(padx=10, pady=2, row = 3, column = 0)
        B7 = ttk.Button(inputfield, text ="Expression data...", command=self.dataFile)
        B7.grid(row=6,column=1, padx=15, pady=6)
        B7_1 = ttk.Button(diagnosis, text ="Expression data...", command=self.dataFile2)
        B7_1.grid(row=6,column=1, padx=15, pady=6)
        self.B5 = ttk.Button(buttonfield, text ="Calculate", state = 'disabled', command=self.click)
        self.B5.grid(row=0,column=0, padx=15, pady=1)
        self.B6 = ttk.Button(buttonfield, state = 'disabled', text ="Print Output", command = self.writeFile)
        self.B6.grid(row=0,column=1, padx=15, pady=1)
        master.iconbitmap('logo.ico')
        master.config(menu=menubar)
        headerfield = Frame(master, height=150)
        headerfield.grid(padx=0, pady=10, row = 0, column = 0)
        panel = Label(headerfield, image = img)
        panel.grid(row = 0, column = 0)

        
        
if __name__ == '__main__':
	freeze_support()
	top = Tk()
	img = PhotoImage(file = "header.png")
	app = interface(top)
	top.mainloop()