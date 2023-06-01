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

std::list<std::string> parse_rcpt(const char* val) {
    size_t val_len = strlen(val);
    char* copy = new char[val_len + 1];
    memcpy(copy, val, val_len + 1);

    std::list<std::string> result;
    size_t begin_index;
    for (size_t i = 0; copy[i] != NULL; i++) {
        switch (copy[i]) {
        case '<':
            begin_index = i + 1;
            break;
        case '>':
            copy[i] = NULL;
            result.push_back(std::string(copy + begin_index));
            break;
        default:
            break;
        }
    }

    delete [] copy;
    return result;
}

int main() {
    std::cout << CONSOLE_SET C_CYAN << "Start posting.\n" << CONSOLE_RESET;
    
    // Parsing email archive.
    std::string filename, buffer, sender;
    std::list<std::string> to_rcpt, cc_rcpt, bcc_rcpt;
    std::map<std::string, std::string> ext_headers;
    std::getline(std::cin, filename);
    // filename = "..\\..\\..\\saved\\2023.05.30-18.36.00-fQLMt2-4Qwp-uy9L.eml";
    std::ifstream fin(filename.data());
    while (!fin.eof()) {
        std::getline(fin, buffer);
        if (buffer == "") {
            break;
        }
        else if (buffer.substr(0, 3) == "To:") {
            to_rcpt = parse_rcpt(buffer.data());
        }
        else if (buffer.substr(0, 3) == "Cc:") {
            cc_rcpt = parse_rcpt(buffer.data());
        }
        else if (buffer.substr(0, 4) == "Bcc:") {
            bcc_rcpt = parse_rcpt(buffer.data());
        }
        else if (buffer.substr(0, 5) == "From:") {
            sender = buffer.substr(6);
        }
        else if (buffer.substr(0, 12) == "Content-Type") {
            break;
        }
        else {
            size_t index;
            for (index = 0; buffer[index] != ':'; index++);
            ext_headers.insert({buffer.substr(0, index), buffer.substr(index + 2)});
        }
    }
    std::string mail_body = "";
    while (!fin.eof()) {
        mail_body += buffer;
        mail_body += "\n";
        std::getline(fin, buffer);
    }

    // Constructing mail.
    MailProxy::Email mail;
    mail.body = mail_body;
    mail.to_rcpt = to_rcpt;
    mail.cc_rcpt = cc_rcpt;
    mail.bcc_rcpt = bcc_rcpt;
    mail.ext_headers = ext_headers;
    std::cout << CONSOLE_SET C_CYAN << "Email constructed.\n" << CONSOLE_RESET;
    
    // Encoding login name and auth code to Base 64.
    std::string login_name = "1429099037@qq.com", auth_code = "mhoiwlvonflhjjfi";
    char* login_name_base64 = new char[base64_encode_len(strlen(login_name.data()))];
    char* auth_code_base64 = new char[base64_encode_len(strlen(auth_code.data()))];
    base64_encode(login_name_base64, login_name.data(), strlen(login_name.data()));
    base64_encode(auth_code_base64, auth_code.data(), strlen(auth_code.data()));

    // Sending email.
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
    smtp_conn.smtp_send(login_name, mail);
    if (smtp_conn.get_smtp_status() == MailProxy::SmtpStatus::SmtpErr) {
        std::cerr << CONSOLE_SET F_BOLD C_RED << "SMTP posting failed with code "
                  << static_cast<int>(smtp_conn.get_smtp_reply().code) << CONSOLE_RESET << std::endl;
        // std::cout << CONSOLE_SET F_REGULAR C_CYAN << "Sending feedback\n" << CONSOLE_RESET;
    }
    else if (smtp_conn.get_smtp_status() == MailProxy::SmtpStatus::TcpErr) {
        std::cerr << CONSOLE_SET F_BOLD C_RED << "TCP service error!" << CONSOLE_RESET << std::endl;
        exit(-2);
    }
    std::cout << CONSOLE_SET F_BOLD C_GREEN << "Post succeeded!" << CONSOLE_RESET << std::endl;

    return 0;
}