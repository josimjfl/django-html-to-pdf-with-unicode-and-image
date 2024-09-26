
 #### Tutorial for converting HTML to PDF in a Django project, using WeasyPrint.
 ### JFL IT Lab
 ## jflitlab@gmail.com
---

# HTML to PDF Conversion in Django Using WeasyPrint

## Overview
In this tutorial, you'll learn how to convert HTML templates to PDF using the WeasyPrint library in Django. We'll install the required dependencies, set up a Django view, and configure the template to generate PDFs.

## IF You are a windows user you have to download and install 

On Windows, installing WeasyPrint dependencies like gobject and cairo manually can be tricky. You can resolve this by downloading the GTK package, which includes all necessary libraries.

Steps:
Download GTK (version 3 or higher):

Download the GTK 3 bundle for Windows.
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
Install it on your system.
Add the bin folder (inside the GTK installation directory) to your system's PATH environment variable.
For example, if GTK is installed in C:\Program Files\GTK3, add C:\Program Files\GTK3\bin to your system's PATH.

## 1. **Install Dependencies**

First, you need to install the WeasyPrint library and its dependencies.

### For Ubuntu/Debian:
```bash
sudo apt-get install libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libcairo2 libpangoft2-1.0-0 libjpeg-dev libpng-dev
pip install weasyprint
```

### For Windows:
Install WeasyPrint via pip:
```bash
pip install weasyprint
```
You may also need additional libraries like `GTK`. You can download the required dependencies from the [GTK project](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer).

## 2. **Set Up Django View to Generate PDF**

Create a Django view that renders an HTML template and converts it to a PDF using WeasyPrint.

### **views.py**
```python
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.templatetags.static import static

def generate_pdf(request):
    # Build absolute URI for static resources (like fonts, images)
    image_url = request.build_absolute_uri(static('images/sample_image.png'))
    font_url = request.build_absolute_uri(static('fonts/nikosh.ttf'))

    # Context to pass into the template
    context = {
        'image_url': image_url,
        'unicode_text': 'Sample Unicode Text: বাংলা, 中文, हिन्दी',
        'font_url': font_url
    }

    # Render HTML template to a string
    html_content = render_to_string('pdf_template.html', context)

    # Convert HTML to PDF using WeasyPrint
    pdf_file = HTML(string=html_content).write_pdf()

    # Return PDF as a downloadable response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="document.pdf"'
    return response
```

## 3. **Create HTML Template for PDF**

Create an HTML template with your desired structure and styling. Use `@font-face` to add custom fonts and ensure the use of absolute URLs for static files like images.

### **pdf_template.html**
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Export</title>
    <style>
        @font-face {
            font-family: 'Nikosh';
            src: url("{{ font_url }}") format('truetype');
        }

        body {
            font-family: 'Nikosh', sans-serif;
            font-size: 14px;
        }

        .content {
            text-align: center;
            margin: 20px;
        }

        .image-container img {
            width: 200px;
            height: auto;
        }

        .unicode-text {
            font-size: 18px;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>PDF Export Example</h1>

        <!-- Image -->
        <div class="image-container">
            <img src="{{ image_url }}" alt="Sample Image">
        </div>

        <!-- Unicode Text -->
        <p class="unicode-text">
            {{ unicode_text }}
        </p>
    </div>
</body>
</html>
```

## 4. **Setting Up Static Files**

Ensure your static files (fonts, images) are correctly set up in your project.

### Project Structure:
```
/your_project/
    /static/
        /fonts/
            nikosh.ttf
        /images/
            sample_image.png
```

### In **settings.py**:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

## 5. **URL Configuration**

Add a URL to trigger the PDF generation in your `urls.py` file.

### **urls.py**
```python
from django.urls import path
from .views import generate_pdf

urlpatterns = [
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
]
```

## 6. **Test the PDF Generation**

Run the Django server:
```bash
python manage.py runserver
```

Go to the URL:
```
http://127.0.0.1:8000/generate-pdf/
```

This will download a PDF file that contains your HTML content, images, and Unicode text with the custom font.

---

### Common Issues:
- **Static files not loading in the PDF**: Make sure you are using `request.build_absolute_uri()` for absolute paths to fonts or images.
- **Font not displaying**: Verify that the font file is valid and supported by WeasyPrint.

