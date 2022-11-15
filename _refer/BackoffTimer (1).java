
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

	def get_back_off_timer(transNum):
		rnd = random.randrange(1, 100)

		# 과제 제공물의 BackofTimer를 python으로 변환
def back_of_timer_func(trans_number:int):
    trans_number = trans_number if trans_number<=10 else 10
    time = random.randrange(0,  * math.pow(2, trans_number)-1)
    return time

def update_back_off_time(msec_data:int):    # update back_off_timer
    back_off_timer = datetime.now() + timedelta(milliseconds=msec_data)

def check_back_off_time():
    if back_off_end_time == None: back_off_end_time = update_back_off_time(random.randrange(1,100))
    return False if back_off_end_time > datetime.now() else True



	//////////////////////////////////////////////
