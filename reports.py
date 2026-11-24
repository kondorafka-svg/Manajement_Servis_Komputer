from database import fetch_all

def export_excel(table_key, output_path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter

    queries = {
        "pelanggan": ("SELECT id_pelanggan, nama, alamat, telepon FROM pelanggan",
                      ["ID", "Nama", "Alamat", "Telepon"]),
        "perangkat": ("SELECT p.id_perangkat, pl.nama AS pelanggan, p.jenis, p.merek, p.model, p.nomor_seri FROM perangkat p JOIN pelanggan pl ON p.id_pelanggan=pl.id_pelanggan",
                      ["ID", "Pelanggan", "Jenis", "Merek", "Model", "Nomor Seri"]),
        "teknisi": ("SELECT id_teknisi, nama, telepon, keahlian FROM teknisi",
                    ["ID", "Nama", "Telepon", "Keahlian"]),
        "servis": ("SELECT s.id_servis, pl.nama AS pelanggan, p.jenis, p.merek, s.tanggal_masuk, s.kerusakan, t.nama AS teknisi, s.status, s.biaya FROM servis s JOIN perangkat p ON s.id_perangkat=p.id_perangkat JOIN pelanggan pl ON p.id_pelanggan=pl.id_pelanggan LEFT JOIN teknisi t ON s.id_teknisi=t.id_teknisi",
                   ["ID", "Pelanggan", "Jenis", "Merek", "Tanggal Masuk", "Kerusakan", "Teknisi", "Status", "Biaya"]),
        "pembayaran": ("SELECT pb.id_pembayaran, pb.id_servis, pb.tanggal_bayar, pb.jumlah, pb.metode FROM pembayaran pb",
                       ["ID", "ID Servis", "Tanggal Bayar", "Jumlah", "Metode"]),
    }
    sql, headers = queries[table_key]
    rows = fetch_all(sql)
    wb = Workbook()
    ws = wb.active
    ws.title = table_key.title()
    ws.append(headers)
    for row in rows:
        ws.append(list(row.values()))
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1769AA")
    for col in ws.columns:
        width = min(max(max(len(str(c.value or "")) for c in col) + 2, 12), 40)
        ws.column_dimensions[get_column_letter(col[0].column)].width = width
    wb.save(output_path)

def export_pdf(output_path):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    rows = fetch_all("""
        SELECT s.id_servis, pl.nama, p.jenis, p.merek, s.tanggal_masuk,
               s.status, s.biaya
        FROM servis s
        JOIN perangkat p ON s.id_perangkat=p.id_perangkat
        JOIN pelanggan pl ON p.id_pelanggan=pl.id_pelanggan
        ORDER BY s.id_servis DESC
    """)
    data = [["ID", "Pelanggan", "Jenis", "Merek", "Tanggal", "Status", "Biaya"]]
    for r in rows:
        data.append([r["id_servis"], r["nama"], r["jenis"], r["merek"],
                     str(r["tanggal_masuk"]), r["status"], f'Rp {r["biaya"]:,.0f}'])
    doc = SimpleDocTemplate(output_path, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    story = [Paragraph("Laporan Manajemen Servis Komputer", styles["Title"]), Spacer(1, 16)]
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1769AA")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#EFF6FF")]),
        ("PADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(table)
    doc.build(story)