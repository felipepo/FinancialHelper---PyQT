from utilities import funs
import random
from interfacestyle import card
# import os.path
# QssExist = os.path.exists("FinHelper/data/style/Style.qss")

class Create():
    # Class to customize the interface. It works using a dictionary with the following format
    # stylesDict = {
    #     'selectorStr':"",
    #     'idStr':"",
    #     'classStr':"",
    #     'descendantStr':"",
    #     'childStr':"",
    #     'propStr':propStr,
    #     'propertyDic':propertyDic
    # }
    # rgb(255, 255, 127)

    def __init__(self, allCategories):
        self.allCategories = allCategories
        self.styleFile = "FinHelper/data/style/Style.qss"
        self.InterfaceStyle = ""
        self.widgetStyles = []
        try:
            self.readQSS()
        except:
            self.createQSS()

    def readQSS(self):
        with open(self.styleFile,"r") as fh:
            self.InterfaceStyle = fh.read()

    def createQSS(self):
        stringQSS = ""
        styledicts = self.defaultStyle()
        for iStyle in range(len(styledicts)):
            stringQSS = stringQSS + self.createStyle(styledicts[iStyle])

        self.InterfaceStyle = stringQSS
        self.createQSSFile()

    def createQSSFile(self):
        with open(self.styleFile,"w+") as fh:
            fh.write(self.InterfaceStyle)

    def appendStyle(self,styledict):
        self.InterfaceStyle = self.InterfaceStyle + self.createStyle(styledict)

    def renameStyle(self, oldName, newName):
        # Change in QSS
        self.InterfaceStyle = self.InterfaceStyle.replace(oldName, newName)

    def removeStyle(self, styleName):
        # Remove in Category Class
        pass
        # Remove in QSS

    def createStyle(self, stylesDict):
        propertyDic = stylesDict['propertyDic']
        selectorString = self.createSelector(stylesDict)

        particularStyle = """selectorString {
    property: propertyValue;
}\n"""

        particularStyle = particularStyle.replace('selectorString', selectorString)

        countProps = 0
        for key in list(propertyDic.keys()):
            if countProps > 0:
                particularStyle = particularStyle.replace(";",  ";\n    property: propertyValue;", 1)
            particularStyle = particularStyle.replace("propertyValue", propertyDic[key])
            particularStyle = particularStyle.replace("property", key)
            countProps += 1

        return particularStyle

    def defaultStyle(self):
        # Set the default style for the interface
        styleList =[]
        # QPushButton
        # QFrame
        # QLabel
        # QGroupBox
        # QComboBox
        # QTabWidget
        # QStackedWidget
        # Category - Related
        for iCategory in self.allCategories:
            color = self.allCategories[iCategory]
            currCat = funs.formatCategoryName(iCategory)
            styleList.append({
                'selectorStr':["QFrame"],
                'idStr':[currCat],
                'classStr':[""],
                'descendantStr':[""],
                'childStr':[""],
                'propStr':[{}],
                'propertyDic':{'background-color':color}
            })
            styleList.append({
                'selectorStr':["QLabel"],
                'idStr':['Color'+currCat],
                'classStr':[""],
                'descendantStr':[""],
                'childStr':[""],
                'propStr':[{}],
                'propertyDic':{'background-color':color, "border":"2px solid black"}
            })
        styleList = styleList + card.cardappearence()
        return styleList

    def getStyle(self, selectorStr="", idStr="", classStr="", descendantStr="", childStr="", propStr={}, propertyDic={}):
        stylesDict = {
            'selectorStr':[selectorStr],
            'idStr':[idStr],
            'classStr':[classStr],
            'descendantStr':[descendantStr],
            'childStr':[childStr],
            'propStr':[propStr],
            'propertyDic':propertyDic
        }
        return stylesDict

    def createSelector(self,stylesDict):
        selectorStr = stylesDict['selectorStr']
        idStr = stylesDict['idStr']
        classStr = stylesDict['classStr']
        descendantStr = stylesDict['descendantStr']
        childStr = stylesDict['childStr']
        propStr = stylesDict['propStr']

        for iWidget in range(len(selectorStr)):
            particularSelector = 'selectorStridStrclassStrpropStr'
            if idStr[iWidget]:
                idStr[iWidget] = "#" + idStr[iWidget]
            if classStr[iWidget]:
                classStr[iWidget] = "." + classStr[iWidget]
            if descendantStr[iWidget]:
                descendantStr[iWidget] = descendantStr[iWidget] + " > " + selectorStr[iWidget]
            if childStr[iWidget]:
                childStr[iWidget] = childStr[iWidget] + " > " + selectorStr[iWidget]
            if not propStr[iWidget]:
                propStr[iWidget] = ""
            else:
                for key in list(propStr[iWidget].keys()):
                    value = propStr[iWidget][key]
                    propStr = '''[key="value"]'''
                    propStr = propStr.replace('key',key)
                    propStr = propStr.replace('value',value)

            replaces = ('selectorStr', 'idStr', 'classStr', 'propStr')
            repValues = {
                'selectorStr':selectorStr[iWidget],
                'idStr':idStr[iWidget],
                'classStr':classStr[iWidget],
                'propStr':propStr[iWidget]}

            for iRep in replaces:
                particularSelector = particularSelector.replace(iRep, repValues[iRep])

            if iWidget > 0:
                resultSelector = resultSelector + ', ' + particularSelector
            else:
                resultSelector = particularSelector

        return resultSelector

class testingCats():
    def __init__(self):
        self.category = {
            "Feira": 'rgb(255, 200, 127)',
            "Transporte": 'rgb(200, 255, 127)',
            "Remedio": 'rgb(255, 255, 200)',
            "Academia": 'rgb(255, 155, 127)',
            "Aluguel": 'rgb(155, 255, 127)',
            "Condominio": 'rgb(155, 155, 127)',
            "Telefone": 'rgb(200, 200, 127)',
            "Internet": 'rgb(55, 255, 127)',
            "Luz": 'rgb(255, 55, 127)',
            "Outros": 'rgb(55, 55, 127)'
            }

if __name__ == "__main__":
    allCategories = testingCats()
    style = Create(allCategories)