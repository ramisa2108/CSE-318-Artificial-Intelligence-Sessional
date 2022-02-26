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
 * Playing around with 8-queens puzzle
 * <p>
 * @author Charles Prud'homme
 * @since 27/05/2016.
 */
public class FutoShiki {

    public void modelAndSolve(){
        Model model = new Model("Futoshiki");
        
        IntVar[][] rows = model.intVarMatrix("rows", 9, 9, 1, 9);
        IntVar[][] cols = model.intVarMatrix("cols", 9, 9, 1, 9);
        
        for(int i=0;i<9;i++){
            model.allDifferent(rows[i]).post();
            model.allDifferent(cols[i]).post();
        }
        
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                model.arithm(rows[i][j], "=", cols[j][i]).post();
            }
        }
        
        
        
        model.arithm(rows[0][5], "=", 9).post();
        model.arithm(rows[0][8], "=", 2).post();
        
        model.arithm(rows[1][1], "=", 8).post();
        model.arithm(rows[1][7], "=", 4).post();
        
        model.arithm(rows[2][6], "=", 2).post();
        model.arithm(rows[2][7], "=", 3).post();
        
        model.arithm(rows[3][5], "=", 2).post();
        
        model.arithm(rows[4][0], "=", 3).post();
        model.arithm(rows[4][2], "=", 5).post();
        model.arithm(rows[4][5], "=", 6).post();
        
        
        model.arithm(rows[5][1], "=", 7).post();
        model.arithm(rows[5][6], "=", 6).post();
        
        
        model.arithm(rows[7][3], "=", 7).post();
        
        
        model.arithm(rows[0][3], "<", rows[0][4]).post();
        model.arithm(rows[0][6], "<", rows[0][7]).post();
        
        model.arithm(rows[1][2], "<", rows[0][2]).post();
        model.arithm(rows[1][6], "<", rows[0][6]).post();
        model.arithm(rows[1][8], "<", rows[0][8]).post();
        
        
        model.arithm(rows[1][3], "<", rows[1][4]).post();
        model.arithm(rows[1][5], "<", rows[1][6]).post();
        
        
        model.arithm(rows[2][3], "<", rows[2][2]).post();
        
        model.arithm(rows[3][0], "<", rows[2][0]).post();
        model.arithm(rows[2][1], "<", rows[3][1]).post();
        
        model.arithm(rows[3][4], "<", rows[3][5]).post();
        
        model.arithm(rows[4][5], "<", rows[4][4]).post();
        
        model.arithm(rows[4][3], "<", rows[5][3]).post();
        model.arithm(rows[5][6], "<", rows[4][6]).post();
        model.arithm(rows[5][8], "<", rows[4][8]).post();
        
        
        model.arithm(rows[5][7], "<", rows[5][8]).post();
        
        model.arithm(rows[5][0], "<", rows[6][0]).post();
        model.arithm(rows[5][3], "<", rows[6][3]).post();
        model.arithm(rows[5][4], "<", rows[6][4]).post();
        model.arithm(rows[6][8], "<", rows[5][8]).post();
        
        model.arithm(rows[6][1], "<", rows[6][0]).post();
        
        model.arithm(rows[7][5], "<", rows[7][6]).post();
        
        model.arithm(rows[8][1], "<", rows[7][1]).post();
        model.arithm(rows[8][7], "<", rows[7][7]).post();
        model.arithm(rows[8][8], "<", rows[7][8]).post();
        
        model.arithm(rows[8][3], "<", rows[8][2]).post();
        model.arithm(rows[8][5], "<", rows[8][6]).post();
        
        
        Solver solver = model.getSolver();
        solver.showStatistics();
        solver.showSolutions();
        solver.findSolution();
        
        
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                System.out.print(rows[i][j].getValue() + " ");
            }
            System.out.println();
        }
        
        
        
        
        
        
        
    
        
    }

    public static void main(String[] args) {
        new FutoShiki().modelAndSolve();
    }

}
