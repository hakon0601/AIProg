import csp_base
import copy

class CSP(csp_base.BaseCSP):
    def __init__(self):
        # Tuples with pairs of variable indexes and constraints
        self.revise_queue = []

    def init_revise_queue(self, constraints, variable_dict):
        for constr in constraints:
            # TODO NB
            #self.revise_queue.append((constr.involved_variables[0], constr))
            for variable in constr.involved_variables:
                #print "var: " + str(variable_dict[variable]) + " --- constr: " + str(constr)
                self.revise_queue.append((variable, constr))
        #print "REVISE QUEUE"
        #for tuple in self.revise_queue:
            #print tuple

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
                            #print "Append to queue: " + str(involved_variable_in_involved_constraint) + ", c: " + str(involved_constraint)
                            #print ""
                            #print "QUEUE:"
                            #for q in self.revise_queue:
                                #print q


    def revise(self, variable, constr, variable_dict):
        is_reduced = False
        # temporarily scan variable so that we do not mess with the iterations
        scan = copy.deepcopy(variable.domain)
        if constr.all_involved_vars_are_in_same_line():
            for e in scan:
                #print ""
                #print variable
                #print "for e = " + str(e)
                if self.is_breaking(constr, variable, e):
                    variable.domain.remove(e)
                    #print "refined variable domain: " + str(variable.domain)
                    is_reduced = True
            # If variable is a singleton domain, then reduce all adjacent variables domains
            #if len(variable.domain) == 1:
                #self.reduce_neighbours_of_singleton_domain(variable_dict, variable)
            return is_reduced
        else:
            # row and column intersecting
            other_var = constr.get_other(variable)
            spec = None
            if other_var.spec == "row":
                spec = "column"
            else:
                spec = "row"

            if variable.spec == spec:
                if len(other_var.domain) == 1 and int(other_var.domain[0]) == int(variable.index):
                    for e in scan:
                        print "REMOVING " + str(e) + " from neighbour variable:"
                        print "variable index was: " + str(variable.index)
                        print "---------"
                        variable.domain.remove(e)
                        is_reduced = True
                #else:
                    # not singleton domain, but can we reduce anyways?
            return is_reduced


    def is_breaking(self, constr, variable, e):
        # this method figures out if domain element e should be removed from variable.

        first_var = second_var = None
        var_segment_nr = int(variable.segment_nr)
        other_var = constr.get_other(variable)

        if variable == constr.involved_variables[0] and var_segment_nr < int(other_var.segment_nr) or \
                                variable == constr.involved_variables[1] and var_segment_nr < int(other_var.segment_nr):
            first_var = variable
            second_var = other_var

        elif variable == constr.involved_variables[0] and var_segment_nr > int(other_var.segment_nr) or \
                                variable == constr.involved_variables[1] and var_segment_nr > int(other_var.segment_nr):
            first_var = other_var
            second_var = variable
        else:
            return

        if variable == first_var:
            # first var
            if len(other_var.domain) == 1 and e != int(other_var.domain[0]) - variable.length - 1:
                #print "REMOVING" + str(e) + " because other variable is singleton domain and e is not accurate"
                return True

            if e <= (int(first_var.k) - int(first_var.length) - int(second_var.length) - 1):
                #print "IS NOT REMOVING " + str(e)
                return False
            else:
                # Is breaking
                #print "IS REMOVING " + str(e)
                return True

        elif variable == second_var:
            # TODO check if other is singleton domain
            other_variable = constr.get_other(variable)
            if len(other_variable.domain) == 1 and e != int(other_variable.domain[0]) + other_variable.length + 1:
                #print "REMOVING" + str(e) + " because other variable is singleton domain and e is not accurate"
                return True
            # second var
            if e > first_var.length:
                #print "IS NOT REMOVING " + str(e)
                return False
            else:
                # Is breaking
                #print "IS REMOVING " + str(e)
                return True
        else:
            print "error in Constraint class"


    # TODO Use this or not?
    # Reduces domain of current variable if constraining variable is singleton domain
    def revise2(self, variable, constr, variable_dict):
        for constraining_variable in constr.involved_variables:
            constraining_variable = variable_dict[constraining_variable]
            if variable != constraining_variable and len(constraining_variable.domain) == 1 and constraining_variable.domain[0] in variable.domain:
                # If constraining variable has singleton domain, then reduce this ones domain
                variable.domain.remove(constraining_variable.domain[0])
                return True
        return False