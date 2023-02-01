from fpdf import FPDF
from pathlib import Path
from io import BytesIO

def create_receipt(order):
    '''Create a PDFreceipt for the given order.'''

    date_format = "%d.%m.%Y"
    pdf_config = {
        'line_height': 8,
        'margin_left': 70,
        'font_size_logo': 7.5,
        'font_size': 11
    }

    logo_path = str(Path(__file__).resolve().parent.parent.parent) + '/app/static/images/logo/fub.png'

    pdf = FPDF()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_author('ICT Warrior Academy')
    pdf.set_subject('Quittung')
    pdf.add_page()

    # Logo
    pdf.image(logo_path, w = 80, type = 'PNG', link = '')

    # pdf.set_font('Arial', '', pdf_config['font_size_logo'])
    # pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], 'Eidgenössisches Departement für')
    # pdf.ln(h = 4)
    # pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], 'Verteidigung, Bevölkerungsschutz und Sport VBS')

    # pdf.ln(h = 6)
    # pdf.set_font('Arial', 'B', pdf_config['font_size_logo'])
    # pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], 'Schweizer Armee')
    # pdf.ln(h = 4)
    # pdf.set_font('Arial', '', pdf_config['font_size_logo'])
    # pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], 'Führungsunterstützungsbasis FUB')

    pdf.ln(30)

    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], 'Quittung Ausleihe ICT Warrior Academy')

    pdf.ln(30)

    # Content
    pdf.set_font('Arial', '', pdf_config['font_size'])  
    pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], f'Hiermit bestätigt:')
    pdf.set_font('Arial', 'I', pdf_config['font_size'])  
    pdf.cell(180, pdf_config['line_height'], f'{order.user.first_name} {order.user.last_name}')
    pdf.ln(pdf_config['line_height'])
    pdf.set_font('Arial', '', pdf_config['font_size'])  
    pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], f'Adresse:')
    pdf.set_font('Arial', 'I', pdf_config['font_size'])  
    pdf.cell(150, pdf_config['line_height'], f'{order.user.email}')

    pdf.ln(2 * pdf_config['line_height'])

    pdf.set_font('Arial', '', pdf_config['font_size'])
    pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], f'den Erhalt:')
    pdf.set_font('Arial', 'I', pdf_config['font_size'])  
    pdf.cell(150, pdf_config['line_height'], f'{order.item.name}')
    pdf.ln(pdf_config['line_height'])
    pdf.set_font('Arial', '', pdf_config['font_size'])  
    pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], f'Interne Bezeichnung:')
    pdf.set_font('Arial', 'I', pdf_config['font_size'])  
    pdf.cell(150, pdf_config['line_height'], f'{order.item.description}')

    pdf.ln(2 * pdf_config['line_height'])

    pdf.set_font('Arial', '', pdf_config['font_size'])
    pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], f'für die Nutzung im Rahmen:')
    pdf.set_font('Arial', 'I', pdf_config['font_size'])  
    pdf.cell(150, pdf_config['line_height'], f'{order.item.name}')
    pdf.ln(pdf_config['line_height'])
    pdf.set_font('Arial', '', pdf_config['font_size'])
    pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], f'für die Dauer:')
    pdf.set_font('Arial', 'I', pdf_config['font_size'])  
    pdf.cell(150, pdf_config['line_height'], f'{order.started_at.strftime(date_format)} - {order.ended_at.strftime(date_format)}')


    pdf.ln(5 * pdf_config['line_height'])


    #Signatures
    pdf.set_font('Arial', '', pdf_config['font_size'])
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + pdf_config['margin_left'], pdf.get_y())
    pdf.line(pdf.get_x() + 1.5 * pdf_config['margin_left'], pdf.get_y(), pdf.get_x() + 2.4 * pdf_config['margin_left'], pdf.get_y())
    pdf.cell(pdf_config['margin_left'] * 1.5, pdf_config['line_height'], f'Unterschrift Herausgeber/in')
    pdf.cell(pdf_config['margin_left'], pdf_config['line_height'], f'Unterschrift Empfänger/in')


    return BytesIO(bytes(pdf.output(dest = 'S'), encoding='latin1'))

