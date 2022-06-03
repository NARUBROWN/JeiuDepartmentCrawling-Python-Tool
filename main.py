import os
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError

# "aic"코드는 학교 자체 사이트가 아니라 제외
department_code = ["ele", "ete", "ci", "mar", "bs", "log", "air", "hre", "GHF", "cec", "ece", "welfare", "NURS",
                   "MA", "SDB", "SDB", "bhm", "HM", "inc", "mus", "ptg", "design", "CF", "WC", "MB"]
# "AI융복합과"는 학교 자체 사이트가 아니라 제외
department_name = ["AI응용전기전자과", "AI정보통신과", "AI컴퓨터정보과", "마케팅경영과", "경영과", "스마트유통물류과", "항공운항서비스과", "호텔관광과", "호텔외식조리과",
                   "아동보육과", "유아교육과", "사회복지과", "간호학과", "보건의료행정과", "송도바이오과", "송도바이오과", "뷰티아트과", "건강관리과", "바이오코스메틱과",
                   "실용음악과", "사진영상 미디어과", "실내건축과", "외식조리창업과", "복지케어과", "마케팅빅데이터과"]

# 학과 첫 페이지 URL 생성을 위한 BASE URL
baseURL = "https://dep.jeiu.ac.kr/"

# 첫번째 반복문
for i in range(len(department_code)):

    print(department_name[i], "페이지 크롤링을 시작합니다." + '\n')
    # 교수 소개 페이지로 들어가는 URL 생성
    runURL = baseURL + department_code[i] + "/intro/degree.asp"

    # 두번째 For 를 위한 URL 생성  (degree.asp가 필요 없음)
    seconRunBaseURL = baseURL + department_code[i] + "/intro"

    try:
        # runURL에 들어가기 전 urllib 에 헤더 지정
        html_road = urllib.request.Request(runURL, headers={
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/604.1'
        })

        # html_road에서 받아온 body를 html에 저장
        html = urllib.request.urlopen(html_road)

        # html.paser를 통해 변환해서 soup_jeiu에 저장
        soup_jeiu = BeautifulSoup(html, 'html.parser')

        all_professor = soup_jeiu.select('#contents_in > div > div > div.degree_right > table')
        all_professor_list = list(all_professor)

        # soup_jeiu에 있는 요소를 선택해서 degree에 저장
        degree = soup_jeiu.select('.txt_center.pdt5 a[href]')

        # 약력 저장할 곳
        more_detail = []

        # 새로 해보는거
        new_data_set = []

        # 세부 페이지 로드
        for a in degree:
            # 두번째 URL 생성
            secondRun = seconRunBaseURL + "/" + a['href']
            print(secondRun)

            # 두번째 html 로드 및 해더 지정
            html_under_road = urllib.request.Request(secondRun, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
            })

            print("세부 페이지를 불러옵니다")

            # degree_html에 html_under_road를 저장
            degree_html = urllib.request.urlopen(html_under_road)

            # html.paser을 통해 degree_html을 변환하여 soup_degree에 저장
            soup_degree = BeautifulSoup(degree_html, 'html.parser')


            new_try = []

            # contents_in의 class를 가진 객체를 가져옵니다.
            new_try_body = soup_degree.find(id='contents_in')
            new_try_body.find('div', 'degree').decompose()

            for d in new_try_body:
                new_try.append(str(d.getText('<br>').strip()))


            new_try.pop()

            new_try = [v for v in new_try if v]

            result_data = []
            for j in new_try:
                result_data.append(j + '<br>')
            result_data.pop()

            new_data_set.append(result_data)

        html_start = f'<!DOCTYPE html><meta charset="utf-8"><html><head>' \
                     f'<style>section {{ margin: 0 auto; width: 50%; }} table{{ width: 100%; margin: 0 auto; border: ' \
                     f'1px solid #444444; border-collapse: collapse;}} th, td {{ border: 1px solid #444444; }}\
                            </style> <title>{department_name[i]}_교수진</title></head><body><section>'

        html_end = f'</section></body></html>'

        html_body = []

        for a in range(len(all_professor)):
            html_body.append(f'{all_professor[a]} <br> {new_data_set[a]}')

        html_body = str(html_body).lstrip('[').rstrip(']')
        html_body = html_body.replace('교수소개', "")
        html_body = html_body.replace('인천재능대학교 ' + department_name[i] + '  입니다.', "")
        html_body = html_body.replace('인천재능대학교 ' + department_name[i] + ' 교수소개 입니다.', "")
        html_body = html_body.replace('\\n', "")
        html_body = html_body.replace('\\', "")
        html_body = html_body.replace("'", "")
        html_body = html_body.replace("{", "")
        html_body = html_body.replace("[", "")
        html_body = html_body.replace("]", "")
        html_body = html_body.replace("}", "")
        html_body = html_body.replace('"', "")
        html_body = html_body.replace(',', "")
        html_body = html_body.replace('리스트', "")

        html_finish = html_start + html_body + html_end

        with open(f'./{department_name[i]}_교수진.html', 'w', encoding='utf8') as html_file:
            html_file.write(html_finish)

        print('\n' + '데이터를 HTML로 만들었습니다.' + '\n')

    except urllib.error.URLError as e:
        err = e.reason
        print(runURL, "| 연결이 불량 입니다.", err, "\n")
