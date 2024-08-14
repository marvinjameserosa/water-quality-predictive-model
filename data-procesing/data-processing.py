import pandas as pd

def csv_to_html(csv_file, output_path, num_rows=100):
    df = pd.read_csv(csv_file)  
    df_head = df.head(num_rows)

    html_table = df_head.to_html(classes='table table-striped', index=False, border=0)
    html_output = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>CSV to HTML</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
            {html_table}
            </div>
        </body>
    </html>
    """

    # Save the HTML content to the specified file path
    with open(output_path, 'w') as f:
        f.write(html_output)

    return html_output

csv_file_path = 'data-processing/water_qua.csv' 
# Specify the desired output file path
output_file_path = 'data-processing/output.html'  # Replace with your actual path

html_content = csv_to_html(csv_file_path, output_file_path)

from IPython.display import display, HTML
display(HTML(html_content))