-- 데이터베이스 생성
CREATE DATABASE future_political_leader_trend;

-- 해당 데이터베이스를 사용
\c future_political_leader_trend;

-- survey_info 
CREATE TABLE IF NOT EXISTS survey_info (
    survey_id SERIAL PRIMARY KEY,
    registration_number INT NOT NULL,
    survey_agency TEXT NOT NULL,
    client TEXT NOT NULL,
    survey_start_date DATE NOT NULL,
    survey_end_date DATE NOT NULL,
    survey_method TEXT NOT NULL,
    sampling_frame TEXT NOT NULL,
    sample_size INT NOT NULL,
    contact_rate FLOAT NOT NULL,
    response_rate FLOAT NOT NULL,
    margin_of_error_95ci TEXT NOT NULL
);

-- candidate_info
CREATE TABLE IF NOT EXISTS candidate_info (
    candidate_id SERIAL PRIMARY KEY,
    candidate_name TEXT NOT NULL
)

-- political_party_info
CREATE TABLE IF NOT EXISTS political_party_info (
    political_party_id SERIAL PRIMARY KEY, 
    political_party_name TEXT UNIQUE NOT NULL
)

-- candidate_log
CREATE TABLE IF NOT EXISTS candidate_log (
    cid SERIAL PRIMARY KEY,
    survey_id INT NOT NULL,
    candidate_name TEXT NOT NULL,
    approval_rating FLOAT NOT NULL,
    FOREIGN KEY (survey_id) REFERENCES survey_info(survey_id) ON DELETE CASCADE
)

-- political_party_log
CREATE TABLE IF NOT EXISTS political_party_log (
    pid SERIAL PRIMARY KEY,
    survey_id INT NOT NULL,
    political_party_name TEXT NOT NULL,
    support_rate FLOAT NOT NULL,
    FOREIGN KEY (survey_id) REFERENCES survey_info(survey_id) ON DELETE CASCADE
);

-- theme_info
CREATE TABLE IF NOT EXISTS theme_info (
    lid SERIAL PRIMARY KEY,
    stock_name TEXT NOT NULL,
    candidate_name TEXT NOT NULL,
    FOREIGN KEY (stock_name) REFERENCES stock_info(kor_stock_abbr) ON DELETE CASCADE,
    FOREIGN KEY (candidate_name) REFERENCES candidate_info(candidate_name) ON DELETE CASCADE
)

-- stock_info
CREATE TABLE IF NOT EXISTS stock_info (
    stock_id SERIAL PRIMARY KEY,
    standard_code TEXT UNIQUE NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    kor_stock_name TEXT NOT NULL,
    kor_stock_abbr TEXT NOT NULL,
    eng_stock_name TEXT NOT NULL,
    listing_date DATE NOT NULL,
    market_type TEXT NOT NULL,
    security_type TEXT NOT NULL,
    affiliated_dept TEXT NOT NULL,
    stock_type TEXT NOT NULL,
    listed_shares BIGINT NOT NULL
);

-- 네이버 블로그 데이터 저장 테이블
CREATE TABLE IF NOT EXISTS naver_blog (
    id SERIAL PRIMARY KEY,
    candidate TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL,  -- 중복 데이터 방지
    description TEXT,
    blogger_name TEXT,
    blogger_link TEXT,
    post_date DATE,
    scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 성능 최적화를 위한 인덱스 설정
CREATE INDEX IF NOT EXISTS idx_candidate ON naver_blog(candidate);
CREATE INDEX IF NOT EXISTS idx_post_date ON naver_blog(post_date);

-- 테스트용 후보 데이터 삽입 (필요하면 주석 해제)
-- INSERT INTO candidate_info (candidate_name) VALUES ('테스트 후보 1'), ('테스트 후보 2');

-- 권한 설정 (Airflow 등에서 접근 가능하도록)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myuser;