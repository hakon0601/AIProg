import csp_base
import copy

class CSP(csp_base.BaseCSP):
    def __init__(self):
        # Tuples with pairs of variable indexes and constraints
        self.revise_queue = []

    def init_revise_queue(self, constraints, variable_dict):
        for constr in constraints:
            # TODO NB
            self.revise_queue.append((constr.involved_variables[0], constr))

            #for variable in constr.involved_variables:
                #print "var: " + str(variable_dict[variable]) + " --- constr: " + str(constr)
                #self.revise_queue.append((variable, constr))
        print "REVISE QUEUE"
        for tuple in self.revise_queue:
            print tuple

    def domain_filtering_loop(self, variable_dict):
        while self.revise_queue:
            variable, constr = self.revise_queue.pop()
            # If a variables domain is reduced
            if self.revise(variable, constr, variable_dict):
                # Add a revise-pairs for all constraints and variables connected to this variable
                for involved_constraint in variable.involved_constraints:
                    for involved_variable_in_involved_constraint in involved_constraint.involved_variables:
                        if variable != involved_variable_in_involved_constraint:
                            self.revise_queue.append((involved_variable_in_involved_constraint, involved_constraint))
                            print "Append to queue: " + str(involved_variable_in_involved_constraint) + ", c: " + str(involved_constraint)
                            print ""
                            print "QUEUE:"
                            for q in self.revise_queue:
                                print q


    def revise(self, variable, constr, variable_dict):
        is_reduced = False
        #refined_domain = copy.deepcopy(variable.domain)
        scan = []
        for e in variable.domain:
            scan.append(e)

        for e in scan:
            print ""
            print variable
            print "for e = " + str(e)
            if constr.is_breaking(variable, e):
                #refined_domain.remove(e)
                variable.domain.remove(e)
                print "removing e: " + str(e)
                # "refined variable domain: " + str(refined_domain)
                print "refined variable domain: " + str(variable.domain)
                is_reduced = True
                #continue
        #variable.domain = refined_domain
        return is_reduced

        # TODO Use this one as well
        # Reduces domain of current variable if constraining variable is singleton domain
    def revise2(self, variable, constr, variable_dict):
        for constraining_variable in constr.involved_variables:
            constraining_variable = variable_dict[constraining_variable]
            if variable != constraining_variable and len(constraining_variable.domain) == 1 and constraining_variable.domain[0] in variable.domain:
                # If constraining variable has singleton domain, then reduce this ones domain
                variable.domain.remove(constraining_variable.domain[0])
                return True
        return False