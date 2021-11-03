'''
This program is based on
kivy: https://github.com/kivy/kivy

and

PyPDF2: https://github.com/mstamy2/PyPDF2/

Mac OS is assumed for this program.
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

def create_booklet(pdf_path,output_path):
    pdf_reader = PdfFileReader(pdf_path)
    pdf_writer = PdfFileWriter()
    pdf_writer.appendPagesFromReader(pdf_reader)

    Num_addPages = 4 - (pdf_reader.numPages % 4)

    if Num_addPages != 4:
        for i in range(int(Num_addPages)):
            pdf_writer.addBlankPage()
    
    Num_Pages = pdf_writer.getNumPages() 
    booklet = PdfFileWriter()   
    for i in range(Num_Pages // 4):        
        booklet.addPage(pdf_writer.getPage(int(Num_Pages - 2 * i - 1)))
        booklet.addPage(pdf_writer.getPage(int(2 * i)))
        booklet.addPage(pdf_writer.getPage(int(2 * i + 1)))
        booklet.addPage(pdf_writer.getPage(int(Num_Pages - 2 * i - 2)))

    output_path += "booklet.pdf"
    with open(output_path, 'wb') as fh:
        booklet.write(fh)

class MyLabel(Label):
    def __init__(self):
        super(MyLabel,self).__init__()
        self.text = "Drag & Drop \n a PDF file !"
        self.font_size = '60'
        self.valign = 'middle'
        self.halign = 'center'

class Booklet_CreatorApp(App):    
    def build(self):
        self.title  = "Booklet Creator"
        Window.bind(on_dropfile=self._on_file_drop)
        Window.size = (400,300)

        
        BaseLabel = MyLabel()
        MyLayout = BoxLayout()
        MyLayout.orientation = 'vertical'
        MyLayout.add_widget(BaseLabel)
        
        return MyLayout
    
    def _on_file_drop(self, window, file_path):     
        pdf_path = file_path.decode("utf-8")

        if pdf_path[-4::] == ".pdf":
            if(PdfFileReader(pdf_path).isEncrypted == False) :

                output_path = os.getcwd() + "/.output/"
                if os.path.exists(output_path) == False:
                    os.mkdir(output_path)
                    
                create_booklet(pdf_path,output_path)
                os.system("open " + output_path + "booklet.pdf")
                self.root.children[0].text = "Converted!\n\nAdd a new File"
            else :
                self.root.children[0].text = "The file is Encrypted\n\nRetry after a decryption"
        else:
            self.root.children[0].text = "Not a PDF\n\nAdd a PDF File"
    
if __name__ == "__main__":
    Booklet_CreatorApp().run()