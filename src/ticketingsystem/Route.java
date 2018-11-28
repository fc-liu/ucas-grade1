package ticketingsystem;

/**
 * Created by lfc on 2016/12/17.
 */

public class Route {
    Coach[] coaches;
    int coachNum;

    public Route(int coachNum, int seatNum, int stationNum) {
        this.coachNum = coachNum;
        this.coaches = new Coach[coachNum];

        for (int i = 0; i < coachNum; i++) {
            this.coaches[i] = new Coach(seatNum, stationNum);
        }
    }


    /**
     * starvation-free
     *
     * @param departure
     * @param arrival
     * @return
     */
    public Ticket buy(int departure, int arrival) {
        Ticket ticket = null;
        for (int i = 0; i < this.coachNum; i++) {
            ticket = this.coaches[i].buy(departure, arrival);
            if (null != ticket) {
                ticket.coach = i + 1;
                break;
            }
        }
        return ticket;
    }

    /**
     * wait-free
     *
     * @param departure
     * @param arrival
     * @return total rest tickets
     */
    public int inquiry(int departure, int arrival) {
        int total = 0;
        for (int i = 0; i < this.coachNum; i++) {
            total += this.coaches[i].inquiry(departure, arrival);
        }

        return total;
    }

    /**
     * wait-free
     *
     * @param ticket
     * @return
     */
    public boolean refund(Ticket ticket) {
        int coach = ticket.coach;
        if (coach > this.coachNum) {
            return false;
        }
        coach--;
        return this.coaches[coach].refund(ticket);
    }
}

class Coach {
    Seat[] seats;
    int seatNum;

    public Coach(int seatNum, int stationNum) {
        seats = new Seat[seatNum];
        this.seatNum = seatNum;
        for (int i = 0; i < seatNum; i++) {
            this.seats[i] = new Seat(stationNum);
        }
    }

    /**
     * starvation-free
     *
     * @param departure
     * @param arrival
     * @return
     */
    public Ticket buy(int departure, int arrival) {
        Ticket ticket = null;
        for (int i = 0; i < seatNum; i++) {
            ticket = this.seats[i].buy(departure, arrival);
            if (null != ticket) {
                ticket.seat = i + 1;
                break;
            }
        }
        return ticket;
    }


    /**
     * wait-free
     *
     * @param departure
     * @param arrival
     * @return
     */
    public int inquiry(int departure, int arrival) {
        int total = 0;
        for (int i = 0; i < this.seatNum; i++) {
            if (!this.seats[i].isBought(departure, arrival)) {
                total++;
            }
        }

        return total;
    }

    /**
     * wait-free
     *
     * @param ticket
     * @return
     */
    public boolean refund(Ticket ticket) {
        int seat = ticket.seat - 1;
        if (seat >= this.seatNum) {
            return false;
        }
        return this.seats[seat].refund(ticket);
    }
}

class Seat {
    StationSeat[] ss;
    MyReadWriteLock myLock;
    int stationNum;

    public Seat(int stationNum) {
        this.stationNum = stationNum;
        this.ss = new StationSeat[stationNum];
        this.myLock = new MyReadWriteLock();

        for (int i = 0; i < stationNum; i++) {
            this.ss[i] = new StationSeat();
        }
    }

    /**
     * starvation-free
     */
    public void lock() {
        this.myLock.writeLock().lock();
    }

    /**
     * starvation-free
     */
    public void unlock() {
        this.myLock.writeLock().unlock();
    }

    /**
     * starvation-free
     *
     * @param departure
     * @param arrival
     * @return
     */
    public Ticket buy(int departure, int arrival) {
        departure = departure - 1;
        arrival = arrival - 1;
        if (departure >= arrival) {
            return null;
        } else if ((arrival >= this.stationNum) || (departure < 0)) {
            return null;
        }
        for (int i = departure; i <= arrival; i++) {
            boolean isBought = this.ss[i].isBought();
            if (isBought) {
                return null;
            }
        }
        Ticket ticket;
        try {
            lock();
            long tid;
            for (int i = departure; i <= arrival; i++) {
                boolean isBought = this.ss[i].isBought();
                if (isBought) {
                    return null;
                }
            }
            tid = TicketingDS.increaId();
            for (int i = departure; i <= arrival; i++) {
                this.ss[i].buy(tid);
            }
            ticket = new Ticket();
            ticket.arrival = arrival + 1;
            ticket.tid = tid;
            ticket.departure = departure + 1;

        } finally {
            unlock();
        }


        return ticket;
    }

    /**
     * wait-free
     *
     * @param departure
     * @param arrival
     * @return
     */
    public boolean isBought(int departure, int arrival) {
        departure = departure - 1;
        arrival = arrival - 1;

        if ((departure < 0) || (arrival >= stationNum) || (departure >= stationNum)) {
            return true;
        }
        for (int i = departure; i <= arrival; i++) {
            if (this.ss[i].isBought()) {
                return true;
            }
        }
        return false;
    }

    /**
     * wait-free
     *
     * @param ticket
     * @return
     */
    public boolean refund(Ticket ticket) {
        int departure = ticket.departure;
        int arrival = ticket.arrival;
        departure = departure - 1;
        arrival = arrival - 1;

        if ((departure < 0) || (arrival >= stationNum) || (departure >= stationNum)) {
            return false;
        }

        long id = ticket.tid;

        for (int i = departure; i <= arrival; i++) {
            if (!this.ss[i].isBought()) {
                return false;
            } else if (this.ss[i].getTid() != ticket.tid) {
                return false;
            }
        }

        for (int i = departure; i <= arrival; i++) {
            this.ss[i].refund(id);
        }

        return true;

    }
}

class StationSeat {
    private boolean isBought;
    private long tid;

    public StationSeat() {
        this.isBought = false;
        this.tid = -1;
    }

    /**
     * wait-free
     *
     * @return whether this seat of this station is bought
     */
    public boolean isBought() {
        return isBought;
    }

    /**
     * wait-free
     *
     * @return
     */
    public long getTid() {
        return this.tid;
    }

    /**
     * wait-free
     *
     * @param id
     * @return
     */
    public boolean buy(long id) {
        if (!this.isBought) {
            this.isBought = true;
            this.tid = id;
            return true;
        } else {
            return false;
        }
    }

    /**
     * wait-free refund
     *
     * @param tid
     * @return is refund success
     */
    public boolean refund(long tid) {
        if (this.isBought && tid == this.tid) {
            this.isBought = false;
            this.tid = -1;
            return true;
        } else {
            return false;
        }
    }

}
