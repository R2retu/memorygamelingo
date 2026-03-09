from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'main.py Original', 0, 1, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Courier', '', 8)

with open('main_py_jugando bien en desdktop.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.encode('latin-1', 'replace').decode('latin-1')
        line = line.replace('\n', '')
        pdf.cell(0, 4, txt=line, new_x="LMARGIN", new_y="NEXT")

pdf.output("main_original.pdf")
