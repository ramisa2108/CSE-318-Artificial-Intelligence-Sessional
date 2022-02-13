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
public class TwoPlusTwo {

    public void modelAndSolve() {
        
        Model model = new Model("TwoPlusTwo");
        
        IntVar T = model.intVar("T", 1, 9);
        IntVar W = model.intVar("W", 0, 9);
        IntVar O = model.intVar("O", 0, 9);
        IntVar F = model.intVar("F", 1, 9);
        IntVar U = model.intVar("U", 0, 9);
        IntVar R = model.intVar("R", 0, 9);
        
        IntVar[] C = model.intVarArray("C",3,  0, 1);
        
        model.allDifferent(T, W, O, F, U, R).post();
        
        IntVar[] vars1 = new IntVar[] {O, R, C[0]};
        IntVar[] vars2 = new IntVar[] {C[0], W, U, C[1]};
        IntVar[] vars3 = new IntVar[] {C[1], T, O, C[2]};
        
        int [] coeffs1 = new int[] {2, -1, -10};
        int [] coeffs2 = new int[] {1, 2, -1, -10};
        int [] coeffs3 = new int[] {1, 2, -1, -10};
        
        model.scalar(vars1, coeffs1, "=", 0).post();
        model.scalar(vars2, coeffs2, "=", 0).post();
        model.scalar(vars3, coeffs3, "=", 0).post();

        model.arithm(C[2], "=", F);
        
        Solver solver = model.getSolver();
        solver.showStatistics();
        solver.showSolutions();
        solver.findSolution();
        
        
        
    }

    public static void main(String[] args) {
        new TwoPlusTwo().modelAndSolve();
    }
}
