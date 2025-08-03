from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime


def generate_pdf_report(scorecard) -> bytes:
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
    
    # Build the PDF content
    story = []
    
    # Header section
    story.append(Paragraph("Software Scorecard Report", title_style))
    story.append(Paragraph(f"{scorecard.product.name} - {scorecard.category.title()} Assessment", subtitle_style))
    story.append(Spacer(1, 12))
    
    # Overview information
    overview_data = [
        ["Product:", scorecard.product.name],
        ["Category:", scorecard.category.title()],
        ["Assessment Date:", scorecard.date.strftime("%B %d, %Y")],
        ["Overall Score:", f"{scorecard.score:.1f}%"],
        ["Generated On:", datetime.now().strftime("%B %d, %Y at %I:%M %p")]
    ]
    
    overview_table = Table(overview_data, colWidths=[2*inch, 4*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
    ]))
    
    story.append(overview_table)
    story.append(Spacer(1, 20))
    
    # Detailed breakdown section
    story.append(Paragraph("Detailed Assessment Results", section_style))
    story.append(Spacer(1, 12))
    
    # Create breakdown table based on category
    breakdown_data = [["Assessment Criteria", "Status", "Notes"]]
    
    field_labels = get_field_labels(scorecard.category)
    
    for field, value in scorecard.breakdown.items():
        status = "✓ Yes" if value else "✗ No"
        status_color = colors.green if value else colors.red
        label = field_labels.get(field, field.replace('_', ' ').title())
        breakdown_data.append([label, status, ""])
    
    breakdown_table = Table(breakdown_data, colWidths=[3*inch, 1.5*inch, 2*inch])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    
    story.append(breakdown_table)
    story.append(Spacer(1, 20))
    
    # Feedback section
    if scorecard.feedback:
        story.append(Paragraph("Assessment Feedback", section_style))
        feedback_text = scorecard.feedback.replace('\n', '<br/>')
        story.append(Paragraph(feedback_text, styles['Normal']))
        story.append(Spacer(1, 15))
    
    # Tool suggestions section
    if scorecard.tool_suggestions:
        story.append(Paragraph("Recommended Tools & Actions", section_style))
        suggestions_text = scorecard.tool_suggestions.replace('\n', '<br/>')
        story.append(Paragraph(suggestions_text, styles['Normal']))
        story.append(Spacer(1, 15))
    
    # Score interpretation
    story.append(Paragraph("Score Interpretation", section_style))
    score_interpretation = get_score_interpretation(scorecard.score)
    story.append(Paragraph(score_interpretation, styles['Normal']))
    
    # Build the PDF
    doc.build(story)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data


def get_field_labels(category: str) -> dict:
    """Get human-readable labels for scorecard fields"""
    labels = {
        "security": {
            "sast": "Static Application Security Testing (SAST)",
            "dast": "Dynamic Application Security Testing (DAST)", 
            "sast_dast_in_ci": "Security Testing Integrated in CI/CD",
            "triaging_findings": "Security Findings Triaged & Remediated",
            "secrets_scanning": "Secrets Scanning in CI",
            "sca_tool_used": "Software Composition Analysis (SCA) Tool",
            "cve_alerts": "Critical CVE Auto-Alerts",
            "pr_enforcement": "Dependency Scanning in Pull Requests",
            "training": "Developer Security Training",
            "threat_modeling": "Threat Modeling Process",
            "bug_bounty_policy": "Bug Bounty or Disclosure Policy",
            "compliance": "Compliance Standards (SOC2, FedRAMP, etc.)",
            "secure_design_reviews": "Security in Design Reviews",
            "predeployment_threat_modeling": "Pre-deployment Threat Modeling"
        },
        "automation": {
            "ci_pipeline": "Continuous Integration Pipeline",
            "automated_testing": "Automated Testing Suite",
            "deployment_automation": "Automated Deployment Process",
            "monitoring_alerts": "Automated Monitoring & Alerts",
            "infrastructure_as_code": "Infrastructure as Code"
        },
        "performance": {
            "load_testing": "Load Testing Implementation",
            "performance_monitoring": "Performance Monitoring Tools",
            "caching_strategy": "Caching Strategy Implementation",
            "database_optimization": "Database Performance Optimization",
            "cdn_usage": "Content Delivery Network Usage"
        },
        "cicd": {
            "automated_builds": "Automated Build Process",
            "automated_tests": "Automated Testing in Pipeline",
            "code_quality_gates": "Code Quality Gates",
            "deployment_pipeline": "Deployment Pipeline",
            "rollback_strategy": "Rollback Strategy",
            "environment_parity": "Environment Parity"
        }
    }
    return labels.get(category, {})


def get_score_interpretation(score: float) -> str:
    """Get interpretation text based on score"""
    if score >= 90:
        return "🌟 <b>Excellent (90-100%)</b>: Outstanding performance with industry-leading practices implemented."
    elif score >= 80:
        return "✅ <b>Very Good (80-89%)</b>: Strong performance with most best practices in place. Minor improvements recommended."
    elif score >= 70:
        return "👍 <b>Good (70-79%)</b>: Solid foundation with room for enhancement in key areas."
    elif score >= 60:
        return "⚠️ <b>Fair (60-69%)</b>: Basic practices implemented but significant improvements needed."
    elif score >= 50:
        return "🔄 <b>Needs Improvement (50-59%)</b>: Major gaps identified. Immediate action recommended."
    else:
        return "🚨 <b>Critical (0-49%)</b>: Significant deficiencies requiring urgent attention and comprehensive remediation."
    
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
