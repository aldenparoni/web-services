from unifier_requests.dmlib import DM

#file_id = 18195
file_id = 33580
env = 'stage'
project_number = 'jctest21'

assert env=='stage', 'env must be \'stage\'!'
x = DM(env = env,project_number = project_number)

# get_doc_by_file_id_tiff downloads in the image preview format
x.get_doc_by_file_id_tiff(file_id = file_id)

# get_doc_by_file_id downloads in the original format
#x.get_doc_by_file_id(file_id = file_id)
