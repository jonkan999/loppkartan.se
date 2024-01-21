from jinja2 import Environment, FileSystemLoader
import os
import yaml



def generate_page(config, config_aux,page_type):
    # Load the Jinja2 template
    # Get the directory path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Move up one folder to the parent directory
    parent_dir = os.path.join(script_dir, '..')

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(searchpath=parent_dir))
    # Print the template loader's search path
    print(f"Template search path: {env.loader.searchpath}")
    # Register the filter function with the Jinja2 environment
    template = env.get_template(f"{page_type}_template.html")
    data = {
        'config': config,
        'config_aux': config_aux
    }
    html = template.render(data=data)

    page_path = f"../{config_aux[f'{page_type}_name']}.html"
    print(f"Saving page to {page_path}")
    # Save the generated HTML page
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    with open("../collection_configuration/general_config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) 

    # Load the configuration and generate each page type
    for page_type in ["add_race", "contact", "about", "submission_success"]:
        with open(f"../collection_configuration/{page_type}_config.yaml", 'r', encoding='utf-8') as f:
            page_config = yaml.safe_load(f)
        print(f"Generating {page_type} page")
        print(page_config)
        generate_page(config, page_config, page_type)


