from termcolor import colored
def write_output_to_file(file,data):
    with open(file,"a") as file:
        file.write(data)
        file.close()
def pythia_query_parser(data,output_file):
    if output_file:
        write_output_to_file(output_file,"Pythia Query: "+data['title']+"\n")
    else:
        print(colored("[+]", 'green') +"Pythia Query: "+data['title'])
    condition=data['query']['condition']
    new_condition=condition

    for part in data['query']['parameters']:
        part_number=part
        for key in data['query']['parameters'][part].keys():
            string_part_number=key + data['query']['parameters'][part][key]
            new_condition=new_condition.replace(part_number,string_part_number)

    if output_file:
        write_output_to_file(output_file,"Pythia format query: " +new_condition+"\n")
    else:
        print(colored("[+]", 'green') +"Pythia format query: " +new_condition)