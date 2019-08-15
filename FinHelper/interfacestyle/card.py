# Card - Labels
def cardappearence():
    styleList = []
    styleList.append({
        'selectorStr':["QLabel"],
        'idStr':["CardCategoryLbl"],
        'classStr':[""],
        'descendantStr':[""],
        'childStr':[""],
        'propStr':[{}, {}],
        'propertyDic':{"font": "63 7pt \"Segoe UI Semibold\";"}
    })
    styleList.append({
        'selectorStr':["QLabel"],
        'idStr':["CardDateLbl"],
        'classStr':[""],
        'descendantStr':[""],
        'childStr':[""],
        'propStr':[{}, {}],
        'propertyDic':{"font-style": "italic"}
    })
    styleList.append({
        'selectorStr':["QLabel"],
        'idStr':["CardCurrencyLbl"],
        'classStr':[""],
        'descendantStr':[""],
        'childStr':[""],
        'propStr':[{}, {}],
        'propertyDic':{"font-weight":"bold"}
    })
    styleList.append({
        'selectorStr':["QLabel"],
        'idStr':["CardCommentLbl"],
        'classStr':[""],
        'descendantStr':[""],
        'childStr':[""],
        'propStr':[{}, {}],
        'propertyDic':{"text-decoration": "underline"}
    })
    styleList.append({
        'selectorStr':["QLabel"],
        'idStr':["CardBankLbl"],
        'classStr':[""],
        'descendantStr':[""],
        'childStr':[""],
        'propStr':[{}, {}],
        'propertyDic':{"font-family": "Times New Roman"}
    })
    styleList.append({
        'selectorStr':["QLabel"],
        'idStr':["CardPositive"],
        'classStr':[""],
        'descendantStr':[""],
        'childStr':[""],
        'propStr':[{}, {}],
        'propertyDic':{"color": "green", "font-weight":"bold"}
    })
    styleList.append({
        'selectorStr':["QLabel"],
        'idStr':["CardNegative"],
        'classStr':[""],
        'descendantStr':[""],
        'childStr':[""],
        'propStr':[{}, {}],
        'propertyDic':{"color": "red"}
    })
    return styleList

if __name__ == '__main__':
    from PySide2 import QtWidgets
    import style

    class test(QtWidgets.QFrame):
        def __init__(self):
            super().__init__()
            self.cardWidth = 200

    financHelper = QtWidgets.QApplication([])
    parent = test()
    templateData = {'Category':'Academia','Value':00,'Date':'10/10/2010','Comment':'Template', 'AccName':'Conta', 'AccType':1}
    cardTemplate = Card.Card(parent, templateData, 'Template')
    parent.show()
    financHelper.exec_()