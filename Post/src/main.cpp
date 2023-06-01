#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vcruntime.h>
#include <vcruntime_string.h>
#include "Base64.h"
#include "BasicSmtp.h"
#include "Email.h"
#include "EscSeq.h"

void append_rcpt(std::list<std::string>& rcpt_list, const char* val) {
    size_t val_len = strlen(val);
    char* copy = new char[val_len + 1];
    memcpy(copy, val, val_len + 1);

    size_t begin_index;
    for (size_t i = 0; copy[i] != NULL; i++) {
        switch (copy[i]) {
        case '<':
            begin_index = i + 1;
            break;
        case '>':
            copy[i] = NULL;
            rcpt_list.push_back(std::string(copy + begin_index));
            break;
        default:
            break;
        }
    }

    delete [] copy;
}

int main() {
    std::cout << CONSOLE_SET C_CYAN << "Start posting.\n" << CONSOLE_RESET;
    
    // Parse email archive.
    std::string login_name = "1429099037@qq.com", auth_code = "mhoiwlvonflhjjfi";
    std::string filename, buffer, sender, mail_data{"From: <" + login_name + ">\n"};
    std::list<std::string> rcpt{};
    std::getline(std::cin, filename);
    filename = "..\\..\\..\\saved\\2023.05.30-18.36.00-fQLMt2-4Qwp-uy9L.eml";
    std::ifstream fin(filename.data());
    while (!fin.eof()) {
        std::getline(fin, buffer);
        if (buffer == "") {
            mail_data += buffer + "\n";
            break;
        }
        else if (buffer.substr(0, 3) == "To:") {
            mail_data += buffer + "\n";
            append_rcpt(rcpt, buffer.data());
        }
        else if (buffer.substr(0, 3) == "Cc:") {
            mail_data += buffer + "\n";
            append_rcpt(rcpt, buffer.data());
        }
        else if (buffer.substr(0, 4) == "Bcc:") {
            mail_data += buffer + "\n";
            append_rcpt(rcpt, buffer.data());
        }
        else if (buffer.substr(0, 5) == "From:") {
            sender = buffer.substr(6);
        }
        else if (buffer.substr(0, 5) == "Date:") {
            continue;
        }
        else {
            mail_data += buffer + "\n";
        }
    }
    while (!fin.eof()) {
        std::getline(fin, buffer);
        mail_data += buffer + "\n";
    }
    
    // Encode login name and auth code to Base 64.
    char* login_name_base64 = new char[base64_encode_len(strlen(login_name.data()))];
    char* auth_code_base64 = new char[base64_encode_len(strlen(auth_code.data()))];
    base64_encode(login_name_base64, login_name.data(), strlen(login_name.data()));
    base64_encode(auth_code_base64, auth_code.data(), strlen(auth_code.data()));

    // Login.
    MailProxy::BasicSmtp smtp_conn;
    smtp_conn.smtp_login("smtp.qq.com", login_name_base64, auth_code_base64);
    if (smtp_conn.get_smtp_status() == MailProxy::SmtpStatus::SmtpErr) {
        std::cerr << CONSOLE_SET F_BOLD C_RED << "SMTP login failed with code "
                  << static_cast<int>(smtp_conn.get_smtp_reply().code) << CONSOLE_RESET << std::endl;
        exit(-2);
    }
    else if (smtp_conn.get_smtp_status() == MailProxy::SmtpStatus::TcpErr) {
        std::cerr << CONSOLE_SET F_BOLD C_RED << "TCP service error!" << CONSOLE_RESET << std::endl;
        exit(-4);
    }
    delete [] login_name_base64;
    delete [] auth_code_base64;
    std::cout << CONSOLE_SET C_GREEN << "Login succeeded!" << CONSOLE_RESET << std::endl;

    // Send email.
    smtp_conn.smtp_send_raw(login_name, rcpt, mail_data);
    if (smtp_conn.get_smtp_status() == MailProxy::SmtpStatus::SmtpErr) {
        std::cerr << CONSOLE_SET F_BOLD C_RED << "SMTP posting failed with code "
                  << static_cast<int>(smtp_conn.get_smtp_reply().code) << std::endl;
        std::cerr << smtp_conn.get_smtp_reply().msg << CONSOLE_RESET << std::endl;
        std::cout << CONSOLE_SET F_REGULAR C_CYAN << "Sending feedback\n" << CONSOLE_RESET;
    }
    else if (smtp_conn.get_smtp_status() == MailProxy::SmtpStatus::TcpErr) {
        std::cerr << CONSOLE_SET F_BOLD C_RED << "TCP service error!" << CONSOLE_RESET << std::endl;
        exit(-2);
    }
    std::cout << CONSOLE_SET F_BOLD C_GREEN << "Post succeeded!" << CONSOLE_RESET << std::endl;

    return 0;
}