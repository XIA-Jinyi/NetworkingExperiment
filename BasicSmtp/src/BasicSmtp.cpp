/******************************************************************************
* 
* BasicSmtp.cpp
* 
* Author: 黄凯博, 夏锦熠
* 
******************************************************************************/

#include "BasicSmtp.h"
#include <iostream>
#include <string>
#include "EscSeq.h"

MailProxy::BasicSmtp::BasicSmtp() {
    tcp_conn = new MailProxy::ClientTcp(8192, [](const char *log) -> void {
        std::cerr << CONSOLE_SET C_RED << "Tcp: " << log << CONSOLE_RESET << std::endl;
    });
};

MailProxy::BasicSmtp::~BasicSmtp(){
    tcp_conn->tcp_send("QUIT\r\n");
    if (check_tcp())
        tcp_conn->tcp_receive();
    delete tcp_conn;
};

auto MailProxy::BasicSmtp::get_smtp_status() -> MailProxy::SmtpStatus {
    return this->status;
}

auto MailProxy::BasicSmtp::get_smtp_reply() -> MailProxy::SmtpReply {
    return SmtpReply{this->reply_code, this->reply_msg};
}


auto MailProxy::BasicSmtp::get_smtp_info() -> std::string {
    return this->info;
}


auto MailProxy::BasicSmtp::get_tcp_status() -> MailProxy::TcpStatus {
    return this->tcp_conn->get_status();
}

void MailProxy::BasicSmtp::smtp_login(const char* server_addr, const char* username, const char* password)
{
    // 若服务器为 QQ 邮箱，则发送消息的结尾应为 "\r\n"
    tcp_conn->tcp_connect(server_addr, "25");
    tcp_conn->tcp_receive();
    if (!check()) return;
   
    tcp_conn->tcp_send("EHLO Bupt\r\n");
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;
   

    tcp_conn->tcp_send("AUTH LOGIN\r\n");
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;
    
    // 发送方邮箱的base64
    tcp_conn->tcp_send((username + std::string("\r\n")).c_str());
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;
      
    // 授权码base64
    tcp_conn->tcp_send((password + std::string("\r\n")).c_str());
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;
}

void MailProxy::BasicSmtp::smtp_send(std::string sender, MailProxy::Email email)
{
    // 设定发送对象
    tcp_conn->tcp_send(("MAIL FROM:<" + sender + ">" + std::string("\r\n")).c_str());
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;

    // 分别输出RCPT TO目标对象
    send_email_rcpt(email.to_rcpt);
    send_email_rcpt(email.cc_rcpt);
    send_email_rcpt(email.bcc_rcpt);
    
    //输出接收对象
    std::string rcptlist;
    append_rcpt(rcptlist, email.to_rcpt);
    std::string cc_rcptlist;
    append_rcpt(cc_rcptlist, email.cc_rcpt);
    std::string bcc_rcptlist;
    append_rcpt(bcc_rcptlist, email.bcc_rcpt);
    std::string headers_str;
    
    tcp_conn->tcp_send("DATA\r\n");
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;

    for (const auto& entry : email.ext_headers) {
        headers_str = entry.first + ": " + entry.second;
    }

    std::string message =
        "From: <"+ sender + ">\r\n"
        "To: <" +  rcptlist + ">\r\n"
        "Cc: <" + cc_rcptlist + ">\r\n"
        "Bcc: <" + bcc_rcptlist + ">\r\n"
        + headers_str + " \r\n"
        "\r\n" + 
        email.body + "\r\n"
        "\r\n.\r\n";
    // std::cout << message << std::endl;
    tcp_conn->tcp_send(message.c_str());
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;
}

void MailProxy::BasicSmtp::smtp_send_raw(std::string sender, std::list<std::string> rcpt, std::string raw_data)
{
    tcp_conn->tcp_send(("MAIL FROM:<" + sender + ">" + std::string("\r\n")).c_str());
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;

    send_email_rcpt(rcpt);
    
    tcp_conn->tcp_send("DATA\r\n");
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;

    tcp_conn->tcp_send((raw_data + "\r\n.\r\n").c_str());
    if (!check_tcp()) return;
    tcp_conn->tcp_receive();
    if (!check()) return;
}

void MailProxy::BasicSmtp::send_email_rcpt(const std::list<std::string>& recipients)
{
    for (const std::string& rcpt : recipients)
    {   
        tcp_conn->tcp_send(("RCPT TO:<" + rcpt + ">" + std::string("\r\n")).c_str());
        if (!check_tcp()) return;
        tcp_conn->tcp_receive();
        if (!check()) return;
    }
}

void MailProxy::BasicSmtp::append_rcpt(std::string& rcptlist, const std::list<std::string>& rcpt)
{
    for (auto it = rcpt.begin(); it != rcpt.end(); ++it)
    {
        rcptlist += *it;
        if (std::next(it) != rcpt.end())
            rcptlist += ">;<";
    }
}

bool MailProxy::BasicSmtp::check_tcp() {
    if (tcp_conn->get_status() != TcpStatus::OK) {
        this->status = SmtpStatus::TcpErr;
        return false;
    }
    return true;
}

bool MailProxy::BasicSmtp::check() {
    //检查状态是否是OK
    if (tcp_conn->get_status() != TcpStatus::OK) {
        this->status = SmtpStatus::TcpErr;
        return false;
    }

    //截取目标信息
    //code:截取前三位数字码
    //reply_msg:抹去msg前4位,获取信息
    std::string msg = tcp_conn->get_received();
    //std::cout << msg;
    std::string code= msg.substr(0, 3);
    reply_msg = msg.erase(0, 4);
    int code_num = std::stoi(code);
    
    //设置reply_code
    reply_code = static_cast<SmtpReplyCode>(code_num);

    // 设置 status
    // 4, 5 开头认为SMTP错误
    switch (code_num / 100) {
    case 4:
    case 5:
        status = SmtpStatus::SmtpErr;
        return false;
    default:
        status = SmtpStatus::OK;
        break;
    }
    return true;
}
