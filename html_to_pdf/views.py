from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import os

def generate_pdf(request):
    font_url = request.build_absolute_uri('/static/fonts/AdorshoLipi.ttf')
    # Sample data for rendering
    context = {
        'font_url': font_url,
        'image_url': request.build_absolute_uri('/static/images/josim_circle.png'),  # Image path
        'unicode_text': 'This is a sample Unicode text: বাংলা, 中文, हिन्दी,  আমার নাম জসিম উদ্দিন ' # Unicode content
    }

    # Render the HTML template to a string
    html_string = render_to_string('html_to_pdf/pdf_template.html', context)

    # Convert the HTML to PDF
    pdf_file = HTML(string=html_string).write_pdf()

    # Return the PDF as a response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="exported_file.pdf"'
    return response
