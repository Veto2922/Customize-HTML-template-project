
class HtmlProcessManager:
    def __init__(self ):
        pass
        

    def geneate_new_html(self , new_json_placeholder, html_placeholder): 
        # Replace placeholders in the HTML with values from the JSON object
        for key, value in new_json_placeholder.items():
            placeholder = f"{key}"  # Assuming placeholders in HTML are in the format {{C1}}, {{C2}}, etc.
            html_placeholder = html_placeholder.replace(placeholder, value)
        return html_placeholder
    
    def save_new_html(self , new_html , save_path):      
        # Save the new HTML to a file
        with open(save_path, 'w' ,  encoding='utf-8') as file:
            file.write(new_html)
            
    def get_json_placeholder(self , path):
        # Load the JSON placeholder file
        with open(path, 'r' ,   encoding='utf-8') as file:
            json_placeholder = file.read()
        return json_placeholder
    
    def get_html_placeholder(self , path):
        # Load the HTML placeholder file
        with open(path, 'r' ,   encoding='utf-8') as file:
            html_placeholder = file.read()
        return html_placeholder
            
        
       
        