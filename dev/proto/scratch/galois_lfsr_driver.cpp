#include "../modules/galois_lfsr.hpp"

#include "sigutils1.hpp"

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

int sc_main(int argc, char *argv[]) {

    // ---------- SYSTEMC UUT INIT ---------- //
    sc_signal<bool> clock;
    sc_signal<bool> reset;
    sc_signal<sc_uint<4> > data_out;

    // Connect the DUT
    galois_lfsr DUT("GALOIS_LFSR");
    DUT.clock(clock);
    DUT.reset(reset);
    DUT.data_out(data_out);
    // ---------- SYSTEMC UUT INIT ---------- //

    int m_socket = socket(AF_UNIX, SOCK_STREAM, 0);
    SignalReceiver sh_in;

    sh_in.set_params(m_socket, argv[1], false);

    sh_in.set("pid", getpid(), SC_UINT_T);
    sh_in.send();

    while (true) {

        sc_start(1, SC_NS);

        printf("receiving\n");
        // RECEIVING
        sh_in.recv();
        printf("received\n");

        if (!sh_in.alive()) {
            break;
        }
        clock = sh_in.get_clock_pulse("clock");
        reset = sh_in.get<bool>("reset");
        std::cout << "\033[33mGALOIS LFSR\033[0m (pid: " << getpid() << ") -> clock: " << sc_time_stamp()
                  << " | reset: " << sh_in.get<bool>("reset") << " -> galois_lfsr_out: " << data_out << std::endl;

        // SENDING
        sh_in.set("data_out", data_out, SC_UINT_T);
        sh_in.send();

    }

    return 0;

}
