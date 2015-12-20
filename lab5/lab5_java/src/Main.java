import java.io.File;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

import org.apache.lucene.index.IndexReader;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.store.FSDirectory;


public class Main {

	public static void main(String[] args) throws Exception {
		PrintWriter writer = new PrintWriter("/Users/gaby/Documents/MIRI/3rd_Semester/IR/Lab5/cosine_similarities.txt", "UTF-8");
		
		ArrayList<TweetFilesSimilarity> cosineSimilarities = calculateCosineSimilarities();
		Collections.sort(cosineSimilarities, new Comparator<TweetFilesSimilarity>() {

			@Override
			public int compare(TweetFilesSimilarity o1, TweetFilesSimilarity o2) {
				if (o1.getCosineSimilarity() < o2.getCosineSimilarity()) {
					return -1;
				}
				else if (o1.getCosineSimilarity().equals(o2.getCosineSimilarity())) {
					return 0;
				}
				else {
					return 1;
				}
			}
		});
		Collections.reverse(cosineSimilarities);
		
		for (TweetFilesSimilarity cosineSimilarity : cosineSimilarities) {
			writer.println(cosineSimilarity.getTweetFileName1() + ";" + cosineSimilarity.getTweetFileName2() + ";" + cosineSimilarity.getCosineSimilarity());			
		}
		
		writer.close();
	}

	public static ArrayList<TweetFilesSimilarity> calculateCosineSimilarities() throws Exception {
		String tweetsDirectory = "/Users/gaby/Documents/MIRI/3rd_Semester/IR/Lab5/tweets";
		
		File dir = new File(tweetsDirectory);
		File[] directoryListing = dir.listFiles();
		ArrayList<String> tweetFileNames = new ArrayList<String>();
				
		for (File child : directoryListing) {
			if (child.getName().equals(".DS_Store")) {
				continue;
			}
			
			tweetFileNames.add(child.getAbsolutePath());
		}
		
		ArrayList<TweetFilesSimilarity> cosineSimilarities = new ArrayList<TweetFilesSimilarity>();
		
		String indexDirectory = "/Users/gaby/Documents/MIRI/3rd_Semester/IR/Lab5/indexes/lab5_index";
		
		IndexReader reader = IndexReader.open(FSDirectory.open(new File(indexDirectory)));
		IndexSearcher searcher = new IndexSearcher(reader);
		
		int id1;
		int id2;
		
		TermWeight[] v1;
		TermWeight[] v2;
		
		String auxTweetFileName1;
		String auxTweetFileName2;
		String [] auxSplit;
		
		for (String tweetFileName1 : tweetFileNames) {
			for (String tweetFileName2 : tweetFileNames) {
				if (!tweetFileName1.equals(tweetFileName2)) {
					id1 = TfIdfViewer.findDocId(searcher, tweetFileName1);
					id2 = TfIdfViewer.findDocId(searcher, tweetFileName2);
					
					v1 = TfIdfViewer.toTfIdf(reader, id1);
					v2 = TfIdfViewer.toTfIdf(reader, id2);
					
					auxSplit = tweetFileName1.split("/");
					auxTweetFileName1 = auxSplit[auxSplit.length - 1];
					
					auxSplit = tweetFileName2.split("/");
					auxTweetFileName2 = auxSplit[auxSplit.length - 1];
					
					cosineSimilarities.add(new TweetFilesSimilarity(auxTweetFileName1, auxTweetFileName2, new Double(TfIdfViewer.cosineSimilarity(v1, v2))));
				}				
			}			
		}
		
		searcher.close();
		reader.close();
		
		return cosineSimilarities;
	}
}
