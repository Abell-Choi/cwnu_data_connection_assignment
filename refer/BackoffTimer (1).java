
	//////////////////////////////////////////////
    /*
	 * Randomly selected back-off time,
	 * Calculated according to the retransmission number
	 * random multiples by k times for k-th retransmission
	 * @param transNum  : number of retransmission
	 * @return Random multiples
	 */

	public int BackoffTimer(int transNum) { 
		int rndom;
		int temp;
		temp=Math.min(transNum,10);
		rndom=(int)(Math.random()*(Math.pow(2,temp)-1));
		return rndom;
	}
	//////////////////////////////////////////////
