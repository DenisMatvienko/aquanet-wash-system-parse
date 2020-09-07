import requests
from bs4 import BeautifulSoup
import csv
from mixin.page_data_mixin import PageDataMixin


""" Header of csv file outside iteration"""
with open('aquanet.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Наименование', 'URL', 'Артикул', 'Бренд', 'Path', 'Коллекция', 'Тип', 'Назначение',
                     'Управление', 'Установка', 'Ширина', 'Высота', 'Глубина', 'Материал', 'Дизайн', 'Цвет',
                     'Количество монтажных отверстий', 'Тип излива', 'Форма излива', 'Длина излива',
                     'Смеситель в комплекте', 'Ручной душ', 'Шланг в комплекте', 'Стандарт подводки', 'Длина шланга',
                     'Верхний душ в комплекте', 'Страна производителя', 'Тропический душ в комплекте',
                     'Количество режимов душа', 'Диаметр лейки', 'Термостат', 'Размер верхнего душа', 'Вес',
                     'Количество режимов верхнего душа'])


""" Headers by client request """
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
           "Connection": "keep-alive",
           "Cookie": "roistat_is_need_listen_requests=0; PHPSESSID=dkqigsqjnpog23oi06ve8e78cn; "
                     "BITRIX_SM_SALE_UID=53262055; activity=0|20; _gcl_au=1.1.1930093311.1581921401;"
                     " BITRIX_SM_VREGION_SUBDOMAIN=spb; BITRIX_SM_VREGION_SUBDOMAIN=spb; roistat_visit=778381; "
                     "roistat_first_visit=778381; roistat_marker_old=; _ga=GA1.2.550948518.1581921402; _"
                     "gid=GA1.2.680255184.1581921402; tmr_reqNum=5; tmr_lvid=76a44c8277ca4aa4a4b803049f61ad74; "
                     "tmr_lvidTS=1581921402025; _ym_uid=1581921402466203911; _ym_d=1581921402; leadhunter_expire=1; _"
                     "gat=1; _ym_visorc_23245510=w; _ym_isad=2; _fbp=fb.1.1581921402948.1181980815; ___"
                     "dc=c8ad68ce-ab99-43f6-9729-12c2fe7a6b8b; tmr_detect=0%7C1581921404947; BX_"
                     "USER_ID=0662459c6c9a798caa9c90b46efe2528; _gat_UA-44466602-1=1",
           "Host": "www.aquanet.ru",
           "Referer": "https://www.aquanet.ru/catalog/verkhnie_dushi/",
           "TE": "Trailers",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}


def get_html(url):
    """ Get method of request on site """
    r = requests.get(url, headers=headers)
    return r.text


def write_csv(data):
    """ Write data after pars """
    with open('aquanet.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['name'],
                         data['url'],
                         data['art'],
                         data['brand'],
                         data['path'],
                         data['collections'],
                         data['type_of'],
                         data['purpose'],
                         data['controlling'],
                         data['install'],
                         data['width'],
                         data['height'],
                         data['depth'],
                         data['material'],
                         data['design'],
                         data['color'],
                         data['hole_for_montage'],
                         data['type_of_wash'],
                         data['format_of_wash'],
                         data['len_of_wash'],
                         data['mixer_in_complect'],
                         data['handheld_showerhead'],
                         data['tube_in_complect'],
                         data['flexible_connection'],
                         data['len_of_tube'],
                         data['overhead_shower_in_complect'],
                         data['country'],
                         data['tropical_wash'],
                         data['wataring_mode'],
                         data['radius'],
                         data['termo'],
                         data['size_top'],
                         data['weigth'],
                         data['wataring_mode_top']])


def get_page_data(response):
    """ Method of parse data """
    soup = BeautifulSoup(response, 'lxml')
    divs = soup.find_all('div', class_='item')

    urls = []

    for div in divs:
        """ First page """
        url = div.select_one('a').get('href')
        urls.append('https://www.aquanet.ru' + url)

    for url in urls:
        """
            Page of each products
            Request & pars param's
            Use PageDataMixin, for created short entry of exceptions
            Use methods find_paragraph & find_links, for different param's of search text on page
        """
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')

        try:
            """ Find path """
            part_of_path_1 = soup.find('div', id='breadcrumb').select_one('a').text
            part_of_path_2 = soup.find('div', id='breadcrumb').select_one('a').find_next('a').text
            part_of_path_3 = soup.find('div', id='breadcrumb').select_one('a').find_next('a').find_next('a').text
            path = part_of_path_1 + '@' + part_of_path_2 + '@' + part_of_path_3
        except:
            path = 'empty'

        """ Get properties from each pages """
        name = soup.find('div', id='content').select_one('h1').text.strip()
        art = PageDataMixin(soup.select_one, {'data-id': '125'}).find_paragraph()
        brand = PageDataMixin(soup.select_one, {'data-id': '126'}).find_links()
        collections = PageDataMixin(soup.select_one, {'data-id': '226'}).find_links()
        type_of = PageDataMixin(soup.select_one, {'data-id': '142'}).find_paragraph()
        purpose = PageDataMixin(soup.select_one, {'data-id': '153'}).find_paragraph()
        controlling = PageDataMixin(soup.select_one, {'data-id': '189'}).find_paragraph()
        install = PageDataMixin(soup.select_one, {'data-id': '137'}).find_paragraph()
        width = PageDataMixin(soup.select_one, {'data-id': '132'}).find_paragraph()
        height = PageDataMixin(soup.select_one, {'data-id': '133'}).find_paragraph()
        depth = PageDataMixin(soup.select_one, {'data-id': '134'}).find_paragraph()
        material = PageDataMixin(soup.select_one, {'data-id': '127'}).find_paragraph()
        design = PageDataMixin(soup.select_one, {'data-id': '158'}).find_paragraph()
        color = PageDataMixin(soup.select_one, {'data-id': '128'}).find_paragraph()
        hole_for_montage = PageDataMixin(soup.select_one, {'data-id': '280'}).find_paragraph()
        type_of_wash = PageDataMixin(soup.select_one, {'data-id': '191'}).find_paragraph()
        format_of_wash = PageDataMixin(soup.select_one, {'data-id': '157'}).find_paragraph()
        len_of_wash = PageDataMixin(soup.select_one, {'data-id': '281'}).find_paragraph()
        mixer_in_complect = PageDataMixin(soup.select_one, {'data-id': '298'}).find_paragraph()
        handheld_showerhead = PageDataMixin(soup.select_one, {'data-id': '299'}).find_paragraph()
        tube_in_complect = PageDataMixin(soup.select_one, {'data-id': '326'}).find_paragraph()
        flexible_connection = PageDataMixin(soup.select_one, {'data-id': '283'}).find_paragraph()
        len_of_tube = PageDataMixin(soup.select_one, {'data-id': '307'}).find_paragraph()
        overhead_shower_in_complect = PageDataMixin(soup.select_one, {'data-id': '307'}).find_paragraph()
        country = PageDataMixin(soup.select_one, {'data-id': '397'}).find_paragraph()
        tropical_wash = PageDataMixin(soup.select_one, {'data-id': '485'}).find_paragraph()
        wataring_mode = PageDataMixin(soup.select_one, {'data-id': '303'}).find_paragraph()
        radius = PageDataMixin(soup.select_one, {'data-id': '306'}).find_paragraph()
        termo = PageDataMixin(soup.select_one, {'data-id': '155'}).find_paragraph()
        size_top = PageDataMixin(soup.select_one, {'data-id': '562'}).find_paragraph()
        weigth = PageDataMixin(soup.select_one, {'data-id': '589'}).find_paragraph()
        wataring_mode_top = PageDataMixin(soup.select_one, {'data-id': '303'}).find_paragraph()

        # Write data to dict and get to the write csv func
        data = {'name': name,
                'url': url,
                'art': art,
                'brand': brand,
                'path': path,
                'collections': collections,
                'type_of': type_of,
                'purpose': purpose,
                'controlling': controlling,
                'install': install,
                'width': width,
                'height': height,
                'depth': depth,
                'material': material,
                'design': design,
                'color': color,
                'hole_for_montage': hole_for_montage,
                'type_of_wash': type_of_wash,
                'format_of_wash': format_of_wash,
                'len_of_wash': len_of_wash,
                'mixer_in_complect': mixer_in_complect,
                'handheld_showerhead': handheld_showerhead,
                'tube_in_complect': tube_in_complect,
                'flexible_connection': flexible_connection,
                'len_of_tube': len_of_tube,
                'overhead_shower_in_complect': overhead_shower_in_complect,
                'country': country,
                'tropical_wash': tropical_wash,
                'wataring_mode': wataring_mode,
                'radius': radius,
                'termo': termo,
                'size_top': size_top,
                'weigth': weigth,
                'wataring_mode_top': wataring_mode_top}
        write_csv(data)


def main():
    pattern = 'https://www.aquanet.ru/catalog/dushevye_programmy/?PAGEN_1={}'

    for i in range(1, 81):
        """ Loop requests to get response data from page on 81 pages   """
        url = pattern.format(str(i))
        get_page_data(get_html(url))


if __name__ == '__main__':
    main()