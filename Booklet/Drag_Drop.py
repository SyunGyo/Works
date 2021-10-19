from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import StringProperty
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

def create_booklet(pdf_path,output_path):
    pdf_reader = PdfFileReader(pdf_path)
    pdf_writer = PdfFileWriter()
    pdf_writer.appendPagesFromReader(pdf_reader)

    Num = pdf_reader.numPages % 4

    if Num != 0:
        for i in range(int(4 - Num)):
            pdf_writer.addBlankPage()
    
    Num_Pages = pdf_writer.getNumPages() 
    booklet = PdfFileWriter()   
    for i in range(Num_Pages // 4):        
        booklet.addPage(pdf_writer.getPage(int(Num_Pages - 2 * i - 1)))
        booklet.addPage(pdf_writer.getPage(int(2 * i)))
        booklet.addPage(pdf_writer.getPage(int(2 * i + 1)))
        booklet.addPage(pdf_writer.getPage(int(Num_Pages - 2 * i - 2)))
     
    with open(output_path, 'wb') as fh:
        booklet.write(fh)

class MyRoot(BoxLayout):
    file_path = StringProperty("")

class Booklet_CreatorApp(App):    
    def build(self):
        self.title  = "Booklet Creator"
        Window.bind(on_dropfile=self._on_file_drop)

    def _on_file_drop(self, window, file_path):
        pdf_path = file_path.decode("utf-8")
        output_path = os.getcwd() + "/.output/booklet.pdf"

        create_booklet(pdf_path,output_path)
        os.system("open " + output_path)

if __name__ == "__main__":
    Booklet_CreatorApp().run()