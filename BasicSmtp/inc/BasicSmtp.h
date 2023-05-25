/******************************************************************************
* 
* BasicSmtp.h
* 
* Author: 夏锦熠
* 
******************************************************************************/

#pragma once

#ifndef MAILPROXY_BASICSMTP_
#define MAILPROXY_BASICSMTP_

#include <cstdint>
#include <BasicTcp.h>
#include <functional>
#include <list>
#include <string>
#include "Email.h"

namespace MailProxy {

    enum class SmtpReplyCode : uint16_t {
        /**
         * @brief Syntax error, command unrecognized
         */
        CmdSyntaxErr = 500,
        /**
         * @brief Syntax error in parameters or arguments
         */
        ParamSyntaxErr = 501,
        /**
         * @brief Command not implemented
         */
        CmdNotImpl = 502,
        /**
         * @brief Bad sequence of commands
         */
        BadCmdSeq = 503,
        /**
         * @brief Command parameter not implemented
         */
        ParamNotImpl = 504,

        /**
         * @brief System status, or system help reply
         */
        SysStatus = 211,
        /**
         * @brief Help message
         */
        HelpMsg = 214,
        /**
         * @brief <domain> Service ready
         */
        ServiceReady = 220,
        /**
         * @brief <domain> Service closing transmission channel
         */
        ServiceClosing = 221,
        /**
         * @brief <domain> Service not available, closing transmission channel
         */
        ServiceUnavailable = 421,
        
        /**
         * @brief Requested mail action okay, completed
         */
        Completed = 250,
        /**
         * @brief User not local; will forward to <forward-path>
         */
        Forward = 251,
        /**
         * @brief Cannot VRFY user, but will accept message and attempt delivery
         */
        UnverifiedAccept = 252,
        /**
         * @brief Server unable to accommodate parameters
         */
        UnableAccommodateParam = 455,
        /**
         * @brief MAIL FROM/RCPT TO parameters not recognized or not implemented
         */
        MailParamNotImpl = 555,
        /**
         * @brief Requested mail action not taken: mailbox unavailable
         */
        TransientMailboxUnavailable = 450,
        /**
         * @brief Requested action not taken: mailbox unavailable
         */
        PermanentMailboxUnavailable = 550,
        /**
         * @brief Requested action aborted: error in processing
         */
        ProcessingErr = 451,
        /**
         * @brief User not local; please try <forward-path>
         */
        UserNotLocal = 452,
        /**
         * @brief Requested action not taken: insufficient system storage
         */
        InsufficientSysStorage = 452,
        /**
         * @brief Requested mail action aborted: exceeded storage allocation
         */
        ExceededStorageAllocation = 552,
        /**
         * @brief Requested action not taken: mailbox name not allowed
         */
        MailboxNotAllowed = 553,
        /**
         * @brief Start mail input; end with <CRLF>.<CRLF>
         */
        StartingMailInput = 354,
        /**
         * @brief Transaction failed
         */
        TransactionFailed = 554,
    };

    struct SmtpReply {
        SmtpReplyCode code;
        std::string msg;
    };

    enum class SmtpStatus : int {
        OK = 0,
        TcpErr,
        SmtpErr,
    };

    class BasicSmtp {
    private:
        ClientTcp tcp_conn;
        SmtpStatus status;
        SmtpReplyCode reply_code;
        std::string reply_msg;
        std::function<void(const char*)> log = NULL;
        std::string info;
    
    public:
        BasicSmtp();

        ~BasicSmtp();

        /**
         * @brief 登录到 ESMTP 服务器。
         * 
         * @param server_addr 服务器地址
         * @param username 用户名（base64 编码）
         * @param password 密码（base64 编码）
         */
        void smtp_login(const char* server_addr, const char* username, const char* password);

        /**
         * @brief 发送构造好的邮件。
         * 
         * @param sender
         * @param email 
         */
        void smtp_send(std::string sender, Email email);

        /**
         * @brief 获取当前 SMTP 状态。
         * 
         * @return SmtpStatus 
         */
        auto get_smtp_status() -> SmtpStatus;

        /**
         * @brief 获取最新一次的回复。
         * 
         * @return SmtpReply 
         */
        auto get_smtp_reply() -> SmtpReply;

        /**
         * @brief 预留接口，供此模块与上层模块通信使用。
         * 
         * @attention 直接返回 info，不做改动
         * 
         * @return std::string 
         */
        auto get_smtp_info() -> std::string;

        /**
         * @brief 下层 Tcp 状态。
         * 
         * @return TcpStatus 
         */
        auto get_tcp_status() -> TcpStatus;
    };
}

#endif
