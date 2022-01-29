from fpdf import FPDF
import os


class PDF(FPDF):
    pdf_w=210
    pdf_h=297
    def lines(self):
        self.set_line_width(0.0)
        self.line(5.0,5.0,205.0,5.0)
        self.line(5.0,292.0,205.0,292.0)
        self.line(5.0,5.0,5.0,292.0)
        self.line(205.0,5.0,205.0,292.0)

        self.line(10.0,80.0,185.0,80.0)
        self.set_line_width(0.5)
        self.line(5.0,60.0,205.0,60.0)

    
    def imagex(self):
        self.set_xy(6,6)
        self.image('static/pictures/logoVelke_trans.png', link='', type='', w=1586/40, h=1920/40)

    def rectitle(self,data):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0,0,0)
        self.cell(w=210.0, h=40.0, align='C', txt="Danovy doklad c. "+data["rec_id"])
    
    def acceptedby(self,data):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0,0,0)
        self.cell(w=210.0, h=60.0, align='C', txt="Vyhotovil "+data["user"])


    def labels(self):
        self.set_xy(0.0,0.0)
        self.set_font('Arial','', 11)
        self.set_text_color(0,0,0)
        self.cell(w=40.0, h=155.0, align='C', txt="Polozka")
        self.cell(w=70.0, h=155.0, align='C', txt="Pocet")
        self.cell(w=90.0, h=155.0, align='C', txt="Cena")
        
    def itemData(self,item,i):
        self.set_xy(0.0,0.0)
        self.set_font('Arial','', 11)
        self.set_text_color(0,0,0)
        self.cell(w=40.0, h=175.0+(i*20.0), align='C', txt=item[1])
        self.cell(w=70.0, h=175.0+(i*20.0), align='C', txt="1")
        self.cell(w=90.0, h=175.0+(i*20.0), align='C', txt=item[3]+" CZK")

    def labels2(self):
        self.set_xy(0.0,0.0)
        self.set_font('Arial','', 11)
        self.set_text_color(0,0,0)
        self.cell(w=330.0, h=20.0, align='C', txt="Datum: ")

    def labels3(self,data):
        self.set_xy(0.0,0.0)
        self.set_font('Arial','', 11)
        self.set_text_color(0,0,0)
        self.cell(w=380.0, h=20.0, align='C', txt=data["date"])

    def labels4(self,i):
        self.set_xy(0.0,0.0)
        self.set_font('Arial','', 11)
        self.set_text_color(0,0,0)
        self.cell(w=265.0, h=175.0+(i*20.0), align='C', txt="Celkem:")
    
    def costsSum(self,data,i):
        self.set_xy(0.0,0.0)
        self.set_font('Arial','', 11)
        self.set_text_color(0,0,0)
        self.cell(w=310.0, h=175.0+(i*20.0), align='C', txt=data["sum"]+" CZK")



def createPDF(data):
    pdf = PDF(format='A4',unit='mm',orientation='P' )
    pdf.add_page()
    pdf.lines()
    pdf.imagex()
    pdf.rectitle(data)
    pdf.acceptedby(data)
    pdf.labels()
    pdf.labels2()
    pdf.labels3(data)
    i=0
    for i,item in enumerate(data["items"]):
        pdf.itemData(item,i)
    pdf.labels4(i+1)
    pdf.costsSum(data,i+1)
    
    pdf.output('static/receipts/'+data["name"]+'.pdf', dest='F')

def openPDF(data):
    os.startfile(os.path.dirname(__file__)[:-6]+'/static/receipts/'+data["name"]+'.pdf')