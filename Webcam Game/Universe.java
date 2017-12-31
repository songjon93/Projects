import java.awt.*;
import java.awt.image.*;
import java.util.*;

/**
 * Universe for PS-1 Catch game.
 * Holds the fliers and the background image.
 * Also finds and holds the regions in the background image.
 * Each region is a list of contiguous points with colors similar to a target color.
 * Universe class, Lab 1, Dartmouth CS 10, Winter 2015
 * 
 * @author Chris Bailey-Kellogg, Winter 2014 (based on a very different structure from Fall 2012)
 * @author Travis W. Peters, Dartmouth CS 10, Updated Winter 2015
 * @author Sung Jun Park, Dartmouth CS 10
 */
public class Universe {
	private static final int maxColorDiff = 30;				// how similar a pixel color must be to the target color, to belong to a region
	private static final int minRegion = 50; 				// how many points in a region to be worth considering

	private BufferedImage image;                            // a reference to the background image for the universe
	private Color trackColor;                               // color of regions of interest (set by mouse press)

	private ArrayList<ArrayList<Point>> regions;			// a region is a list of points
	// so the identified regions are in a list of lists of points

	private ArrayList<Flier> fliers;                        // all of the fliers

	/**
	 * New universe with a background image and an empty list of fliers
	 * @param image
	 */
	public Universe(BufferedImage image) {
		this.image = image;		
		fliers = new ArrayList<Flier>();
	}

	/**
	 * Set the image (from the webcam) that makes up the universe's background
	 * @param image
	 */
	public void setImage(BufferedImage image) {
		this.image = image;
	}

	/**
	 * Allow others to ask about the state of the trackColor in the universe
	 * @return
	 */
	public Color getTrackingColor() {
		return trackColor;
	}

	/**
	 * Setting the color from an explicitly defined Color object 
	 * as opposed to getting input from the player.
	 * @param color
	 */
	public void setTrackingColor(Color color) {
		trackColor = color;
	}

	/**
	 * Allow others to ask about the size of the universe (width)
	 * @return
	 */
	public int getWidth() {
		return image.getWidth();
	}

	/**
	 * Allow others to ask about the size of the universe (height)
	 * @return
	 */
	public int getHeight() {
		return image.getHeight();
	}

	/**
	 * Accesses the currently-identified regions.
	 * @return
	 */
	public ArrayList<ArrayList<Point>> getRegions() {
		return regions;
	}

	/**
	 * Set the universe's regions.
	 * @return
	 */
	public void setRegions(ArrayList<ArrayList<Point>> regions) {
		this.regions = regions;
	}

	/**
	 * Adds the flier to the universe
	 * @param f
	 */
	public void addFlier(Flier f) {
		fliers.add(f);
	}

	/**
	 *  Move the flier and detect catches and misses
	 */
	public void moveFliers() {
		for (Flier fly: fliers){
			fly.move();
			fly.checkWin();
			fly.checkLose();
		}
		// TODO: YOUR CODE HERE
	}

	/**
	 * Draw the fliers
	 */
	public void drawFliers(Graphics g) {
		for (Flier fly: fliers){
			fly.draw(g);
		}
	}
	/**
	 * Sets regions to the flood-fill regions in the image, similar enough to the trackColor.
	 * @return 
	 */
	public void findRegions() {
		boolean [][] visited = new boolean[image.getWidth()][image.getHeight()]; // give every x, y coordinate a boolean value for whether it has been visited or not
		regions = new ArrayList<ArrayList<Point>>(); //initialize regions
		
		// look over every pixel
		for (int x = 0; x < getWidth(); x++){
			for (int y = 0; y < getHeight(); y++){
				
				Color c = new Color(image.getRGB(x,y)); //get RGB value for the pixel
				
				if (visited[x][y] == false && colorMatch(c, trackColor)){
					
					ArrayList<Point> region = new ArrayList<Point>(); //Create an ArrayList of Points and call that region
					ArrayList<Point> to_visit = new ArrayList<Point>(); //Create an ArrayList of Points for coordinates to be visited
					
					Point p = new Point(x,y);
					to_visit.add(p);
					while(to_visit.size() > 0){
						Point visiting = to_visit.remove(to_visit.size() - 1);
						if(visited[visiting.x][visiting.y] == false) {
							region.add(visiting);
							visited[visiting.x][visiting.y] = true;
							for (int nx = Math.max(0, visiting.x - 1); nx < Math.min(image.getWidth(), visiting.x + 2); nx++){
								for (int ny = Math.max(0, visiting.y - 1); ny < Math.min(image.getHeight(), visiting.y + 2); ny++){
									Color nc = new Color(image.getRGB(nx, ny));
									if (visited[nx][ny] == false && colorMatch(nc, trackColor)){
										to_visit.add(new Point(nx, ny));
									}
								}
							}
						}
					}
					if (region.size() >= minRegion){
						regions.add(region);
					}
				}
			}
		}
	}

	/**
	 * Tests whether the two colors are "similar enough" (your definition, subject to the static threshold).
	 * @param c1
	 * @param c2
	 * @return
	 */
	private static boolean colorMatch(Color c1, Color c2) {
		int r = Math.abs(c1.getRed() - c2.getRed());
		int g = Math.abs(c1.getGreen() - c2.getGreen());
		int b = Math.abs(c1.getBlue() - c2.getBlue());
		if (r <= maxColorDiff && g <= maxColorDiff && b <= maxColorDiff){
			return true;
		}
		else{
			return false;
		}
	}

	/**
	 * Recolors image so that each region is a random uniform color, so we can see where they are
	 */
	public void recolorRegions() {
		for (ArrayList<Point> region : regions){
			int r = (int)(Math.random() * 255);
			int g = (int)(Math.random() * 255);
			int b = (int)(Math.random() * 255);
			Color c = new Color(r, g, b);
			for (Point point: region){
				image.setRGB(point.x, point.y, c.getRGB());
			}
		}
	}
}
