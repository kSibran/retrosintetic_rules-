from CGRtools.files import RDFread, RDFwrite
from enumeration_reaction import enumeration_cgr
from new_cycl import  cycl
from constructor import constructor
import pickle

det = False
#with RDFread('/home/ravil/Desktop/Projects/retro/Error.rdf') as reaction_file:
with RDFread('/home/ravil/Desktop/Projects/retro/USPTO.rdf') as reaction_file, \
       RDFwrite('/home/ravil/Desktop/Projects/retro/Error.rdf') as err:
# with RDFread('/home/ravil/Desktop/Projects/retro/rules_patents_09_19.rdf') as reaction_file, \
#        RDFwrite('/home/ravil/Desktop/Projects/retro/Error.rdf') as err:
#with  RDFread('/home/ravil/2_5_reactions.rdf') as reaction_file,\
    #RDFwrite('/home/ravil/Desktop/Error.rdf') as err: #'/home/ravil/Desktop/query_graphs_and_other/base/db_task/readliner_out/diol.rdf'
# with RDFread('/home/ravil/Desktop/Projects/retro/example.rdf') as reaction_file,\
#      RDFwrite('/home/ravil/Desktop/Projects/retro/enumerated_re.rdf') as en_re:
    fg_fg = {}
    for n, reaction in enumerate(reaction_file, start = 1):
        print(n)
        # if n != 58925:
        #     continue
        # err.write(reaction)
        # if n > 100:
        #     break
        reaction.meta['id'] = n
        try:
            cgrs = ~reaction
        except ValueError:
            continue

        if cgrs.center_atoms:
            v= cgrs.center_atoms
            if any(x.is_radical or x.p_is_radical for _, x in cgrs.atoms()):
                continue
            if cgrs.center_atoms:
                print('len_fg_fg = ' + str(len(fg_fg)))
                perebor = enumeration_cgr(reaction)

                for new_reaction in perebor:
                    new_reaction.standardize()
                    new_reaction.meta['id'] = n
                    if not constructor(*cycl(new_reaction),fg_fg,n):
                        print('COMPOSITION IS None '+ str(n))
                        det = True
                        break
            if det :
                break
with open('/home/ravil/Desktop/Projects/retro/transfoRmULES', 'wb') as rule_dump:
    pickle.dump(fg_fg,rule_dump)
with RDFwrite('/home/ravil/Desktop/Projects/retro/transfoRmULES.rdf') as fg:
    for x in fg_fg.values():
        fg.write(x)



