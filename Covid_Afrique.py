from arcpy import*
from arcpy.mapping import*
import os
import datetime
i=0
j=0
a=0
b=0
startTime=GetParameterAsText(1)
endTime=GetParameterAsText(2)
pdf=GetParameterAsText(3)
mxd=arcpy.mapping.MapDocument(arcpy.GetParameterAsText(0))
x=startTime.split('/',3)
X=endTime.split('/',3)
fileName ="atlas.pdf"
pdfdoc=PDFDocumentCreate(os.path.join(pdf,fileName))
Daily=ListDataFrames(mxd)[0]
Total=ListDataFrames(mxd)[1]
env.workspace="rC:\Users\hp\Downloads\convexHull\data\QS.gdb"
MakeFeatureLayer_management ("COVID19", "covid1")
if datetime.datetime(int(X[2]),int(X[1]),int(X[0]))>datetime.datetime(2020,04,19) or datetime.datetime(int(x[2]),int(x[1]),int(x[0]))<datetime.datetime(2020,02,14)or datetime.datetime(int(X[2]),int(X[1]),int(X[0]))< datetime.datetime(int(x[2]),int(x[1]),int(x[0])): 
    arcpy.AddError("Vous avez spécifier des dates erronées (date début supérieure à date fin, date qui n’est pas incluse dans la fourchette des données.....")                                                                                                                                                                       
else :
    Daily.time.currentTime =datetime.datetime(int(x[2]),int(x[1]),int(x[0]))
    Total.time.currentTime =datetime.datetime(int(x[2]),int(x[1]),int(x[0]))
    while Daily.time.currentTime <=datetime.datetime(int(X[2]),int(X[1]),int(X[0])) :
        with da.SearchCursor("covid1",["Date","SUM_Daily_Cases","SUM_Total_Cases"])as cursor: 
            for row in cursor:
                if (row[0]==Daily.time.currentTime):
                    a=a+row[1]
                    b=b+row[2]
                    ListLayoutElements(mxd,"TEXT_ELEMENT")[0].text= "cas journaliere :"+str(a)+"cas cumulé :"+str(b)
                a=0
                b=0
        i=i+1
        for elm in ListLayoutElements(mxd,"TEXT_ELEMENT"):
            if elm.text==str(j) :
                elm.text=str(i)
        j=j+1
        fileName = str(Daily.time.currentTime).split(" ")[0] + "MJT.pdf"
        ExportToPDF(mxd,os.path.join(pdf,fileName))
        pdfdoc.appendPages(os.path.join(pdf,fileName))
        Daily .time.currentTime =Daily.time.currentTime+datetime.timedelta(days=1)
        Total.time.currentTime =Total.time.currentTime+datetime.timedelta(days=1)
        
    pdfdoc.insertPages (r"C:\Users\hp\Desktop\page1.pdf")
    pdfdoc.appendPages(r"C:\Users\hp\Desktop\FIN.pdf")
    
del mxd


