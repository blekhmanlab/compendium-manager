import sys # for the command-line params

import db.loader
import results.parsing
import projects.parsing

if __name__ == "__main__":
    #load_xml('txid408170', 'txid408170.221220.xml', save_samples=True, save_tags=False)
    #load_xml('txid408170', save_samples=False, save_tags=True)

    # only command-line param is how many to do in this session
    if sys.argv[1] == 'runs':
        todo = 2000 if len(sys.argv) < 3 else sys.argv[2]
        db.loader.find_runs(todo, per_query=80)
    elif sys.argv[1] == 'results':
        print(results.parsing.Load_asv_data('PRJNA842201'))
        projects.parsing.Process_summary('PRJNA842201')
    #db.write_lists(min_samples=50)
