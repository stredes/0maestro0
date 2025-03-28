from fpdf import FPDF
import os
import platform
import subprocess

def generar_resultado_pdf(historial_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Historial de Exámenes", ln=True, align="C")
    pdf.ln(10)

    # Encabezados
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 8, "Código", border=1)
    pdf.cell(60, 8, "Examen", border=1)
    pdf.cell(40, 8, "Resultado", border=1)
    pdf.cell(30, 8, "Estado", border=1)
    pdf.ln()

    # Datos
    pdf.set_font("Arial", size=11)
    for row in historial_data:
        pdf.cell(50, 8, str(row[0]), border=1)
        pdf.cell(60, 8, str(row[1]), border=1)
        pdf.cell(40, 8, str(row[2]), border=1)
        pdf.cell(30, 8, str(row[3]), border=1)
        pdf.ln()

    output_dir = "resultados_pdf"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "historial_paciente.pdf")
    pdf.output(output_path)
    print(f"✅ PDF generado: {output_path}")
    return output_path  # <-- ¡Muy importante!

def imprimir_pdf(ruta_pdf):
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(ruta_pdf, "print")
        elif sistema == "Darwin":
            subprocess.run(["lp", ruta_pdf])
        else:
            subprocess.run(["lp", ruta_pdf])
        print("✅ PDF enviado a impresión")
    except Exception as e:
        print(f"❌ Error al imprimir: {e}")
from fpdf import FPDF
import os
import platform
import subprocess

def generar_resultado_pdf(historial_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Historial de Exámenes", ln=True, align="C")
    pdf.ln(10)

    # Encabezados
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 8, "Código", border=1)
    pdf.cell(60, 8, "Examen", border=1)
    pdf.cell(40, 8, "Resultado", border=1)
    pdf.cell(30, 8, "Estado", border=1)
    pdf.ln()

    # Datos
    pdf.set_font("Arial", size=11)
    for row in historial_data:
        pdf.cell(50, 8, str(row[0]), border=1)
        pdf.cell(60, 8, str(row[1]), border=1)
        pdf.cell(40, 8, str(row[2]), border=1)
        pdf.cell(30, 8, str(row[3]), border=1)
        pdf.ln()

    output_dir = "resultados_pdf"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "historial_paciente.pdf")
    pdf.output(output_path)
    print(f"✅ PDF generado: {output_path}")
    return output_path

def imprimir_pdf(ruta_pdf):
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(ruta_pdf, "print")
        elif sistema == "Darwin":
            subprocess.run(["lp", ruta_pdf])
        else:
            subprocess.run(["lp", ruta_pdf])
        print("✅ PDF enviado a impresión")
    except Exception as e:
        print(f"❌ Error al imprimir: {e}")

# --- NUEVO: Generación de resultados por lote ---
def generar_resultado_lote_pdf(pacientes_list):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for paciente in pacientes_list:
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Informe de Resultados - Paciente", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"Nombre: {paciente.nombre}", ln=True)
        pdf.cell(0, 8, f"RUT: {paciente.rut}", ln=True)
        pdf.cell(0, 8, f"Edad: {paciente.edad}", ln=True)
        pdf.cell(0, 8, f"Sexo: {paciente.sexo}", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(60, 8, "Examen", border=1)
        pdf.cell(40, 8, "Resultado", border=1)
        pdf.ln()

        pdf.set_font("Arial", size=11)
        for examen in paciente.examenes:
            pdf.cell(60, 8, examen.examen, border=1)
            pdf.cell(40, 8, str(examen.resultado), border=1)
            pdf.ln()

        pdf.ln(10)

    output_dir = "resultados_pdf"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "resultados_lote.pdf")
    pdf.output(output_path)
    print(f"✅ PDF de lote generado: {output_path}")
    return output_path
