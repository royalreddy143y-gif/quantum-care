import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image as RLImage, KeepTogether
)

from app.core.config import settings


def generate_pdf_report(
    analysis_data: Dict[str, Any],
    patient_data: Dict[str, Any],
    prediction_data: Dict[str, Any],
    image_path: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Generates a professional research analysis PDF report using ReportLab.
    Saves to output_path or creates one in settings.REPORTS_DIR.
    Returns the absolute path to the generated PDF.
    """
    if not output_path:
        report_filename = f"Report_{analysis_data.get('analysis_code', 'QC')}_{int(datetime.now(timezone.utc).timestamp())}.pdf"
        output_path = os.path.join(settings.REPORTS_DIR, report_filename)

    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a')
    )

    tagline_style = ParagraphStyle(
        'Tagline',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0284c7')
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f172a')
    )

    story: List[Any] = []

    # 1. Header with Logo & Brand
    header_data = [
        [
            Paragraph("<b>QUANTUMCARE</b>", title_style),
            Paragraph(f"<b>ANALYSIS REPORT</b><br/><font color='#64748b' size='8'>Ref: {analysis_data.get('analysis_code', 'N/A')}</font>", ParagraphStyle('RightH', parent=body_style, alignment=2))
        ],
        [
            Paragraph("Hybrid Quantum Machine Learning Platform for Early Disease Detection", tagline_style),
            Paragraph(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", ParagraphStyle('RightDate', parent=body_style, alignment=2))
        ]
    ]
    t_header = Table(header_data, colWidths=[330, 200])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_header)
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0284c7'), spaceBefore=6, spaceAfter=10))

    # 2. Patient & Analysis Information
    story.append(Paragraph("1. Patient & Case Metadata", h2_style))
    patient_info = [
        [
            Paragraph("<b>Patient ID:</b>", bold_body), Paragraph(str(patient_data.get('patient_id', 'N/A')), body_style),
            Paragraph("<b>Full Name:</b>", bold_body), Paragraph(str(patient_data.get('name', 'N/A')), body_style)
        ],
        [
            Paragraph("<b>Age / Gender:</b>", bold_body), Paragraph(f"{patient_data.get('age', 'N/A')} yrs / {patient_data.get('gender', 'N/A')}", body_style),
            Paragraph("<b>Architecture:</b>", bold_body), Paragraph("<font color='#0284c7'><b>Hybrid QML (Swin-T + VQC)</b></font>", body_style)
        ],
        [
            Paragraph("<b>Target Target:</b>", bold_body), Paragraph(str(analysis_data.get('target_condition', 'General Tissue Anomaly')), body_style),
            Paragraph("<b>Processing Latency:</b>", bold_body), Paragraph(f"{prediction_data.get('processing_time_ms', 0)} ms", body_style)
        ],
        [
            Paragraph("<b>Symptoms:</b>", bold_body), Paragraph(str(patient_data.get('symptoms') or 'None reported'), body_style),
            Paragraph("<b>Medical History:</b>", bold_body), Paragraph(str(patient_data.get('medical_history') or 'None reported'), body_style)
        ]
    ]
    t_patient = Table(patient_info, colWidths=[110, 155, 110, 155])
    t_patient.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_patient)
    story.append(Spacer(1, 10))

    # 4. Medical Image and Hybrid Prediction
    story.append(Paragraph("2. Hybrid Analysis & Detection Findings", h2_style))

    risk_cat = prediction_data.get('risk_category', 'Low')
    risk_color = '#16a34a' if risk_cat == 'Low' else ('#ea580c' if risk_cat == 'Moderate' else '#dc2626')
    conf_pct = round(prediction_data.get('confidence_score', 0.0) * 100, 1)

    result_table_data = [
        [
            Paragraph("<b>Research Classification:</b>", bold_body),
            Paragraph(f"<b>{prediction_data.get('prediction_label', 'Pending')}</b>", bold_body)
        ],
        [
            Paragraph("<b>Calculated Confidence:</b>", bold_body),
            Paragraph(f"<b>{conf_pct}%</b>", body_style)
        ],
        [
            Paragraph("<b>Risk Stratification:</b>", bold_body),
            Paragraph(f"<font color='{risk_color}'><b>{risk_cat.upper()} RISK</b></font>", bold_body)
        ]
    ]
    t_result = Table(result_table_data, colWidths=[150, 380])
    t_result.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fdf4' if risk_cat == 'Low' else '#fefce8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_result)
    story.append(Spacer(1, 10))

    # 5. Technical Pipeline & Quantum Telemetry
    story.append(Paragraph("3. Hybrid Pipeline & Quantum Circuit Telemetry", h2_style))

    raw_q = prediction_data.get('quantum_features') or []
    q_features = [float(v) for v in raw_q]
    while len(q_features) < 4:
        q_features.append(0.0)
    c_features = prediction_data.get('classical_features') or [0.0, 0.0, 0.0, 0.0]
    q_formatted_str = " | ".join(f"Q{i}: {round(v, 4)}" for i, v in enumerate(q_features))

    q_table_data = [
        [Paragraph("<b>Component</b>", bold_body), Paragraph("<b>Specification / Values</b>", bold_body)],
        [
            Paragraph("Classical Vision Backbone", body_style),
            Paragraph("Swin Transformer (Hierarchical Shifted Window Attention) • 768-D representation", body_style)
        ],
        [
            Paragraph("Dimensionality Reduction", body_style),
            Paragraph(f"Projected {c_features} (Scaled into [0, π] for Angle Encoding)", body_style)
        ],
        [
            Paragraph("Quantum Simulator & Circuit", body_style),
            Paragraph(f"PennyLane default.qubit • {settings.QUANTUM_NUM_QUBITS} Qubits • {settings.QUANTUM_NUM_LAYERS} Parameterized Entangled Layers (Ring CNOT)", body_style)
        ],
        [
            Paragraph("Qubit Pauli-Z Measurements ⟨Z⟩", body_style),
            Paragraph(q_formatted_str, body_style)
        ]
    ]
    t_quantum = Table(q_table_data, colWidths=[180, 350])
    t_quantum.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0f2fe')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_quantum)
    story.append(Spacer(1, 10))

    # 6. Explanation and Research Sign-off
    story.append(Paragraph("4. Algorithmic Explanation & Limitations", h2_style))
    explanation = prediction_data.get('explanation') or "No explanation generated."
    story.append(Paragraph(explanation, body_style))
    story.append(Spacer(1, 14))

    signoff_data = [
        [
            Paragraph("<b>Generated By:</b> QuantumCare Hybrid ML/QML Engine", body_style),
            Paragraph("<b>Supervisor / Researcher Signature:</b> _________________________", body_style)
        ]
    ]
    t_signoff = Table(signoff_data, colWidths=[260, 270])
    story.append(t_signoff)

    doc.build(story)
    return output_path
