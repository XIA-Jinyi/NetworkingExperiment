#include <iostream>
#include "BasicTcp.h"
#include "Email.h"

using namespace MailProxy;

void print_log(const char* log) {
    std::cout << "Tcp::" << log << std::endl;
}

/**
 * @brief 发送邮件（未进行错误处理）。
 * @return 返回值
*/
int main() {
    ClientTcp tcp_conn(8192, print_log);
    tcp_conn.tcp_connect("smtp.126.com", "25"); // 若服务器为 QQ 邮箱，则发送消息的结尾应为 "\r\n"
    tcp_conn.tcp_receive();
    std::cout << tcp_conn.get_received() << std::endl;

    tcp_conn.tcp_send("EHLO Bupt\n");
    tcp_conn.tcp_receive();
    std::cout << tcp_conn.get_received() << std::endl;

    // tcp_conn.tcp_send("AUTH LOGIN\n");
    // tcp_conn.tcp_receive();
    // std::cout << tcp_conn.get_received() << std::endl;
    // tcp_conn.tcp_send("eGlhamlueWlAMTI2LmNvbQ==\n");
    // tcp_conn.tcp_receive();
    // std::cout << tcp_conn.get_received() << std::endl;
    // tcp_conn.tcp_send("********PASSWORD********\n");
    // tcp_conn.tcp_receive();
    // std::cout << tcp_conn.get_received() << std::endl;

    // tcp_conn.tcp_send("MAIL FROM:<xiajinyi@126.com>\n");
    // tcp_conn.tcp_receive();
    // std::cout << tcp_conn.get_received() << std::endl;
    // tcp_conn.tcp_send("RCPT TO:<jinyi.xia@bupt.edu.cn>\n");
    // tcp_conn.tcp_receive();
    // std::cout << tcp_conn.get_received() << std::endl;

    // tcp_conn.tcp_send("DATA\n");
    // tcp_conn.tcp_receive();
    // std::cout << tcp_conn.get_received() << std::endl;
    // tcp_conn.tcp_send(
    //     "From: \"=?utf-8?B?eGlhamlueWk=?=\"<xiajinyi@126.com>\n"
    //     "To: \"=?utf-8?B?amlueWkueGlh?=\"<jinyi.xia@bupt.edu.cn>\n"
    //     "Subject: Test tcp client\n"
    //     "\n"
    //     "A quick brown fox jumps over the lazy dog.\n"
    //     "\n.\n"
    // );
    // tcp_conn.tcp_receive();
    // std::cout << tcp_conn.get_received() << std::endl;
    
    tcp_conn.tcp_send("QUIT\n");
    tcp_conn.tcp_receive();
    std::cout << tcp_conn.get_received() << std::endl;

    // 一般情况下不需要手动 shutdown
    tcp_conn.tcp_shutdown();
    return 0;
}