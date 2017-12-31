import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Map;
import java.util.Queue;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

import net.datastructures.Edge;
import net.datastructures.Vertex;


public class KevinBaconGame {
	private static BufferedReader actors;
	private static BufferedReader movies;
	private static BufferedReader actorMovie;
	private static AdjacencyListGraphMap<String, String> baconGraph;
	
	/*
	 * returns a map that has actor numbers as keys and actor names as values
	 */
	public static Map<String, String> createActorMap(String actorPath) throws IOException{
		try{
			actors = new BufferedReader(new FileReader("inputs/bacon/" + actorPath));
			Map<String, String> actorMap = new TreeMap<String, String>();
			String line;

			while((line = actors.readLine())!= null){
				String [] actorList = line.split("\\|");
				actorMap.put(actorList[0], actorList[1]);
			}
			return actorMap;
		}
		
		finally{
			actors.close();
		}
	}
	
	/*
	 * returns a map that has movie numbers as keys and names as values
	 */
	public static Map<String, String> createMovieMap(String moviePath) throws IOException{
		try{
			movies = new BufferedReader(new FileReader("inputs/bacon/" + moviePath));
			Map<String, String> movieMap = new TreeMap<String, String>();
			String line;
			while((line = movies.readLine())!= null){
				String [] movieList = line.split("\\|");
				movieMap.put(movieList[0], movieList[1]);
			}
			return movieMap;
		}
		
		finally{
			movies.close();
		}
	}
	
	/*
	 * returns a map that has movie names as keys and sets of actor names as values
	 */
	public static Map<String, Set<String>> createActorMovieMap(String actorPath, String moviePath, String actorMoviePath) throws IOException{
		try{
			actorMovie = new BufferedReader(new FileReader("inputs/bacon/" + actorMoviePath));
			Map<String, Set<String>> actorMovieMap = new TreeMap<String, Set<String>>();
			Map<String, String> actorMap = createActorMap(actorPath);
			Map<String, String> movieMap = createMovieMap(moviePath);
			String line;

			while((line = actorMovie.readLine()) != null){
				String [] actorMovieList = line.split("\\|");
				String movie = movieMap.get(actorMovieList[0]);
				String actor = actorMap.get(actorMovieList[1]);

				if (actorMovieMap.containsKey(movie)){
					Set<String> newSet = actorMovieMap.get(movie);
					newSet.add(actor);
					actorMovieMap.put(movie, newSet);
				}
				else{
					Set<String> newSet = new TreeSet<String>();
					newSet.add(actor);
					actorMovieMap.put(movie, newSet);
				}
			}
		return actorMovieMap;
		}
		
		finally{
			actorMovie.close();
		}
	}
	
	/*
	 * creates a undirected graph with individual actors as vertices and movies as edges between them	
	 */
	public static void createGraph(String actorPath, String moviePath, String actorMoviePath) throws IOException{
		Map<String, Set<String>> actorMovieMap = createActorMovieMap(actorPath, moviePath, actorMoviePath);
		baconGraph = new AdjacencyListGraphMap<String, String>();

		//for each movie, get actors who made appearances in the movie, make them vertices, and connect the vertices with edges(movie)
		for(String movie: actorMovieMap.keySet()){
			for (String actor: actorMovieMap.get(movie)){
				Set<String> otherActors = new TreeSet<String>();
				otherActors.addAll(actorMovieMap.get(movie));
				otherActors.remove(actor);

				//only insert vertex if there isn't already one in the graph
				if (!baconGraph.vertexInGraph(actor)){
					baconGraph.insertVertex(actor);
				}
				
				//connect the vertex with other vertexes of actors that made appearance in the same movie
				for (String otherActor: otherActors){
					
					//if the other vertex is not already in the graph, insert one
					if (!baconGraph.vertexInGraph(otherActor)){
						baconGraph.insertVertex(otherActor);
					}
					
					boolean exists = false;

					for (Edge<String> edge : baconGraph.incidentEdges(actor)){
						if (baconGraph.opposite(actor, edge) == (baconGraph.getVertex(otherActor))){
							exists = true;
						}
					}
					
					//insert edge only if there isn't one between the two vertices
					if (!exists){
						baconGraph.insertEdge(actor, otherActor, movie);

					}
				}
			}
		}
	}
	
	/*
	 * returns a breadth first search graph
	 */
	public static DirectedAdjListMap<String, String> createBFSMap(String root, AdjacencyListGraphMap<String, String> graph){
		DirectedAdjListMap<String, String> shortestPath = new DirectedAdjListMap<String, String>();
		Queue<String> baconQue = new ArrayDeque<String>();
		
		//add into the queue and directed graph the root
		baconQue.add(root);
		shortestPath.insertVertex(root);
		
		while (!baconQue.isEmpty()){
			String nextVertex = baconQue.poll(); //dequeue from the queue and assign the dequeued value to nextVertex variable
			
			//add every adjacent vertices (string values) of the dequeued vertex to the queue and build edges between the vertices
			for(Edge<String> edge: graph.incidentEdges(nextVertex)){
				graph.opposite(nextVertex, edge);
				String adjacent = graph.opposite(nextVertex, edge).element();
				
				//add the vertices and edges only if the vertex isn't already in the graph
				if(!shortestPath.vertexInGraph(adjacent)){
					String movie = edge.element();
					Vertex<String> vertex = shortestPath.getVertex(nextVertex);
					Vertex<String> adjacentVertex = shortestPath.insertVertex(adjacent);
					shortestPath.insertDirectedEdge(vertex, adjacentVertex, movie);
					baconQue.add(adjacent);
				}
			}
		}
		return shortestPath;
	}
	
	/*
	 * given the name of an actor, returns on screen the actor's kevin bacon number
	 */
	public static void findBaconNumber(DirectedAdjListMap<String, String> bfsGraph, AdjacencyListGraphMap<String, String> graph){
		String root = "Kevin Bacon";
		Scanner input = new Scanner(System.in);
		System.out.println("To quit the program, type return in answer to a question");
		
		while(true){
			ArrayList<String> shortestPath = new ArrayList<String>();
			System.out.println("Enter the name of an actor: ");
			String name = input.nextLine();
			
			//break from the while loop and end the game if the user inputs "return"
			if (name.equals("return")){
				System.out.println("Thanks for playing");
				break;
			}
			
			//otherwise, play the game
			else{
				Vertex<String> actor = bfsGraph.getVertex(name);
				int baconNumber = 0;
				
				//if the name is neither in the bfsGraph nor the general undirected graph, it is not in our database
				if(!bfsGraph.vertexInGraph(name) && !graph.vertexInGraph(name)){
					System.out.println(name + " is not in our database.");
				}
				
				//if the name can only be found in the general undirected graph and not in the bfs graph, the kevin bacon number of the actor is infinite
				else if (!bfsGraph.vertexInGraph(name) && graph.vertexInGraph(name)){
					System.out.println(name + " has no linkage to Kevin Bacon." + "\n" + "Therefore, " + name + "'s Bacon Number is infinite.");
				}
				
				//otherwise, the actor has kevin bacon number, so find it
				else{
					
					//until we get to the root, keep the while loop
					while(actor != bfsGraph.getVertex(root)){
						
						//there can only be one incident edge with the actor as the destination
						Edge<String> edge = bfsGraph.incidentEdgesIn(actor).iterator().next();
						Vertex<String> adjacentActor = bfsGraph.opposite(actor, edge);
						shortestPath.add(actor + " appeared in " + edge.element() + " with " + adjacentActor);
						actor = adjacentActor;
						baconNumber++;
					}
					
					//once complete, return bacon number and the shortest path from the actor to Kevin Bacon
					System.out.println(name + "'s Bacon Number is: " + baconNumber);
					for (int i = 0; i < shortestPath.size(); i++){
						System.out.println(shortestPath.get(i));
					}
				}
			}
		}
	}	
	
	
	public static void main(String[] args) throws IOException{
		//Test Output
//		AdjacencyListGraphMap<String, String> exampleGraph = new AdjacencyListGraphMap<String, String>();
//		exampleGraph.insertVertex("Kevin Bacon");
//		exampleGraph.insertVertex("actor 1");
//		exampleGraph.insertVertex("actor 2");
//		exampleGraph.insertVertex("actor 3");
//		exampleGraph.insertVertex("actor 4");
//		exampleGraph.insertVertex("actor 5");
//		exampleGraph.insertVertex("actor 6");
//		exampleGraph.insertEdge("Kevin Bacon", "actor 1", "movie 1");
//		exampleGraph.insertEdge("Kevin Bacon", "actor 2", "movie 1");
//		exampleGraph.insertEdge("actor 1", "actor 2", "movie 1");
//		exampleGraph.insertEdge("actor 1", "actor 3", "movie 2");
//		exampleGraph.insertEdge("actor 3", "actor 2", "movie 3");
//		exampleGraph.insertEdge("actor 3", "actor 4", "movie 4");
//		exampleGraph.insertEdge("actor 5", "actor 6", "movie 5");
//		DirectedAdjListMap<String, String> bfsGraph = createBFSMap("Kevin Bacon", exampleGraph);
//		findBaconNumber(bfsGraph, exampleGraph);
//		
		//Real Kevin Bacon Game
		try{
			createGraph("actors.txt", "movies.txt", "movie-actors.txt");
			DirectedAdjListMap<String, String> bfsMap = createBFSMap("Kevin Bacon", baconGraph);
			findBaconNumber(bfsMap, baconGraph);
		}
		catch (IOException e){
			System.out.println("Text File could not be found.");
		}
	}
}