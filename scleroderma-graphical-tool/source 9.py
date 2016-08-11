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
from numpy import array, mean

__version__ = '1.9.0'
__author__ = 'Karl Märka'

 
class diseaseScore:

    file = DataFrame(data=[], index = None, columns = None)

    def __init__(self, patientID, testAll, patientAge, patientW, duration, diseaseType):
        self.patientID = patientID
        self.testAll = testAll
        self.patientAge = patientAge
        self.patientW = patientW
        self.duration = duration
        self.diseaseType = diseaseType
    
    def readFile(filename, colName = "NAME", colName2 = "CLID"):
        try:
            geneExp = read_csv(filename, sep="\t", header = 0)
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
                            dt = dataCropped3.iloc[n]
                            dt = DataFrame(data = dt)
                            dt = dt.T
                            dataCropped2 = concat([dataCropped2, dt])
            dataCropped = dataCropped2.drop_duplicates()
            return dataCropped
        except:
            return 1
               
    def readGeneExp(self, patientID, file, colName = "NAME", colName2 = "CLID"):
        try:
            if type(file) == DataFrame :
                geneExp = file
                geneExp = geneExp[[colName, colName2, patientID]]
                return geneExp
            elif file == 1 :
                return 1
        except KeyError:
            return 2
       
    def concatenator(self, geneExp, geneList, colName = "NAME"):
        dt = DataFrame(data=[])
        for i in geneList:
            dts = geneExp.loc[geneExp[colName] == i]
            dt = concat([dt, dts])
        return dt        
        
    
    def score(self):
        geneExp = self.readGeneExp(self.patientID, self.file)
        if type(geneExp) != DataFrame :
            if geneExp == 1 :
                return "Not calculated. Data file is not in the right format."
            elif geneExp == 2 :
                return "Not calculated. Patient ID not found in the data file."
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
        score = round(score, 2)       
        interface.scoreVal = score
        return score

class diagnosis:

    filename = "data.txt"
    file = DataFrame(data = [])
    oligos = ['A_23_P106', 'A_23_P109913', 'A_23_P119337', 'A_23_P121064',
       'A_23_P121716', 'A_23_P121869', 'A_23_P137248', 'A_23_P141520',
       'A_23_P147245', 'A_23_P15202', 'A_23_P153853', 'A_23_P162374',
       'A_23_P164421', 'A_23_P168306', 'A_23_P202170', 'A_23_P204689',
       'A_23_P211445', 'A_23_P213424', 'A_23_P213562', 'A_23_P218375',
       'A_23_P24616', 'A_23_P313632', 'A_23_P318380', 'A_23_P334218',
       'A_23_P358944', 'A_23_P360754', 'A_23_P370651', 'A_23_P39517',
       'A_23_P40174', 'A_23_P56630', 'A_23_P67618', 'A_23_P74138',
       'A_23_P81408', 'A_23_P99985', 'A_24_P100535', 'A_24_P119094',
       'A_24_P13790', 'A_24_P201353', 'A_24_P201973', 'A_24_P244952',
       'A_24_P254437', 'A_24_P286114', 'A_24_P290163', 'A_24_P378202',
       'A_24_P508410', 'A_24_P658584', 'A_24_P90878', 'A_24_P942604',
       'A_24_P943263', 'A_32_P103633', 'A_32_P110872', 'A_32_P142818',
       'A_32_P148345', 'A_32_P164593', 'A_32_P24877', 'A_32_P25823',
       'A_32_P26443', 'A_32_P26895', 'A_32_P5976', 'A_32_P81173',
        'A_23_P414913', 'A_24_P237443', 'A_32_P168349', 'A_23_P414654', 'A_24_P192914']
    
    def __init__(self, patientID):
        self.patientID = patientID
        self.means = array([0.89668055555555604, 2.7477564101944445, 0.42805734777777787,
        -3.004166666666666, -2.5455405982777779, -0.48877020200000004, 1.3496616666666663,
        0.92047222222222225, -1.2332532051111114, -1.0537222222222222, 0.66252777777777772,
        0.18019444444444443, -0.0054350104722221976, -1.7747777777777776, 0.54261111111111093,
        2.7744166666666672, 0.65284014674999991, -1.4941944444444446, -1.0161326388888889,
        -0.39733333333333337, -1.1878722222222224, -1.5343888888888886, 4.4317436343055556,
        -0.27769444444444452, 0.57166666666666677, -1.958105691166667, 0.13010167713888887,
        0.35823863625000002, 0.28109356711111111, 1.5700534591111104, 1.3979473686666672,
        1.6852500000000001, 1.8683333333333323, 0.48199999999999998, -0.87810069444444416,
        -1.2418888888888893, 0.14661111111111105, 1.2593254716944446, 0.20028611111111125,
        0.029426624749999995, 1.2972437106944446, -2.021616161555555, 0.058405555555555551,
        2.8623573572222227, -0.88541666666666663, -0.089770833333333341, 0.40002604166666667,
        0.68178039833333348, 1.9050833333333337, -2.6663611111111107, 1.0399256944444444,
        -3.3888611111111109, -0.2467222222222222, -1.3254336915555551, 0.041638888888888927,
        -0.020693019833333333, -0.40506394130555556, 0.36911111111111111, 0.36255555555555558,
        1.1405518162499999])       
        self.scales = array([0.10471297759814276, 0.5463255257232309, 0.24158186884592453,
        0.45203475161392914, 0.98006642633574625, 0.42339650064394013, 0.43955610594666983,
        0.16984445271272169, 0.6144671325730332, 0.31908058988209576, 0.19719399445880009,
        0.20964902144145112, 0.28433232233680111, 0.56888873697914644, 0.18490392066298436,
        0.56138882222771613, 0.21204728621200503, 0.56240287158685087, 0.57124219718167968,
        0.28241281840596405, 0.30971077817422493, 0.29663429390579177, 1.0651136563834138,
        0.35353726971883309, 0.31603041344500726, 0.37611921100139595, 0.59193278557228479,
        0.24408025491993293, 0.42446581259077781, 0.52878754598537514, 0.29681831064572856,
        0.4006131671852815, 0.29813130962342377, 0.19428601482236324, 0.20455331335128737,
        0.31119240009444832, 0.16169059578538295, 0.32294035163926404, 0.35278703534441114,
        0.31340567254994556, 0.21765414113382184, 0.65840018146810897, 0.24157255402471675,
        0.47509570624383829, 0.26398341435695455, 0.26388694525965517, 0.21594052366380809,
        0.26225192776348571, 0.41006438349497154, 0.32255586534030367, 0.37688851277074703,
        1.0532297985186585, 0.38216834649369963, 0.72590528534468302, 0.92674727325612039,
        0.31678610880757635, 0.32480052984400637, 0.25693630617742358, 0.24132808977319703,
        0.36660896465856674])
        self.intercept = 0.777777777778
        self.coefs = [0.01241688856064207, -0.08564629722994202, 0.014817955092622036,
        0.0042768676152610784, -0.037956612017078992, 0.031146584900238306, -0.057858259745423135,
        0.020467348917758803, -0.025997131146060577, 0.030201549483987743, -0.010590175358090131,
        -0.017260468308836988, -0.020836141435402526, 0.034139129166309637, -0.01803449931996514,
        -0.034244000989035309, -0.0079182827076723118, -0.03038038704775026, -0.026430120028807343,
        -0.020931387084018593, -0.011122711561558618, -0.065472873982180352, 0.0036274970261607406,
        0.012814611884975877, -0.0031521090943366966, 0.0035117568336603469, 0.058493671261911774,
        0.05390833760046821, -0.0036882670308729971, 0.031541271698841113, -0.040212744724529126,
        0.038048363605863979, 0.01761122571450165, -0.011601195326526153, 0.032059359133897708,
        -0.0092715851147878794, 0.046789254041749516, -0.022504867444767804, 0.031526537461287078,
        -0.013473924196312808, -0.040196878603624614, 0.013364315794528419, 0.014424288021612431,
        0.019553383366054753, -0.023697571482513766, -0.02599286144439741, 0.042068804881449186,
        -0.011581826166080115, -0.014871453634994099, 0.0074665267348795715, -0.012801633930055123,
        0.0038508742579935057, 0.0043140038258145334, -0.064692875547348011, -0.0078655034838449912,
        0.087324656268292514, 0.035578981908016533, -0.0055424423852137991, 0.035423076171128845,
        0.052160357747815328]
        self.intercept_PAH = 0.305555555556
        self.coefs_PAH = [0.030798965441111756, -0.037593248681416808, -0.056519422778160827,
        -0.0018220833523548557, 0.013063577520360622, 0.041286232928798988, -0.011831090874405384,
        -0.016362415406335318, -0.05476925143826239, -0.053202392119545888, 0.0059733453536770474,
        0.0096932019815348831, 0.070930147187924592, 0.031035450610667925, 0.020132641006151385,
        -0.094843567985513549, 0.022432756393593517, 0.045325920959467289, -0.012642748944961401,
        0.011328200084889214, 0.013635678237179932, -0.022208169762119784, 0.030663036050460758,
        -0.046259058495366538, -0.024843020267117689, -0.012290916489525305, 0.022508616610874371,
        -0.04071047817729425, -0.024080631712289271, -0.0029845242078196076, 0.012706656919261679,
        -0.027253801631298265, -0.046589215148918998, 0.00046967022414273751, 0.00062690691841379639,
        -0.010404274616756255, 0.0029714519389829122, -0.015547504996973743, 0.05931629902460403,
        0.0050017593764783708, 0.020155412967860685, -0.0020595781281915367, 0.0033825168277304739,
        0.065155505208815828, -0.022768580787355129, -0.015463514962430938, -0.038884376056750131,
        0.010894569042881375, -0.054713138213540451, -0.043060098554802473, -0.034034019590693493,
        0.073482594212618657, 0.065078529725063228, 0.012571985661872911, 0.0034960934336166205,
        0.0010912222065603775, -0.010444515402710415, 0.00028211361409821376, 0.0046208386762301504,
        -0.0017396055351479494] 
        self.normprobes = ['A_23_P414913', 'A_24_P237443', 'A_32_P168349', 'A_23_P414654', 'A_24_P192914']
        self.means_sc = array([-3.2449249999999994, -1.3938491453611108, -3.7135482077777775,
        -7.145772222222222, -6.6871461538333339, -4.6303757575555551, -2.7919438888888894,
        -3.2211333333333325, -5.3748587606666671, -5.1953277777777753, -3.479077777777777,
        -3.9614111111111114, -4.147040566027778, -5.9163833333333331, -3.5989944444444442,
        -1.3671888888888892, -3.488765408805556, -5.6358000000000006, -5.1577381944444447,
        -4.5389388888888869, -5.3294777777777762, -5.6759944444444441, 0.29013807874999997,
        -4.419299999999998, -3.5699388888888888, -6.0997112467222214, -4.0115038784166659,
        -3.7833669193055561, -3.8605119884444443, -2.5715520964444445, -2.7436581868888896,
        -2.4563555555555552, -2.2732722222222215, -3.6596055555555549, -5.0197062499999987,
        -5.3834944444444428, -3.994994444444445, -2.8822800838611098, -3.9413194444444439,
        -4.1121789308055554, -2.8443618448611114, -6.1632217171111101, -4.0832000000000006,
        -1.2792481983333333, -5.0270222222222216, -4.2313763888888882, -3.7415795138888885,
        -3.4598251572222214, -2.2365222222222232, -6.8079666666666654, -3.1016798611111103,
        -7.5304666666666655, -4.3883277777777776, -5.4670392471111118, -4.0999666666666661,
        -4.1622985753888884, -4.5466694968611101, -3.7724944444444453, -3.7790500000000002,
        -3.0010537393055543]) 
        self.scales_sc = array([0.32110927646294418, 0.5864160162138331, 0.43843364177641958,
        0.56773457247551029, 0.97233373595869133, 0.57821896147039564, 0.50499089060693725,
        0.41179201330553045, 0.69290792590399919, 0.4923894803298563, 0.37528712941716086,
        0.40920315504497923, 0.33960251971868555, 0.46064480742879443, 0.40146384501972848,
        0.68078119334326237, 0.4235787523567201, 0.60351784103242934, 0.54652726825606257,
        0.37647801121990998, 0.38499172942856186, 0.42658411567581073, 0.98041344423807331,
        0.47600335082854189, 0.49715680919816307, 0.57493879444108553, 0.64189454883002539,
        0.40664880980567686, 0.49959575509326398, 0.634210197013371, 0.38274401037455047,
        0.40138700945350059, 0.42553681170644214, 0.33614459020589821, 0.43152781314761762,
        0.51361587134985331, 0.38787951590413305, 0.34496799491316976, 0.53539654245938961,
        0.48886667291932018, 0.33788170769156373, 0.74756285019602309, 0.37377517901065127,
        0.52352259511716803, 0.45530704115837578, 0.42317640911000409, 0.33949286282273466,
        0.39198939477789102, 0.5146183554134024, 0.5066111164723226, 0.37725624865137553,
        1.0469991329721551, 0.49916681725713419, 0.7863470948494391, 0.99534261047250538,
        0.45240353839807046, 0.43783228318564787, 0.42642165748134292, 0.44674186524957188,
        0.49362012760844326])

    def readFile2(filename):
        oligos = diagnosis.oligos
        test = read_csv(filename, header = 0, index_col = 0, sep = '\t', low_memory = False)
        test = test.ix[oligos]
        return test              

    def readFileDiagnosis(self, test, patientID):
        try:
            test = test[patientID].sort_index(axis = 0)
            normprobes_test = test.ix[self.normprobes]
            normprobes_test = [float(x) for x in normprobes_test.tolist()]
            test = test.astype(float)
            test_sc = test.subtract(mean(normprobes_test))
            test = test.drop(self.normprobes)
            test_sc = test_sc.drop(self.normprobes)
            test_header = test.index
            test = test.T
            test_sc = test_sc.T            
            test = ((array(test.as_matrix())) - self.means)/self.scales
            test_sc = ((array(test_sc.as_matrix())) - self.means_sc)/self.scales_sc
            test = DataFrame(data = test, columns = [patientID], index = test_header) 
            test_sc = DataFrame(data = test_sc, columns = [patientID], index = test_header)
            return test, test_sc
        except KeyError:
            return 'Patient ID not found in data file'

    def linearRegression(self, data, intercept, coefs):
        value = 0    
        for x, y in enumerate(data.index):
            a = coefs[x] * float(data.ix[y])
            value += a
        prediction = intercept + value
        return prediction

    def diagnose(self):
        try:
            data, data_sc = self.readFileDiagnosis(self.file ,self.patientID)                
            prediction_sc = self.linearRegression(data_sc, self.intercept, self.coefs) 
            prediction_pah = self.linearRegression(data, self.intercept_PAH, self.coefs_PAH)
            # Returning the diagnosis
            if prediction_sc > 1.0 :
                diagnosis_sc = ' is Scleroderma positive with a proability > 99%. '
            elif prediction_sc > 0.5 :
                diagnosis_sc = ' is Scleroderma positive with a probability of ' + str(round(prediction_sc * 100)) + '%. '
            elif 0.5 >= prediction_sc > 0 :
                diagnosis_sc = ' is Scleroderma negative with a probability of ' + str(round(100 - (prediction_sc * 100))) + '%. '
            else:
                diagnosis_sc = ' is Scleroderma negative with a proability > 99%. '
            if prediction_pah > 1.0 :
                diagnosis_pah = 'The probability for PAH is > 99%.'
            elif prediction_pah > 0.1 :
                diagnosis_pah = 'The probability for PAH is ' + str(round(prediction_pah * 100)) + '%.'
            else:
                diagnosis_pah = 'The probability for PAH is < 1%.'           
            if prediction_sc <= 0.5 :
                return 'Patient ' + self.patientID + diagnosis_sc
            else:
                return 'Patient ' + self.patientID + diagnosis_sc + diagnosis_pah                               
        except ValueError:
            return 'Patient ID not found in data file.'
        except:
            return 'Error calculating probabilities. Data file is in a wrong format or corrupt.'
        


class interface:

    scoreVal = 0.00

    def helpM(self):
        helpBox = Toplevel(self.top)
        w = 270
        h = 340
        helpBox.geometry('%dx%d+%d+%d' % (w, h, self.x, self.y))
        helpBox.wm_title("Help")
        helpBox.resizable(width=FALSE, height=FALSE)
        helpBox.iconbitmap('logo.ico')
        helpBox.configure(background = 'white')
        helpFrame = Frame(helpBox, background = 'white')
        helpFrame.grid(padx=1, pady=1, row = 0, column = 0)
        H1 = Label (helpFrame, text="The program can run in two modes. If the 'Diagnosis' tab is selected, the user can determine the overall diagnosis and the probability for pulmonary arterial hypertension. If the 'MRSS' tab is selected, the user can calculate the Modified Rodnan Skin Score." , justify = LEFT, wraplength = 255, background = 'white')
        H1.grid(row=0,column=0, padx=5, pady=5)
        H2 = Label (helpFrame, text="1. Begin by filling out the required input values. The MRSS algorithm can use either all of the supplied parameters or use only the gene expression values. The 'Disease duration' units are months. The program will notify the user of any missing values." , justify = LEFT, wraplength = 255, background = 'white')
        H2.grid(row=1,column=0, padx=5, pady=5)
        H3 = Label (helpFrame, text="2. The predictions will be shown in the output console. The user can also choose to save the results either in a simple .txt form when calculating the overall diagnosis or as a graphical .pdf file when calculating the MRSS." , justify = LEFT, wraplength = 255, background = 'white')
        H3.grid(row=2,column=0, padx=5, pady=5)
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
        A1 = Label (aboutFrame, text="August 8th, 2016  Karl Märka", justify = CENTER)
        A1.grid(row=1,column=0, padx=5, pady=2)
        button = ttk.Button(aboutBox, text="Close", command=aboutBox.withdraw)
        button.grid(row=5,column=0, padx=5, pady=5)

    def dataFile(self, function):
        try:       
            self.outputBox.config(state = 'normal')
            self.outputBox.delete('1.0', 'end')
            self.outputBox.insert('1.0 + 2 lines', 'Please wait. Reading data...')
            self.outputBox.config(state = 'disabled')
            fileObj = filedialog.askopenfile()
            filename = fileObj.name
            filename = str(filename)
            q = Queue()
            db = Process(target=q.put, args=(function(filename),))
            db.start()        
            db.join
            file = q.get()
            diseaseScore.file, diagnosis.file = file, file
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
            patientID = patientID.strip()
            patientAge = self.E2.get()
            duration = self.E3.get()
            output = diseaseScore(str(patientID), gene, int(patientAge), int(raceVal), int(duration), int(typeVal)).score()    
            output = "Patient " + str(patientID) + " disease score: " + str(output)
            self.outputBox.config(state = 'normal')
            self.outputBox.insert('1.0 + 2 lines', output)
            self.outputBox.insert('2.0 + 2 lines', '\n\nAll patient data was used in calculating the final score.')

    def useGene(self):
        gene = self.options1[self.geneExp.get()]
        self.outputBox.config(state = 'normal')
        self.outputBox.delete('1.0', 'end')
        patientID = self.E1.get()
        patientID = patientID.strip()
        output = diseaseScore(str(patientID), gene, 1, 1, 1, 1).score()
        try:           
            output = "Patient " + str(patientID) + " disease score: " + str(output)
            self.outputBox.insert('1.0 + 2 lines', output)
            self.outputBox.insert('3.0 + 2 lines lineend', '\n\nOnly gene expression data was used in calculating the final score.')
        except:
            self.outputBox.insert('1.0 + 2 lines', output)

    def putDiagnosis(self):
        try:        
            platform = self.options4[self.platformVar.get()]
            if platform == "agi":
                patientID = self.E1_1.get()
                patientID = patientID.strip()
                output = diagnosis(str(patientID)).diagnose()
                self.outputBox.config(state = 'normal')
                self.outputBox.insert('1.0 + 2 lines', output)
                self.B6.config(state = 'normal')
            elif platform == "ilu":
                output = "Illumina platform not yet implemented."
                self.outputBox.config(state = 'normal')
                self.outputBox.insert('1.0 + 2 lines', output)
                self.B6.config(state = 'normal')
                self.B5.config(state = 'disabled')
        except KeyError:
            output = "Please select a platform."
            self.outputBox.config(state = 'normal')
            self.outputBox.insert('1.0 + 2 lines', output)
                           
  
    def click(self):
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
        self.B5.config(state = 'disabled')



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
                x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,
                    32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,
                    60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,
                    89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,
                    113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,
                    135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,
                    157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,
                    179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,
                    201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222]
                y = [0,0,3,3,3,4,4,5,5,5,5,6,6,8,8,9,9,9,10,10,11,12,12,12,12,12,12,13,13,13,13,13,14,14,15,
                    15,15,15,16,16,16,17,17,17,18,18,18,18,18,19,19,19,19,19,20,20,20,20,21,21,22,23,23,24,
                    24,24,24,25,25,25,25,25,26,26,26,26,26,27,27,27,27,27,27,27,27,27,28,28,28,28,28,28,28,
                    28,29,29,29,29,29,29,29,29,29,30,30,30,30,31,31,31,31,31,32,32,32,32,32,33,33,33,33,33,
                    33,33,33,34,34,34,34,34,34,34,34,34,34,34,34,34,34,35,35,35,35,35,35,35,35,35,35,35,35,
                    36,36,36,36,36,36,37,37,37,37,37,37,37,37,38,38,38,38,38,38,38,39,39,39,39,39,39,39,39,
                    39,39,40,40,40,40,40,41,41,41,41,41,41,41,41,42,42,42,42,42,43,43,43,43,43,43,44,44,44,
                    44,45,45,45,46,46,47,47,49,49,50,50,51]
                limit = 222
                val1 = 4.6068*score - 11
                val2 = 4.6068*score - 10
            else:
                score = 45.93 * score - 80.843
                content = str(self.outputBox.get('1.0', 'end')) + '\n\n' + str(dateStamp)
                x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,
                    32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,
                    61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,
                    90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,
                    114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,
                    136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,
                    158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,
                    180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,
                    202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,
                    224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,
                    246,247,248,249,250,251,252,253,254,255,256,257,258,259,260]
                y = [0,0,1,1,1,2,2,4,4,4,5,5,5,5,5,5,5,5,5,6,7,7,7,8,8,8,8,9,9,9,9,10,10,11,11,11,11,11,11,
                    12,12,12,12,12,12,12,12,13,13,13,13,13,13,14,14,14,15,15,15,15,15,15,15,15,16,16,16,16,
                    16,16,17,17,17,17,17,17,17,17,17,17,17,17,18,18,18,18,18,19,19,19,19,19,19,19,19,19,19,
                    19,19,19,19,20,20,20,20,20,20,20,20,20,21,21,21,21,21,21,21,21,21,21,21,22,22,22,22,22,
                    22,22,22,23,23,23,23,23,23,23,23,23,23,23,23,23,23,24,24,24,24,24,24,24,24,24,24,24,24,
                    25,25,25,25,25,25,25,26,26,26,26,26,26,26,26,26,26,26,26,26,27,27,27,27,27,27,27,27,27,
                    27,28,28,28,28,28,28,28,28,29,29,29,29,30,30,30,30,31,31,31,31,31,31,31,31,31,31,32,32,
                    32,32,32,32,32,32,32,33,33,33,33,34,34,34,34,35,35,35,35,35,36,36,36,36,36,37,37,37,38,
                    38,38,39,39,39,39,40,41,41,42,42,43,43,44,44,48,50,51]
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

    def click2(self):
        if self.notebook.index(self.notebook.select()) == 1:
            self.dataFile(diseaseScore.readFile)
        elif self.notebook.index(self.notebook.select()) == 0:
            self.dataFile(diagnosis.readFile2)

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
        diagnosisfield = LabelFrame(frame1, width = 285, text = "Patient Data:")
        diagnosisfield.grid(padx=10, pady=5, row = 0, column = 0)
        L1 = Label (inputfield, text="Patient ID:")
        L1.grid(row=0,column=0, padx=5, pady=5)
        L1_1 = Label (diagnosisfield, text="Patient ID:")
        L1_1.grid(row=0,column=0, padx=23, pady=5)
        L2_1 = Label (diagnosisfield, text="")
        L2_1.grid(row=2,column=0, padx=23, pady=55)
        self.E1_1 = ttk.Entry(diagnosisfield)
        self.E1_1.grid(row=0,column=1, padx=16, pady=5)
        self.E1_1.entrytext = StringVar()
        self.E1 = ttk.Entry(inputfield)
        self.E1.grid(row=0,column=1, padx=16, pady=5)
        self.E1.entrytext = StringVar()
        L2_1 = Label (diagnosisfield, text="Platform:")
        L2_1.grid(row=1,column=0, padx=5, pady=5)
        self.platformVar = StringVar(diagnosisfield)
        self.options4 = {"Agilent": "agi", "Illumina": "ilu"}
        O1_1 = ttk.Combobox(diagnosisfield, state = 'readonly', width = 17, textvariable = self.platformVar, values = (list(self.options4.keys()))).grid(row=1,column=1, padx=1, pady=1)
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
        B7 = ttk.Button(inputfield, text ="Expression data...", command=self.click2)
        B7.grid(row=6,column=1, padx=15, pady=6)
        B7_1 = ttk.Button(diagnosisfield, text ="Expression data...", command=self.click2)
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