from urllib.parse import unquote
from datetime import datetime
from email.mime.text import MIMEText
from sys import stderr

def get_dict(data: str):
    result = {}
    for pair in data.split('&'):
        key, val = pair.split('=')
        result[key] = unquote(val)
    return result

if __name__ == '__main__':
    print('\033[0;36mParser launched!\033[0m')
    try:
        while input() != '':
            pass
        data = input()
    except:
        print('\033[0;33mParse failed: input error!\033[0m', file=stderr)
        exit(-2)
    # data = 'dockey=&bigattachcontent=&mailtype=&0cf34e9b561ceb04ee86f2414bdc4d04=49f103a8cb3a848a398a52724fa174c3&sid=fQLMt2-4Qwp-uy9L&bigattachcnt=&exstore=&from_s=cnew&swap=&signtype=3&newwin=&verifykey=&stationeryCount=&to=%22%E5%A4%8F%26nbsp%3B%E9%94%A6%E7%86%A0%22%3Ccnjyxjy%40outlook.com%3E&swap3=&cc=%22%E5%A4%8F%E9%94%A6%E7%86%A0%22%3Cjinyi.xia%40bupt.edu.cn%3E%3B%20%222487867519%22%3C2487867519%40qq.com%3E&bcc=%22jinyi.xia%22%3Cjinyi.xia%40outlook.com%3E&subject=&content__html=%3Cdiv%3E%26amp%3B%26amp%3B%26amp%3B%3D%3D%3D%26amp%3B%3D%26amp%3B%3D%26amp%3B%3D%3D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%3Chr%20align%3D%22left%22%20style%3D%22margin%3A%200%200%2010px%200%3Bborder%3A%200%3Bborder-bottom%3A1px%20solid%20%23E4E5E6%3Bheight%3A0%3Bline-height%3A0%3Bfont-size%3A0%3Bpadding%3A%2020px%200%200%200%3Bwidth%3A%2050px%3B%22%3E%3Cdiv%20style%3D%22font-size%3A14px%3Bfont-family%3AVerdana%3Bcolor%3A%23000%3B%22%3E%3Ca%20class%3D%22xm_write_card%22%20id%3D%22in_alias%22%20style%3D%22white-space%3A%20normal%3B%20display%3A%20inline-block%3B%20text-decoration%3A%20none%20!important%3Bfont-family%3A%20-apple-system%2CBlinkMacSystemFont%2CPingFang%20SC%2CMicrosoft%20YaHei%3B%22%20href%3D%22https%3A%2F%2Fwx.mail.qq.com%2Fhome%2Findex%3Ft%3Dreadmail_businesscard_midpage%26amp%3Bnocheck%3Dtrue%26amp%3Bname%3D%25E5%25A4%258F%25E9%2594%25A6%25E7%2586%25A0%26amp%3Bicon%3Dhttp%253A%252F%252Fp.qlogo.cn%252Fqqmail_head%252FHa4jSSokMLhzkrjKibdkUv8mQIgRZIjGSias6x3rL8wlsJfCEK8ibbJoibtDH7D1lFx6%252F160%26amp%3Bmail%3Djinyi.xia%2540foxmail.com%26amp%3Bcode%3DNQqewBmWXMSuETRybjbQwB5_FjJum0e3ivhY6Cl5je4Q4-c5vVyfu8ywp2dG_BJ_91G1Dv75QHRhIbm8xww8T1TrNDhFAE8_qb_QdBh0Uek%22%20target%3D%22_blank%22%3E%3Ctable%20style%3D%22white-space%3A%20normal%3Btable-layout%3A%20fixed%3B%20padding-right%3A%2020px%3B%22%20contenteditable%3D%22false%22%20cellpadding%3D%220%22%20cellspacing%3D%220%22%3E%3Ctbody%3E%3Ctr%20valign%3D%22top%22%3E%3Ctd%20style%3D%22width%3A%2040px%3Bmin-width%3A%2040px%3B%20padding-top%3A10px%22%3E%3Cdiv%20style%3D%22width%3A%2038px%3B%20height%3A%2038px%3B%20border%3A%201px%20%23FFF%20solid%3B%20border-radius%3A50%25%3B%20margin%3A%200%3Bvertical-align%3A%20top%3Bbox-shadow%3A%200%200%2010px%200%20rgba(127%2C152%2C178%2C0.14)%3B%22%3E%3Cimg%20src%3D%22http%3A%2F%2Fp.qlogo.cn%2Fqqmail_head%2FHa4jSSokMLhzkrjKibdkUv8mQIgRZIjGSias6x3rL8wlsJfCEK8ibbJoibtDH7D1lFx6%2F160%22%20style%3D%22width%3A100%25%3Bheight%3A100%25%3Bborder-radius%3A50%25%3Bpointer-events%3A%20none%3B%22%3E%3C%2Fdiv%3E%3C%2Ftd%3E%3Ctd%20style%3D%22padding%3A%2010px%200%208px%2010px%3B%22%3E%3Cdiv%20class%3D%22businessCard_name%22%20style%3D%22font-size%3A%2014px%3Bcolor%3A%20%2333312E%3Bline-height%3A%2020px%3B%20padding-bottom%3A%202px%3B%20margin%3A0%3Bfont-weight%3A%20500%3B%22%3E%E5%A4%8F%E9%94%A6%E7%86%A0%3C%2Fdiv%3E%3Cdiv%20class%3D%22businessCard_mail%22%20style%3D%22font-size%3A%2012px%3Bcolor%3A%20%23999896%3Bline-height%3A%2018px%3B%20margin%3A0%3B%22%3Ejinyi.xia%40foxmail.com%3C%2Fdiv%3E%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%20colspan%3D%222%22%20style%3D%22padding-left%3A%2050px%3Bpadding-top%3A%202px%3Bfont-size%3A%2013px%3Bcolor%3A%20%23999896%3B%20line-height%3A%2020px%3B%22%20class%3D%22businessCard_other_info%22%3E%E5%8C%97%E4%BA%AC%E9%82%AE%E7%94%B5%E5%A4%A7%E5%AD%A6%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftbody%3E%3C%2Ftable%3E%3C%2Fa%3E%3C%2Fdiv%3E%3C%2Fdiv%3E%3Cdiv%3E%26nbsp%3B%3C%2Fdiv%3E&sendmailname=jinyi.xia%40foxmail.com&savesendbox=1&swap2=&transattach=&SrcMailCharset=&xqqstyle=&mailbgmusic=&actiontype=send&priority=&sendname=%E5%A4%8F%E9%94%A6%E7%86%A0&acctid=0%20&ReAndFw=&separatedcopy=false&fmailid=ZD1730-CnXBonrEn9ajtyNHRil0Hd5&ReAndFwMailid=&cattachelist=&upfilelist=&rsturl=&fileidlist=&t=backgroundsend&verifycode=&verifycode_cn=&s=comm&from=&hitaddrbook=0&selfdefinestation=-1&backurl=&noatcp=&domaincheck=0&cgitm=1685428200909&clitm=1685428201469&comtm=1685438132778&logattcnt=0&logattsize=0&logattmethod=&timezone=28800&timezone_dst=0&resp_charset=UTF8&bgsend=1'
    try:
        data_dict = get_dict(data)
    except:
        print('\033[0;33mParse failed: not the packet!\033[0m', file=stderr)
        exit(-4)
    try:
        lines = ['From: %s\n' % data_dict['sendmailname']]
        if (val := data_dict.get('to')) != None:
            lines += [f'To: {val}\n']
        if (val := data_dict.get('cc')) != None:
            lines += [f'Cc: {val}\n']
        if (val := data_dict.get('bcc')) != None:
            lines += [f'Bcc: {val}\n']
        lines += ['Subject: %s\n' % data_dict['subject']]
        lines += ['Date: %s\n' % datetime.now().strftime('%a, %d %B %Y %H:%M:%S +0800')]
        lines += [str(MIMEText(data_dict['content__html'], 'html'))]
    except:
        print('\033[0;33mParse failed: syntax error!\033[0m', file=stderr)
        exit(-8)
    try:
        file_name = datetime.now().strftime('%Y.%m.%d-%H.%M.%S-')
        with open(f'./saved/{file_name}.eml', 'w') as fout:
            fout.writelines(lines)
    except:
        print('\033[1;31mParse failed: can\'t write email to file!\033[0m', file=stderr)
        exit(-16)
    print('\033[1;32mParse succeeded!\033[0m')

# 'dockey=&bigattachcontent=&mailtype=&0cf34e9b561ceb04ee86f2414bdc4d04=49f103a8cb3a848a398a52724fa174c3&sid=fQLMt2-4Qwp-uy9L&bigattachcnt=&exstore=&from_s=cnew&swap=&signtype=3&newwin=&verifykey=&stationeryCount=&to=%22%E5%A4%8F%26nbsp%3B%E9%94%A6%E7%86%A0%22%3Ccnjyxjy%40outlook.com%3E&swap3=&cc=%22%E5%A4%8F%E9%94%A6%E7%86%A0%22%3Cjinyi.xia%40bupt.edu.cn%3E%3B%20%222487867519%22%3C2487867519%40qq.com%3E&bcc=%22jinyi.xia%22%3Cjinyi.xia%40outlook.com%3E&subject=&content__html=%3Cdiv%3E%26amp%3B%26amp%3B%26amp%3B%3D%3D%3D%26amp%3B%3D%26amp%3B%3D%26amp%3B%3D%3D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%3Chr%20align%3D%22left%22%20style%3D%22margin%3A%200%200%2010px%200%3Bborder%3A%200%3Bborder-bottom%3A1px%20solid%20%23E4E5E6%3Bheight%3A0%3Bline-height%3A0%3Bfont-size%3A0%3Bpadding%3A%2020px%200%200%200%3Bwidth%3A%2050px%3B%22%3E%3Cdiv%20style%3D%22font-size%3A14px%3Bfont-family%3AVerdana%3Bcolor%3A%23000%3B%22%3E%3Ca%20class%3D%22xm_write_card%22%20id%3D%22in_alias%22%20style%3D%22white-space%3A%20normal%3B%20display%3A%20inline-block%3B%20text-decoration%3A%20none%20!important%3Bfont-family%3A%20-apple-system%2CBlinkMacSystemFont%2CPingFang%20SC%2CMicrosoft%20YaHei%3B%22%20href%3D%22https%3A%2F%2Fwx.mail.qq.com%2Fhome%2Findex%3Ft%3Dreadmail_businesscard_midpage%26amp%3Bnocheck%3Dtrue%26amp%3Bname%3D%25E5%25A4%258F%25E9%2594%25A6%25E7%2586%25A0%26amp%3Bicon%3Dhttp%253A%252F%252Fp.qlogo.cn%252Fqqmail_head%252FHa4jSSokMLhzkrjKibdkUv8mQIgRZIjGSias6x3rL8wlsJfCEK8ibbJoibtDH7D1lFx6%252F160%26amp%3Bmail%3Djinyi.xia%2540foxmail.com%26amp%3Bcode%3DNQqewBmWXMSuETRybjbQwB5_FjJum0e3ivhY6Cl5je4Q4-c5vVyfu8ywp2dG_BJ_91G1Dv75QHRhIbm8xww8T1TrNDhFAE8_qb_QdBh0Uek%22%20target%3D%22_blank%22%3E%3Ctable%20style%3D%22white-space%3A%20normal%3Btable-layout%3A%20fixed%3B%20padding-right%3A%2020px%3B%22%20contenteditable%3D%22false%22%20cellpadding%3D%220%22%20cellspacing%3D%220%22%3E%3Ctbody%3E%3Ctr%20valign%3D%22top%22%3E%3Ctd%20style%3D%22width%3A%2040px%3Bmin-width%3A%2040px%3B%20padding-top%3A10px%22%3E%3Cdiv%20style%3D%22width%3A%2038px%3B%20height%3A%2038px%3B%20border%3A%201px%20%23FFF%20solid%3B%20border-radius%3A50%25%3B%20margin%3A%200%3Bvertical-align%3A%20top%3Bbox-shadow%3A%200%200%2010px%200%20rgba(127%2C152%2C178%2C0.14)%3B%22%3E%3Cimg%20src%3D%22http%3A%2F%2Fp.qlogo.cn%2Fqqmail_head%2FHa4jSSokMLhzkrjKibdkUv8mQIgRZIjGSias6x3rL8wlsJfCEK8ibbJoibtDH7D1lFx6%2F160%22%20style%3D%22width%3A100%25%3Bheight%3A100%25%3Bborder-radius%3A50%25%3Bpointer-events%3A%20none%3B%22%3E%3C%2Fdiv%3E%3C%2Ftd%3E%3Ctd%20style%3D%22padding%3A%2010px%200%208px%2010px%3B%22%3E%3Cdiv%20class%3D%22businessCard_name%22%20style%3D%22font-size%3A%2014px%3Bcolor%3A%20%2333312E%3Bline-height%3A%2020px%3B%20padding-bottom%3A%202px%3B%20margin%3A0%3Bfont-weight%3A%20500%3B%22%3E%E5%A4%8F%E9%94%A6%E7%86%A0%3C%2Fdiv%3E%3Cdiv%20class%3D%22businessCard_mail%22%20style%3D%22font-size%3A%2012px%3Bcolor%3A%20%23999896%3Bline-height%3A%2018px%3B%20margin%3A0%3B%22%3Ejinyi.xia%40foxmail.com%3C%2Fdiv%3E%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%20colspan%3D%222%22%20style%3D%22padding-left%3A%2050px%3Bpadding-top%3A%202px%3Bfont-size%3A%2013px%3Bcolor%3A%20%23999896%3B%20line-height%3A%2020px%3B%22%20class%3D%22businessCard_other_info%22%3E%E5%8C%97%E4%BA%AC%E9%82%AE%E7%94%B5%E5%A4%A7%E5%AD%A6%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftbody%3E%3C%2Ftable%3E%3C%2Fa%3E%3C%2Fdiv%3E%3C%2Fdiv%3E%3Cdiv%3E%26nbsp%3B%3C%2Fdiv%3E&sendmailname=jinyi.xia%40foxmail.com&savesendbox=1&swap2=&transattach=&SrcMailCharset=&xqqstyle=&mailbgmusic=&actiontype=send&priority=&sendname=%E5%A4%8F%E9%94%A6%E7%86%A0&acctid=0%20&ReAndFw=&separatedcopy=false&fmailid=ZD1730-CnXBonrEn9ajtyNHRil0Hd5&ReAndFwMailid=&cattachelist=&upfilelist=&rsturl=&fileidlist=&t=backgroundsend&verifycode=&verifycode_cn=&s=comm&from=&hitaddrbook=0&selfdefinestation=-1&backurl=&noatcp=&domaincheck=0&cgitm=1685428200909&clitm=1685428201469&comtm=1685438132778&logattcnt=0&logattsize=0&logattmethod=&timezone=28800&timezone_dst=0&resp_charset=UTF8&bgsend=1'