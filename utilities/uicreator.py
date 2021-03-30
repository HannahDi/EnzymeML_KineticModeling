import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Button, interact
from tkinter import Tk, filedialog

class UICreator:
    def __init__(self, nbH):
        self.nbH = nbH
        
    def convertUI(self):
        self.outConverter = widgets.Output()
        # text field to enter EnzymeML name
        self.textOmexName = widgets.Text(
            value='',
            placeholder='name.omex',
            description='OmexName:',
            disabled=False
        )
        # button to open directory, to select excel file
        buttonSelExcel = widgets.Button(
            description='Select Excel File',
            disabled=False,
            button_style='',
            tooltip='Click me',
            icon=''
        )
        if self.nbH.getWorkspace() is None:
            with self.outConverter:
                print('Workspace not set!')
        buttonSelExcel.on_click(self._convertExcel2Omex)
        display(self.textOmexName, buttonSelExcel)
        display(self.outConverter)

    def _convertExcel2Omex(self, b):
        self.outConverter.clear_output()   
        root = Tk()
        root.withdraw()                                        # Hide the main window.
        root.call('wm', 'attributes', '.', '-topmost', True)   # Raise the root to the top of all windows.
        b.excelPath = filedialog.askopenfilename(filetypes=[("Excel files", ".xls .xlsx .xlsm")],multiple=False)    # List of selected files will be set button's file attribute.
        self.omexName = self.textOmexName.value
        reqResponse=self.nbH.convertSpreadsheet(b.excelPath, self.omexName)
        if reqResponse == 200:
            with self.outConverter:
                print('Omex created; EnzymeML document loaded')
        else:
            with self.outConverter:
                print('Conversion failed. API Error: '+str(reqResponse))

    def workspaceButton(self):
        self.outWorkspace = widgets.Output()
        self.outWorkspace.clear_output()
        buttonWorkspace = widgets.Button(
            description='Set Workspace',
            disabled=False,
            button_style='',
            tooltip='',
            icon=''
        )
        buttonWorkspace.on_click(self._setWorkspace)
        display(buttonWorkspace, self.outWorkspace)
    
    def _setWorkspace(self,b):
        #button preparation
        self.outWorkspace.clear_output()
        root = Tk()
        root.withdraw()                                        # Hide the main window.
        root.call('wm', 'attributes', '.', '-topmost', True)   # Raise the root to the top of all windows.
        b.path = filedialog.askdirectory()
        with self.outWorkspace:
            if len(b.path) != 0:
                print('Workspace: ' + str(b.path))
                self.nbH.setWorkspace(b.path)
            else:
                self.nbH.setWorkspace(None)
                print('Workspace not set!')