"""
利用该爬虫脚本爬取51job中的招聘信息
爬取的项目有'职位', '公司', '工作地点', '薪水', '发布日期','职位信息','福利','学历','经验年数','招聘人数'
共爬取16万条数据
"""

import requests 
import re
from bs4 import  BeautifulSoup
import xlwt
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
}
def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def get_html():
    k=1 #参数k代表存储到excel的行数
    wb = xlwt.Workbook()  # 创建工作簿
    f = wb.add_sheet("招聘信息")  # 创建工作表
    raw = ['职位', '公司', '工作地点', '薪水', '发布日期','职位信息','福利','学历','经验年数','招聘人数']
    for i in range(len(raw)):
        f.write(0, i, raw[i])
    url='https://search.51job.com/list/000000,000000,0100%252C2500%252C2600%252C2700,01%252C38%252C32%252C40,9,99,%2B,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    try:
        for page in range(1,2):#解析前20页
            res = get_one_page(url.format(page))
            soup = BeautifulSoup(res, 'html.parser')
            t1 = soup.select('.t1 span a')
            t2 = soup.select('.t2 a')
            t3 = soup.select('.t3')
            t4 = soup.select('.t4')
            t5 = soup.select('.t5')
            for i in range(len(t2)):
                job = t1[i].get('title')#获取职位
#                 print (job)
                href = t1[i].get('href')#获取链接
                company = t2[i].get('title')#获取公司名
                location = t3[i+1].text#获取工作地点
                salary = t4[i+1].text#获取薪水
                date = t5[i+1].text#获取发布日期
                link = BeautifulSoup(get_one_page(href), 'html.parser')
                message=link.find('div',class_=re.compile('bmsg job_msg inbox'))
                if (message):
                    message=message.text
                    labellist=link.find('div',class_=re.compile('t1')).find_all('span')
                    labelist=[]
                    for label in labellist:
                        labelist.append(label.text)
                    xljyzp=link.find('p',class_=re.compile('msg ltype')).text.split('\xa0\xa0|\xa0\xa0')
                    jy,xl,zp='','',''
                    for i in xljyzp:
                        if '经验' in i:
                            jy=i.strip()
                        elif i.strip() in ['本科','大专','高中','中专','中技','硕士','博士','初中']:
                            xl=i.strip()
                        elif '招' in i:
                            zp=i.strip()
                    print (xljyzp)
                else:
                    message=""
                f.write(k,0,job)
                f.write(k,1,company)
                f.write(k,2,location)
                f.write(k,3,salary)
                f.write(k,4,date)
                f.write(k,5,message)
                f.write(k,6,','.join(labelist))
                f.write(k,7,xl)
                f.write(k,8,jy)
                f.write(k,9,zp)
                k+=1#每存储一行 k值加1
        wb.save('D:/招聘201.xls')#写完后掉用save方法进行保存
        
    except TimeoutError:
        print("请求失败")
        return  None
if __name__=='__main__':
    get_html()
