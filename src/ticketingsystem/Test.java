package ticketingsystem;


import java.util.ArrayList;

public class Test extends Thread {
    static int method_call_num = 10000;

    final static double inquiry_percent = 0.6;
    final static double buy_percent = 0.3;
    final static double refund_percent = 0.1;

    static int inq_num = 0;
    static int buy_num = 0;
    static int refund_num = 0;

    static int routenum = 5;
    static int coachnum = 8;
    static int seatnum = 100;
    static int stationnum = 10;

    static TicketingDS tds;


    static {
        tds = new TicketingDS(routenum, coachnum, seatnum, stationnum);
        inq_num = Integer.parseInt(new java.text.DecimalFormat("0").format(inquiry_percent * method_call_num));
        buy_num = Integer.parseInt(new java.text.DecimalFormat("0").format(buy_percent * method_call_num));
        refund_num = method_call_num - inq_num - buy_num;
    }

    @Override
    public void run() {
        int departure;
        int arrival;
        int route = 1;
        int rest;
//        Ticket[] tickets = new Ticket[buy_num];
        for (int i = 0; i <= buy_num; i++) {
            departure = 1;
            arrival = (int) Math.round(Math.random() * (stationnum - 1) + 1);
//            int rest = tds.inquiry(1, departure, arrival);
//            println("rest : " + rest);
            Ticket ticket = tds.buyTicket(currentThread().getName(), route, departure, arrival);
//            tickets[i] = ticket;
//            println(ticket);

            if (i <= inq_num) {
                rest = tds.inquiry(route, departure, arrival);
//                println(rest);
            }

            if (i <= refund_num && (null != ticket)) {
                boolean refres = tds.refundTicket(ticket);
//                println(refres);
            }
        }
    }

    public void test() {
//        int departure = 1;
//        int arrival = 5;
//
//
//        int rest;
//        Ticket ticket = tds.buyTicket(currentThread().getName(), 1, departure, arrival);
//        boolean ref = tds.refundTicket(ticket);
//        println("ref : " + ref);
//        rest = tds.inquiry(1, departure, arrival);
//        println("rest : " + rest);
////        rest = tds.inquiry(1, departure, arrival);
////        println("rest : " + rest);

////        rest = tds.inquiry(1, departure, arrival);
////        println("rest : " + rest);
////        rest = tds.inquiry(1, 6, 10);
////        println("rest : " + rest);
////        Ticket ticket1 = tds.buyTicket(currentThread().getName(), 1, 6, 10);
////        rest = tds.inquiry(1, 6, 10);
////        println("rest : " + rest);
////        tds.refundTicket(ticket);
////        rest = tds.inquiry(1, departure, arrival);
////        println("rest : " + rest);
////        tds.refundTicket(ticket1);
////        rest = tds.inquiry(1, 6, 10);
////        println("rest : " + rest);

    }

    public static void main(String[] args) {
        int threadNum = Integer.parseInt(args[0]);
        Thread[] threads = new Test[threadNum];
        long start;
        long end;
        start = System.currentTimeMillis();
        for (int i = 0; i < threadNum; i++) {
            threads[i] = new Test();
            threads[i].start();
        }
        for (int i = 0; i < threadNum; i++) {
            try {
                threads[i].join();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        end = System.currentTimeMillis();

        println("total time : " + (end - start));

//        Test test = new Test();
//        test.test();

    }


    public static void println(Object obj) {
        System.out.println(obj);
    }


}

