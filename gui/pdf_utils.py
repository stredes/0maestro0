from fpdf import FPDF
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Logo opcional
        if os.path.exists("assets/logo.png"):
            self.image("assets/logo.png", 10, 8, 33)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Laboratorio Clínico - Informe de Resultados', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def generar_informe_pdf(nombre_paciente, rut, fecha_nacimiento, historial, nombre_tecnologo):
    if not os.path.exists("informes"):
        os.makedirs("informes")

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"informes/Informe_{nombre_paciente.replace(' ', '_')}_{fecha_actual}.pdf"

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Datos del paciente
    pdf.cell(0, 10, f"Paciente: {nombre_paciente}", ln=True)
    pdf.cell(0, 10, f"RUT: {rut}", ln=True)
    pdf.cell(0, 10, f"Fecha Nacimiento: {fecha_nacimiento}", ln=True)
    pdf.cell(0, 10, f"Fecha Informe: {fecha_actual}", ln=True)
    pdf.ln(10)

    # Tabla encabezados
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, "Código", 1)
    pdf.cell(60, 10, "Examen", 1)
    pdf.cell(30, 10, "Resultado", 1)
    pdf.cell(30, 10, "Estado", 1)
    pdf.cell(30, 10, "Fecha", 1)
    pdf.ln()

    # Tabla contenido
    pdf.set_font('Arial', '', 10)
    for row in historial:
        pdf.cell(40, 10, row[0], 1)
        pdf.cell(60, 10, row[1], 1)
        pdf.cell(30, 10, row[2], 1)
        pdf.cell(30, 10, row[3], 1)
        pdf.cell(30, 10, row[4], 1)
        pdf.ln()

    # Firma
    pdf.ln(20)
    pdf.cell(0, 10, f"Tecnólogo Médico: {nombre_tecnologo}", ln=True)
    pdf.cell(0, 10, "Firma Electrónica: ______________________", ln=True)

    pdf.output(nombre_archivo)

    return nombre_archivo
