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
             
        </head>
        <body>
            <div class="container">
            {html_table}
            </div>
        </body>
    </html>
    """

    with open(output_path, 'w') as f:
        f.write(html_output)

if __name__ =='__main__':
    csv_to_html()


 