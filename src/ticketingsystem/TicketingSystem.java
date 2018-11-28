package ticketingsystem;

class Ticket {
    long tid;
    String passenger;
    int route;
    int coach;
    int seat;
    int departure;
    int arrival;

    @Override
    public String toString() {
        return "Ticket{" +
                "tid=" + tid +
                ", passenger='" + passenger + '\'' +
                ", route=" + route +
                ", coach=" + coach +
                ", seat=" + seat +
                ", departure=" + departure +
                ", arrival=" + arrival +
                '}';
    }
}

public interface TicketingSystem {

    Ticket buyTicket(String passenger, int route,
                     int departure, int arrival);

    /**
     * inquiry rest tickets number of route from station departure to arrival
     *
     * @param route
     * @param departure
     * @param arrival
     * @return rest tickets amount
     */
    int inquiry(int route, int departure, int arrival);

    boolean refundTicket(Ticket ticket);
}