#include <iostream>
#include "BasicTcp.h"

void print_log(const char* log) {
    std::cout << log << std::endl;
}

int main() {
    MailProxy::BasicTcp tcp_conn(4096, print_log);
    tcp_conn.connect("127.0.0.1", "80");
    tcp_conn.send(NULL);
    tcp_conn.receive();
    tcp_conn.shutdown();
    return 0;
}