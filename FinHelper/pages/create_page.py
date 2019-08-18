from . import standard_page

class CreditPage(standard_page.StandarPage):
    def __init__(self, parent):
        super().__init__(parent, "CreditPage")

class DebitPage(standard_page.StandarPage):
    def __init__(self, parent):
        super().__init__(parent, "AccPage")