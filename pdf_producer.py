import pdfkit
from jinja2 import Template
import os
import scheduler


def create_pdf(schedule_data, destination):

    percentage_data = scheduler.get_spent_time(schedule_data)

    with open('./template/template.html', 'r') as file:
        html_template = file.read()

    template = Template(html_template)
    rendered_html = template.render(schedule=schedule_data, dir=os.getcwd() + '/template', percentage_data = percentage_data)
    
    with open("./export/rendered_template.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)
    # Convert the HTML to PDF
    pdfkit.from_string(rendered_html, destination, options={"enable-local-file-access": ""})
    return True
