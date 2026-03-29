"""
Report generation service (CSV and PDF)
"""
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Service for generating reports in various formats"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def generate_csv_report(self, df: pd.DataFrame, output_path: str, summary: Optional[pd.DataFrame] = None) -> str:
        """
        Generate CSV report with optional summary sheet
        """
        try:
            # Save main data
            df.to_csv(output_path, index=False)
            
            # If summary provided, save it as separate file
            if summary is not None:
                summary_path = output_path.replace('.csv', '_summary.csv')
                summary.to_csv(summary_path, index=False)
                logger.info(f"Summary saved to: {summary_path}")
            
            logger.info(f"CSV report generated: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error generating CSV report: {str(e)}")
            raise
    
    def generate_pdf_report(
        self,
        df: pd.DataFrame,
        output_path: str,
        title: str = "Data Processing Report",
        stats: Optional[Dict] = None,
        summary: Optional[pd.DataFrame] = None
    ) -> str:
        """
        Generate comprehensive PDF report
        """
        try:
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            elements = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=30,
                alignment=1  # Center
            )
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Report metadata
            metadata_text = f"""
            <b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
            <b>Total Records:</b> {len(df)}<br/>
            <b>Total Columns:</b> {len(df.columns)}
            """
            elements.append(Paragraph(metadata_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            # Statistics Section
            if stats:
                elements.append(Paragraph("<b>Processing Statistics</b>", self.styles['Heading2']))
                elements.append(Spacer(1, 0.1*inch))
                
                stats_data = [[key.replace('_', ' ').title(), str(value)] for key, value in stats.items()]
                stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                elements.append(stats_table)
                elements.append(Spacer(1, 0.3*inch))
            
            # Summary Section
            if summary is not None and not summary.empty:
                elements.append(Paragraph("<b>Data Summary</b>", self.styles['Heading2']))
                elements.append(Spacer(1, 0.1*inch))
                
                summary_data = [summary.columns.tolist()] + summary.head(20).values.tolist()
                summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                elements.append(summary_table)
                elements.append(PageBreak())
            
            # Data Preview (first 15 rows)
            elements.append(Paragraph("<b>Data Preview (First 15 Rows)</b>", self.styles['Heading2']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Prepare data preview
            preview_df = df.head(15)
            
            # Limit columns if too many (max 6 columns for PDF width)
            if len(preview_df.columns) > 6:
                preview_df = preview_df.iloc[:, :6]
                elements.append(Paragraph(
                    f"<i>Note: Showing first 6 of {len(df.columns)} columns</i>",
                    self.styles['Normal']
                ))
                elements.append(Spacer(1, 0.1*inch))
            
            # Convert to table data
            table_data = [preview_df.columns.tolist()] + preview_df.values.tolist()
            
            # Calculate column widths dynamically
            col_width = 6.5 * inch / len(preview_df.columns)
            
            data_table = Table(table_data, colWidths=[col_width] * len(preview_df.columns))
            data_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            elements.append(data_table)
            
            # Footer
            elements.append(Spacer(1, 0.5*inch))
            footer_text = f"<i>Full data available in CSV format. Total records: {len(df)}</i>"
            elements.append(Paragraph(footer_text, self.styles['Normal']))
            
            # Build PDF
            doc.build(elements)
            logger.info(f"PDF report generated: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            raise
    
    def generate_complete_report(
        self,
        df: pd.DataFrame,
        output_dir: str,
        job_name: str,
        stats: Optional[Dict] = None,
        summary: Optional[pd.DataFrame] = None
    ) -> Dict[str, str]:
        """
        Generate both CSV and PDF reports
        Returns dict with paths to both files
        """
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f"{job_name}_{timestamp}"
            
            # Generate CSV
            csv_path = output_dir / f"{base_filename}.csv"
            self.generate_csv_report(df, str(csv_path), summary)
            
            # Generate PDF
            pdf_path = output_dir / f"{base_filename}.pdf"
            self.generate_pdf_report(
                df,
                str(pdf_path),
                title=f"{job_name} - Processing Report",
                stats=stats,
                summary=summary
            )
            
            return {
                'csv': str(csv_path),
                'pdf': str(pdf_path)
            }
        
        except Exception as e:
            logger.error(f"Error generating complete report: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    # Create sample data
    df = pd.DataFrame({
        'Product': ['Widget A', 'Widget B', 'Widget C', 'Widget D'],
        'Sales': [1500, 2300, 1800, 2100],
        'Revenue': [45000, 69000, 54000, 63000],
        'Region': ['North', 'South', 'East', 'West']
    })
    
    stats = {
        'total_rows': 100,
        'processed_rows': 96,
        'error_rows': 4,
        'processing_time': '2.5 seconds'
    }
    
    summary = pd.DataFrame({
        'Metric': ['Total Sales', 'Total Revenue', 'Average Revenue'],
        'Value': [7700, 231000, 57750]
    })
    
    generator = ReportGenerator()
    
    # Generate reports
    reports = generator.generate_complete_report(
        df,
        './storage/reports',
        'sample_job',
        stats=stats,
        summary=summary
    )
    
    print(f"Reports generated:")
    print(f"CSV: {reports['csv']}")
    print(f"PDF: {reports['pdf']}")
