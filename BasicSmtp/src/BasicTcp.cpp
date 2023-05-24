/******************************************************************************
*
* BasicTcp.cpp
*
* Author: 张原赫, 夏锦熠
*
******************************************************************************/

#include "BasicTcp.h"
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <winsock2.h>

#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")

void record_error(
    MailProxy::TcpStatus& status_dest,
    std::string& status_info,
    std::function<void(const char*)> log,
    MailProxy::TcpStatus status,
    const char* message,
    int code
) {
    status_dest = status;
    char error_info[256];
    sprintf(error_info, "%s: %d", message, code);
    status_info = std::string(error_info);
    if (log) {
        log(error_info);
    }
}

MailProxy::ClientTcp::ClientTcp(size_t default_buflen, std::function<void(const char*)> log_callback)
{
    this->log = log_callback;
    this->buflen = default_buflen;
    
    // Initialize Winsock
    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0) {
        record_error(
            status,
            status_info,
            log,
            MailProxy::TcpStatus::WsaStartupFailed,
            "WSAStartup failed with error",
            iResult
        );
        return;
    }

    recvbuf = (char*)calloc(default_buflen, sizeof(char));
}

MailProxy::ClientTcp::~ClientTcp()
{
    free(recvbuf);
    tcp_shutdown();
    if (status == TcpStatus::OK || status == TcpStatus::Closed)
        closesocket(ConnectSocket);
        WSACleanup();
}

void MailProxy::ClientTcp::tcp_connect(const char* server_addr, const char* port)
{
    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    // Resolve the server address and port
    iResult = getaddrinfo(server_addr, port, &hints, &result);
    if (iResult != 0) {
        record_error(
            status,
            status_info,
            log,
            MailProxy::TcpStatus::GetAddrInfoFailed,
            "getaddrinfo failed with error",
            iResult
            );
        WSACleanup();
        return;
    }

    // Attempt to connect to an address until one succeeds
    for (ptr = result; ptr != NULL; ptr = ptr->ai_next) {

        // Create a SOCKET for connecting to server
        ConnectSocket = socket(ptr->ai_family, ptr->ai_socktype,
            ptr->ai_protocol);
        if (ConnectSocket == INVALID_SOCKET) {
            record_error(
                status,
                status_info,
                log,
                MailProxy::TcpStatus::SocketFailed,
                "socket failed with error",
                WSAGetLastError()
            );
            WSACleanup();
            return;
        }

        // Connect to server.
        iResult = connect(ConnectSocket, ptr->ai_addr, (int)ptr->ai_addrlen);
        if (iResult == SOCKET_ERROR) {
            closesocket(ConnectSocket);
            ConnectSocket = INVALID_SOCKET;
            continue;
        }
        break;
    }

    freeaddrinfo(result);

    if (ConnectSocket == INVALID_SOCKET) {
        status = MailProxy::TcpStatus::ConnServerFailed;
        char error_info[256]= "Unable to connect to server!\n";
        status_info = std::string(error_info);
        log(error_info);
        WSACleanup();
        return;
    }
}

void MailProxy::ClientTcp::tcp_send(const char* data, int flags)
{
    iResult = send(ConnectSocket, data, (int)strlen(data), flags);
    if (iResult == SOCKET_ERROR) {
        record_error(
            status,
            status_info,
            log,
            MailProxy::TcpStatus::SendFailed,
            "send failed with error",
            WSAGetLastError()
        );
        closesocket(ConnectSocket);
        ConnectSocket = INVALID_SOCKET;
        WSACleanup();
        return;
    }
}

void MailProxy::ClientTcp::tcp_receive(int flags)
{
    iResult = recv(ConnectSocket, recvbuf, buflen - 1, flags);
    if (iResult < 0) {
        record_error(
            status,
            status_info,
            log,
            MailProxy::TcpStatus::RecvFailed,
            "recv failed with error",
            WSAGetLastError()
        );
        closesocket(ConnectSocket);
        ConnectSocket = INVALID_SOCKET;
        WSACleanup();
        return;
    }
    recvbuf[iResult] = 0;
}

void MailProxy::ClientTcp::tcp_shutdown(int how)
{
    if (ConnectSocket != INVALID_SOCKET) {
		iResult = shutdown(ConnectSocket, how);
		if (iResult == SOCKET_ERROR) {
			record_error(
				status,
				status_info,
				log,
				TcpStatus::ShutdownFailed,
				"shutdown failed with error",
				WSAGetLastError()
			);
			closesocket(ConnectSocket);
            ConnectSocket = INVALID_SOCKET;
			WSACleanup();
			return;
		}
	}
}

std::string MailProxy::ClientTcp::get_received()
{
    return std::string(this->recvbuf);
}

MailProxy::TcpStatus MailProxy::ClientTcp::get_status()
{
    return this->status;
}

std::string MailProxy::ClientTcp::get_status_info()
{
    return this->status_info;
}
