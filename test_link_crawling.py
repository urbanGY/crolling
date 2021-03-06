import pytest
from selenium import webdriver
import link_crawling
import json

#pytest --site 0,1,2,3 test_link_crawling.py
# https://watcha.com/ko-KR
# https://watcha.com/ko-KR/search?query=%EC%97%91%EC%8B%9C%ED%8A%B8
# https://watcha.com/ko-KR/contents/mdErj22
# 왓챠 엑시트
@pytest.fixture(scope = 'module')
def site_index(pytestconfig):
    val = '0'
    val = pytestconfig.getoption("site")
    return int(val)

@pytest.fixture(scope = 'module')
def browser():
    chrome_option = webdriver.ChromeOptions() #headless 옵션 객체 생성
    chrome_option.add_argument('headless')
    chrome_option.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_option) #chrome driver 사용 및 headless 옵션 객체 적용
    driver.implicitly_wait(3) #랜더링 완료 시간 대기
    yield driver
    driver.close()

@pytest.fixture(scope = 'module')
def site(site_index):
    site_list = link_crawling.read_site_list()
    return site_list[site_index]

@pytest.fixture(scope = 'module')
def movie():
    m_l = ['엑시트','한국','2019','2018']
    return m_l

def test_remove_blank():
    text = 'abcd efgh'
    result = link_crawling.remove_blank(text)
    assert result == 'abcdefgh'

def test_init():
    driver = link_crawling.init()
    assert driver #안됐을 때 케이스에 대한 고려

def test_read_site_list(site_index):
    site_list = link_crawling.read_site_list()
    test = ['watcha','naver_movie','daum_movie','maxmovie']
    assert test[site_index] == site_list[site_index]['site_name']

def test_search_title(browser, site, movie):
    driver = browser
    title = movie[0]
    default_url = site['site_url']
    search_xpath = site['search_xpath']
    link_crawling.search_title(driver,title,default_url,search_xpath)
    assert 1

def test_get_url(browser, site, movie):
    driver = browser
    url = 'https://watcha.com/ko-KR/search?query=%EC%97%91%EC%8B%9C%ED%8A%B8'
    driver.get(url)
    title = movie[0]
    contry = movie[1]
    open_year = movie[2]
    start_year = movie[3]
    title_xpath = site['title_xpath']
    check_xpath = site['check_xpath']
    content_url = link_crawling.get_url(driver, title, contry, open_year, start_year, title_xpath, check_xpath)
    assert content_url == 'https://watcha.com/ko-KR/contents/mdErj22'

def test_get_score(browser, site):
    url = 'https://watcha.com/ko-KR/contents/mdErj22'
    driver = browser
    driver.get(url)
    score_xpath = site['score_xpath']
    score = link_crawling.get_score(driver, score_xpath)
    scale = site['scale_type']
    score = link_crawling.score_scaling(score, scale)
    assert score == '6.6'
