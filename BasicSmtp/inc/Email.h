/******************************************************************************
* 
* Email.h
* 
* Author: 夏锦熠
* 
******************************************************************************/

#pragma once

#ifndef MAILPROXY_EMAIL_
#define MAILPROXY_EMAIL_

#include <string>
#include <map>
#include <list>

namespace MailProxy {
    auto check_email_addr(const char* addr) -> bool;

    struct Email {
        /**
         * @brief 邮件正文
         */
        std::string body;
        /**
         * @brief 邮件标头中的 "To", "Cc" 和 "Bcc" 部分
         *
         * 用 list 存储多个收件人的邮箱地址。
         */
        std::list<std::string> to_rcpt, cc_rcpt, bcc_rcpt;
        /**
         * @brief 邮件标头中除 "From", "To", "Cc" 和 "Bcc" 之外的部分
         * （如 "Subject" 等）
         * 
         * 用键值对存储标签和内容。
         */
        std::map<std::string, std::string> ext_headers;
    };
}

#endif