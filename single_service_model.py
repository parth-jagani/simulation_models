import numpy as np

MEAN_INTERARRIVAL = 1
MEAN_SERVICE = 0.5
NUM_DELAYS_REQUIRED = 1000

Q_LIMIT = 100
BUSY = 1
IDLE = 0
NUM_EVENTS = 2

sim_time = 0.0
time_last_event = 0
time_arrival = [0] * (Q_LIMIT + 1)
time_next_event = [0] * 2


def timing(outfile):
    global sim_time, time_next_event
    min_time_next_event = 10000000000000000000
    next_event_type = 0

    for i in range(0, NUM_EVENTS):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i + 1

    if next_event_type == 0:
        outfile.write("Event list is empty at time {}".format(sim_time))
        exit(1)

    sim_time = min_time_next_event

    return next_event_type


def arrive(server_status, num_in_q, num_custs_delayed, total_of_delays, outfile):

    global sim_time

    time_next_event[0] = sim_time + expon(MEAN_INTERARRIVAL)

    if server_status == BUSY:

        num_in_q = num_in_q + 1

        if num_in_q > Q_LIMIT:
            outfile.write("Overflow of the array time arrival at time {}".format(sim_time))
            exit(2)

        time_arrival[num_in_q] = sim_time

    else:
        delay = 0.0
        total_of_delays = total_of_delays + delay

        num_custs_delayed = num_custs_delayed + 1
        server_status = BUSY

        time_next_event[1] = sim_time + expon(MEAN_SERVICE)

    return server_status, num_in_q, num_custs_delayed, total_of_delays


def depart(server_status, num_in_q, num_custs_delayed, total_of_delays):

    if num_in_q == 0:
        server_status = IDLE
        time_next_event[1] = 100000000000000000

    else:
        num_in_q = num_in_q - 1
        delay = sim_time - time_arrival[1]
        total_of_delays = total_of_delays + delay

        num_custs_delayed = num_custs_delayed + 1
        time_next_event[1] = sim_time + expon(MEAN_SERVICE)

        for i in range(0, num_in_q + 1):
            time_arrival[i] = time_arrival[i + 1]

    return server_status, num_in_q, num_custs_delayed, total_of_delays


def report(area_server_status, area_num_in_q, num_custs_delayed, total_of_delays, outfile):

    print("Average Delay in Queue   {:.4f} minutes".format(total_of_delays / num_custs_delayed))
    print("Average Number in Queue  {:.4f} people".format(area_num_in_q / sim_time))
    print("Server Utilization       {:.2%} of time".format(area_server_status / sim_time))
    print("Simulation Time          {:.2f} seconds".format(sim_time))

    outfile.write("Average Delay in Queue {:.4f} minutes\n\n".format(total_of_delays / num_custs_delayed))
    outfile.write("Average number in Queue {:.4f}\n\n".format(area_num_in_q / sim_time))
    outfile.write("Server Utilization {:.2%}\n\n".format(area_server_status / sim_time))
    outfile.write("Time when simulation eneded {:.2f}".format(sim_time))


def update_time_avg_status(area_server_status, area_num_in_q, server_status, num_in_q):

    global sim_time, time_last_event

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    area_num_in_q = area_num_in_q + num_in_q * time_since_last_event

    area_server_status = area_server_status + server_status * time_since_last_event

    return area_server_status, area_num_in_q


def expon(mean):
    return mean * (np.random.exponential(1))


def main():
    outfile = open("mm1_out.txt", "w")

    num_custs_delayed = 0
    num_in_q = 0
    server_status = IDLE
    area_num_in_q = 0.0
    area_server_status = 0.0
    total_of_delays = 0.0

    global sim_time, time_last_event
    sim_time = 0.0
    time_last_event = 0.0

    time_next_event[0] = sim_time + expon(MEAN_INTERARRIVAL)
    time_next_event[1] = 100000000000000000000

    outfile.write("Single Server Quiuing System\n\n")
    outfile.write("Mean Interarrival Time: {} minutes\n\n".format(MEAN_INTERARRIVAL))
    outfile.write("Mean Service Time: {} minutes\n\n".format(MEAN_SERVICE))
    outfile.write("Number of Customer: {} \n\n".format(NUM_DELAYS_REQUIRED))

    while num_custs_delayed < NUM_DELAYS_REQUIRED:

        next_event_type = timing(outfile)
        area_server_status, area_num_in_q = update_time_avg_status(area_server_status, area_num_in_q, server_status,
                                                                   num_in_q)

        if next_event_type == 1:
            server_status, num_in_q, num_custs_delayed, total_of_delays = \
                arrive(server_status, num_in_q, num_custs_delayed, total_of_delays, outfile)
        else:
            server_status, num_in_q, num_custs_delayed, total_of_delays = \
                depart(server_status, num_in_q, num_custs_delayed, total_of_delays)

    report(area_server_status, area_num_in_q, num_custs_delayed, total_of_delays, outfile)

    outfile.close()


if __name__ == '__main__':
    main()
