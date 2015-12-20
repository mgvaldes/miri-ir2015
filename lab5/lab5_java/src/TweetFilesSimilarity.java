
public class TweetFilesSimilarity {
	private String tweetFileName1;
	private String tweetFileName2;
	private Double cosineSimilarity;
	
	public TweetFilesSimilarity(String tweetFileName1, String tweetFileName2,
			Double cosineSimilarity) {
		super();
		this.tweetFileName1 = tweetFileName1;
		this.tweetFileName2 = tweetFileName2;
		this.cosineSimilarity = cosineSimilarity;
	}

	public String getTweetFileName1() {
		return tweetFileName1;
	}

	public void setTweetFileName1(String tweetFileName1) {
		this.tweetFileName1 = tweetFileName1;
	}

	public String getTweetFileName2() {
		return tweetFileName2;
	}

	public void setTweetFileName2(String tweetFileName2) {
		this.tweetFileName2 = tweetFileName2;
	}

	public Double getCosineSimilarity() {
		return cosineSimilarity;
	}

	public void setCosineSimilarity(Double cosineSimilarity) {
		this.cosineSimilarity = cosineSimilarity;
	}
}
