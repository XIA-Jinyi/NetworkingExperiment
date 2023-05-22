/******************************************************************************
* 
* BasicTcp.h
* 
* Author: 夏锦熠
* 
******************************************************************************/

#pragma once

#ifndef MAILPROXY_BASICTCP_
#define MAILPROXY_BASICTCP_

#define WIN32_LEAN_AND_MEAN

#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdint.h>
#include <functional>
#include <string>

namespace MailProxy {

    enum class TcpStatus : uint8_t {
        /**
         * @brief 正常
        */
        OK = 0x00,
        /**
         * @brief Socket 连接关闭
        */
        Closed = 0x01,

        /**
         * @brief Winsock 初始化失败
        */
        WsaStartupFailed = 0xFE,
        /**
         * @brief getaddrinfo 失败
        */
        GetAddrInfoFailed = 0xFD,
        /**
         * @brief Socket 初始化失败
        */
        SocketFailed = 0xFB,
        /**
         * @brief 连接服务器失败
        */
        ConnServerFailed = 0xF7,
        /**
         * @brief 接收数据失败
        */
        RecvFailed = 0xF7,
        /**
         * @brief 发送数据失败
        */
        SendFailed = 0xEF,
        /**
         * @brief 关闭连接失败
        */
        ShutdownFailed = 0xDF,
        /**
         * @brief 未知错误
        */
        UnknownError = 0xFF,
    };

    class BasicTcp{
    private:
        WSADATA wsaData;
        SOCKET ConnectSocket = INVALID_SOCKET;
        struct addrinfo* result = NULL, * ptr = NULL, hints;
        int iResult;
        char* sendbuf = NULL, * recvbuf = NULL;
        std::function<void(const char*)> log = NULL;
        TcpStatus status = TcpStatus::OK;
        std::string status_info;

    public:
        /**
         * @brief 初始化 Winsock 及其他资源。
         * @param default_buflen 默认的缓冲区大小
         * @param log_callback 记录日志的回调函数
        */
        BasicTcp(
            size_t default_buflen = 4096,
            std::function<void(const char*)> log_callback = NULL
        );

        /**
         * @brief 关闭连接并释放所有资源。
        */
        ~BasicTcp();

        /**
         * @brief 建立 TCP 连接。
         * @param server_addr 服务器地址
         * @param port 端口号
        */
        void tcp_connect(
            const char* server_addr,
            const char* port
        );

        /**
         * @brief 发送数据。
         * @param data 待发送的数据
         * @param flags 传递给 send 函数的 flags 参数
        */
        void tcp_send(
            const char* data,
            int flags = 0
        );

        /**
         * @brief 接收数据。
         * @param flags 传递给 recv 函数的 flags 参数
        */
        void tcp_receive(
            int flags = 0
        );

        /**
         * @brief 关闭连接。
         * @param how 关闭连接的方式
        */
        void tcp_shutdown(
            int how = SD_BOTH
        );

        /**
         * @brief 取出收到的数据。
         * @return 缓冲区内的数据
        */
        auto get_received() -> std::string;

        /**
         * @brief 获取当前连接状态。
         * @return 状态码
        */
        auto get_status() -> TcpStatus;

        /**
         * @brief 获取当前连接状态的相关信息。
         * @return 状态相关信息
        */
        auto get_status_info() -> std::string;
    };

}

#endif
