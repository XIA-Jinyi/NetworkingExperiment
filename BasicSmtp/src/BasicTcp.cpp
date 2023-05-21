/******************************************************************************
*
* BasicTcp.cpp
*
* Author: 张原赫, 夏锦熠
*
******************************************************************************/

#include "BasicTcp.h"

#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")

MailProxy::BasicTcp::BasicTcp(size_t default_buflen, std::function<void(const char*)> log_callback)
{
	this->log = log_callback;
	if (log) {
		log("MailProxy::BasicTcp::BasicTcp");
	}
}

MailProxy::BasicTcp::~BasicTcp()
{
	if (log) {
		log("MailProxy::BasicTcp::~BasicTcp");
	}
}

void MailProxy::BasicTcp::connect(const char* server_addr, const char* port)
{
	if (log) {
		log("void MailProxy::BasicTcp::connect");
	}
}

void MailProxy::BasicTcp::send(const char* data, int flags)
{
	if (log) {
		log("void MailProxy::BasicTcp::send");
	}
}

void MailProxy::BasicTcp::receive(int flags)
{
	if (log) {
		log("void MailProxy::BasicTcp::receive");
	}
}

void MailProxy::BasicTcp::shutdown(int how)
{
	if (log) {
		log("void MailProxy::BasicTcp::shutdown");
	}
}

std::string MailProxy::BasicTcp::get_received()
{
	return std::string(this->recvbuf);
}

MailProxy::TcpStatus MailProxy::BasicTcp::get_status()
{
	return this->status;
}

std::string MailProxy::BasicTcp::get_status_info()
{
	return this->status_info;
}
