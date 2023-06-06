import tkinter as tk
import xml.etree.ElementTree as ET
import uuid
from datetime import datetime
from os import path

time_stamp_format = "%m-%d-%Y %H:%M:%S"

def init_xml(file_path):
    # Read existing XML file if it exists
    if path.exists(file_path):
        # Read element tree
        tree = ET.parse(file_path)

    # File does not exist, so make a new one
    else:
        root = ET.Element("root")
        
        meta = ET.SubElement(root, "meta_data")
        ET.SubElement(meta, "entry_count", name="entries").text = 0 
        now = datetime.now()
        dt_string = now.strftime(time_stamp_format) 
        ET.SubElement(meta, "date_created", name="created").text = dt_string
        ET.SubElement(meta, "date_last_modified", name="modified").text = dt_string
        
        entries = ET.SubElement(root, "entries")
        titles = ET.SubElement(root, "titles")
        companies = ET.SubElement(root, "companies")

        tree = ET.ElementTree(root)
        ET.indent(tree, '  ')
        tree.write(file_path, encoding="UTF-8")

    return tree

def update_entry_xml(doc_tree, title, body, company=None, rating=None):
    """
    Creates new XML file if none exists, otherwise appends to existing file
    """

    # Encode new body as ElementTree items
    
    # update timestamp
    now = datetime.now()
    dt_string = now.strftime(time_stamp_format) 
    
    # Update timestamp
    now = datetime.now()
    dt_string = now.strftime(time_stamp_format) 
    meta = doc_tree.find("meta_data")
    updated = meta.find("date_created")
    updated.text = dt_string
    
    # Create and append new entry
    entries = doc_tree.find("entries")
    id = uuid.uuid1()
    position = ET.SubElement(entries, "position", id=str(id), time_stamp = str(dt_string))
    ET.SubElement(position, "title", name="title").text = str(title)
    if company:
        ET.SubElement(position, "company", name="company").text = str(company)
        
    if rating:
        ET.SubElement(position, "rating", name="rating").text = str(rating)
    ET.SubElement(position, "body", name="body").text = str(body)
        
    return doc_tree



def write_xml(doc_tree, file_path):
    print("Written!")
    ET.indent(doc_tree, '  ')
    doc_tree.write(file_path, encoding="UTF-8")


def buddy_run(entry_tree, xml_file):
    main = tk.Tk()
    
    ## TODO: Make better layout for input feilds, maybe a slider for the rating?
    # position title field
    title_entry = tk.Entry(main)
    title_entry.pack()
    
    # company name field
    company_entry = tk.Entry(main)
    company_entry.pack()
    
    # position listing/body field
    text_entry = tk.Text(main)
    text_entry.pack()


    title_entry.focus_set()

    def clear_fields():
        title_entry.delete(1, "end")
        company_entry.delete(1, "end")
        text_entry.delete("1.0", "end")        

    def callback():
        title_str = title_entry.get()
        body_str = text_entry.get("1.0", "end")
        
        company_str = company_entry.get()
        rating = 10

        # Print for debug
        print(title_str, body_str) # This is the text you may want to use later

        update_entry_xml(entry_tree, title_str, body_str, company_str, rating)
        write_xml(entry_tree, xml_file)
        
        clear_fields()

    ok_button = tk.Button(main, text = "OK", width = 10, command = callback)
    ok_button.pack()

    tk.mainloop()


xml_file = "test_xml.xml"
if __name__ == "__main__":
    element_tree = init_xml(xml_file)
    buddy_run(element_tree, xml_file)

    