/******************************************************************************
* 
* BasicSmtp.cpp
* 
* Author: 黄凯博、夏锦熠
* 
******************************************************************************/

#include "BasicSmtp.h"

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
    return this->tcp_conn.get_status();
}