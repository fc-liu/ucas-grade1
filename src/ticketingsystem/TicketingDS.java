package ticketingsystem;

public class TicketingDS implements TicketingSystem {
    int routenum;
    Route[] routes;
    static long id;

    static synchronized long increaId() {
        id++;
        return id;
    }

    public TicketingDS(int routenum, int coachnum, int seatnum, int stationnum) {
        id = 0;
        this.routenum = routenum;
        this.routes = new Route[routenum];
        for (int i = 0; i < routenum; i++) {
            this.routes[i] = new Route(coachnum, seatnum, stationnum);
        }
    }

    @Override
    public Ticket buyTicket(String passenger, int route, int departure, int arrival) {
        //tid unique
        Ticket ticket = null;
        if (route > this.routenum) {
            return ticket;
        }
        ticket = this.routes[route - 1].buy(departure, arrival);
        if (null != ticket) {
            ticket.route = route;
            ticket.passenger = passenger;
        }
        return ticket;
    }

    /**
     * wait-free
     *
     * @param route
     * @param departure
     * @param arrival
     * @return total rest tickets from departure to arrival
     */
    @Override
    public int inquiry(int route, int departure, int arrival) {
        // no need to lock
        int total;
        if (route > this.routenum) {
            return 0;
        }
        total = this.routes[route - 1].inquiry(departure, arrival);
        return total;
    }

    /**
     * wait-free
     *
     * @param ticket
     * @return
     */
    @Override
    public boolean refundTicket(Ticket ticket) {
        //tid invalid
        if (null == ticket) {
            return false;
        }
        int route = ticket.route;

        if (route > this.routenum) {
            return false;
        }
        route -= 1;
        return this.routes[route].refund(ticket);
    }
}