import requests
from bs4 import BeautifulSoup
import os

def get_html_content(url):  # 获得整个html的内容 get the whole html content.
    html = requests.get(url)
    if (html.status_code == 200):
        code = html.apparent_encoding # 根据html内容来分析网页编码 get the code according to the page content.
        text = html.content.decode(code)
        return text
    else:
        return ''

def filter_html_content(text): # 获得图片列表 get the picture list.
    result_list = []
    soup = BeautifulSoup(text, 'html.parser')
    for i in range(0, 10, 1):
        result_list.append(soup.findAll('img', class_='scaleimg2' + str(i)))
    return result_list

def download(pic_list): # 提取链接进行下载 download every picture to local pc according to hyperlinks.
    for i in range(0, len(pic_list), 1):
        hyperlink = pic_list[i][0].attrs['src']
        pic_name = hyperlink.rsplit('/', 1)[1]

        os.chdir(os.environ['HOME'])
        save_dir = os.getcwd()
        
        # 当前目录下是否有该子目录, 没有就创建一个
        # if the current direction hasn't sub-direction, then create it.
        if not os.path.exists('crwaler_dir'): 
            os.mkdir('crwaler_dir')
        save_dir += '/crwaler_dir'
        save_file = save_dir + '/' + pic_name
        
        pic = requests.get(hyperlink, stream = True)

        # 将图片保存到当前目录 save the pics to the current directions
        with open(save_file, 'wb') as f:
            for chunk in pic.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        

def main():
    url = 'http://www.niurencun.cn/blank112121.html?bannerId=1&t=1507541167193'
    html_text = get_html_content(url)
    result = filter_html_content(html_text)
    download(result) 
    
if __name__ == '__main__':
    main()

