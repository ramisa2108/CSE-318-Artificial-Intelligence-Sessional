/**
 * Copyright (c) 2016, Ecole des Mines de Nantes
 * All rights reserved.
 */
package org.chocosolver.samples;

import org.chocosolver.solver.Model;
import org.chocosolver.solver.Solver;
import org.chocosolver.solver.constraints.Constraint;
import org.chocosolver.solver.search.loop.monitors.IMonitorSolution;
import org.chocosolver.solver.search.strategy.Search;
import org.chocosolver.solver.search.strategy.assignments.DecisionOperator;
import org.chocosolver.solver.variables.IntVar;
import org.chocosolver.util.tools.ArrayUtils;

import java.util.Arrays;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * Aircraft Landing Problem
 * <p>
 *
 * @author Charles Prud'homme
 * @since 27/05/2016.
 */
public class NQueen {

    public void modelAndSolve(int n) {
        
        Model model = new Model("NQueen");
        
        IntVar[] P = model.intVarArray("P", 8, 1, 8);
        
        model.allDifferent(P).post();
        
        for(int i=0;i<8;i++){
            for(int j=0;j<8;j++){
                
                if(i != j){
                
                    model.arithm(P[i], "-", P[j], "!=", i-j).post();
                    model.arithm(P[j], "-", P[i], "!=", i-j).post();
                    
                }
                
            }
        }
        
        Solver solver = model.getSolver();
        solver.showStatistics();
        solver.showSolutions();
        solver.findSolution();
        
    }

    public static void main(String[] args) {
        new NQueen().modelAndSolve(8);
    }
}
