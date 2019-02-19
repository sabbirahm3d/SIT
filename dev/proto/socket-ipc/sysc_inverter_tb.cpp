#include "sysc_inverter.cpp"

#include "sstsysc.hpp"
#include <systemc.h>

#include <mpi.h>

int sc_main(int argc, char *argv[]) {

    sc_signal<bool> clock;
    sc_signal<sc_uint<4> > data_in;
    sc_signal<sc_uint<4> > data_out;

    // Connect the DUT
    sysc_inverter sysc_inverter("INVERTER");
    sysc_inverter.data_in(data_in);
    sysc_inverter.data_out(data_out);

    int done_already;
    MPI_Initialized(&done_already);
    if (!done_already) {
        MPI_Init(nullptr, nullptr);
    }

    // Find out rank, size
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    MPI_Comm intercomm;
    MPI_Comm_get_parent(&intercomm);

    /*
    int sock_fd = socket(AF_INET, SOCK_STREAM, 0);
//    int sock_fd = 26;
    struct hostent *server = gethostbyname("work-vm01");
    struct sockaddr_in serv_addr{};

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy(server->h_addr, (char *) &serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons((uint16_t) std::stoi(argv[1]));

    if (connect(sock_fd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
        perror("CHILD");
        exit(-1);
    }

    // create an empty structure (null)
    json m_data_in;
    json m_data_out;

    if (sock_fd < 0) {
        perror("ERROR on accept");
    }


    std::string pid = to_string(getpid());
    if (write(sock_fd, pid.c_str(), pid.size()) != pid.size()) {
        perror("ERROR writing to socket");
    }

    try {

        bool flag;

        do {

            char m_buffer[BUFSIZE];

            sc_start(1, SC_NS);

            m_data_out["data_out"] = to_string(data_out);

            send_json(m_data_out, sock_fd);
            m_data_out.clear();

            m_data_in = recv_json(m_buffer, sock_fd);

            flag = m_data_in["on"].get<bool>();
            data_in = m_data_in["data_in"].get<int>();

            std::cout << "\033[33mINVERTER\033[0m (pid: " << getpid() << ") -> clock: " << clock << " | data_in: "
                      << m_data_in["data_in"] << std::endl;
            m_data_in.clear();

        } while (flag);

    } catch (json::type_error &e) {

        std::cout << getpid() << " INVERTER JSON TYPE ERROR " << e.what() << m_data_in << " ON " << sock_fd << std::endl;

    }


    close(sock_fd);

    return 0;  // Terminate simulation
*/

    int sendbuf[2] = {3, 6};
    int recvbuf[2];

    MPI_Scatter(sendbuf, 1, MPI_INT, recvbuf, 1, MPI_INT, 0, intercomm);
    printf("INVERTER=%d WORLD=%d SIZE=%d PID=%d\n", *recvbuf, world_rank, world_size, getpid());
    MPI_Gather(sendbuf, 1, MPI_INT, recvbuf, 1, MPI_INT, 0, intercomm);

    MPI_Scatter(sendbuf, 1, MPI_INT, recvbuf, 1, MPI_INT, 0, intercomm);
    printf("INVERTER=%d WORLD=%d SIZE=%d PID=%d\n", *recvbuf, world_rank, world_size, getpid());
    MPI_Gather(sendbuf, 1, MPI_INT, recvbuf, 1, MPI_INT, 0, intercomm);

    MPI_Finalize();
    return 0;


}
