from bs4 import BeautifulSoup as bs
import requests
import html5lib
import os

def main():
    manga_info = otakusan_get_manga()
    chap_list = get_chapter_list(manga_info)
    
    start_chap = int(input('\033[1;92;40m\n\t Nhập Số Chap Bắt Đầu:'))
    end_chap = int(input('\033[1;92;40m\n\t Nhập Số Chap Kết Thúc:'))
    
    for chap_number in range(start_chap, end_chap + 1):
        chapter_info = get_chapter(manga_info, chap_list, chap_number)
        get_link_image(chapter_info)
        down_img(manga_info, chapter_info)

def otakusan_get_manga():
    name = input('\033[1;92;40m\tNhập Tên Truyện Cần Lấy:')
    print('\033[1;37;40m')
    url = f'https://otakusan.net/Home/Search?search={name}'
    all_supporting_text_divs = []
    r = requests.get(url)
    raw = bs(r.text ,'html5lib')
    title_manga = []
    link_manga = []
    flag_manga = []
    div_best_match = raw.find_all('div', {'class': "collection shadow-z-1-home"})
    sub_link = 'https://otakusan.net'
    for div in div_best_match:
        supporting_text_divs = div.find_all('div', {'class': 'mdl-card__supporting-text mdl-color-text--grey-600'})
        for item in supporting_text_divs:
            head_manga = item.find('h4', {'class': "text-overflow capitalize"}).find('a').get('title')
            direct_link = item.find('h4', {'class': "text-overflow capitalize"}).find('a').get('href')
            flag = item.find('h4', {'class': "text-overflow capitalize"}).find('a').find('img').get('src').split('/')[-1][:-4].upper()
            title_manga.append(head_manga)
            link_manga.append(sub_link + direct_link)
            flag_manga.append(flag)
    for i , name in enumerate(title_manga, start=0):
        print(f'\n\t「{i + 1}」: --{flag_manga[i]} -- {name}')
    user_choice = int(input('\033[1;92;40m\n\t Nhập Số Của Truyện Cần Lấy:'))
    link_manga_get = link_manga[user_choice - 1]
    return link_manga_get, head_manga

def get_chapter_list(manga_info):
    url = manga_info[0]
    r = requests.get(url)
    raw = bs(r.text, 'html5lib')
    name_chap = []
    link_chap = []
    sub_link = 'https://otakusan.net'
    chap_table = raw.find_all('table', {'class': 'table mdi-table table-clickable-td'})
    
    for table in chap_table:
        td_chap = table.find_all('td', {'class': 'read-chapter'})
        for td in td_chap:
            a_tag = td.find('a')
            if a_tag:
                alt_chap = a_tag.get('alt')
                name_chap.append(alt_chap)
                href_chap = a_tag.get('href')
                link_chap.append(sub_link + href_chap)
    
    sorted_chapters = sorted(zip(name_chap, link_chap), key=lambda x: float(x[0].split()[-1]))
    
    print("\nChapters:")
    for i, (name_chapter, link_chapter) in enumerate(sorted_chapters, start=1):
        print(f'\t{i}. {name_chapter} - {link_chapter}')
    
    return sorted_chapters

def get_chapter(manga_info, chap_list, chap_number):
    if 1 <= chap_number <= len(chap_list):
        link_chap_get = chap_list[chap_number - 1][1]
        name_chap = link_chap_get.split('-')[-2] +'_' + link_chap_get.split('-')[-1]
        return link_chap_get, name_chap
    else:
        print(f'\033[1;91;40m\nChap số {chap_number} không tồn tại!')
        exit()

def get_link_image(chapter_info):
    url = chapter_info[0]
    r = requests.get(url)
    raw = bs(r.text,'html5lib')
    div_image = raw.find_all('div',{'class':'image-wraper'})
    list_image = []
    for image in div_image:
        img = image.find('img').get('src')
        if img.startswith('https'):
            list_image.append(img)
    return list_image

def down_img(manga_info, chapter_info):
    DIR = f'/storage/emulated/0/{manga_info[1]}/{chapter_info[1]}'
    link_image = get_link_image(chapter_info)
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    for i, img_url in enumerate(link_image, start=0):
        response = requests.get(img_url)
        if response.status_code == 200:
            image_name = f'image_{i}.png'
            with open(os.path.join(DIR, image_name), 'wb') as f:
                f.write(response.content)
            print(f'Tải về thành công: {image_name}')
    print(f'\n\tDOWNLOAD SUCCES:{chapter_info[1]}')

if __name__ == '__main__':
    main()
