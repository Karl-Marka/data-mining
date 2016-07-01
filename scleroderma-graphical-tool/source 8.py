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

__version__ = '1.7.0'
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
        A1 = Label (aboutFrame, text="May 12, 2016  Karl Märka", justify = CENTER)
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
  
    def click(self):
        print(self.notebook.index(self.notebook.select()))
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

    def writeFile(self):
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
        self.outputBox = Text(outputfield, width = 28, height = 5, state = 'disabled', wrap = 'word', yscrollcommand = scrollbar.set)
        self.outputBox.grid(pady=5, padx=(8, 0), row = 0, column = 0)
        scrollbar.config(command=self.outputBox.yview)
        buttonfield = Frame(top, width = 285, borderwidth = 2)
        buttonfield.grid(padx=10, pady=2, row = 3, column = 0)
        B7 = ttk.Button(inputfield, text ="Expression data...", command=self.dataFile)
        B7.grid(row=6,column=1, padx=15, pady=6)
        B7_1 = ttk.Button(diagnosis, text ="Expression data...", command=self.dataFile)
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