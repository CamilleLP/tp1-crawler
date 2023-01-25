
def export_url_to_txt(list_url, file_name):
    '''
    export_url_to_txt: create a txt file named file_name.txt with list_utl inside
    '''
    with open(file_name, "w") as output:
        output.write(str(list_url))