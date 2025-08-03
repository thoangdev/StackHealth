from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import schemas
from datetime import datetime


def generate_pdf_report(scorecard: schemas.Scorecard) -> bytes:
    """Generate a PDF report for a scorecard using ReportLab"""
    
    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch)
    
    # Get sample styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        alignment=1,  # Center alignment
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=1,  # Center alignment
        spaceAfter=30
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    # Story list to hold PDF elements
    story = []
    
    # Title
    story.append(Paragraph(f"📊 {scorecard.project.name}", title_style))
    story.append(Paragraph(f"Scorecard Report - {scorecard.date.strftime('%B %d, %Y')}", subtitle_style))
    
    # Scores section
    story.append(Paragraph("Performance Scores", section_style))
    
    # Create scores table
    scores_data = [
        ['Area', 'Score', 'Rating'],
        ['🤖 Automation', f"{int(scorecard.automation_score)}%", get_score_rating(scorecard.automation_score)],
        ['⚡ Performance', f"{int(scorecard.performance_score)}%", get_score_rating(scorecard.performance_score)],
        ['🔒 Security', f"{int(scorecard.security_score)}%", get_score_rating(scorecard.security_score)],
        ['🔄 CI/CD', f"{int(scorecard.cicd_score)}%", get_score_rating(scorecard.cicd_score)]
    ]
    
    scores_table = Table(scores_data, colWidths=[2*inch, 1*inch, 1.5*inch])
    scores_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    
    # Add row-specific styling based on scores
    for i, row_data in enumerate(scores_data[1:], 1):
        score = float(row_data[1].replace('%', ''))
        if score >= 80:
            bg_color = colors.HexColor('#d4edda')
        elif score >= 60:
            bg_color = colors.HexColor('#fff3cd')
        else:
            bg_color = colors.HexColor('#f8d7da')
        
        scores_table.setStyle(TableStyle([('BACKGROUND', (1, i), (2, i), bg_color)]))
    
    story.append(scores_table)
    story.append(Spacer(1, 20))
    
    # Feedback section
    if scorecard.feedback:
        story.append(Paragraph("Feedback & Recommendations", section_style))
        
        for feedback in scorecard.feedback:
            # Create feedback table for each item
            feedback_data = [
                ['Area:', feedback.area.title()],
            ]
            
            if feedback.comment:
                feedback_data.append(['Comment:', feedback.comment])
            
            if feedback.tool_recommendation:
                feedback_data.append(['Tools:', feedback.tool_recommendation])
            
            if feedback.marked_for_improvement:
                feedback_data.append(['Status:', '⚠️ Marked for Improvement'])
            
            feedback_table = Table(feedback_data, colWidths=[1.2*inch, 4.8*inch])
            feedback_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            # Highlight improvement items
            if feedback.marked_for_improvement:
                feedback_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fdf2f2')),
                    ('LINEBELOW', (0, 0), (-1, -1), 2, colors.HexColor('#e74c3c'))
                ]))
            
            story.append(feedback_table)
            story.append(Spacer(1, 10))
    
    # Footer
    story.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#666666'),
        alignment=1
    )
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", footer_style))
    story.append(Paragraph("Software Scorecard Dashboard", footer_style))
    
    # Build the PDF
    doc.build(story)
    
    # Get the PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def get_score_rating(score: float) -> str:
    """Get text rating based on score"""
    if score >= 80:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Fair"
    else:
        return "Needs Improvement"
