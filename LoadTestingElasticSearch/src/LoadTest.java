import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Random;

import org.apache.commons.io.IOUtils;

public class LoadTest implements Runnable{
	
	public static volatile ArrayList<double []> runTimeData;
	
	private String completeUrl;
	private double threadId;
	LoadTest(String completeUrl, double threadId){
		this.completeUrl = completeUrl;
		this.threadId = threadId;
	}
	
	public static void main(String[] args) {
		String [] queryList = {"ministry", "found", "conspiracy", "mclaren", "years", "russian", 
								"disturbingly", "london", "samples", "benefited", "competitions", 
								"finger", "agency", "spectators", "football", "attack", "the", 
								"pointed", "professor", "unknowingly", "sports", "paralympic", 
								"canadian", "integrity", "operated", "drugs", "spectators"};
		
		Random rand = new Random(System.currentTimeMillis());

		String baseUrl = "https://search-newssearchengine-rhlbiq3mtga7gj6czbw3box4km.us-east-1.es.amazonaws.com/news/news/_search?q=";

		LoadTest.runTimeData = new ArrayList<double []>();
		
		for(int i=0;i<1000;i++){
			int randomIndex = rand.nextInt(queryList.length);
			String selectedParam = queryList[randomIndex];
			
			String completeUrl = baseUrl + selectedParam;
			//executor.execute(new LoadTest(completeUrl));
			new Thread(new LoadTest(completeUrl, (double) i)).run();
		}
		System.out.println("Completed Threading!");

		FileWriter writer = null;
		try {
			writer = new FileWriter("D:\\output.txt"); 
			for(double [] runData: runTimeData)
				writer.write(
						String.valueOf(runData[0])+","+
						String.valueOf(runData[1])+"\n"
				);
			writer.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@Override
	public void run() {
		long start = System.nanoTime();
		InputStream input = null;
		try{
			input = new URL(completeUrl).openStream();
			StringWriter writer = new StringWriter();
			IOUtils.copy(input, writer, "UTF-8");
			String jsonResult = writer.toString();
			
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
		}
		finally{
			try {
				input.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				//e.printStackTrace();
			}
			long end = System.nanoTime();
			
			double [] runData = { (end - start) / 1.0e9, threadId};
			
			runTimeData.add(runData);
			
			//System.out.println("Time taken(s): " + (end - start) / 1.0e9);
		}
	}
}
