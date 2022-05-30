import os
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import json

department_code = ["aic", "ele", "ete", "ci", "mar", "bs", "log", "air", "hre", "GHF", "cec", "ece", "welfare", "nurse",
                   "MA", "SDB", "SDB", "bhm", "HM", "inc", "mus", "ptg", "design", "CF", "WC", "MB"]

department_name = ["AI융복합과", "AI전기전자과", "AI정보통신과", "AI컴퓨터정보과", "마케팅과", "경영과", "유통물류과", "항공서비스과", "호텔관광과", "호텔외식조리과",
                   "아동보육과", "유아교육과", "사회복지과", "간호학과", "보건의료행정과", "송도바이오생명과", "송도바이오과", "뷰티아트과", "건강관리과", "바이오코스메틱과",
                   "실용음악과", "사진영상미디어과", "실내건축디자인과", "외식조리창업과", "복지케어과", "마케팅빅데이터과"]

# 학과 첫 페이지 URL 생성을 위한 BASE URL
baseURL = "https://dep.jeiu.ac.kr/"

for i in department_name:
    os.mkdir(f'{os.getcwd()}/{i}')

# 첫번째 반복문
for i in range(len(department_code)):

    print(department_name[i])
    # 교수 소개 페이지로 들어가는 URL 생성
    runURL = baseURL + department_code[i] + "/intro/degree.asp"

    # 두번째 For 를 위한 URL 생성  (degree.asp가 필요 없음)
    seconRunBaseURL = baseURL + department_code[i] + "/intro"

    try:
        # runURL에 들어가기 전 urllib 에 헤더 지정
        html_road = urllib.request.Request(runURL, headers={
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/44.0.2403.157 Safari/537.36"
        })

        # html_road에서 받아온 body를 html에 저장
        html = urllib.request.urlopen(html_road)

        # html.paser를 통해 변환해서 soup_jeiu에 저장
        soup_jeiu = BeautifulSoup(html, 'html.parser')

        # soup_jeiu에 있는 요소를 선택해서 degree에 저장
        degree = soup_jeiu.select('.txt_center.pdt5 a[href]')

        # 두번째 For. degree에 저장한 URL에 반복하면서 순환
        for a in degree:
            # 두번째 URL 생성
            secondRun = seconRunBaseURL + "/" + a['href']
            print(secondRun)

            # 두번째 html 로드 및 해더 지정
            html_under_road = urllib.request.Request(secondRun, headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, '
                              'like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'
            })

            # degree_html에 html_under_road를 저장
            degree_html = urllib.request.urlopen(html_under_road)

            # html.paser을 통해 degree_html을 변환하여 soup_degree에 저장
            soup_degree = BeautifulSoup(degree_html, 'html.parser')

            # soup_degree 요소를 선택

            # 교수 테이블
            name_table = soup_degree.select('.degree_list tr th')

            # 교수 테이블 내용 추출
            table = []
            for b in name_table:
                # 분류 먼저 저장
                table.append(str(b.getText()).replace('\n', " "))

            print("교수 테이블: ", table, "\n")

            # 제목 추출
            h5 = []
            name_h5 = soup_degree.select('h5 .gray')
            for d in name_h5:
                h5.append(str(d.getText().strip()))

            print("제목: ", h5, "\n")

            # 학력 및 약력
            career = []
            name_career = soup_degree.select('.degree_hak li')
            for c in name_career:
                career.append(str(c.getText().strip()))

            print("학력 및 약력: ", career, "\n")

            all_data = [{'URL': [secondRun], 'Basic Information': table, 'title': h5, 'Career and Research Performance': career}]

            name = soup_degree.select_one(".degree_list tr td")

            with open(f'./{department_name[i]}/{department_name[i]}_교수진_{name.getText()}.json', 'w', encoding='utf8') as outfile:
                json_file = json.dumps(all_data, indent=4, sort_keys=True, ensure_ascii=False)

                outfile.write(json_file)

    except urllib.error.URLError as e:
        err = e.reason
        print(runURL, "| 연결이 불량 입니다.", err, "\n")
