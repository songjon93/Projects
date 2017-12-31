import java.util.*;
import java.awt.*;
import java.awt.event.ActionEvent;

import javax.swing.AbstractAction;
import javax.swing.Timer;

/**
 * An animated object flying across the scene in a fixed direction
 * Flier class for Lab 1, Dartmouth CS 10, Winter 2015
 * 
 * @author Chris Bailey-Kellogg, Dartmouth CS 10, Fall 2012; revised Winter 2014
 * @author Travis W. Peters, Dartmouth CS 10, Updated Winter 2015
 * @author Sung Jun Park, Dartmouth CS 10
 */
public class Flier extends Agent {

	private ArrayList<Point> borders;
	private double speed;			   // speed
	private double dx;				   // x direction
	private double dy;				   // y direction	
    private Universe universe;         // the universe that a flier exists within

    public Flier(Universe universe) {
        super(0, 0);
        this.universe = universe;
        universe.addFlier(this);
    }

    /**
     * Overrides Agent.move() to step by dx, dy
     */
    public void move() {
    	x = x + dx;
    	y = y + dy;
    }

    /**
     * Detect hitting the region (and restart)
     */
    public void checkWin() {
    	for (ArrayList<Point> region: universe.getRegions()){
    		for (Point point: region){
    			if (super.contains(point.x, point.y)){
    				toss();
    			}
    		}
    	}
    }
    
    public void draw(Graphics g){
    	g.setColor(Color.BLACK);
    	super.draw(g);
    }

    /**
     * Detect exiting the window (and restart)
     */
    public void checkLose() {
    	if (x + r >= universe.getWidth() || y + r >= universe.getHeight() || x - r <= 0 || y - r <= 0){
    		toss();
    	}
    }
    /**
     * Puts the object at a random point on one of the four borders, 
     * flying in to the window at a random speed.
     */
    public void toss() {
    	//create a new arraylist containing all the points of the borders
    	borders = new ArrayList<Point>(); 
    	speed = Math.max(Math.random()*7, 3);
   
    	for (int ux = 0; ux < universe.getWidth(); ux++){
    		borders.add(new Point(ux, 0));
    		borders.add(new Point(ux, universe.getHeight() - 1));
    	}
    	for (int uy = 1; uy < universe.getHeight() - 1; uy++){
    		borders.add(new Point(0, uy));
    		borders.add(new Point(universe.getWidth() - 1, uy));
    	}
    	
    	//have the flier object start off at a random border
    	Point p = borders.get((int)(Math.random()*(borders.size()-1)));
    	//flier's directon will somewhat be regulated so that it is possible for it to be caught by mitt
    	if (p.x == 0){
    		dx = Math.random() * speed;
    	}
    	else{
    		dx = -Math.random()* speed;
    	}
    	if (p.y == 0){
    		dy = Math.sqrt((speed)*(speed) - (dx)*(dx));
    	}
    	else{
    		dy = -Math.sqrt((speed)*(speed) - (dx)*(dx));
    	}
    	x = p.x;
    	y = p.y;
    	move();
    	}  
    }
