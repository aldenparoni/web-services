from unifier_requests.bplib import uai
data = [{
	'title':'abc title'
	, 'genReviewReqdRB':'No'
	, 'ugenAsgnToADP':'System Integration'
	, 'ugenDescSDT2000':None
	, 'ugenSumActionMLT2000':'abc'
}]

env = 'stage'
project_number = 'jctest21'
assert env == 'stage', 'env must be \'stage\'!'
x = uai(env = env, project_number = project_number)
r = x.create(data)

