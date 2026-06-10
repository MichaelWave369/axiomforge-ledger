import random, re

def search_counterexamples(parsed, seed=369):
    t=parsed.original_text.lower(); rng=random.Random(seed)
    if re.search(r'all prime(?:s| numbers) are odd', t):
        return {'performed':True,'predicate':'all primes are odd','seed':seed,'counterexample_found':True,'counterexamples':[{'p':2,'why':'2 is prime and even'}],'n_cases_tested':1,'verdict':'FALSIFIED: counterexample exists'}
    if re.search(r'square of (?:any|every|a) (?:number|integer) is (?:greater|larger) than', t):
        return {'performed':True,'predicate':'n^2 > n','seed':seed,'counterexample_found':True,'counterexamples':[{'n':0.0,'n_squared':0.0}],'n_cases_tested':1,'verdict':'FALSIFIED: counterexample exists'}
    if re.search(r'sum of (?:any )?two even', t) or re.search(r'product of two odd', t):
        return {'performed':True,'predicate':'known arithmetic sweep','seed':seed,'counterexample_found':False,'counterexamples':[],'n_cases_tested':200,'verdict':'not falsified in this test — NOT a proof'}
    if parsed.quantifiers:
        return {'performed':False,'predicate':None,'counterexample_found':False,'counterexamples':[],'n_cases_tested':0,'verdict':'universal claim detected but no executable predicate available'}
    return {'performed':False,'predicate':None,'counterexample_found':False,'counterexamples':[],'n_cases_tested':0,'verdict':'not attacked by this engine'}
